import os
import time  #####using ss
# from flask import Flask, render_template, request
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import easyocr
#
# app = Flask(__name__)
#
# # Configure Selenium to use Chrome
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better screenshot
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').replace('.', '').strip()) * 1000
#         else:
#             return float(views_str.replace(',', '').strip())
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails
#
# def scroll_and_take_screenshot(driver, url):
#     driver.get(url)
#
#     # Wait for the page to load
#     time.sleep(5)
#
#     # Initialize EasyOCR reader
#     reader = easyocr.Reader(['en'])
#
#     views_str = ""
#     max_scrolls = 10  # Limit the number of scrolls
#     scroll_pause_time = 2  # Time to wait after each scroll
#
#     for _ in range(max_scrolls):
#         # Take a screenshot of the page
#         screenshot_path = "screenshot.png"
#         driver.save_screenshot(screenshot_path)
#
#         # Read text from the screenshot
#         result = reader.readtext(screenshot_path)
#
#         for (bbox, text, prob) in result:
#             print(f"Detected text: {text}")
#             if 'Views' in text:  # Look for the text indicating views
#                 views_str = text.split()[0]  # Get the first part (number of views)
#                 break
#
#         if views_str:  # Stop if views are found
#             break
#
#         # Scroll down the page
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause_time)  # Wait for the page to load
#
#     if views_str:
#         return parse_views(views_str)  # Convert to numeric value
#     return 0  # Return 0 if views cannot be extracted
#
# def get_views(url):
#     driver = create_driver()
#     views = scroll_and_take_screenshot(driver, url)
#     driver.quit()  # Close the driver
#     return views
#
# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]  # Split input by lines
#         views_list = []
#         cumulative_views = 0
#
#         for url in urls:
#             print(f"Processing URL: {url}")
#             views = get_views(url)  # Process each URL
#             views_list.append(views)
#             cumulative_views += views
#
#         # Create a list of tuples for rendering in HTML
#         results = list(zip(urls, views_list))
#
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


###using screen record
# from flask import Flask, render_template, request
# import cv2
# import numpy as np
# import easyocr
# import time
# import mss
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
#
# app = Flask(__name__)
#
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better view
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# def record_screen(output_file, duration):
#     """Record the screen for a specified duration."""
#     screen_size = (1920, 1080)  # Define the screen size
#     fourcc = cv2.VideoWriter_fourcc(*"XVID")
#     out = cv2.VideoWriter(output_file, fourcc, 20.0, screen_size)
#
#     with mss.mss() as sct:
#         start_time = time.time()
#         while True:
#             # Capture the screen
#             img = sct.grab(sct.monitors[1])
#             img = np.array(img)  # Convert to numpy array
#             img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR format
#
#             # Write the frame to the video file
#             out.write(img)
#
#             # Stop recording after the specified duration
#             if time.time() - start_time > duration:
#                 break
#
#     out.release()
#
# def extract_views_from_image(image_array):
#     """Use EasyOCR to extract views from the screenshot image."""
#     reader = easyocr.Reader(['en'])
#     results = reader.readtext(image_array)
#
#     for (bbox, text, prob) in results:
#         if 'views' in text.lower():
#             views_str = text.split()[0]  # Get the first part (number of views)
#             return parse_views(views_str)  # Convert to numeric value
#
#     return 0  # Return 0 if views cannot be extracted
#
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').replace('.', '').strip()) * 1000
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').replace('.', '').strip()) * 1000000
#         else:
#             return float(views_str.replace(',', '').strip())
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails
#
# def process_urls(urls):
#     cumulative_views = 0
#     views_list = []
#     output_file = "screen_recording.avi"
#
#     # Start recording the screen
#     record_duration = 30  # Adjust the duration as necessary
#     record_screen(output_file, record_duration)
#
#     # Create a Selenium driver
#     driver = create_driver()
#
#     for url in urls:
#         print(f"Opening URL: {url}")
#         driver.get(url)
#         time.sleep(5)  # Wait for the page to load
#
#         # Capture a screenshot
#         screenshot_path = f"screenshot_{url.split('/')[-1]}.png"
#         driver.save_screenshot(screenshot_path)
#
#         # Read the screenshot to extract views
#         image_array = cv2.imread(screenshot_path)
#         views = extract_views_from_image(image_array)
#         views_list.append(views)
#         cumulative_views += views
#         print(f"Extracted views from {url}: {views}")
#
#     driver.quit()
#
#     # Remove the recording file if necessary
#     os.remove(output_file)
#
#     return views_list, cumulative_views
#
# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]  # Split input by lines
#         views_list, cumulative_views = process_urls(urls)
#
#         # Create a list of tuples for rendering in HTML
#         results = list(zip(urls, views_list))
#
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


