# import dendencies
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time
import pymongo

# create browser function to call as needed with scraping
def init_browser():
    from webdriver_manager.chrome import ChromeDriverManager
    executable_path = {'executable_path': ChromeDriverManager().install()}
   
    return Browser('chrome', **executable_path, headless=False)

# create scraping function
def scrape():
    mars_dict = {}

    # nasa news
    # url to scrape
    url = 'https://mars.nasa.gov/news/'
    # Retrieve page with the requests module
    response = requests.get(url)
    # html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    # headlines
    headlines = soup.find_all('div', class_='content_title')
    #store first head line as news_title
    news_title = headlines[0].text.strip()
    #find first paragraph
    teaser = soup.find_all('div', class_="rollover_description_inner")
    #store paragraph as news_p
    news_p = teaser[0].text.strip()
     

    # jpl image
    browser = init_browser()
    # new url 
    jplurl = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    # splinter url 
    browser.visit(jplurl)
    time.sleep(3)
    # Retrieve page html
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')
    image = soup.find('a', class_="showimg")['href']
    featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image
    browser.quit() 

    # mars facts
    #scrape table from https://space-facts.com/mars/
    tableurl = "https://space-facts.com/mars/"
    # retrieve table 
    tables = pd.read_html(tableurl)
    # check that correct table is in dataframe
    df = tables[0]
    # Use Pandas to convert the data to a HTML table string.
    html_table = df.to_html(index=False, header=False)  

    # mars hemispheres
    browser = init_browser()
    # set up urls 
    # this url is the base to use to find both the name and image info
    base_url = 'https://astrogeology.usgs.gov'
    # this addition to the base will allow us to scrape the hemisphere name
    url = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'  
    # visit url in splinter
    browser.visit(base_url + url)
    time.sleep(3)
    # Retrieve html
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')  
    # name is in div class='item' in h3 element
    names = soup.find_all('div', class_='item')    
    # loop to get and store names in a list
    titles=[]

    for name in names:
        titles.append(name.find('h3').text.strip())
    
    # loop the get and store hemisphere urls to get image sub url. This is loacted in a element and must be concatenated
    # to the base url
    title_url = []

    for name in names:
        title_url.append(base_url + (name.find('a')['href']))

    # check the above route to url
    browser.visit(title_url[0])

    # Retrieve html
    html = browser.html
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    # check info scrape
    img_sub_url = soup.find('img', class_='wide-image')['src']

    #loop to pull all full size image urls
    img_url = []

    for h_url in title_url:
        #open browser for each url
        browser.visit(h_url)
        # Create BeautifulSoup object; parse with 'html.parser'
        soup = BeautifulSoup(html, 'html.parser')
        # create new url for list
        image_url = base_url + soup.find('img', class_='wide-image')['src']
        # add url to list for dict 
        img_url.append(image_url)

    browser.quit() 

    # create a list of dict called 'hemisphere_image_urls' use key 'title' from list titles and value 'img_url' 
    # blank list
    hemisphere_image_urls =[]

    # loop to combine list into dictonary and then add to blank list
    for x in range(len(img_url)):
        # for x combine the key value pair with comprehension and add the h_i_u list
        hemisphere_image_urls.append({'title':titles[x], 'img_url': img_url[x]})



    mars_dict = {
        'news_title': news_title  ,
        'news_p': news_p ,
        'featured_image_url': featured_image_url  ,
        'fact_table' : str(html_table)  ,
        'hemisphere_images' : hemisphere_image_urls
        }
    


    return mars_dict


    

    





