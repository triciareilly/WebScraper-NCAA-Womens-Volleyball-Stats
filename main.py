import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


import urllib.request
import logging
from selenium import webdriver
from bs4 import BeautifulSoup

if __name__ == '__main__':
    """ main """

    logger = logging.getLogger()

    from selenium import webdriver

    # driver = webdriver.Chrome("\\chromedriver.exe")

    # url = 'https://www.ncaa.com/sports/volleyball-women/d1'
    url = "https://www.ncaa.com/game/6079447"

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    page = driver.execute_script('return document.body.innerHTML')

    # soup = BeautifulSoup(page, 'html.parser')

    # homeBoxScores = soup.find_all("table")
    boxscores = driver.find_elements(By.XPATH, '//*[@id="gamecenterAppContent"]/div/div[2]/div[1]/table')
    for boxscore in boxscores:
        print(boxscore.get_attribute('innerHTML'))


    # homeBoxScores = soup.find("table", class_="boxscore-table_sets_home")
    # print(homeBoxScores)

