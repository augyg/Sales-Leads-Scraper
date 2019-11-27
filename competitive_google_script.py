# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 13:43:03 2019

@author: Owner1
"""

"""
I need to fix the scrolling to find the next page element in linkedin task 




Remember to add back in L6H !!!!

format_list = [industry, name, territory designation, rep_name, postal code, address, website, contact1, contact2, contact3, contact4, contact5]

"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementNotVisibleException
import datetime
import time
import csv
import re
import sys
import psutil
#import os



def update_search_bar(search_bar, search_term):
    search_bar.clear()
    search_bar.send_keys(search_term)
    search_bar.submit()

def build_search_terms(ind_list, postal_codes_list):
    terms = []
    post = []
    for x in postal_codes:
        for i in whose_postal:
            for j in i[2]:
                if x==j:
                    post.append(x)
                    
    for p in post: 
        for i in ind_list:
            terms.append('"'+p+'"'+' '+i)
    return terms

def regex_parse(tags, contact, company_name):
    #NEEDS TO: Prioritize most useful contacts 
    #this takes a tag or set of tags as input then searches a string for the pattern
    output = False # length should be equal to length of jobTags
    if company_name.lower() in contact[1].lower():
        current_index = 1 #the importance of contact  based on position
        for tag in tags:
            if(isinstance(tag, list)):
                lengthToIterate = len(tag)
                while output == False and lengthToIterate > 0:
                    for t in tag: 
                        if t in contact[1].lower():
                            output = [current_index, contact[0], contact[1]]
                            
                        lengthToIterate =- 1

            else: 
                if tag in contact[1].lower():
                    output = [current_index, contact[0], contact[1]]
                    break
                
            current_index +=1
 
    return output

def google_search(search_terms, master_list_this_run):
    global running_total
#    global search_terms
    global search_term_index
    global todays_date
    sizeof_list = 0
    print(search_terms)
    while search_term_index < len(search_terms) and sizeof_list < 3500:
    
        print('at start')
#    for term in search_terms:    
        search_bar = driver.find_element_by_xpath("//input[@title='Search']")
        update_search_bar(search_bar, search_terms[search_term_index])
        
        #============================================================================================================#
        
        #add in ensuring that the time between searches is long enough to not get stopped by captcha
        
        
        
        
        
        
        #============================================================================================================#
        
        
        
        
        current_industry = search_terms[search_term_index][6:] #grabs the piece after postal and spaces
        test_counter = 0
        condition = True
        fails_in_row = 0 
        total_fails = 0
        while condition == True:
            #below grabs the a.href of each box so that it can be clicked
            try:
                print('Try block')
                companies_listed_on_page = WebDriverWait(driver, 5).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@jsl='$t t-8x4sQ9CC-MQ;$x 0;']//a[@role='link']"))
                )
                sleep(2)
                companies_listed_on_page = driver.find_elements_by_xpath("//div[@jsl='$t t-8x4sQ9CC-MQ;$x 0;']//a[@role='link']")
            except:
                fails_in_row +=1
                print('excpept block')
                #no results found
                search_term_index +=1
                if fails_in_row > 5:
                  sleep(8)
                  
                
                condition = False
                
                #extra sleep condition
                
                
                break
            
            if companies_listed_on_page:
              fails_in_row = 0
            
            for c in companies_listed_on_page:
                #future: deets = get_deets(c) -> append to master ; make into function
                