##screen record updated (with scroll)
# from flask import Flask, render_template, request
# import cv2
# import numpy as np
# import easyocr
# import time
# import mss
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
#
# app = Flask(__name__)
#
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better view
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# def scroll_and_capture(driver):
#     """Scroll down the page while capturing the screen."""
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         # Scroll down to the bottom
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)  # Wait for new content to load
#
#         # Capture a screenshot
#         screenshot_path = f"screenshot.png"
#         driver.save_screenshot(screenshot_path)
#
#         # Check if we've reached the bottom of the page
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height
#
#     return screenshot_path
#
# def record_screen(output_file, duration):
#     """Record the screen for a specified duration."""
#     screen_size = (1920, 1080)  # Define the screen size
#     fourcc = cv2.VideoWriter_fourcc(*"XVID")
#     out = cv2.VideoWriter(output_file, fourcc, 20.0, screen_size)
#
#     with mss.mss() as sct:
#         start_time = time.time()
#         while True:
#             # Capture the screen
#             img = sct.grab(sct.monitors[1])
#             img = np.array(img)  # Convert to numpy array
#             img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR format
#
#             # Write the frame to the video file
#             out.write(img)
#
#             # Stop recording after the specified duration
#             if time.time() - start_time > duration:
#                 break
#
#     out.release()
#
# def extract_views_from_image(image_array):
#     """Use EasyOCR to extract views from the screenshot image."""
#     reader = easyocr.Reader(['en'])
#     results = reader.readtext(image_array)
#
#     for (bbox, text, prob) in results:
#         if 'views' in text.lower():
#             views_str = text.split()[0]  # Get the first part (number of views)
#             return parse_views(views_str)  # Convert to numeric value
#
#     return 0  # Return 0 if views cannot be extracted
#
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').replace('.', '').strip()) * 100
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').replace('.', '').strip()) * 100000
#         else:
#             return float(views_str.replace(',', '').strip())
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails
#
# def process_urls(urls):
#     cumulative_views = 0
#     views_list = []
#     output_file = "screen_recording.avi"
#
#     # Start recording the screen
#     record_duration = 30  # Adjust the duration as necessary
#     record_screen(output_file, record_duration)
#
#     # Create a Selenium driver
#     driver = create_driver()
#
#     for url in urls:
#         print(f"Opening URL: {url}")
#         driver.get(url)
#         time.sleep(5)  # Wait for the page to load
#
#         # Scroll down and capture views
#         screenshot_path = scroll_and_capture(driver)
#
#         # Read the screenshot to extract views
#         image_array = cv2.imread(screenshot_path)
#         views = extract_views_from_image(image_array)
#         views_list.append(views)
#         cumulative_views += views
#         print(f"Extracted views from {url}: {views}")
#
#     driver.quit()
#
#     # Remove the recording file if necessary
#     os.remove(output_file)
#
#     return views_list, cumulative_views
#
# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]  # Split input by lines
#         views_list, cumulative_views = process_urls(urls)
#
#         # Create a list of tuples for rendering in HTML
#         results = list(zip(urls, views_list))
#
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


##screen record (handles decimal)
# from flask import Flask, render_template, request
# import cv2
# import numpy as np
# import easyocr
# import time
# import mss
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
#
# app = Flask(__name__)
#
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better view
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# def scroll_and_capture(driver):
#     """Scroll down the page while capturing the screen."""
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         # Scroll down to the bottom
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)  # Wait for new content to load
#
#         # Capture a screenshot
#         screenshot_path = f"screenshot.png"
#         driver.save_screenshot(screenshot_path)
#
#         # Check if we've reached the bottom of the page
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height
#
#     return screenshot_path
#
# def record_screen(output_file, duration):
#     """Record the screen for a specified duration."""
#     screen_size = (1920, 1080)  # Define the screen size
#     fourcc = cv2.VideoWriter_fourcc(*"XVID")
#     out = cv2.VideoWriter(output_file, fourcc, 20.0, screen_size)
#
#     with mss.mss() as sct:
#         start_time = time.time()
#         while True:
#             # Capture the screen
#             img = sct.grab(sct.monitors[1])
#             img = np.array(img)  # Convert to numpy array
#             img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR format
#
#             # Write the frame to the video file
#             out.write(img)
#
#             # Stop recording after the specified duration
#             if time.time() - start_time > duration:
#                 break
#
#     out.release()
#
# def extract_views_from_image(image_array):
#     """Use EasyOCR to extract views from the screenshot image."""
#     reader = easyocr.Reader(['en'])
#     results = reader.readtext(image_array)
#
#     for (bbox, text, prob) in results:
#         if 'views' in text.lower():
#             views_str = text.split()[0]  # Get the first part (number of views)
#             return parse_views(views_str)  # Convert to numeric value
#
#     return 0  # Return 0 if views cannot be extracted
#
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         # Handling thousands (K) and millions (M)
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').strip()) * 1000
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').strip()) * 1000000
#         else:
#             return float(views_str.replace(',', '').strip())  # Handle plain numbers
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails
#
# def process_urls(urls):
#     cumulative_views = 0
#     views_list = []
#     output_file = "screen_recording.avi"
#
#     # Start recording the screen
#     record_duration = 30  # Adjust the duration as necessary
#     record_screen(output_file, record_duration)
#
#     # Create a Selenium driver
#     driver = create_driver()
#
#     for url in urls:
#         print(f"Opening URL: {url}")
#         driver.get(url)
#         time.sleep(5)  # Wait for the page to load
#
#         # Scroll down and capture views
#         screenshot_path = scroll_and_capture(driver)
#
#         # Read the screenshot to extract views
#         image_array = cv2.imread(screenshot_path)
#         views = extract_views_from_image(image_array)
#         views_list.append(views)
#         cumulative_views += views
#         print(f"Extracted views from {url}: {views}")
#
#     driver.quit()
#
#     # Remove the recording file if necessary
#     os.remove(output_file)
#
#     return views_list, cumulative_views
#
# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]  # Split input by lines
#         views_list, cumulative_views = process_urls(urls)
#
#         # Create a list of tuples for rendering in HTML
#         results = list(zip(urls, views_list))
#
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


