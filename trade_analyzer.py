import math
import csv
import time
import bisect
import bs4
from bs4 import BeautifulSoup
import string
import requests
import random
import requests
import click
from selenium import webdriver
from selenium.webdriver import PhantomJS
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from sys import argv
from urllib.parse import urlparse
from urllib.parse import urljoin
from urllib.request import Request, urlopen

def analyze_trade(league, left_players, right_players, headless):
    nfl_url = 'https://www.fantasysp.com/nfl_trade_analyzer/'
    nba_url = 'https://www.fantasysp.com/nba_trade_analyzer/'

    if headless:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = '/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary'
        driver = webdriver.Chrome(executable_path='/Users/rakeshbhatia/anaconda/envs/fantasy_mgr/chromedriver',   chrome_options=chrome_options)

        #DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0'
        #driver = webdriver.PhantomJS(executable_path='/Users/rakeshbhatia/anaconda/envs/fantasy_mgr/bin/phantomjs')
    else:
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(executable_path='/Users/rakeshbhatia/anaconda/envs/fantasy_mgr/chromedriver', chrome_options=chrome_options)
        driver.set_window_size(1920, 1080)
        driver.maximize_window()

    try:
        print('Getting url')
        if league == 'nfl':
            driver.get(nfl_url)
        elif league == 'nba':
            driver.get(nba_url)

        print('Entering left players')
        for i in range(len(left_players)):
            driver.find_element_by_name('leftplayer' + str(i+1)).send_keys(left_players[i])

        print('Entering right players')
        for i in range(len(right_players)):
            driver.find_element_by_name('rightplayer' + str(i+1)).send_keys(right_players[i])

        wait_time = round(max(2, 6 + random.gauss(0,3)), 2)
        time.sleep(wait_time)

        print('Clicking submit')
        driver.find_element_by_class_name('analyze-trade-submit').click()

        wait_time = round(max(2, 6 + random.gauss(0,3)), 2)
        time.sleep(wait_time)

        #left_div = driver.find_element_by_class_name('point-total')
        left_span = driver.find_element_by_class_name('icon-left')
        left_result = left_span.get_attribute('tally')
        print('left_players: ', left_result)

        #right_div = driver.find_element_by_class_name('point-total')
        right_span = driver.find_element_by_class_name('icon-right')
        right_result = right_span.get_attribute('tally')
        print('right_players: ', right_result)

        if float(left_result) > float(right_result):
            print('Left players are stronger!')
        elif float(left_result) < float(right_result):
            print('Right players are stronger!')
        elif float(left_result) == float(right_result):
            print('Trade is equal!')

        driver.close()

    except:
        print('Exception occurred.')
        driver.close()

def main():
    start_time = time.time()
    #left_players = ['']
    #right_players = ['']
    #left_players = ['']
    #right_players = ['']
    #left_players = ['']
    #right_players = ['']
    #left_players = ['']
    #right_players = ['']
    #left_players = ['']
    #right_players = ['']
    #left_players = ['Chris Paul', 'Andre Drummond', 'Markieff Morris', 'Jordan Bell']
    #right_players = ['Robert Covington', 'Clint Capela', 'Jarrett Allen', 'Kris Dunn']
    left_players = ['Ben Simmons', 'DeAndre Jordan', 'Carmelo Anthony', 'Dirk Nowitzki']
    right_players = ['Joe Ingles', 'Rudy Gobert', 'Dejounte Murray', 'Kristaps Porzingis']
    #left_players = ['Antonio Brown', 'Christian McCaffrey']
    #right_players = ['DeAndre Hopkins', 'Kareem Hunt']
    #left_players = ['Le\'Veon Bell', 'Jay Ajayi']
    #right_players = ['Ezekiel Elliott', 'Derrick Henry']
    headless = False
    league = 'nba'
    analyze_trade(league, left_players, right_players, headless)
    print("--- %s seconds ---" % (time.time() - start_time))

main()