#                row_format = []
                try:
                    c.click()
                except:
                    try:
                        sleep(1)
                        c.click()
                    except:
                        #holy fuck 
                        continue
                        
                test_counter+=1
                running_total+=1
                deets = []
                
 #================================Change to append 2nd ===============================================================#               
                deets.append(current_industry)
 #====================================================================================================================#
                
                #keep here to ensure that the driver gets a new value and not the old pane
                xpath_company_name = "//div[@data-attrid='title']//span" #.text
                xpath_address = "//span[@class='LrzXr']" #break down into postal and street
                xpath_website = "//a[@class='CL9Uqc ab_button']" #.get_attribute("href")    
                xpath_phone = "//span[@class='LrzXr zdqRlf kno-fv//a[@data-pstn-out-call-url title='Call via Hangouts']"

                
                details_list = [xpath_company_name, xpath_address, xpath_website, xpath_phone]
                valid = False
                try:
                    pane = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "//div[@data-attrid='title']//span"))
                    )
                except TimeoutException:
                    condition = False
                    print('I am lost for how this even can occur -if this continues happening then try printing body of response')
                    break
                    
                sleep(0.8)
                for i in details_list:
                    try:
                        x = driver.find_element_by_xpath(i)
                        if i == xpath_website:
                            tag = x.get_attribute("href")
                            #if we do email scraping -> logic here
                        else:
                            tag = x.text
                            if i == xpath_address:
                                tag_postal = tag[-7:]
                                
                                
                                
                                for i in whose_postal:
                                    for j in i[2]:
                                        if tag_postal[0:3] == j:
                                            valid = True
                                            current_territory_code = i[1]
                                            current_rep_name = i[0]
                                            deets.append(current_territory_code)
                                            deets.append(current_rep_name)
                                        
                                
                                deets.append(tag_postal)
                                tag = tag[:-7]
                                a_pieces = tag.split(',')
                                if a_pieces[0].lower() == 'canada':
                                    a_pieces.remove('Canada')
                                
                                deets.append(a_pieces[1])
                                deets.append(a_pieces[2])
                                
                                tag = a_pieces[0] 
                                for char in tag:
                                    if char.isdigit() == False:
                                        break
#                                    if char.isdigit():
                            if i == xpath_company_name:
                                #clean for crap in the string 
                                tag = re.sub(r"[^A-Za-z0-9\-\s]", '', tag)
                                
                                
                                #can add check by regex to ensure actually a postal code eventually
                        print(tag)
                        deets.append(tag)
                    except:
                        tag = 'NF'
                        #postal code spins off of address and rep+territory is determined by postal code
                        if i == xpath_address:
                            deets.append('Territory undefined')
                            deets.append('Rep undefined')
                            deets.append('NF - Postal')
                            
                            
                        deets.append(tag)
                        
                deets.append(todays_date)
                if valid:
                    master_list_this_run.append(deets)
            try:
                go_to_next_page = driver.find_element_by_xpath("//a[@id='pnnext']")
                go_to_next_page.click()
                companies_listed_on_page = driver.find_elements_by_xpath("//div[@jsl='$t t-8x4sQ9CC-MQ;$x 0;']//a[@role='link']")


            except:
                #search term has been used up
                condition = False
                sizeof_list = sys.getsizeof(master_list_this_run)
                search_term_index += 1
                
            
        print(len(search_terms), search_term_index)
        print(test_counter, search_terms[search_term_index-1])
        print('Running total is now', running_total)
    
        
    return master_list_this_run

def add_linkedin_contacts(master_list_this_run):
    for company in master_list_this_run:
        company = search_contacts_for_company(company)
    
        
        
        #=======================================================================================================#
def search_contacts_for_company(company):
    name = company[1]   
    linkedin_condition = True
    while linkedin_condition == True:
        search_string = 'https://www.linkedin.com/search/results/people/?authorCompany=%5B%5D&authorIndustry=%5B%5D&contactInterest=%5B%5D&facetCity=%5B%5D&facetCompany=%5B%5D&facetConnectionOf=%5B%5D&facetCurrentCompany=%5B%5D&facetCurrentFunction=%5B%5D&facetGeoRegion=%5B%5D&facetGroup=%5B%5D&facetGuides=%5B%5D&facetIndustry=%5B%5D&facetNetwork=%5B%5D&facetNonprofitInterest=%5B%5D&facetPastCompany=%5B%5D&facetProfessionalEvent=%5B%5D&facetProfileLanguage=%5B%5D&facetRegion=%5B%5D&facetSchool=%5B%5D&facetSeniority=%5B%5D&facetServiceCategory=%5B%5D&facetState=%5B%5D&groups=%5B%5D&keywords='+ str(name) +'&origin=GLOBAL_SEARCH_HEADER&page=1&refresh=false&skillExplicit=%5B%5D&topic=%5B%5D'
        try:
            driver.get(search_string)
        except UnicodeEncodeError:
            continue
        
        people_at_company = []

        try:
            num_pages = driver.find_elements_by_xpath("//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']//*")[-1].text
        except IndexError or NoSuchElementException:
            
            num_pages = 1
        
        
        print(num_pages, 'pages')
        num_pages = int(num_pages)
        
        