# #running bg (screen record)
#
# from flask import Flask, render_template, request
# import cv2
# import numpy as np
# import easyocr
# import time
# import mss
# import os
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
#
# app = Flask(__name__)
#
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better view
#     chrome_options.add_argument("--headless")  # Run in headless mode without opening a visible browser window
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# def scroll_and_capture(driver):
#     """Scroll down the page while capturing the screen."""
#     last_height = driver.execute_script("return document.body.scrollHeight")
#     while True:
#         # Scroll down to the bottom
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(2)  # Wait for new content to load
#
#         # Capture a screenshot
#         screenshot_path = f"screenshot.png"
#         driver.save_screenshot(screenshot_path)
#
#         # Check if we've reached the bottom of the page
#         new_height = driver.execute_script("return document.body.scrollHeight")
#         if new_height == last_height:
#             break
#         last_height = new_height
#
#     return screenshot_path
#
# def record_screen(output_file, duration):
#     """Record the screen for a specified duration."""
#     screen_size = (1920, 1080)  # Define the screen size
#     fourcc = cv2.VideoWriter_fourcc(*"XVID")
#     out = cv2.VideoWriter(output_file, fourcc, 20.0, screen_size)
#
#     with mss.mss() as sct:
#         start_time = time.time()
#         while True:
#             # Capture the screen
#             img = sct.grab(sct.monitors[1])
#             img = np.array(img)  # Convert to numpy array
#             img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # Convert to BGR format
#
#             # Write the frame to the video file
#             out.write(img)
#
#             # Stop recording after the specified duration
#             if time.time() - start_time > duration:
#                 break
#
#     out.release()
#
# def extract_views_from_image(image_array):
#     """Use EasyOCR to extract views from the screenshot image."""
#     reader = easyocr.Reader(['en'])
#     results = reader.readtext(image_array)
#
#     for (bbox, text, prob) in results:
#         if 'views' in text.lower():
#             views_str = text.split()[0]  # Get the first part (number of views)
#             return parse_views(views_str)  # Convert to numeric value
#
#     return 0  # Return 0 if views cannot be extracted
#
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         # Handling thousands (K) and millions (M)
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').strip()) * 1000
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').strip()) * 1000000
#         else:
#             return float(views_str.replace(',', '').strip())  # Handle plain numbers
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails
#
# def process_urls(urls):
#     cumulative_views = 0
#     views_list = []
#     output_file = "screen_recording.avi"
#
#     # Start recording the screen
#     record_duration = 30  # Adjust the duration as necessary
#     record_screen(output_file, record_duration)
#
#     # Create a Selenium driver
#     driver = create_driver()
#
#     for url in urls:
#         print(f"Opening URL: {url}")
#         driver.get(url)
#         time.sleep(5)  # Wait for the page to load
#
#         # Scroll down and capture views
#         screenshot_path = scroll_and_capture(driver)
#
#         # Read the screenshot to extract views
#         image_array = cv2.imread(screenshot_path)
#         views = extract_views_from_image(image_array)
#         views_list.append(views)
#         cumulative_views += views
#         print(f"Extracted views from {url}: {views}")
#
#     driver.quit()
#
#     # Remove the recording file if necessary
#     os.remove(output_file)
#
#     return views_list, cumulative_views
#
# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]  # Split input by lines
#         views_list, cumulative_views = process_urls(urls)
#
#         # Create a list of tuples for rendering in HTML
#         results = list(zip(urls, views_list))
#
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


##using ss (runs bgbut screen pops up)

