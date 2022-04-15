from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import pyperclip
from config import NAVER_ID, NAVER_PW



def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def get_naver_cookies():
    driver = set_chrome_driver()
    driver.get("https://nid.naver.com/nidlogin.login")
    pyperclip.copy(NAVER_ID)
    driver.find_element(By.ID,'id').click()
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
    sleep(1)
    pyperclip.copy(NAVER_PW)
    driver.find_element(By.ID,'pw').click()
    ActionChains(driver).key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
    sleep(1)
    driver.find_element(By.ID,'log.login').click()
    sleep(1)
    cookies = driver.get_cookies()
    return cookies