from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
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

    driver.get("https://cafe.naver.com/chocammall?iframe_url_utf8=%2FArticleRead.nhn%253Fclubid%3D20486145%2526page%3D1%2526menuid%3D214%2526boardtype%3DL%2526articleid%3D7586243%2526referrerAllArticles%3Dfalse")    
    sleep(0.2)
    driver.switch_to.frame('cafe_main')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup.find('strong', {'class':'cost'}).text.strip())
    
    driver.get("https://cafe.naver.com/chocammall?iframe_url_utf8=%2FArticleRead.nhn%253Fclubid%3D20486145%2526page%3D1%2526menuid%3D214%2526boardtype%3DL%2526articleid%3D7586307%2526referrerAllArticles%3Dfalse")
    sleep(0.2)
    driver.switch_to.frame('cafe_main')
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup.find('strong', {'class':'cost'}).text.strip())
    # driver.get("cafe.naver.com/ArticleList.nhn?search.clubid=20486145&search.menuid=214&search.boardtype=L")
    # sleep(1)
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # print(soup)

    return driver