# from flask import Flask, render_template, request
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import easyocr
#
# app = Flask(__name__)
#
# # Configure Selenium to use Chrome in headless mode
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better screenshot
#     chrome_options.add_argument("--headless")  # Run Chrome in headless mode
#     chrome_options.add_argument('--disable-gpu')  # Disable GPU acceleration (optional)
#     chrome_options.add_argument('--log-level=3')  # Suppress unnecessary logs
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         # Handle cases like '12K', '12.5K', '1.2M'
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').strip()) * 1000  # Handles both '12K' and '12.5K'
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').strip()) * 1000000  # Handles '1.2M'
#         else:
#             return float(views_str.replace(',', '').strip())  # Handle cases like '12000'
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails
#
# def scroll_and_take_screenshot(driver, url):
#     driver.get(url)
#
#     # Wait for the page to load
#     time.sleep(5)
#
#     # Initialize EasyOCR reader
#     reader = easyocr.Reader(['en'])
#
#     views_str = ""
#     max_scrolls = 10  # Limit the number of scrolls
#     scroll_pause_time = 2  # Time to wait after each scroll
#
#     for _ in range(max_scrolls):
#         # Take a screenshot of the page
#         screenshot_path = "screenshot.png"
#         driver.save_screenshot(screenshot_path)
#
#         # Read text from the screenshot
#         result = reader.readtext(screenshot_path)
#
#         for (bbox, text, prob) in result:
#             print(f"Detected text: {text}")
#             if 'Views' in text or 'views' in text:  # Look for the text indicating views
#                 views_str = text.split()[0]  # Get the first part (number of views)
#                 break
#
#         if views_str:  # Stop if views are found
#             break
#
#         # Scroll down the page
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause_time)  # Wait for the page to load
#
#     if views_str:
#         return parse_views(views_str)  # Convert to numeric value
#     return 0  # Return 0 if views cannot be extracted
#
# def get_views(url):
#     driver = create_driver()
#     views = scroll_and_take_screenshot(driver, url)
#     driver.quit()  # Close the driver
#     return views
#
# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]  # Split input by lines
#         views_list = []
#         cumulative_views = 0
#
#         for url in urls:
#             print(f"Processing URL: {url}")
#             views = get_views(url)  # Process each URL
#             views_list.append(views)
#             cumulative_views += views
#
#         # Create a list of tuples for rendering in HTML
#         results = list(zip(urls, views_list))
#
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


# #completely headless browser, takes ss,,,,still isnt completeley headless, needs update
#
# from flask import Flask, render_template, request
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import easyocr
#
# app = Flask(__name__)
#
# # Configure Selenium to use Chrome in full headless mode
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better screenshot
#     chrome_options.add_argument("--headless=new")  # Run Chrome in headless mode
#     chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
#     chrome_options.add_argument("--disable-software-rasterizer")  # Prevent rendering
#     chrome_options.add_argument("--disable-extensions")  # Disable extensions for improved performance
#     chrome_options.add_argument("--disable-logging")  # Disable unnecessary logs
#     chrome_options.add_argument("--log-level=3")  # Suppress logs
#     chrome_options.add_argument("--remote-debugging-port=9222")  # Required for some headless environments
#     chrome_options.add_argument("--hide-scrollbars")  # Hide scrollbars in screenshots
#     chrome_options.add_argument("--disable-notifications")  # Disable notifications
#     chrome_options.add_argument("--disable-infobars")  # Disable info bars like "Chrome is being controlled"
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# # Parse views from string (handles 'K' and 'M' suffixes for large numbers)
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         # Handle cases like '12K', '12.5K', '1.2M'
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').strip()) * 1000  # Handles both '12K' and '12.5K'
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').strip()) * 1000000  # Handles '1.2M'
#         else:
#             return float(views_str.replace(',', '').strip())  # Handle cases like '12000'
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails
#
# # Scroll the page and capture screenshot
# def scroll_and_take_screenshot(driver, url):
#     driver.get(url)
#
#     # Wait for the page to load
#     time.sleep(5)
#
#     # Initialize EasyOCR reader
#     reader = easyocr.Reader(['en'])
#
#     views_str = ""
#     max_scrolls = 10  # Limit the number of scrolls
#     scroll_pause_time = 2  # Time to wait after each scroll
#
#     for _ in range(max_scrolls):
#         # Take a screenshot of the page
#         screenshot_path = "screenshot.png"
#         driver.save_screenshot(screenshot_path)
#
#         # Read text from the screenshot
#         result = reader.readtext(screenshot_path)
#
#         for (bbox, text, prob) in result:
#             print(f"Detected text: {text}")
#             if 'Views' in text:  # Look for the text indicating views
#                 views_str = text.split()[0]  # Get the first part (number of views)
#                 break
#
#         if views_str:  # Stop if views are found
#             break
#
#         # Scroll down the page
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause_time)  # Wait for the page to load
#
#     if views_str:
#         return parse_views(views_str)  # Convert to numeric value
#     return 0  # Return 0 if views cannot be extracted
#
# # Function to get views from the URL
# def get_views(url):
#     driver = create_driver()
#     views = scroll_and_take_screenshot(driver, url)
#     driver.quit()  # Close the driver
#     return views
#
# # Flask app routes
# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]  # Split input by lines
#         views_list = []
#         cumulative_views = 0
#
#         for url in urls:
#             print(f"Processing URL: {url}")
#             views = get_views(url)  # Process each URL
#             views_list.append(views)
#             cumulative_views += views
#
#         # Create a list of tuples for rendering in HTML
#         results = list(zip(urls, views_list))
#
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)
#
#
# ##headless v1.ss
#
# from flask import Flask, render_template, request
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import easyocr
#
# app = Flask(__name__)
#
# # Configure Selenium to use Chrome in full headless mode
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better screenshot
#     chrome_options.add_argument("--headless")  # Run Chrome in headless mode
#     chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
#     chrome_options.add_argument("--disable-software-rasterizer")  # Prevent rendering
#     chrome_options.add_argument("--disable-extensions")  # Disable extensions for improved performance
#     chrome_options.add_argument("--log-level=3")  # Suppress logs
#     chrome_options.add_argument("--remote-debugging-port=9222")  # Required for some headless environments
#     chrome_options.add_argument("--hide-scrollbars")  # Hide scrollbars in screenshots
#     chrome_options.add_argument("--disable-notifications")  # Disable notifications
#     chrome_options.add_argument("--disable-infobars")  # Disable info bars like "Chrome is being controlled"
#     chrome_options.add_argument("--headless=new")  # This is needed to make sure the headless mode runs in the background on some systems
#
#     # Suppress any automation-related infobars and UI elements
#     chrome_options.add_argument("--disable-automation")  # Disable automation UI warnings
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# # Parse views from string (handles 'K' and 'M' suffixes for large numbers)
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').replace('.', '').strip()) * 1000  # Handles both '12K' and '12.5K'
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').strip()) * 1000000  # Handles '1.2M'
#         else:
#             return float(views_str.replace(',', '').strip())  # Handle cases like '12000'
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails

