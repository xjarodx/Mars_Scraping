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
    time.sleep(1)
    full_image.click()
    time.sleep(1)
    m_info = browser.find_link_by_partial_text('more info')
    m_info
    m_info.click()
    new_html = browser.html
    new_soup = bs(new_html, 'html.parser')
    full_image =new_soup.select_one('figure.lede a img').get("src")
    full_image_summary = new_soup.find('div', class_="wysiwyg_content").get("p")
    jpl_url = 'https://www.jpl.nasa.gov'
    featured_image_url = jpl_url + full_image
    mars_dict["Featured_Image_Link"] = featured_image_url
    mars_dict["Image_Summary"] = full_image_summary
    full_image_title = new_soup.find('h1', class_="article_title")
    mars_dict["Featured_Image_Title"] = full_image_title.text.strip('\n\t": ')

    ## Part 3 ##
    marsweather = 'https://twitter.com/marswxreport'
    response2 = requests.get(marsweather)
    soup2 = bs(response2.text, 'html.parser')
    weather = []
    
    for w_info in soup2.find_all('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text"):
           weather.append(w_info.text.strip())
    
    for tweet in reversed (weather):
        if tweet[:3]=="InS":
            mars_weather=tweet

            mars_dict["weather_info"] = mars_weather

    ## Part 4 ##
    pandaurl = 'https://space-facts.com/mars/'
    tables = pd.read_html(pandaurl)
    df = tables[0]
    df.columns = ['Mars Facts', 'Values']
    df.set_index("Mars Facts")
    mars_facts_html = df.to_html(index=False, classes="table-hover table-dark table-sm")
    mars_dict["facts_table"] = mars_facts_html

    ## Part 5 ##
    hemishperes = ['Cerberus', 'Schiaparelli', 'Syrtis Major', 'Valles Marineris']

    hem_title = []
    img_urls = []

    for i in hemishperes:
        my_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/' + i
        browser.visit(my_url)
        time.sleep(1)
        url_html = browser.html
        page_soup = bs(url_html, "html.parser")
        
        hem_images = page_soup.find('div', class_='downloads').find('li').a['href']
        img_urls.append(hem_images)
        
        hem_name = i + ' Hemisphere'
        hem_title.append(hem_name)
    
        print (hem_name + ' is a great success!')

    d = dict(zip(hem_title, img_urls))
    hemisphere_image_urls = [{'image_url': v} for k, v in zip(hem_title, img_urls)]
    hemisphere_image_titles = [{'hem_title': b} for b, l in zip(hem_title, img_urls)]
    mars_dict["Hemisphere_image_data"] = hemisphere_image_urls
    mars_dict["Hemisphere_title_data"] = hemisphere_image_titles
    browser.quit()

    return mars_dict