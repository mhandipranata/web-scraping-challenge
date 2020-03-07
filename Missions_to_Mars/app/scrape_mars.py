from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import datetime as dt
import time
import re


def mars_news(browser):
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(news_url)
    time.sleep(5)

    html = browser.html
    news_soup = bs(html, 'html.parser')

    # Examine the results, then determine element that contains sought info
    # results are returned as an iterable list

    # Identify and return news title of listing
    news_title = news_soup.find('div', class_='content_title').text
            
    # Identify and return news content of listing
    news_p = news_soup.find('div', class_='article_teaser_body').text
    
    return news_title, news_p 

def featured_image(browser):
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)

    # Use splinter to click on the 'FULL IMAGE' button
    full_image_button = browser.find_by_css('.button.fancybox')
    full_image_button.click()

    # Use splinter to click on the 'more info' button
    more_info_button = browser.links.find_by_partial_text('more info')
    more_info_button.click()

    html = browser.html
    featured_img_soup = bs(html, 'html.parser')

    featured_img = featured_img_soup.find('img', class_='main_image')['src']
    featured_image_url = f'https://www.jpl.nasa.gov{featured_img}'
    
    return featured_image_url

def mars_weather(browser):
    weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(weather_url)
    time.sleep(5)

    html = browser.html
    weather_soup = bs(html, 'html.parser')

    weather_result = weather_soup.find('div', attrs ={"class": "tweets", "data-name": "Mars Weather"})

    try:
        mars_weather = weather_result.find('p', 'tweet-text').get_text()
    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather = weather_soup.find('span', text=pattern).text

    return mars_weather

def mars_facts(browser):
    # URL of page to be scraped
    facts_url = "https://space-facts.com/mars/"

    # Retrieve page with the requests module
    response = requests.get(facts_url)

    # Create BeautifulSoup object; parse with ''html.parser'
    facts_scrape = bs(response.content, 'html.parser')

    table = facts_scrape.find('table', class_='tablepress-id-p-mars')

    col_1 = []
    col_2 = []

    for data in table.find_all('tr'):
        col_1.append(data.find('td', class_='column-1').text)
        col_2.append(data.find('td', class_='column-2').text)
        
    mars_table = pd.DataFrame(columns = ["Characteristics", "Mars"])
    mars_table["Characteristics"] = col_1
    mars_table["Mars"] = col_2

    mars_facts_html = mars_table.to_html(index=False)

    return mars_facts_html

def mars_hemisphere(browser):
    # Visit the website of Mars Hemispheres using Splinter
    hemisphere_link = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_link)

    # Getting the links of each hemisphere products
    html = browser.html
    hemispheres_img_soup = bs(html, 'html.parser')

    hemispheres_img = hemispheres_img_soup.find_all('div', class_='description')

    img_links = []

    for div in hemispheres_img:
        link = div.find('a', class_='itemLink product-item')['href']
        img_links.append(f'https://astrogeology.usgs.gov{link}')

    # Visit each hemisphere products' links
    img_hem_title = []
    img_hem_href = []

    for img_link in img_links:
        browser.visit(img_link)
        
        html = browser.html
        img_hem_soup = bs(html, 'html.parser')
        
        # Scrape Image Title and Link
        
        img_hem_title.append(img_hem_soup.find('h2', class_="title").text)
            
        img_hem_div = img_hem_soup.find_all('div', class_="downloads")   
        
        for img in img_hem_div:  
            img_hem_href.append(img.find('a')['href'])
    
    # Insert the Mars Hemispheres Title and URLs to DataFrame
    img_hem_df = pd.DataFrame(columns=['title', 'img_url'])
    img_hem_df['title'] = img_hem_title
    img_hem_df['img_url'] = img_hem_href

    hemisphere_image_url = img_hem_df.to_dict('records')

    return hemisphere_image_url

def scrape_all():
    
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    # browser = Browser("chrome", executable_path="chromedriver", headless=False)
    
    news_title, news_p = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image": featured_image(browser),
        "mars_weather": mars_weather(browser),
        "mars_hemisphere": mars_hemisphere(browser),
        "mars_facts": mars_facts(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    return data

if __name__ == "__main__":

    # If the script is running, it will print the scraped data
    print(scrape_all())