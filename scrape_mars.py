# Misson to Mars

# Dependencies
import time
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd



# Choose the executable path to driver 
def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)




def scrape():
    browser = init_browser()
    marsfacts = {}
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


# HTML Object
    html = browser.html

# Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')


# Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text
    marsfacts['news_title'] = news_title
    marsfacts['news_paragraph'] = news_p

# Featured Mars image
    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)
    html = browser.html
    soup = bs(html, "html.parser")
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image
    marsfacts["featured_image"] = featured_image_url

# Mars Weather

    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)
    html_weather = browser.html

# Parse HTML with Beautiful Soup
    soup = bs(html_weather, 'html.parser')
    latest_tweets = soup.find_all('div', class_='js-tweet-text-container')
    for tweet in latest_tweets: 
        weather_tweet = tweet.find('p').text
        if 'Sol' and 'pressure' in weather_tweet:
            print(weather_tweet)
            break
        else: 
            pass

    marsfacts["mars_weather"] = weather_tweet

# Mars Facts

    url_facts = "https://space-facts.com/mars/"

    mars_facts_list = pd.read_html(url_facts)
    mars_facts_df = mars_facts_list[0]
    mars_facts_df.columns = ["Parameter", "Values"]
    mars_facts_df.set_index(["Parameter"])
   
    mars_facts_html = mars_facts_df.to_html(header=False, index=False)
    mars_facts_html = mars_facts_html.replace("\n", "")
    marsfacts["mars_facts_table"] = mars_facts_html

    # Mars Hemisperes

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})

        marsfacts["img_url"] = mars_hemisphere

        return marsfacts



