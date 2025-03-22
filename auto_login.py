# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "007140934E371D6B58DC7D05FC163AD891CFF716F5B06252A6A8FC97A2B18B4A3541C1D8A9F59A6FFE67EABF82BF3974BF7A89C7034069703BBE7B852101ACFE3A3323DF769EDDBC339D9A6F27E17FF429AF0DC5214F8AAF80A043F28D97084A3A442E9D9361F9601973C213D6966B3EB1AB414ABDEAD215F3455A1EDC876D5843C98D317DE61A4FABA4CA426DBFC86A8E09B29C2460356FDCF7997CF6998242650C6BBE95575C3A6C96CAFA73FD51B8552EC7DA5F8B90397A660FF7A257300A0780CEB9582252B6AC3D2E88BA2A85FDF7BF3ACDACDB83F3C6625EA5277818AC824A48F5ECC5BD161FBCB65F1AF69E928A72E42DB01F98745932770C816BE7F20302504390FD4D49A8BFFDB8F854BE30E80833701D91D889728986E0797D44163A079405D59D5F54215A061F5CB428C5D7635572DB4D9DEF989EB7A762954E98747F32F74B64827B1E942CB468EA816144"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
