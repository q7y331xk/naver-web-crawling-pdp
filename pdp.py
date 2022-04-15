from time import sleep
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium import webdriver


def pdp(driver):
    driver.get("cafe.naver.com/ArticleList.nhn?search.clubid=20486145&search.menuid=214&search.boardtype=L")
    sleep(1)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    print(soup)
