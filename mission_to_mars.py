
# coding: utf-8

# In[1]:


get_ipython().system('pip install selenium splinter')


# In[2]:


#sudo apt-get install python-bs4
get_ipython().system('pip install beautifulsoup4')


# In[3]:


# Dependencies
from pprint import pprint
import pymongo
import time
from splinter import Browser
from bs4 import BeautifulSoup as bs
from os import getcwd
from os.path import join
import requests
import pandas as pd


# In[4]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'


# In[5]:


# Retrieve page with the requests module
response = requests.get(url)
# Create BeautifulSoup object; parse with 'html.parser'
soup = bs(response.text, 'html.parser')


# In[6]:


# Examine the results, then determine element that contains sought info
print(soup.prettify())


# In[7]:


# results are returned as an iterable list ##title
results = soup.find('div',class_ = "content_title")


# In[8]:


news_title = results.find('a').text
news_url = 'https://mars.nasa.gov'+ results.a['href']
print(news_title)
print(news_url)


# In[9]:


# Retrieve page with the requests module
new_response = requests.get(news_url)
# Create BeautifulSoup object; parse with 'html.parser'
newsoup = bs(new_response.text, 'html.parser')


# In[10]:


# Examine the results, then determine element that contains sought info
print(newsoup.prettify())


# In[11]:


# results are returned as an iterable list ##paragraph
news_p = newsoup.find('p').text
news_p


# In[13]:


jpl_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)
#browser = Browser('chrome', headless=False)
browser.visit(jpl_image_url)
browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(2)


# In[14]:


#Use splinter to navigate the site and find the image url for the current Featured Mars Image 
#and assign the url string to a variable called featured_image_url.
html = browser.html
jplSoup = bs(html, 'html.parser')

result_img = jplSoup.find('img', class_ = "fancybox-image")
url_img = result_img['src'] 

featured_image_url = 'https://www.jpl.nasa.gov'+ url_img

print(featured_image_url)


# In[15]:


#Mars Weather
# URL of page to be scraped
url = 'https://twitter.com/marswxreport?lang=en'
# Retrieve page with the requests module
response = requests.get(url)
# Create BeautifulSoup object; parse with 'html.parser'
WeatherSoup = bs(response.text, 'html.parser')
# Examine the results, then determine element that contains sought info
print(WeatherSoup.prettify())


# In[16]:


# results are returned as an iterable list ##title
mars_weather = WeatherSoup.find('p',"TweetTextSize").text
mars_weather


# In[17]:


#Mars Facts
url = 'https://space-facts.com/mars/'
tables = pd.read_html(url)
tables
#print(type(tables))


# In[18]:


#Use Pandas to convert the data to a HTML table string.
df = tables[0]
df.columns = ['Parameter', 'Value']
#df.set_index('Parameter', inplace=True)
df.head()


# In[19]:


html_table= df.to_html()
html_table
#print(type(html_table))


# In[20]:


#You may have to strip unwanted newlines to clean up the table.
html_table.replace('\n', '')


# In[21]:


#You can also save the table directly to a file.
df.to_html('table.html')
# OSX Users can run this to open the file in a browser, 
# or you can manually find the file and open it in the browser
get_ipython().system('open table.html')


# In[22]:


tableSoup=bs(open("table.html"),"html.parser")
## Stripping the soup data and saving in mars_facts disctionary, mars_info is a temperory list used
mars_info=[]
mars_table={}
for z in tableSoup.table('td'):
    #print(z.text)
    mars_info.append(z.text.strip(':'))
    mars_table=dict([(k, v) for k,v in zip (mars_info[::2], mars_info[1::2])])
print(mars_table)


# In[23]:


#Mars Hemisperes
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
#Retrieve page with the requests module
response = requests.get(url)
#Create BeautifulSoup object; parse with 'html.parser'
HemisphereSoup = bs(response.text, 'html.parser')


# In[34]:


#Examine the results, then determine element that contains sought info
titles_hemisphere = HemisphereSoup.find_all('div', class_ = "description")
print(titles_hemisphere)

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
print("****")
print(title)  


# In[44]:


# Examine the results, then determine element that contains sought info
#print(HemisphereSoup.prettify())
imgs_hemisphere = HemisphereSoup.find_all('a', "itemLink product-item")

interim_url = []
for result in imgs_hemisphere:
    interim_url.append('https://astrogeology.usgs.gov'+ result['href'])
                  #'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced' 

#print(interim_url)


# In[72]:


img_url = []
for url in interim_url:
    response = requests.get(url)
    imgSoup = bs(response.text, 'html.parser')
    result=imgSoup.find('div', "downloads")
    #print(x)
    aBlock = result.find('a')
    #print("---")
    img_url.append(aBlock['href'])
print(img_url)


# In[26]:


imgs_hemisphere


# In[ ]:


#Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
hemisphere_image_urls = []
for i in range(0, len(title)):
    dict_hemi = {title[i]:img_url[i]}
    hemisphere_image_urls.append(dict_hemi)
hemisphere_image_urls


# In[ ]:


hemisphere_image_urls[0].keys()


# In[ ]:


hemisphere_image_urls[0].values()


# In[ ]:


type(hemisphere_image_urls)


# In[ ]:


for i in range (0, len(hemisphere_image_urls)):
    for key, value in hemisphere_image_urls[i].items():
        print("img source is: "+ value)
        print("title is: "+ key)


# In[ ]:


img_url

