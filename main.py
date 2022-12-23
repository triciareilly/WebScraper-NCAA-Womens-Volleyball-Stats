#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Module documentation goes here
   and here
   and ...
"""
__author__ = "Patricia Reilly"
__contact__ = "triciaereilly@gmail.com"
__copyright__ = ""
__credits__ = []
__date__ = "2022/12/20"
__deprecated__ = False
__email__ =  "triciaereilly@gmail.com"
__license__ = ""
__maintainer__ = "developer"
__status__ = ""
__version__ = "0.0.1"

# Standard Library
import json
import logging

# Third Party Packages
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.remote.webelement import WebElement
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By



player_stats = []


def get_headers_from_html_table(boxscore: WebElement) -> list:
    """
    Returns the second row (the proper headers) from the boxscore html table
    as a list.

    The boxscore web element contains a html table of player stats. The table
    contains two rows of headers. The second row of headers in the table is
    found, cleaned up, and returned in a list.
    """
    headers = []
    # Retrieve header data
    for table_body in boxscore.find_elements(By.TAG_NAME, 'thead'):
        # Find the header rows
        rows = table_body.find_elements(By.TAG_NAME, 'tr')

        # Header labels in the second row are more relevant to the data
        for col in rows[1].find_elements(By.TAG_NAME, 'th'):
            # Pull out and clean up the data from the cells and store them in a
            # list
            tmp = col.get_attribute('innerHTML').replace('\n', '')
            headers.append(tmp)
    return headers


def get_rows_from_html_table(boxscore: WebElement, headers: list) -> list:
    """
    Returns all the rows from the boxscore html table as a list of dicts with
    the headers.

    The boxscore web element contains a html table of player stats. The table
    contains many rows of data. The rows of data in the table is
    found, cleaned up, and returned in a list excluding the final row which
    contains the word "Final".

    """
    boxscore_stats = []
    # Retrieve table data from body of table
    for table_body in boxscore.find_elements(By.TAG_NAME, 'tbody'):
        # Store each row
        rows = table_body.find_elements(By.TAG_NAME, 'tr')
        for row in rows:
            # Find the data in the cells of each row
            cells = row.find_elements(By.TAG_NAME, 'td')
            boxscore_stat = {}

            # Pair up each cell with the corresponding header label for storing
            # in JSON
            for (cell, header) in zip(cells, headers):
                # Pull out and clean up the data from the cells and store them
                # in a list
                data = cell.get_attribute('innerHTML').replace('\n', '')
                # Last line of table is irrelevant and shows total so skip
                # storing this row
                if "total" in str(data).lower():
                    break
                print(header + ": " + data)
                # Store header label and data in a list of dictionaries
                boxscore_stat[header].append(data)
        boxscore_stats.append(boxscore_stat)

    return boxscore_stats


if __name__ == '__main__':
    """ main """

    logger = logging.getLogger()

    player_stats = []
    # driver = webdriver.Chrome("\\chromedriver.exe")

    # url = 'https://www.ncaa.com/sports/volleyball-women/d1'
    url = "https://www.ncaa.com/game/6079447"

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(url)
    page = driver.execute_script('return document.body.innerHTML')

    boxscores = driver.find_elements(By.XPATH, '//*[@id="gamecenterAppContent"]/div/div[2]/div[1]/table')

    if len(boxscores) <= 0:
        raise Exception(f"No Boxscore data was found at {url}.")
    else:
        for boxscore in boxscores:
            # Assumption made that there is only one boxscore on the page
            headers = get_headers_from_html_table(boxscore)
            player_stats = get_rows_from_html_table(boxscore, headers)


