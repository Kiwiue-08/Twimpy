import os
import time
import webbrowser  # Import webbrowser module
from threading import Timer

from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import easyocr

app = Flask(__name__)

# Configure Selenium to use Chrome in headless mode
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280x720")  # Lower resolution for performance
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
    chrome_options.add_argument("--disable-software-rasterizer")  # Prevent rendering
    chrome_options.add_argument("--disable-extensions")  # Disable extensions for improved performance
    chrome_options.add_argument("--log-level=3")  # Suppress logs
    chrome_options.add_argument("--disable-background-networking")  # Avoid unnecessary network traffic
    chrome_options.add_argument("--disable-sync")
    chrome_options.add_argument("--disable-translate")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.reader = easyocr.Reader(['en'], gpu=False)  # Disable GPU for EasyOCR
    return driver

# Function to open a URL and ensure the page loads
def open_url(driver, url):
    driver.get(url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Wait for the body to load

# Parse views from string (handles 'K' and 'M' suffixes for large numbers)
def parse_views(views_str):
    """Convert views string to numeric value."""
    try:
        if 'K' in views_str:
            return float(views_str.replace('K', '').strip()) * 1000  # Handles both '12K' and '12.5K'
        elif 'M' in views_str:
            return float(views_str.replace('M', '').strip()) * 1000000  # Handles '1.2M'
        else:
            return float(views_str.replace(',', '').strip())  # Handle cases like '12000'
    except ValueError:
        print(f"Could not convert views string '{views_str}' to float.")
        return 0  # Return 0 if conversion fails

# Scroll the page and capture screenshot
def scroll_and_take_screenshot(driver, url):
    open_url(driver, url)  # Open the URL

    views_str = ""
    max_scrolls = 5
    scroll_pause_time = 1.5

    for _ in range(max_scrolls):
        screenshot_path = "screenshot.png"
        driver.save_screenshot(screenshot_path)

        result = driver.reader.readtext(screenshot_path)

        for _, text, _ in result:
            if 'Views' in text:
                views_str = text.split()[0]  # Get the first part (number of views)
                break

        if views_str:
            break

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause_time)

    return parse_views(views_str) if views_str else 0  # Return parsed views or 0 if not found

# Function to get views from multiple URLs using the same driver instance in parallel
def get_views_in_parallel(driver, urls):
    views_list = []
    for url in urls:
        views_list.append(get_views(driver, url))
    return views_list

# Function to get views from a single URL
def get_views(driver, url):
    views = scroll_and_take_screenshot(driver, url)
    return views

# Flask app routes
@app.route("/", methods=["GET", "POST"])
def home():
    driver = create_driver()  # Initialize the driver once
    if request.method == "POST":
        urls_input = request.form.get("urls")
        urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
        cumulative_views = 0

        # Get views for all URLs sequentially to ensure each one is properly processed
        views_list = get_views_in_parallel(driver, urls)

        for views in views_list:
            cumulative_views += views

        results = list(zip(urls, views_list))
        driver.quit()  # Close the driver after processing all URLs
        return render_template("index.html", results=results, cumulative=cumulative_views)

    return render_template("index.html")

def open_browser():
    """Open the Flask app in the default browser."""
    webbrowser.open_new("http://127.0.0.1:5000/")

if __name__ == "__main__":
    Timer(1, open_browser).start()  # Delay the browser opening slightly to avoid race conditions
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
