import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException

# Path to ChromeDriver
driver_path = "/usr/local/bin/chromedriver"

# Setup Chrome options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Initialize driver
driver = webdriver.Chrome(service=Service(driver_path), options=options)

try:
    url = "https://atg.party"
    print("🌐 Opening atg.party...")

    # Start timer for load time
    start_time = time.time()

    # Step 1: Check HTTP status using requests
    response = requests.get(url)
    print("✅ HTTP Status Code for https://atg.party:", response.status_code)

    # Step 2: Open URL in browser
    driver.get(url)

    # Step 3: Wait until page is loaded
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    load_time = round(time.time() - start_time, 2)
    print(f"⏱ Page load time: {load_time} seconds")

    # Step 4: Click Login
    print("🔐 Clicking on Login...")
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "loginbtn_new"))
    )
    login_button.click()

    # Step 5: Fill login form
    print("📨 Filling login credentials...")
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "email_landing"))
    )
    driver.find_element(By.ID, "email_landing").send_keys("wiz_saurabh@rediffmail.com")
    driver.find_element(By.ID, "password_landing").send_keys("Pass@123")

    # Step 6: Submit form
    print("📤 Submitting form...")
    time.sleep(1)  # Ensure layout is stable before click

    submit_divs = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "button-holder"))
    )
    clicked = False
    for div in submit_divs:
        try:
            div.click()
            clicked = True
            break
        except Exception:
            continue

    if not clicked:
        raise TimeoutException("❌ No clickable login button found.")

    print("✅ Login submitted.")
    time.sleep(3)

    # Step 7: Navigate to article page
    driver.get("https://atg.party/article")

    # Step 8: Fill article form
    print("📝 Filling article form...")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "title"))
    ).send_keys("Sample Article Title")
    driver.find_element(By.NAME, "description").send_keys("This is a sample article posted using Selenium.")

    # Upload cover image (make sure the image path exists)
    image_input = driver.find_element(By.NAME, "cover")
    image_input.send_keys("/home/ajaz/selenium-task/sample.jpg")

    # Step 9: Post the article
    print("📨 Posting article...")
    post_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "post-btn"))
    )
    post_btn.click()

    # Step 10: Wait for redirection and print new URL
    WebDriverWait(driver, 10).until(
        lambda d: d.current_url != "https://atg.party/article"
    )
    print("✅ Article posted. Redirected to:", driver.current_url)

except TimeoutException as te:
    print("❌ Timeout occurred:", te.msg)
except ElementNotInteractableException as e:
    print("❌ Element not interactable:", e.msg)
except Exception as e:
    print("❌ An unexpected error occurred:", str(e))
finally:
    print("🟢 Browser closed.")
    driver.quit()
