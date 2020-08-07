#Import Libraries
#Web Scraping tools 
from bs4 import BeautifulSoup as bs
from selenium import webdriver
#from splinter import Browser

#DataFrame tools
import pandas as pd

#Misc tools for web scraping
import time
import requests

#Function to initianilze browser.
def init_browser():

    #Settings for headless mode.
    options = webdriver.ChromeOptions()
    options.add_argument('headless')

    #path to the driver and load the options.
    browser = webdriver.Chrome("/usr/local/bin/chromedriver",chrome_options = options)

    #returns the brower.
    return browser

def scrapper():

    #Call browser function
    browser = init_browser()
    #Dictionary to store all the results.
    marsInfo_dict = {}

    #Code to get NASA Mars News ----------------------------------------------------------------------------------------------
    try:

        url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&year=2020%3Apublish_date&category=19%2C165%2C184%2C204&blank_scope=Latest"

        #splinter option - open url
        #browser.visit(url)

        #Open url.
        browser.get(url)

        #Time to let the website load all the elements
        time.sleep(4)  

        #splinter option - save HTML 
        #html = browser.html 

        #save the html source.
        html = browser.page_source

        #Use bs4 to parse the html response.
        soup = bs(html, "html.parser")

        #Collect the latest news title
        news_title = soup.find_all('li', class_="slide")[0].find(class_="content_title").text
        news_p = soup.find_all('li', class_="slide")[0].text

        marsInfo_dict['news_title'] = news_title
        marsInfo_dict['news_p'] = news_p
    
    except :
        print(f"Problem at website {url}")

    #Code to get JPL Mars Space Images - Featured Image ---------------------------------------------------------------------------------
    try:

        url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

        #splinter option - open url
        #browser.visit(url)

        #Opens the url.
        browser.get(url)

        #splinter option - FULL IMAGE BUTTON
        #browser.click_link_by_id("full_image")

        #Interact with the FULL IMAGE BUTTON
        browser.find_element_by_id("full_image").click()

        time.sleep(4)

        #splinter option - save HTML 
        #html = browser.html 

        #save the html source.
        html = browser.page_source

        #Use bs4 to parse the html response.
        soup = bs(html, "html.parser")

        featured_image_url = "https://www.jpl.nasa.gov/" + soup.find_all('img', class_="fancybox-image")[0]['src']

        marsInfo_dict['featured_image_url'] = featured_image_url
    
    except :
        print(f"Problem at website {url}")
    
    #Mars Weather ------------------------------------------------------------------------------------------------------------------------
    try:
        url = "https://twitter.com/marswxreport?lang=en"
        
        #splinter option - open url
        #browser.visit(url)

        #Open the url.
        browser.get(url)

        #Time to let the website load all the elements
        time.sleep(4)

        #splinter option - save HTML 
        #html = browser.html 

        #save the html source.
        html = browser.page_source

        #Use bs4 to parse the html response.
        soup = bs(html, "html.parser")

        mars_weather = soup.find_all('article', class_="css-1dbjc4n r-1loqt21 r-18u37iz r-1ny4l3l r-o7ynqc r-6416eg")[0].text.strip().replace('Mars Weather@MarsWxReport·19hInSight ','')

        marsInfo_dict['mars_weather'] = mars_weather
    
    except :
        print(mars_weather)
        print(f"Problem at website {url}")

    # Mars Facts--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    try:
        url = 'http://space-facts.com/mars/'

        #Load url to pandas read html.
        tables = pd.read_html(url)

        #Tables
        marsFacts_df = tables[0]
        earthMars_df = tables[1]

        #Rename columns
        marsFacts_df.columns = ['Facts', 'Values']


        #Outpout
        html_outputFacts = marsFacts_df.to_html(index = False)
        html_outputFacts = html_outputFacts.replace('\n', '')

        html_outputMarsEarth = earthMars_df.to_html(index = False)
        html_outputMarsEarth = html_outputMarsEarth.replace('\n', '')

        marsInfo_dict['html_outputFacts'] = html_outputFacts
        marsInfo_dict['html_outputMarsEarth'] = html_outputMarsEarth

    except :
        print(f"Problem at website {url}")

    #hemisphereImages ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    try:
        temp_list = []

        url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

        #splinter option - open url
        #browser.visit(url)

        #Opens the url.
        browser.get(url)

        time.sleep(4)

        #splinter option - save HTML 
        #html = browser.html 

        #save the html source.
        html = browser.page_source

        # close web browser
        browser.close()

        #Use bs4 to parse the html response.
        soup = bs(html, "html.parser")

        links = soup.find_all('div', class_="description")

        for link in links:

            highDef_url = f"https://astrogeology.usgs.gov{link.find('a')['href']}"

            responseHighDef = requests.get(highDef_url)

            soupHighDef = bs(responseHighDef.text, 'html.parser')

            highDef_url = soupHighDef.find_all("div", class_="downloads")[0].find('a')['href']

            title = link.find('h3').text 

            temp_list.append({"title" : title, "img_url" : highDef_url})

        marsInfo_dict['hemisphere_image_urls'] = temp_list

    except :
        print(f"Problem at website {url}")

    return marsInfo_dict