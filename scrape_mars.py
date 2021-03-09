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
    return browser

# create scraping function
def scrape():
    #splinter
    browser = init_browser()
    # create empty dict for HTML rendering
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

    # JPL Image 
    
    jpl_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(jpl_url)
    time.sleep(3)
    html = browser.html
    jpl_image_soup = bs(html, 'html.parser')

    # scrape the needed link and concatnate with link for full image link
    image = jpl_image_soup.find('a', class_='showimg')['href']
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image

    # Mars Facts-Scrape table and convert to HTML
    tableurl = "https://space-facts.com/mars/"
    tables = pd.read_html(tableurl)
    df = tables[0]
    html_table = df.to_html(index=False, header=False)

    # Mars Hemispheres
    # set up urls 
    # this url is the base to use to find both the name and image info
    base_url = 'https://astrogeology.usgs.gov'
    # this addition to the base will allow us to scrape the hemisphere name
    url = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(base_url + url)
    time.sleep(3)
    facts_soup = bs(html, 'html.parser')
    names = facts_soup.find_all('div', class_='item')
    # loop to get and store names in a list
    titles=[]
    for name in names:
        titles.append(name.find('h3').text.strip())
    # loop the get and store hemisphere urls to get image sub url. This is loacted in a element and must be concatenated
    # to the base url
    title_url = []
    for name in names:
        title_url.append(base_url + (name.find('a')['href']))

    





