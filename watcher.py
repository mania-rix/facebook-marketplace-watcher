import smtplib
import time
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import requests
from datetime import datetime, timedelta
import hashlib

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# File handler
file_handler = logging.FileHandler('wlog_scraper.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))

# Add handlers only if they haven't been added yet
if not logger.hasHandlers():
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

# Email configuration
EMAIL = "your email"
PASSWORD = "your password"
TO_EMAIL = "recipient email"
# SMTP server configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Facebook URLs
LOGIN_URL = "https://www.facebook.com/login/device-based/regular/login/"
MARKETPLACE_URL = "https://www.facebook.com/marketplace/auto/"


# Your Facebook credentials
FB_EMAIL = "your email"
FB_PASSWORD = "your password"

# Keep track of seen listings
sent_listings = set()

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))  # Change to 'html' for HTML email

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, TO_EMAIL, msg.as_string())
        logger.info("Email sent successfully")
    except Exception as e:
        logger.error(f"Failed to send email: {e}")

def login_facebook(page):
    page.goto(LOGIN_URL)
    try:
        page.fill('input[name="email"]', FB_EMAIL)
        page.fill('input[name="pass"]', FB_PASSWORD)
        page.click('button[name="login"]')
        page.wait_for_timeout(3000)  # Wait for 3 seconds to ensure the login process completes
        page.goto(MARKETPLACE_URL)
        logger.info("Logged into Facebook successfully")
    except Exception as e:
        logger.error(f"Failed to log in to Facebook: {e}")

def extract_item_id(url):
    item_id = url.split('/item/')[1].split('/')[0]  # Extract the item ID from the URL
    base_url = f"https://www.facebook.com/marketplace/item/{item_id}"
    return base_url

def process_listing(page, listing, current_time):
    try:
        title_tag = listing.find('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')
        price_tag = listing.find('span', class_='x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u')
        link_tag = listing.find('a', class_='x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv')
        details_tags = listing.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84')

        if not (title_tag and price_tag and link_tag and details_tags):
            logger.warning("Missing necessary tag(s) in listing")
            return None

        title = title_tag.text
        price = price_tag.text
        post_url = "https://www.facebook.com" + link_tag['href']
        base_url = extract_item_id(post_url)

        # Extract kilometers value from details_tags
        kilometers = None
        for tag in details_tags:
            if "km" in tag.text:
                kilometers = tag.text
                break

        if not kilometers:
            logger.warning("Missing kilometers value")
            return None

        listing_id = hashlib.md5(post_url.encode()).hexdigest()

        if listing_id in sent_listings:
            logger.info(f"Skipping already processed listing: {title}")
            return None

        # Navigate to each listing to get the posted time
        page.goto(post_url)
        page.wait_for_timeout(2000)  # Wait for the listing page to load

        # Scrape the posted time
        post_html = page.content()
        post_soup = BeautifulSoup(post_html, 'html.parser')
        time_tag = post_soup.find('span', string=lambda x: x and "Listed" in x and ("minute ago" in x or "minutes ago" in x))

        if not time_tag:
            time_tag = post_soup.find('div', string=lambda x: x and "Listed" in x and ("minute ago" in x or "minutes ago" in x))

        if not time_tag:
            # Try alternative method to find the time tag
            for div in post_soup.find_all('div'):
                if div.text and "Listed" in div.text and ("minute ago" in div.text or "minutes ago" in div.text):
                    time_tag = div
                    break

        if not time_tag:
            logger.warning(f"Missing time tag for listing: {post_url}")
            return None

        # Extract the "minutes ago" part accurately and cleanly
        time_text_parts = time_tag.text.strip().split("Listed")
        if len(time_text_parts) > 1:
            time_text = time_text_parts[1].strip()
            if "minute ago" in time_text:
                minutes_ago = 1
            else:
                time_text = time_text.split("minutes ago")[0].strip()
                minutes_ago = int(time_text)
        else:
            logger.warning(f"Could not extract time from tag text for listing: {post_url}")
            return None

        post_time = current_time - timedelta(minutes=minutes_ago)

        # Calculate time difference
        time_difference = current_time - post_time

        if time_difference <= timedelta(minutes=20):  # within 20 minutes ago
            sent_listings.add(listing_id)
            return f"""
                <b>Title:</b> {title}<br>
                <b>Price:</b> {price}<br>
                <b>Link:</b> <a href="{base_url}">View Listing</a><br>
                <b>Kilometers:</b> {kilometers}<br>
                <b>Posted:</b> {minutes_ago} minutes ago<br>
                """

        return None

    except Exception as e:
        logger.error(f"Error processing listing: {e}")
        return None

def check_marketplace(page):
    logger.info("Checking Facebook Marketplace")
    try:
        page.goto(MARKETPLACE_URL)
        # Try to wait for multiple selectors, whichever comes first
        page.wait_for_selector('div[class*="x1jx94hy"], div[class*="x9f619"]', timeout=30000)  # Wait for either selector to appear within 30 seconds
        page.wait_for_timeout(3000)  # Wait for 3 seconds to ensure the page is fully loaded
    except PlaywrightTimeoutError:
        logger.error("Timeout while waiting for marketplace listings to load, retrying...")
        return check_marketplace(page)  # Retry on timeout

    html = page.content()
    soup = BeautifulSoup(html, 'html.parser')
    listings = soup.find_all('div', class_='x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e x1iorvi4 xjkvuk6 xnpuxes x291uyu x1uepa24')

    if not listings:
        logger.info("No listings found in the page source")
    else:
        logger.info(f"Found {len(listings)} listings")

    new_listings = []
    current_time = datetime.now()

    for listing in listings[:4]:  # Process the first 4 listings
        result = process_listing(page, listing, current_time)
        if result:
            new_listings.append(result)

    if new_listings:
        logger.info(f"Found {len(new_listings)} new listings")
        email_body = "<br><br>".join(new_listings)
        send_email("New Listings", email_body)
        logger.info("New listings found and email sent")
    else:
        logger.info("No new listings found")

def run_scraper():
    logger.info("Script started")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        login_facebook(page)
        while True:
            check_marketplace(page)
            time.sleep(30)  # Refresh every 30 seconds

if __name__ == "__main__":
    run_scraper()