# # Scroll the page and capture screenshot
# def scroll_and_take_screenshot(driver, url):
#     driver.get(url)
#
#     # Wait for the page to load
#     time.sleep(5)
#
#     # Initialize EasyOCR reader
#     reader = easyocr.Reader(['en'])
#
#     views_str = ""
#     max_scrolls = 10  # Limit the number of scrolls
#     scroll_pause_time = 2  # Time to wait after each scroll
#
#     for _ in range(max_scrolls):
#         # Take a screenshot of the page
#         screenshot_path = "screenshot.png"
#         driver.save_screenshot(screenshot_path)
#
#         # Read text from the screenshot
#         result = reader.readtext(screenshot_path)
#
#         for (bbox, text, prob) in result:
#             print(f"Detected text: {text}")
#             if 'Views' in text:  # Look for the text indicating views
#                 views_str = text.split()[0]  # Get the first part (number of views)
#                 break
#
#         if views_str:  # Stop if views are found
#             break
#
#         # Scroll down the page
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause_time)  # Wait for the page to load
#
#     if views_str:
#         return parse_views(views_str)  # Convert to numeric value
#     return 0  # Return 0 if views cannot be extracted
#
# # Function to get views from the URL
# def get_views(url):
#     driver = create_driver()
#     views = scroll_and_take_screenshot(driver, url)
#     driver.quit()  # Close the driver
#     return views
#
# # Flask app routes
# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]  # Split input by lines
#         views_list = []
#         cumulative_views = 0
#
#         for url in urls:
#             print(f"Processing URL: {url}")
#             views = get_views(url)  # Process each URL
#             views_list.append(views)
#             cumulative_views += views
#
#         # Create a list of tuples for rendering in HTML
#         results = list(zip(urls, views_list))
#
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