#================================================================================================================#
        
#            while len(people_at_company) < 5:
        for page in range(num_pages):
            #get and analyze data ; job title
            
            if(len(people_at_company) > 5):
                print('This happened (5 contacts) with ', name)
                break
            yield_page, data_avail =  analyze_linkedin_page(page, name)
            if data_avail == False:
                break
            if len(yield_page) > 0:
                for contact in yield_page:    
                    people_at_company.append(contact)
            
            #could be a good use of a probability function : P(Find | F(Current_size, Page))
            if page == 25 and len(people_at_company) < 3:
                #then defective name string -> hard af to fix/make better 
                    #could also handle that ^ inside this if statement
                break
            
            #==============================================+#

            #==============================================================# 
            
            if num_pages > 1: 
                try:
                    next_page = driver.find_element_by_xpath("//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']")
                    next_page.click()                                          
                except (ElementNotVisibleException, ElementClickInterceptedException):
                    try:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        next_page = driver.find_element_by_xpath("//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']")
                        next_page.click()
                    except ElementClickInterceptedException:
                        
                        sleep(3)
                        try:    
                            next_page = driver.find_element_by_xpath("//button[@class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']")
                        except NoSuchElementException:
                            break
                        
                        next_page.click()
                except NoSuchElementException:
                    break
                    
                        
#===============CHANGE --> CONDITION HANDLED ABOVE ==================================================#             
                            
        people_at_company.sort(key=lambda x: x[0])
        if len(people_at_company) <5:
            #needed = 5-len(p@c)
            for i in range(5-len(people_at_company)):
                people_at_company.append('NA')
        else:
            #greater than 5 -> prioritize
            people_at_company = people_at_company[:5]
            
            
        for item in people_at_company:
            #2 cases generally: 5 NA's or a list of lists
            if(isinstance(item, list)):
                #build contact 
                cont = item[1] + " - " + item[2]    
                company.append(cont)
            else:    
                company.append(item)
        linkedin_condition = False
        
    return company
        #=======================================================================================================#    
    
def analyze_linkedin_page(page, name):
    #check if there are actually contacts on this page 
    important_titles = [['ceo','chief executive officer', 'broker of record', 'broker', 'partner', 'owner'], 'president',
                        ['cfo', 'chief financial officer'], 
                        ['coo','chief operating officer'], ['cto', 'chief technology officer'], 
                        ['cmo', 'chief marketing officer'], ['cio', 'chief information officer'], 'director'
                        'controller', 'office manager', 'head of', 'operations']
    
    people_at_company = []
    try:
        contact_name_elems = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//span[@class='name actor-name']"))
        )
        data_avail = True
    except TimeoutException:
        data_avail = False
    
    if data_avail:
        i = 0
    #                contact_name_elems = driver.find_elements_by_xpath("//span[@class='name actor-name']")
        contact_names = []
        
        while i < len(contact_name_elems):
            try:
                contact_names.append(contact_name_elems[i].text)
                i +=1
            except StaleElementReferenceException:
                del contact_name_elems
                contact_name_elems = driver.find_elements_by_xpath("//span[@class='name actor-name']")
                
        i = 0
        contact_roles_elems = driver.find_elements_by_xpath("//p[@class='subline-level-1 t-14 t-black t-normal search-result__truncate']//span[@dir='ltr']")
        contact_roles = []
        while i < len(contact_roles_elems):
            try:
                
                contact_roles.append(contact_roles_elems[i].text.lower())
                i +=1
            except StaleElementReferenceException:
                del contact_roles_elems
                contact_roles_elems = driver.find_elements_by_xpath("//p[@class='subline-level-1 t-14 t-black t-normal search-result__truncate']//span[@dir='ltr']")
        
        
        """
        
        Add in check and analysis of "Current: Blah blah at Blah" section
        
        
        """
        
        #build contacts with the extracted information
        for i in range(len(contact_names)):
            contact = []
            contact.append(contact_names[i])
            contact.append(contact_roles[i])
            useful = regex_parse(important_titles, contact, name)
    #                    print(useful)
            if useful != False:
                people_at_company.append(useful)
                print(people_at_company)
    
    return people_at_company, data_avail
                
        
