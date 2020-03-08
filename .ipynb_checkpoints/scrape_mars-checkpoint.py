

import pandas as pd
import lxml
from bs4 import BeautifulSoup
from splinter import Browser
import time


def init_browser():
    executable_path = {"executable_path": "C:\Program Files\chromedriver_win32\chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)



def scrape():
    browser = init_browser()
    mars = {}



    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #scrape for featured title and text
    mars['news_title'] = soup.find('div', class_='content_title').text
    mars['news_p'] = soup.find('div', class_='rollover_description_inner').text
    time.sleep(1)


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # scrape for featured link
    featured_image = soup.find('a', class_='button fancybox')['data-fancybox-href']
    # url received as a partial, concatenate with origin url to get full url
    mars['featured_image_url'] = 'https://www.jpl.nasa.gov'+featured_image
    time.sleep(1)



    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #search for latest tweet and save to variable
    mars['mars_weather'] = soup.find('div', class_="js-tweet-text-container").text
    time.sleep(1)



    # set up scrape for mars fact using pandas
    url = 'https://space-facts.com/mars/'
    mars_table = pd.read_html(url)
    # convert tabe list into dataframe
    mars_df = mars_table[0]
    mars_df.columns=['Statistic','Value']
    # convert dataframe to html table string
    mars['mars_df_html'] = mars_df.to_html()
    time.sleep(1)


    #set up scrape for hemis
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #
    hemisphere_image_url = list({})


    hemisphere_title = soup.find_all('h3')
    for title in hemisphere_title:
        hemisphere_image_url.append(title.text)
        img = soup.find('img', class_='thumb')['src']
        hemisphere_image_url.append('https://astrogeology.usgs.gov/'+img)
    time.sleep(1)
    
    mars['hemisphere_image_url'] = hemisphere_image_url

    #quit browser when done
    browser.quit()




    return mars
