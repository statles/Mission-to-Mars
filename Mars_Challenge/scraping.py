#import splinter and beautifulsoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager

#import pandas
import pandas as pd
import datetime as dt

#initialize the browser, create data dictionary, end the webdrier and return scraped data
def scrape_all():
    #initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    #set our variables
    news_title, news_paragraph = mars_news(browser)
    
    #store scraping results in a dictionary
    data = {"news_title":news_title,
           "news_paragraph":news_paragraph,
           "featured_image":featured_image(browser),
           "facts":mars_facts(),
           "last_modified":dt.datetime.now(),
           "hemispheres":mars_hemispheres(browser)}
    
    #quit the browser
    browser.quit()
    return data

# refactor code into a function
def mars_news(browser):
    # visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    #optional delay for loading time
    browser.is_element_present_by_css('div.list_text', wait_time=1)
    
    #convert browser html into soup object and then quite the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    
    #add try and except
    try:   
        slide_elem = news_soup.select_one('div.list_text')
        #use the aprent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        
    except AttributeError:
        return None, None
    
    return news_title, news_p

#refactor 'featured image' code into a function
def featured_image(browser):
    # visit the mars nasa news site
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    #find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click
    #parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')
    #add try/except for errors
    try:
        #gind the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image', text='alt').get('src')
    except AttributeError:
        return None
    #use the base url to create absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

#refactor 'mars facts'
def mars_facts():
    #add try/except with BaseException
    try:
        # use 'read_html' to scrape the facts into a df
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    #assign columns and set index
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    #convert df into HTML format, add bootstrap
    return df.to_html()

#refactor hemisphere data into a function
def mars_hemispheres(browser):
    #vist the URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    #create a list to hold the dictionaries of images and titles
    hemisphere_image_urls = []

    #use a for loop to loop through the four hemispheres and retrieve the images and titles
    #use the range function to only collect the first four h3 tags
    # the last h3 is not related to the hemisphere data
    for i in range(0,4):
    # create an empty dictionary 
        hemispheres = {}
        #find using the h3 tag
        hemisphere = browser.find_by_tag('h3')[i]
        #click on the header to take you to the full scale image page
        hemisphere.click()
        html = browser.html
        mars_soup = soup(html, 'html.parser')
        #find the full res image by class a
        img_url_rel = mars_soup.find('a', target='_blank', text='Sample').get('href')
        img_url = f"https://marshemispheres.com/{img_url_rel}"
        #append to dictionary
        hemispheres.update({'img_url':img_url})
        #find the heading
        mars_title = mars_soup.find('h2', class_='title').get_text()
        #add the heading to the dictionary
        hemispheres.update({'title':mars_title})
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    #return list of dictionaries of hemisphere urls and titles
    return hemisphere_image_urls

if __name__ == "__main__":
    #if running script, print scraped data
    print(scrape_all())

