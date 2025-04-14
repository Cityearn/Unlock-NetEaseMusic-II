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
    browser.add_cookie({"name": "MUSIC_U", "value": "0011EFA0A294A985C4918ABB6114FD4505239063F1CA560D9A255FCD14F11CABC09C86F4C286AC5BBB59371F5BDB392A1F1D3FBF02FCCAA1E7170D7DD11F8329FD10A7AFCE5037F35765AB0F1394423F7D72D47A2306D65DA3BB365925435D0263B3E8902A38C9AE7E0CDC4A87B0394C734240C77A00851ED0E83DA7267290C61AAFBD702FED14143297263644C8C61FF13CF14697D3F78D6A0C5BB8ACC7F3F48ECB42350854C7C38E41A1903EA26389D75ACDC968A17221EE5ED68C0A91245404A78FBD0B85F0409C53559E7BF662CEDAF679C967101DA8A3CEFD4B56B5DFA5E8656BD6A108F2F85364B5E58E7BF65C0A121CD716C51BD02A31F4A1497D4A7766FF025E20B3CE2A06717922DF2EA777EFBB00F5F5D22B97D6AE2177B7C1946FF856AA8FDF158D9F33188B8AC8A8772C8140585B1226CC3EDA96CC110E60503F1F722C54E178817D8A75ECE19F93C777D5
"})
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
