import time
import requests
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

# === Logging Setup ===
log_filename = "automation_log.txt"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename, mode='w', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# === Chrome Setup ===
driver_path = "/usr/local/bin/chromedriver"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(driver_path), options=options)

try:
    # === Open Website ===
    logging.info("🌐 Opening atg.party...")
    url = "https://atg.party"
    start_time = time.time()
    response = requests.get(url)
    logging.info("✅ HTTP Status Code: %s", response.status_code)

    driver.get(url)
    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    load_time = round(time.time() - start_time, 2)
    logging.info("⏱ Page load time: %s seconds", load_time)
    time.sleep(2)

    # === Login ===
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "loginbtn_new"))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "email_landing"))).send_keys("autotest@yopmail.com")
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "password_landing"))).send_keys("Pass@123")

    for btn in WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "button-holder"))):
        try:
            btn.click()
            break
        except:
            continue

    time.sleep(3)

    # === Go to edit bio page ===
    driver.get("https://atg.party/edit-user-bio")
    logging.info("📝 Navigated to edit-user-bio page")
    time.sleep(2)

    # === Update Username ===
    try:
        username = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "new_user_name")))
        username.clear()
        username.send_keys("autotest_user")
        logging.info("✍ Username updated.")
    except Exception as e:
        logging.error("❌ Failed to update username: %s", str(e))

    # === Update Bio (scroll + verify) ===
    try:
        bio = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "about_me")))
        driver.execute_script("arguments[0].scrollIntoView({behavior:'smooth', block:'center'});", bio)
        time.sleep(2)
        bio.clear()
        bio.send_keys("This is an updated bio using Python Selenium automation.")
        time.sleep(2)
        bio_value = bio.get_attribute("value")
        logging.info(f"✍ Bio updated. Final value set: {bio_value}")
    except Exception as e:
        logging.error("❌ Failed to update bio: %s", str(e))

    # === Scroll to Save button, click it, then screenshot ===
    try:
        save_btn = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "acc-save"))
        )

        for i in range(3):
            try:
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", save_btn)
                time.sleep(2)

                if save_btn.is_displayed() and save_btn.is_enabled():
                    try:
                        save_btn.click()
                        logging.info("💾 Save button clicked.")
                    except:
                        driver.execute_script("arguments[0].click();", save_btn)
                        logging.info("💾 Save button clicked via JS fallback.")

                    # Scroll again for screenshot clarity
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", save_btn)
                    time.sleep(4)  # Pause to see the updated form before screenshot

                    driver.save_screenshot("profile_updated.png")
                    logging.info("📸 Screenshot captured: profile_updated.png")
                    break
            except Exception as e:
                logging.warning(f"⚠ Scroll/click attempt {i+1} failed: {str(e)}")

    except Exception as e:
        logging.error("❌ Failed to save profile or capture screenshot: %s", str(e))
        driver.save_screenshot("save_failed.png")

except Exception as e:
    logging.error("🔥 Unexpected error: %s", str(e))
finally:
    logging.info("🟢 Browser ready. Watch it before closing...")
    time.sleep(5)  # 👀 Let you visually inspect everything

    # driver.quit()  # ❌ Leave commented if you want to manually close
