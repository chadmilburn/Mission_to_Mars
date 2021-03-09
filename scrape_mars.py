# import dendencies
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymongo

# create browser function to call as needed with scraping
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# create scraping function
def scrape():
    #splinter
    browser = init_browser()
    # create dict for HTML rendering
    mars_dict = {}

    # scrape headlines and teaser from news https://mars.nasa.gov/news/ 
    # updated url var for readability
    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)
    time.sleep(3)
    html = browser.html
    news_soup = bs(html, 'html.parser')
    
    # scrape the needed head line and teaser
    news_title = news_soup.find_all('div', class_='content_title')[0].text.strip()
    news_p = news_soup.find_all('div', class_='rollover_description_inner')[0].text.strip()

    return
    print(news_title)