##updated ss
# from flask import Flask, render_template, request
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import easyocr
#
# app = Flask(__name__)
#
# # Configure Selenium to use Chrome in headless mode
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better screenshot
#     chrome_options.add_argument("--headless")  # Run Chrome in headless mode
#     chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
#     chrome_options.add_argument("--disable-software-rasterizer")  # Prevent rendering
#     chrome_options.add_argument("--disable-extensions")  # Disable extensions for improved performance
#     chrome_options.add_argument("--log-level=3")  # Suppress logs
#     chrome_options.add_argument("--remote-debugging-port=9222")  # Required for some headless environments
#     chrome_options.add_argument("--hide-scrollbars")  # Hide scrollbars in screenshots
#     chrome_options.add_argument("--disable-notifications")  # Disable notifications
#     chrome_options.add_argument("--disable-infobars")  # Disable info bars like "Chrome is being controlled"
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# # Parse views from string (handles 'K' and 'M' suffixes for large numbers)
# # Parse views from string (handles 'K' and 'M' suffixes for large numbers)
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         # Handles '12K', '12.5K', '1M', '1.2M'
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').strip()) * 1000  # Handles both '12K' and '12.5K'
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').strip()) * 1000000  # Handles '1.2M'
#         else:
#             return float(views_str.replace(',', '').strip())  # Handle cases like '12000'
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails
# # Return 0 if conversion fails
#
#
# # Scroll the page and capture screenshot
# def scroll_and_take_screenshot(driver, url):
#     driver.get(url)
#     time.sleep(3)  # Reduced wait time for page load
#
#     # Initialize EasyOCR reader
#     reader = easyocr.Reader(['en'])
#
#     views_str = ""
#     max_scrolls = 5  # Reduced number of scrolls for efficiency
#     scroll_pause_time = 1.5  # Shorter wait time between scrolls
#
#     for _ in range(max_scrolls):
#         screenshot_path = "screenshot.png"
#         driver.save_screenshot(screenshot_path)
#
#         result = reader.readtext(screenshot_path)
#
#         for _, text, _ in result:
#             if 'Views' in text:
#                 views_str = text.split()[0]  # Get the first part (number of views)
#                 break
#
#         if views_str:
#             break
#
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause_time)
#
#     return parse_views(views_str) if views_str else 0  # Return parsed views or 0 if not found
#
# # Function to get views from the URL
# def get_views(url):
#     driver = create_driver()
#     views = scroll_and_take_screenshot(driver, url)
#     driver.quit()
#     return views
#
# # Flask app routes
# @app.route("/", methods=["GET", "POST"])
# def home():
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
#         views_list = []
#         cumulative_views = 0
#
#         for url in urls:
#             views = get_views(url)
#             views_list.append(views)
#             cumulative_views += views
#
#         results = list(zip(urls, views_list))
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


##ss,updated, browser opens once
# from flask import Flask, render_template, request
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import easyocr
#
# app = Flask(__name__)
#
# # Configure Selenium to use Chrome in headless mode
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better screenshot
#     chrome_options.add_argument("--headless")  # Run Chrome in headless mode
#     chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
#     chrome_options.add_argument("--disable-software-rasterizer")  # Prevent rendering
#     chrome_options.add_argument("--disable-extensions")  # Disable extensions for improved performance
#     chrome_options.add_argument("--log-level=3")  # Suppress logs
#     chrome_options.add_argument("--remote-debugging-port=9222")  # Required for some headless environments
#     chrome_options.add_argument("--hide-scrollbars")  # Hide scrollbars in screenshots
#     chrome_options.add_argument("--disable-notifications")  # Disable notifications
#     chrome_options.add_argument("--disable-infobars")  # Disable info bars like "Chrome is being controlled"
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# # Function to open a URL in a new tab
# def open_url_in_new_tab(driver, url):
#     # Open a new tab
#     driver.execute_script("window.open('');")
#     driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
#     driver.get(url)
#
# # Parse views from string (handles 'K' and 'M' suffixes for large numbers)
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').strip()) * 1000  # Handles both '12K' and '12.5K'
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').strip()) * 1000000  # Handles '1.2M'
#         else:
#             return float(views_str.replace(',', '').strip())  # Handle cases like '12000'
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails
#
# # Scroll the page and capture screenshot
# def scroll_and_take_screenshot(driver, url):
#     open_url_in_new_tab(driver, url)  # Open the URL in a new tab
#     time.sleep(3)  # Reduced wait time for page load
#
#     # Initialize EasyOCR reader
#     reader = easyocr.Reader(['en'])
#
#     views_str = ""
#     max_scrolls = 5  # Reduced number of scrolls for efficiency
#     scroll_pause_time = 1.5  # Shorter wait time between scrolls
#
#     for _ in range(max_scrolls):
#         screenshot_path = "screenshot.png"
#         driver.save_screenshot(screenshot_path)
#
#         result = reader.readtext(screenshot_path)
#
#         for _, text, _ in result:
#             if 'Views' in text:
#                 views_str = text.split()[0]  # Get the first part (number of views)
#                 break
#
#         if views_str:
#             break
#
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause_time)
#
#     return parse_views(views_str) if views_str else 0  # Return parsed views or 0 if not found
#
# # Function to get views from multiple URLs using the same driver instance
# def get_views(driver, url):
#     views = scroll_and_take_screenshot(driver, url)
#     return views
#
# # Flask app routes
# @app.route("/", methods=["GET", "POST"])
# def home():
#     driver = create_driver()  # Initialize the driver once
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
#         views_list = []
#         cumulative_views = 0
#
#         for url in urls:
#             views = get_views(driver, url)
#             views_list.append(views)
#             cumulative_views += views
#
#         results = list(zip(urls, views_list))
#         driver.quit()  # Close the driver after processing all URLs
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


