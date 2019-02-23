from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import time 
from pprint import pprint

def scrapey_mars():

    mars_dict = {}

    ## Part 1 ##
    news = 'https://mars.nasa.gov/news/'
    response = requests.get(news)
    soup = bs(response.text, 'html.parser')
    title = soup.find('div', class_="content_title")
    news_title = title.a.text
    summary =soup.find('div', class_="rollover_description_inner")
    news_sum = summary.text
    mars_dict["News_Title"] = news_title
    mars_dict["News_Summary"] = news_sum

    ## Part 2 ##
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    full_image = browser.find_by_id('full_image')
    full_image.click()
    m_info = browser.find_link_by_partial_text('more info')
    m_info.click()
    new_html = browser.html
    new_soup = bs(new_html, 'html.parser')
    full_image =new_soup.select_one('figure.lede a img').get("src")
    jpl_url = 'https://www.jpl.nasa.gov'
    featured_image_url = jpl_url + full_image
    mars_dict["Featured_Image_Link"] = featured_image_url

    ## Part 3 ##
    marsweather = 'https://twitter.com/marswxreport'
    response2 = requests.get(marsweather)
    soup2 = bs(response2.text, 'html.parser')
    weather = soup2.find('div', class_="js-tweet-text-container")
    mars_weather = weather.p.text
    mars_dict["weather_info"] = mars_weather

    ## Part 4 ##
    pandaurl = 'https://space-facts.com/mars/'
    tables = pd.read_html(pandaurl)
    df = tables[0]
    df.columns = ['Mars_Facts', 'Values']
    df.to_html("mars_facts.html", index=False)
    df.set_index("Mars_Facts")
    mars_facts_html = df.to_html(classes="facts table table-striped")
    mars_dict["facts_table"] = mars_facts_html

    ## Part 5 ##
    hemishperes = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']

    hem_title = []
    img_urls = []

    for i in hemishperes:
        my_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/' + i
        browser.visit(my_url)
        time.sleep(2)
        url_html = browser.html
        page_soup = bs(url_html, "html.parser")
        
        hem_images = page_soup.find('div', class_='downloads').find('li').a['href']
        img_urls.append(hem_images)
        
        hem_name = i + ' Hemisphere'
        hem_title.append(hem_name)
    
        print (hem_name + ' is a great success!')

    d = dict(zip(hem_title, img_urls))
    hemisphere_image_urls = [{k: v} for k, v in zip(hem_title, img_urls)]
    #print (hemisphere_image_urls)
    mars_dict["Hemisphere_data"] = hemisphere_image_urls