def write_to_file(master_list_this_run, prospects_file):
    with open(prospects_file, mode='a') as prospects_file:
        csv_writer = csv.writer(prospects_file, delimiter=',', lineterminator='\n')
        for i in master_list_this_run:
            csv_writer.writerow([s.decode("utf-8") for s in i]) #needs to be fixed

    prospects_file.close()


def account_type():
#    return current or competitive or major{current, competitive}
    return None
##to get the items on a page


#email would come through scraping site
#create timestamp
#territory designation requires table of t(Person, Postals)



whose_postal = [
    ["Tony", 'x13', ['M6P', 'M6', 'M8','M8W', 'M8Y', 'M8Z', 'L4V', 'L4W', 'L4X','L4Y', 'L5A', 'L5B', 'L5E', 'L5G', 'L5P', 'M9C']],
    ["Shaq",'x11', ['L5C', 'L5H', 'L5J', 'L5K', 'L5L', 'L5M', 'L6J', 'L6K', 'L6L', 'L6M']], #add back in L6H!!! I took it out in order to not do again
    ["Karen",'x14', ['L0J', 'L4H', 'L5N', 'L5R', 'L5V', 'L5W', 'L6P', 'L6R', 'L6S', 'L6V', 'L6W', 'L6X', 'L6Y', 'L6Z', 'L7A']],
    ["Nicola", 'x17',['L4T', 'L4Z', 'L5S', 'L5T', 'L6T']],
    ["Brandon", 'x18',['M6L','M6M', 'M6N', 'M2H', 'M8X', 'M2J', 'M9A', 'M9B', 'M9N', 'M9P', 'M9R', 'M2K', 'M2M', 'M2N', 'M2R', 'M3H', 'M3J']],
    ["Daniel", 'x20', ['L4K' 'L4L', 'M3K', 'M3L', 'M3M', 'M3N', 'M9L', 'M9M', 'M9V', 'M9W']]
]

postal_codes = ['L8E', 'L8H','L8J', 'L8K', 'L8G', #STONEY CREEK 
'L8T','L8V','L8W','L9A','L9C','L9B', #HAMILTON - MOUNTAIN AREA
'L8P','L8R','L8S','L9G','L9K','L9H', #HAMILTON - WEST
'L7L','L7N','L7M','L7P','L7R','L7S','L7T', #BURLINGTON
'L6H','L6J','L6K','L6L','L6M', #OAKVILLE
#L5H IS PORT CREDIT AND L5V IS STREETSVILLE
'L4W','L4X','L4Y','L4Z','L5R','L5A','L5B','L5C','L5K','L5L','L5E','L5G','L5H','L5J','L5M','L5N','L5W','L5V', #MISSISSAUGA
'L6V','L6W','L6X','L6Y','L6Z','L7A','L6P','L6R','L6S','L6T', #BRAMPTON
'M6S','M8V','M8W','M8X','M9A','M9B','M8Y','M8Z','M9C','M9L','M9M','M9N','M9P','M9R','M9V','M9W', #ETOBICOKE
'M6A','M6B','M6C','M6E','M6G','M6H','M6L','M6M','M6N','M6P', #YORK
'M2H','M2J','M2K','M2L','M2M','M2N','M2P','M2R','M3A','M3B','M3C','M3H', #WILLOWDALE
'M4G','M4H','M4N','M4P','M4R','M5P','M4S','M4T','M4V','M5M','M5N', #TORONTO NORTH
'M4C','M4E','M4J','M4K','M4L','M4M','M1B','M1S','M1T','M1W','M1V','M1X', #EAST YORK AND BEACH
'M1B','M1S','M1T','M1W','M1V','M1X', #SCARBOROUGH NORTH
'M1J','M1K','M1L','M1M','M1N','M1P','M1R','M4A','M4B', #SCARBOROUGH WEST
'M1C','M1E','M1G','M1H', #SCARBOROUGH EAST
'L3R','L6C','L6G', #UNIONVILLE
'L3P','L3S','L6B','L6E', #MARKHAM
'L3T','L4J', #THORNHILL
'L3X','L3Y','L4G', #NEWMARKET AND AURORA
'L4B','L4C','L4S','L4E', #RICHMOND HILL
'L4H','L4L','L4K','L6A' #VAUGHAN
]