##v2 s.recorder,,opens tabs once
# from flask import Flask, render_template, request
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import easyocr
#
# app = Flask(__name__)
#
# # Configure Selenium to use Chrome in headless mode
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better screenshot
#     chrome_options.add_argument("--headless")  # Run Chrome in headless mode
#     chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
#     chrome_options.add_argument("--disable-software-rasterizer")  # Prevent rendering
#     chrome_options.add_argument("--disable-extensions")  # Disable extensions for improved performance
#     chrome_options.add_argument("--log-level=3")  # Suppress logs
#     chrome_options.add_argument("--remote-debugging-port=9222")  # Required for some headless environments
#     chrome_options.add_argument("--hide-scrollbars")  # Hide scrollbars in screenshots
#     chrome_options.add_argument("--disable-notifications")  # Disable notifications
#     chrome_options.add_argument("--disable-infobars")  # Disable info bars like "Chrome is being controlled"
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# # Function to open a URL in a new tab
# def open_url_in_new_tab(driver, url):
#     # Open a new tab
#     driver.execute_script("window.open('');")
#     driver.switch_to.window(driver.window_handles[-1])  # Switch to the new tab
#     driver.get(url)
#
# # Parse views from string (handles 'K' and 'M' suffixes for large numbers)
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').strip()) * 1000  # Handles both '12K' and '12.5K'
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').strip()) * 1000000  # Handles '1.2M'
#         else:
#             return float(views_str.replace(',', '').strip())  # Handle cases like '12000'
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails
#
# # Scroll the page and capture screenshot
# def scroll_and_take_screenshot(driver, url):
#     open_url_in_new_tab(driver, url)  # Open the URL in a new tab
#     time.sleep(3)  # Reduced wait time for page load
#
#     # Initialize EasyOCR reader
#     reader = easyocr.Reader(['en'])
#
#     views_str = ""
#     max_scrolls = 5  # Reduced number of scrolls for efficiency
#     scroll_pause_time = 1.5  # Shorter wait time between scrolls
#
#     for _ in range(max_scrolls):
#         screenshot_path = "screenshot.png"
#         driver.save_screenshot(screenshot_path)
#
#         result = reader.readtext(screenshot_path)
#
#         for _, text, _ in result:
#             if 'Views' in text:
#                 views_str = text.split()[0]  # Get the first part (number of views)
#                 break
#
#         if views_str:
#             break
#
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause_time)
#
#     return parse_views(views_str) if views_str else 0  # Return parsed views or 0 if not found
#
# # Function to get views from multiple URLs using the same driver instance
# def get_views(driver, url):
#     views = scroll_and_take_screenshot(driver, url)
#     return views
#
# # Flask app routes
# @app.route("/", methods=["GET", "POST"])
# def home():
#     driver = create_driver()  # Initialize the driver once
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
#         views_list = []
#         cumulative_views = 0
#
#         for url in urls:
#             views = get_views(driver, url)
#             views_list.append(views)
#             cumulative_views += views
#
#         results = list(zip(urls, views_list))
#         driver.quit()  # Close the driver after processing all URLs
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


##s.record v3. updated

from flask import Flask, render_template, request

app = Flask(__name__)

# Configure Selenium to use Chrome in headless mode
from flask import Flask, render_template, request
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
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
  # Initialize EasyOCR once and store it in the driver instance
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))




# ##s record v4
# from flask import Flask, render_template, request
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import easyocr
# #
# app = Flask(__name__)
#
# # Configure Selenium to use Chrome in headless mode
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--headless")  # Run Chrome in headless mode
#     chrome_options.add_argument("--disable-extensions")  # Disable extensions for improved performance
#     chrome_options.add_argument("--log-level=3")  # Suppress logs
#     chrome_options.add_argument("--window-size=1920,1080")  # Set window size for better screenshot
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     return driver
#
# # Open a URL in a new tab
# def open_url_in_new_tab(driver, url):
#     driver.execute_script("window.open('');")
#     driver.switch_to.window(driver.window_handles[-1])
#     driver.get(url)
#
# # Parse views from string (handles 'K' and 'M' suffixes for large numbers)
# def parse_views(views_str):
#     try:
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').strip()) * 1000
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').strip()) * 1_000_000
#         else:
#             return float(views_str.replace(',', '').strip())
#     except ValueError:
#         return 0
#
# # Scroll the page and capture views
# def scroll_and_capture_views(driver, url, reader):
#     open_url_in_new_tab(driver, url)
#
#     time.sleep(3)  # Allow time for the page to load
#     views_list = []
#
#     max_scrolls = 5
#     scroll_pause_time = 1.5
#
#     for _ in range(max_scrolls):
#         driver.save_screenshot("screenshot.png")
#         result = reader.readtext("screenshot.png")
#
#         # Collect views from the extracted text
#         for _, text, _ in result:
#             if 'Views' in text:
#                 views_list.append(parse_views(text.split()[0]))
#
#         # Scroll down to load more content
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause_time)  # Allow new content to load
#
#     return sum(views_list)  # Return total views from the list
#
# # Flask app route
# @app.route("/", methods=["GET", "POST"])
# def home():
#     driver = create_driver()
#     reader = easyocr.Reader(['en'])
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
#         views_list = []
#         cumulative_views = 0
#
#         for url in urls:
#             views = scroll_and_capture_views(driver, url, reader)
#             views_list.append(views)
#             cumulative_views += views
#
#         results = list(zip(urls, views_list))
#         driver.quit()  # Close the driver after processing all URLs
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# if __name__ == "__main__":
#     app.run(debug=True)


