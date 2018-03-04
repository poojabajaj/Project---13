#Dependencies
from splinter import Browser
from pprint import pprint
import pymongo
import time
from bs4 import BeautifulSoup as bs
from os import getcwd
from os.path import join
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def makeSoup(url):
    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html.parser'
    soup = bs(response.text, 'html.parser')
    return soup
    

def scrape():
    browser = init_browser()
    listings = {}

    # URL of page to be scraped
    nasa_soup= makeSoup('https://mars.nasa.gov/news/')

    
    title = nasa_soup.find('div',class_ = "content_title")
    
    #variable to go to dictionary
    news_title = title.find('a').text

    news_url = 'https://mars.nasa.gov'+ title.a['href']

    # Create BeautifulSoup object; parse with 'html.parser'
    newsoup = makeSoup(news_url)

    # results are returned as an iterable list ##paragraph
    #variable to go to dictionary
    news_p = newsoup.find('p').text

    #JPL Mars Space Images - Featured Image
    jpl_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    #browser = Browser('chrome', headless=False)
    browser.visit(jpl_image_url)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2)


    #Use splinter to navigate the site and find the image url for the current Featured Mars Image 
    #and assign the url string to a variable called featured_image_url.
    html = browser.html
    jplSoup = bs(html, 'html.parser')
    result_img = jplSoup.find('img', class_ = "fancybox-image")
    url_img = result_img['src'] 

     #variable to go to dictionary
    featured_image_url = 'https://www.jpl.nasa.gov'+ url_img


    #Mars Weather
    # URL of page to be scraped
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    # Create BeautifulSoup object; parse with 'html.parser'
    WeatherSoup = makeSoup(twitter_url)

    # results are returned as an iterable list ##title
    #variable to go to dictionary
    mars_weather = WeatherSoup.find('p',"TweetTextSize").text

    #Mars Facts
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    #Use Pandas to convert the data to a HTML table string.
    df = tables[0]
    df.columns = ['Parameter', 'Value']

    #variable to go to dictionary
    html_table = df.to_html()

    #stripping the space
    html_table.replace('\n', '')

    #You can also save the table directly to a file.
    df.to_html('table.html')

    tableSoup=bs(open("table.html"),"html.parser")
    ## Stripping the soup data and saving in mars_facts disctionary, mars_info is a temperory list used
    mars_info=[]
    mars_table={}
    for z in tableSoup.table('td'):
        #print(z.text)
        mars_info.append(z.text.strip(':'))
        mars_table=dict([(k, v) for k,v in zip (mars_info[::2], mars_info[1::2])])
    print(mars_table)

    #Mars Hemisperes
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    #Create BeautifulSoup object; parse with 'html.parser'
    HemisphereSoup = makeSoup(hemisphere_url)

    #Examine the results, then determine element that contains sought info
    titles_hemisphere = HemisphereSoup.find_all('div', class_ = "description")
    
    #list of titles
    title = []
    for result in titles_hemisphere:
        # Error handling
        try:
            # Identify and return title of listing
            t = result.find('h3').text
            title.append(t)
        except Exception as e:
            print(e)
   
    imgs_hemisphere = HemisphereSoup.find_all('a', "itemLink product-item")

    interim_url = []
    for result in imgs_hemisphere:
        interim_url.append('https://astrogeology.usgs.gov'+ result['href'])

    img_url = []
    for url in interim_url:
        response = requests.get(url)
        imgSoup = bs(response.text, 'html.parser')
        result=imgSoup.find('div', "downloads")
        aBlock = result.find('a')
        img_url.append(aBlock['href'])

    #Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    hemisphere_image_urls = []
    for i in range(0, len(title)):
        dict_hemi = {title[i]:img_url[i]}
        #variable to go to dictionary
        hemisphere_image_urls.append(dict_hemi)

    #creating dictionary
    listings["news_title"] = news_title
    listings["news_url"] = news_url
    listings["news_para"] = news_p
    listings["featured_image_url"] = featured_image_url
    listings["mars_weather"] = mars_weather
    listings["mars_table"] = mars_table
    listings["hemisphere_image_urls"] = hemisphere_image_urls
    return listings

#a = scrape()
#print(a)