industries = [
'Copier',
'Canon',
'Toshiba',
'Kyocera',
'Ricoh',
'Konica Minolta',
'Sharp Printer',
'Printer',
'HP',
'Managed Print',
'Document Management',
'Oki Data',
'Printing Solutions',
'Production Print',
'Colour Management'
]



if __name__ == "__main__":
    opts = Options()
#    prefs = {'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'javascript': 2, 
#                 'plugins': 2, 'popups': 2, 'geolocation': 2, 
#                 'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2, 
#                 'mouselock': 2, 'mixed_script': 2, 'media_stream': 2, 
#                 'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2, 
#                 'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2, 
#                 'push_messaging': 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop': 2, 
#                 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement': 2, 
#                 'durable_storage': 2, 'disk-cache-size': 4096}}
#    opts.add_experimental_option("prefs", prefs)
    opts.add_argument("--user-data-dir=/home/galensprout/.config/google-chrome")
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=opts)
    
    
    process_id = psutil.Process(driver.service.process.pid)
    print("Process Information(Parent): ", process_id)
    child_processes = process_id.children(recursive=True)
    for child in child_processes:
        print('Child PID', child)
    
    
    search_terms = build_search_terms(industries, postal_codes)
    todays_date = datetime.datetime.today().strftime('%Y-%m-%d')
    master_list_this_run = []
    running_total = 0 
    search_term_index = 0
    while search_term_index < len(search_terms):    
        time_start_process = time.time()
            
        driver.get('https://www.google.com/search?source=hp&ei=TtleXfv5JeSI_QaZ44_YBQ&q=m3h%20realtors&oq=m3h+realtors&gs_l=psy-ab.3..33i160l2.1798.4372..4439...0.0..0.113.934.9j2......0....1..gws-wiz.......0i131j0j38j0i22i30j0i22i10i30.8QpbyNqCNcI&ved=2ahUKEwif24G9iJfkAhXuQ98KHUGsC4MQvS4wAHoECAsQIA&uact=5&npsic=0&rflfq=1&rlha=0&rllag=43779574,-79469222,752&tbm=lcl&rldimm=13008810070858663899&rldoc=1&tbs=lrf:!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2#rlfi=hd:;si:13008810070858663899;mv:!1m2!1d43.7944211!2d-79.41743699999999!2m2!1d43.6476987!2d-79.6166288!3m12!1m3!1d71126.18765552614!2d-79.51703289999999!3d43.7210599!2m3!1f0!2f0!3f0!3m2!1i291!2i296!4f13.1;tbs:lrf:!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2')

        """insert multiprocessing here - change linkedin code to def get_contacts(driver, company_names): """
        master_list_this_run = google_search(search_terms, master_list_this_run)
   
        time_end_process = time.time()
        
        process_time = (time_end_process - time_start_process)/60
        print("Process time for the list to be appended to file was " + str(process_time))
        
        write_to_file(master_list_this_run, 'competitive_list.csv')
        print(master_list_this_run, search_term_index)
        
        master_list_this_run = [] #reset to 0 after the data has been offloaded into a csv
#    except Exception as err:
#        
#        """ catch error and print  """
#        print("Process Information(Parent): ", process_id)
#        for child in child_processes:
#            print('Child PID', child)
#        
#        
#        print('Error', err)
#        print('Current search_term_index is ' + str(search_term_index))
#        driver.quit()
#        
#        #output found data 
#    
#    print('\n\n\n\n\n')
    driver.quit()
  
            
    
    
    

        
        
    
                
                
                
                
#Search for M2N, doesn't matter too much what the string is as long as it gets to google maps for business listings

