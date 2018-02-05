#Dependences
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd

def scrape():

    #Mars Weather
    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    #NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="rollover_description_inner").text

    #JPL Mars Space Images - Featured Image
    browser = Browser()
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')
    button = browser.find_by_css('#full_image')
    button.click()
    featured_image_url = browser.find_by_css('img.fancybox-image')['src']
    browser.quit()

    #Mars Facts
    url = 'https://space-facts.com/mars/'
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    table = soup.find('table', class_="tablepress tablepress-id-mars")
    df = pd.read_html(str(table))

    #Mars Hemispheres
    hemispheres = ['cerberus', 'schiaparelli','syrtis_major', 'valles_marineris']
    hemisphere_image_urls = []
    for hemisphere in hemispheres:
        browser = Browser()
        browser.visit('https://astrogeology.usgs.gov/search/map/Mars/Viking/' + hemisphere + '_enhanced')
        browser.click_link_by_href('#open')
        url =  browser.find_by_css('img.wide-image')['src']
        title = browser.find_by_css('h2').text
        d = {}
        d['title']=title
        d['img_url']=url
        hemisphere_image_urls.append(d)
    browser.quit()

    #Create dictionary of all the scraped results
    mars_data = {'mars_weather':mars_weather,
                'mars_news_p':news_p,
                'mars_news_title':news_title,
                'featured_image_url':featured_image_url,
                'mars_facts':df,
                'hemisphere_image_urls':hemisphere_image_urls}
    return mars_data



