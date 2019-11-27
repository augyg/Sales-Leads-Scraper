#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 15:04:17 2019

@author: galensprout
"""

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from itertools import cycle
from fake_useragent import UserAgent
import csv
import requests
from lxml.html import fromstring
import ray
from time import sleep
import re
import psutil

def give_me_selenium_with_proxy(proxy):
    opts = Options()    
    ua = UserAgent()
#    global proxies_index
#    proxies_index
#    user_agent = ua.random
    
     # rotating list ---> yield proxy @ i where i is the number of times excepted
    
#    proxy_used = proxies[proxies_index] #to avoid relooping
#    proxies_index +=1
    
    opts.add_argument('--proxy=%s' % proxy)
#    opts.add_argument(f'User-Agent={user_agent}')
    
#    opts.add_argument('--headless')
#    opts.add_argument('--disable-gpu') 

#    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2, 
#             'plugins': 2, 'popups': 2, 'geolocation': 2, 
#             'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
#             'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
#             'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
#             'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
#             'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
#             'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
#             'durable_storage': 2, 'disk-cache-size': 4096}}
#    opts.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(options=opts)    
    return driver

def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    for i in parser.xpath('//tbody/tr')[:10]:
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)

    proxy_pool = cycle(proxies)
    
    
    url = 'https://httpbin.org/ip'
    new_proxy_list = []
    for i in range(1,11):
        #Get a proxy from the pool
        proxy = next(proxy_pool)
    
        try:
            response = requests.get(url,proxies={"http": proxy, "https": proxy})
            #Grab and append proxy if valid
            new_proxy_list.append(proxy)
            print(response.json())
            
            
        except:
            #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
            #We will just skip retries as its beyond the scope of this tutorial and we are only downloading a single url 
            print("Skipping. Connnection error")
    
    return new_proxy_list


drivers = []
#new_proxy_list = get_proxies()

new_proxy_list = ['118.97.100.83', '95.80.93.53', '148.103.9.41', '178.215.190.240', '176.108.103.21', '191.36.244.230']
for i in new_proxy_list:
    driver = give_me_selenium_with_proxy(i)
    drivers.append(driver)

for driver in drivers:
    sleep(10)
    driver.get("https://www.linkedin.com/login?trk=guest_homepage-basic_nav-header-signin")
    
    xpath_username = "//input[@id='username']"
    xpath_password = "//input[@id='password']"
    username = driver.find_element_by_xpath(xpath_username)
    password = driver.find_element_by_xpath(xpath_password)
    username.clear()
    password.clear()
    username.send_keys('spro0640@mylaurier.ca')
    password.send_keys('Warhawks58')
    
    username.submit()
    
    
for driver in drivers:
    name = 'Galen'
    search_string = 'https://www.linkedin.com/search/results/people/?authorCompany=%5B%5D&authorIndustry=%5B%5D&contactInterest=%5B%5D&facetCity=%5B%5D&facetCompany=%5B%5D&facetConnectionOf=%5B%5D&facetCurrentCompany=%5B%5D&facetCurrentFunction=%5B%5D&facetGeoRegion=%5B%5D&facetGroup=%5B%5D&facetGuides=%5B%5D&facetIndustry=%5B%5D&facetNetwork=%5B%5D&facetNonprofitInterest=%5B%5D&facetPastCompany=%5B%5D&facetProfessionalEvent=%5B%5D&facetProfileLanguage=%5B%5D&facetRegion=%5B%5D&facetSchool=%5B%5D&facetSeniority=%5B%5D&facetServiceCategory=%5B%5D&facetState=%5B%5D&groups=%5B%5D&keywords='+ str(name) +'&origin=GLOBAL_SEARCH_HEADER&page=1&refresh=false&skillExplicit=%5B%5D&topic=%5B%5D'
    driver.get(search_string)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
