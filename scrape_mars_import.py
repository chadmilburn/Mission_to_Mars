# %%
# import dendencies
import pandas as pd
import requests
import os
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time 

# %%
# url to scrape
url = 'https://mars.nasa.gov/news/'

# %%
# Retrieve page with the requests module
response = requests.get(url)

# %%
# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(response.text, 'html.parser')

# %%
# Examine the results, then determine element that contains sought info
#print(soup.prettify())

# %%
# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# %%
# splinter url 
browser.visit(url)

# %%
#print headlines
headlines = soup.find_all('div', class_='content_title')

# %%
#print(headlines)

# %%
#store first head line as news_title
news_title = headlines[0].text.strip()
#print(news_title)

# %%
#find first paragraph
teaser = soup.find_all('div', class_="rollover_description_inner")
#print(teaser)

# %%
#store paragraph as news_p
news_p = teaser[0].text.strip()
#print(news_p)

# %%
browser.quit() 

# %%
# open new splinter browser
from webdriver_manager.chrome import ChromeDriverManager
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# %%

# new url 
jplurl = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
# splinter url 
browser.visit(jplurl)
time.sleep(3)

# %%
# Retrieve page html
html = browser.html
# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(html, 'html.parser')

# %%
image = soup.find('a', class_="showimg")['href']
#print(image)

# %%
featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + image
#featured_image_url

# %%
# click link to feature image
 #browser.links.find_by_partial_text('Full Image').click()

# %%
browser.quit() 

# %%
#scrape table from https://space-facts.com/mars/
tableurl = "https://space-facts.com/mars/"

# %%
#!pip install lxml

# %%
# retrieve table 
tables = pd.read_html(tableurl)
#tables

# %%
# check that correct table is in dataframe
df = tables[0]
#df.head()

# %%
# Use Pandas to convert the data to a HTML table string.
html_table = df.to_html(index=False, header=False)
#html_table

# %%
# save HTML to file for later use
#text_file = open("Mars_Table.html", "w")
#text_file.write(html_table)
#text_file.close()

# %%
# open new splinter browser
from webdriver_manager.chrome import ChromeDriverManager
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# %%
# set up urls 
# this url is the base to use to find both the name and image info
base_url = 'https://astrogeology.usgs.gov'
# this addition to the base will allow us to scrape the hemisphere name
url = '/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

# %%
# visit url in splinter
browser.visit(base_url + url)
time.sleep(3)

# %%
# Retrieve html
html = browser.html
# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(html, 'html.parser')
# view the html
#print(soup.prettify())

# %%
# name is in div class='item' in h3 element
names = soup.find_all('div', class_='item')
#print(names)

# %%
# loop to get and store names in a list
titles=[]

for name in names:
    titles.append(name.find('h3').text.strip())

titles

# %%
"""
The loop needs more than just the titles to get the image url. Need go into each hemisphere link to pull the image url.
"""

# %%
# loop the get and store hemisphere urls to get image sub url. This is loacted in a element and must be concatenated
# to the base url
title_url = []

for name in names:
    title_url.append(base_url + (name.find('a')['href']))
    
title_url


# %%
# check the above route to url
browser.visit(title_url[0])

# %%
# Retrieve html
html = browser.html
# Create BeautifulSoup object; parse with 'html.parser'
soup = BeautifulSoup(html, 'html.parser')
# view the html
#print(soup.prettify())

# %%
# check info scrape
img_sub_url = soup.find('img', class_='wide-image')['src']
#img_sub_url

# %%
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
# check loop    
#img_url
    


# %%
browser.quit() 

# %%
# create a list of dict called 'hemisphere_image_urls' use key 'title' from list titles and value 'img_url' 
# blank list
hemisphere_image_urls =[]

# loop to combine list into dictonary and then add to blank list
for x in range(len(img_url)):
    # for x combine the key value pair with comprehension and add the h_i_u list
    hemisphere_image_urls.append({'title':titles[x], 'img_url': img_url[x]})
    
# show list of dict
#hemisphere_image_urls