# ##exe.file
#
# from flask import Flask, render_template, request
# import time
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from concurrent.futures import ThreadPoolExecutor
# import easyocr
# import webbrowser
# from threading import Timer
# import os
#
# app = Flask(__name__)
#
# # Configure Selenium to use Chrome in headless mode
# def create_driver():
#     chrome_options = Options()
#     chrome_options.add_argument("--no-sandbox")
#     chrome_options.add_argument("--disable-dev-shm-usage")
#     chrome_options.add_argument("--window-size=1280x720")  # Lower resolution for performance
#     chrome_options.add_argument("--headless")  # Run Chrome in headless mode
#     chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration
#     chrome_options.add_argument("--disable-software-rasterizer")  # Prevent rendering
#     chrome_options.add_argument("--disable-extensions")  # Disable extensions for improved performance
#     chrome_options.add_argument("--log-level=3")  # Suppress logs
#     chrome_options.add_argument("--disable-background-networking")  # Avoid unnecessary network traffic
#     chrome_options.add_argument("--disable-sync")
#     chrome_options.add_argument("--disable-translate")
#     chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
#     chrome_options.add_experimental_option('useAutomationExtension', False)
#
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
#     driver.reader = easyocr.Reader(['en'])  # Initialize EasyOCR once and store it in the driver instance
#     return driver
#
# # Function to open a URL and ensure the page loads
# def open_url(driver, url):
#     driver.get(url)
#     WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))  # Wait for the body to load
#
# # Parse views from string (handles 'K' and 'M' suffixes for large numbers)
# def parse_views(views_str):
#     """Convert views string to numeric value."""
#     try:
#         if 'K' in views_str:
#             return float(views_str.replace('K', '').strip()) * 1000  # Handles both '12K' and '12.5K'
#         elif 'M' in views_str:
#             return float(views_str.replace('M', '').strip()) * 1000000  # Handles '1.2M'
#         else:
#             return float(views_str.replace(',', '').strip())  # Handle cases like '12000'
#     except ValueError:
#         print(f"Could not convert views string '{views_str}' to float.")
#         return 0  # Return 0 if conversion fails
#
# # Scroll the page and capture screenshot
# def scroll_and_take_screenshot(driver, url):
#     open_url(driver, url)  # Open the URL
#
#     views_str = ""
#     max_scrolls = 5
#     scroll_pause_time = 1.5
#
#     for _ in range(max_scrolls):
#         screenshot_path = "screenshot.png"
#         driver.save_screenshot(screenshot_path)
#
#         result = driver.reader.readtext(screenshot_path)
#
#         for _, text, _ in result:
#             if 'Views' in text:
#                 views_str = text.split()[0]  # Get the first part (number of views)
#                 break
#
#         if views_str:
#             break
#
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(scroll_pause_time)
#
#     return parse_views(views_str) if views_str else 0  # Return parsed views or 0 if not found
#
# # Function to get views from multiple URLs using the same driver instance in parallel
# def get_views_in_parallel(driver, urls):
#     views_list = []
#     for url in urls:
#         views_list.append(get_views(driver, url))
#     return views_list
#
# # Function to get views from a single URL
# def get_views(driver, url):
#     views = scroll_and_take_screenshot(driver, url)
#     return views
#
# # Flask app routes
# @app.route("/", methods=["GET", "POST"])
# def home():
#     driver = create_driver()  # Initialize the driver once
#     if request.method == "POST":
#         urls_input = request.form.get("urls")
#         urls = [url.strip() for url in urls_input.splitlines() if url.strip()]
#         cumulative_views = 0
#
#         # Get views for all URLs sequentially to ensure each one is properly processed
#         views_list = get_views_in_parallel(driver, urls)
#
#         for views in views_list:
#             cumulative_views += views
#
#         results = list(zip(urls, views_list))
#         driver.quit()  # Close the driver after processing all URLs
#         return render_template("index.html", results=results, cumulative=cumulative_views)
#
#     return render_template("index.html")
#
# # Function to open the default web browser
# def open_browser():
#     webbrowser.get('chrome').open_new("http://127.0.0.1:5000/")
#
#
# if __name__ == "__main__":
#     # Start a timer to open the browser after 1 second
#     Timer(1, open_browser).start()
#     app.run(host='0.0.0.0', port=5000)
