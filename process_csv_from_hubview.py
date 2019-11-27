  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 12:50:19 2019

@author: galensprout

Want to reachitect so that it can deal with a variable file


determine how to import own modules

"""

from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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
import os
import tkinter as tk



def name_match(name_one, name_two):
    if len(name_one) > len(name_two):
      name = name_two
      compare_to = name_one
    else: 
      name = name_one
      compare_to = name_two
      
    name_pieces = re.sub('\.', '', name.lower()).split(' ')
    piece_count = 0
    
    p_small = []
    for piece in name_pieces:
      if ((piece != 'ltd') or (piece != 'inc') or (piece != 'limited') or (piece != 'incorporated') or (piece!='ulc') or (piece != 'ULC') or (piece!=' ')):
        p_small.append(piece)
        
    for p in p_small: #make regex later 
      if p in compare_to.lower():
        piece_count +=1
        
    ratio = piece_count/len(p_small)
    #ufck
    return ratio



def update_search_bar(search_bar, search_term):

    search_bar.clear()
    search_bar.send_keys(search_term)
    search_bar.submit()

def build_search_terms(ind_list, postal_codes_list):
    print(postal_codes_list)
    terms = []
    for p in postal_codes_list: 
      
        for i in ind_list:
          print(p, i)
          terms.append('"'+p+'"'+' '+i)
    return terms

def regex_parse(tags, contact, company_name):
    output = False 
    words_that_make_name = re.split('[^0-9A-Za-z]', company_name)
    name_length = len(words_that_make_name)
    words_found_count = 0

    for word in words_that_make_name: 

      x = re.search(r'\W'+r'%s' % word.lower() +r'(\W|\s)', contact[1].lower())
      if x != None:
        words_found_count +=1
    
    acceptable = 0.5
  
    ratio = words_found_count/name_length
    if ratio >= acceptable:
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



def google_search_with_multiple_terms(search_terms, driver, terr):
    master_list_this_run = []
#    global running_total 
#    global search_terms
#    global search_term_index
    search_term_index = 0 
    running_total = 0
#    global running_total
    global page_number
    global today
    sizeof_list = 0
    while search_term_index < len(search_terms) and sizeof_list < 1000000000:
      #=======================================================================================================#
    
      
#    for term in search_terms:    
        search_bar = driver.find_element_by_xpath("//input[@title='Search']")
        update_search_bar(search_bar, search_terms[search_term_index])
        page=0
        current_industry = search_terms[search_term_index][6:] #grabs the piece after postal and spaces
        test_counter = 0
        condition = True
        
        # could make it so that when searching for one term, if that one term is found then condition = false
            
        while condition:
            #below grabs the a.href of each box so that it can be clicked
            try:
                companies_listed_on_page = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//div[@jsl='$t t-8x4sQ9CC-MQ;$x 0;']//a[@role='link']"))
                )
                sleep(2)
                companies_listed_on_page = driver.find_elements_by_xpath("//div[@jsl='$t t-8x4sQ9CC-MQ;$x 0;']//a[@role='link']")
            except:
                #no results found
                condition = False
            
                
            results_from_page = analyze_google_page(companies_listed_on_page, current_industry, driver)
            
            
#            running_total += len(results_from_page)
            
            for result in results_from_page:
              if result[5] == terr[1]:
                master_list_this_run.append(result)
         
            try:
                go_to_next_page = driver.find_element_by_xpath("//a[@id='pnnext']")
                print(go_to_next_page)
                go_to_next_page.click()
                page +=1
                companies_listed_on_page = driver.find_elements_by_xpath("//div[@jsl='$t t-8x4sQ9CC-MQ;$x 0;']//a[@role='link']")


            except NoSuchElementException:
                #search term has been used up
                condition = False
                sizeof_list = sys.getsizeof(master_list_this_run)
        search_term_index += 1
                
            
        print(len(search_terms), search_term_index)
        print(test_counter, search_terms[search_term_index-1])
        print('Running total is now', running_total)
    
        
    return master_list_this_run #in the case that list becomes too large and you need to pick up where you left off
  
def google_search_with_one_term(csv_row, driver):
    #this will only be used to update csv for contact features 
    print(csv_row[0], 'csvrow')
    
    if r'https://www.google.com/search?' not in driver.current_url:
      driver.get('https://www.google.com/search?q=m6p%20consultants&oq=m6p+consultants&aqs=chrome..69i57.5403j0j4&sourceid=chrome&ie=UTF-8&npsic=0&rflfq=1&rlha=0&rllag=43662651,-79463761,1133&tbm=lcl&rldimm=2721499773463418624&ved=2ahUKEwicsoPtmt3kAhX6URUIHRRTAGIQvS4wAHoECAoQFg&rldoc=1&tbs=lrf:!2m1!1e3!3sIAE,lf:1,lf_ui:2#rlfi=hd:;si:2721499773463418624;mv:[[43.667652,-79.444858],[43.652086999999995,-79.4816683]];tbs:lrf:!2m1!1e3!3sIAE,lf:1,lf_ui:2')
    
    if (csv_row[0] == '') or (re.search(r'[0-9]{7}\s(Ontario|ONTARIO)', csv_row[0])):

      name = csv_row[1]
    else:

      name=csv_row[0]
    
    search_bar = driver.find_element_by_xpath("//input[@title='Search']")

    update_search_bar(search_bar, name)
    
    condition = True
    while condition == True:
      try:
          companies_listed_on_page = WebDriverWait(driver, 10).until(
              EC.presence_of_all_elements_located((By.XPATH, "//div[@jsl='$t t-8x4sQ9CC-MQ;$x 0;']//a[@role='link']"))
          )
          sleep(2)
          companies_listed_on_page = driver.find_elements_by_xpath("//div[@jsl='$t t-8x4sQ9CC-MQ;$x 0;']//a[@role='link']")
      except:
          #no results found
          condition = False
          break
                  
                  
      csv_row, condition = analyze_google_page(companies_listed_on_page, '', driver, use_case='update_csv', csv_row=csv_row)
      if condition==False:
          break
      
              
      try:
          go_to_next_page = driver.find_element_by_xpath("//a[@id='pnnext']")
          go_to_next_page.click()
          companies_listed_on_page = driver.find_elements_by_xpath("//div[@jsl='$t t-8x4sQ9CC-MQ;$x 0;']//a[@role='link']")
    
    
      except:
          #search term has been used up
          condition = False

          
    return csv_row
                

  
def analyze_google_page(companies_listed_on_page, current_industry, driver, use_case='competitive', csv_row=None):
      
    results_from_page = []
    
    
    for c in companies_listed_on_page:
        deets, valid = get_deets(c, current_industry, driver)   #resulting data struture is [ industry, company_name, website, phone, postal code, address, city, prov ]
        
        
        print('\n\n deets', deets, '\n\n')
        if use_case == 'competitive':
          print('\n\n\n\n\n\n Competitive \n\n\n\n\n')
          if valid:
            results_from_page.append(deets)
            
          
        
        elif use_case == 'update_csv':
            condition = True
            print(csv_row[0])
            csv_name_pieces = re.sub('\.', '', csv_row[0].lower()).split(' ')
            print(csv_name_pieces, 'csv name pieces')
            piece_count = 0
#            while i < len(csv_name_pieces):
#              if (csv_name_pieces[i] == 'ltd'):
#                csv_name_pieces
            csv_p_small = []
            for piece in csv_name_pieces:
              if ((piece != 'ltd') or (piece != 'inc') or (piece != 'limited') or (piece != 'incorporated') or (piece!='ulc') or (piece != 'ULC') or (piece!=' ')):
                csv_p_small.append(piece)
                
            for p in csv_p_small:
              if p in deets[0].lower():
                piece_count +=1
                
            
            acceptable = 0.65
            risky = 0.5
            ratio = piece_count/len(csv_p_small)
            print('ratio: ', ratio)
            print(piece_count)
            print(len(csv_p_small))
            if ratio > acceptable:
              if ((csv_row[3] == '') or (csv_row[3] == 'http://')) and (deets[2]): #website
                csv_row[3] = deets[2]
              ###########################
              print('acceptable')
          #===============================================================================#
              if csv_row[12] != '': #postal code 
                print('known postal')
                from_csv = re.sub('\s+', '', csv_row[12].lower()) 
                from_deets = re.sub('\s+', '', deets[4].lower())
                print(from_csv)
                print(from_deets)
                if from_csv == from_deets: #then this is the same location
                  condition = False
                  print(condition)
                  if (csv_row[6] == '') and (deets[3]):
                    csv_row[6] = deets[3] # phone 
                  if (csv_row[9] == '') and (deets[7]): #street address
                    csv_row[9] = deets[7] 
                  if (csv_row[10] == '') and (deets[6]): #city 
                    csv_row[10] = deets[6]
                  if csv_row[11] == '': #province
                    csv_row[11] = deets[7]
                  
                
              else: #we dont know postal 
                  print('unknown postal')
                  if csv_row[9] != '': #we dont know postal but do know address
                    if csv_row[9].lower() == deets[5].lower(): #refers to street address
                      csv_row[12] = deets[5] #then get the postal and go check if others are defined 
                      if (csv_row[6] == '') and (deets[3]):
                        csv_row[6] = deets[3] # phone 
                      if (csv_row[10] == '') and (deets[6]): #city 
                        csv_row[10] = deets[6]  
                      if csv_row[11] == '': #province
                        csv_row[11] = deets[7]
                      if ((csv_row[3] == '') or (csv_row[3] == 'http://')) and (deets[3]): #website
                        csv_row[3] = deets[3]
                  else: #we dont know postal or address
                    csv_row[9] = deets[5]
                    if (csv_row[6] == '') and (deets[3]):
                      csv_row[6] = deets[3] # phone 
                    if (csv_row[10] == '') and (deets[6]): #city 
                      csv_row[10] = deets[6]  
                    if csv_row[11] == '': #province
                      csv_row[11] = deets[7]
                    if ((csv_row[3] == '') or (csv_row[3] == 'http://')) and (deets[2]): #website
                      csv_row[3] = deets[2]
            elif risky > ratio > acceptable:
              print('risky')
              #check phone number -> then do the other stuff
              if csv_row[6] != '':
                if csv_row[6] == deets[3]:
                  if ((csv_row[3] == '') or (csv_row[3] == 'http://')) and (deets[2]): #website
                    csv_row[3] = deets[2]
                  #then this is the right company -- figure out if right location or other shit
                  if csv_row[12] != '': #postal code 
                    if re.sub('\s+', '', csv_row[12].lower()) == re.sub('\s+', '', deets[4].lower()): #then this is the same location
                      condition = False
                      if (csv_row[6] == '') and (deets[3]):
                        csv_row[6] = deets[3] # phone 
                      if (csv_row[9] == '') and (deets[7]): #street address
                        csv_row[9] = deets[7] 
                      if (csv_row[10] == '') and (deets[6]): #city 
                        csv_row[10] = deets[6]
                      if csv_row[11] == '': #province
                        csv_row[11] = deets[7]
                      if ((csv_row[3] == '') or (csv_row[3] == 'http://')) and (deets[3]): #website
                        csv_row[3] = deets[3]
                
                  else: #we dont know postal 
                      if csv_row[9] != '': #we dont know postal but do know address
                        if csv_row[9].lower() == deets[5].lower(): #refers to street address
                          csv_row[12] = deets[4] #then get the postal and go check if others are defined 
                          if (csv_row[6] == '') and (deets[3]):
                            csv_row[6] = deets[3] # phone 
                          if (csv_row[10] == '') and (deets[6]): #city 
                            csv_row[10] = deets[6]  
                          if csv_row[11] == '': #province
                            csv_row[11] = deets[7]
                          if ((csv_row[3] == '') or (csv_row[3] == 'http://')) and (deets[3]): #website
                            csv_row[3] = deets[3]
                      else: #we dont know postal or address
                        csv_row[9] = deets[5]
                        if (csv_row[6] == '') and (deets[3]):
                          csv_row[6] = deets[3] # phone 
                        if (csv_row[10] == '') and (deets[6]): #city 
                          csv_row[10] = deets[6]  
                        if csv_row[11] == '': #province
                          csv_row[11] = deets[7]
                        if ((csv_row[3] == '') or (csv_row[3] == 'http://')) and (deets[2]): #website
                          csv_row[3] = deets[2]
                
            else:
                print('else block')
              
                #stop condition -> return different than other cases
                
                
    if use_case == 'update_csv':
      print(csv_row)
      return csv_row, condition
    elif use_case == 'competitive':
      return results_from_page
        
        #====================================================================++++++++++++++++=====#
        
 
  
    return results_from_page      

def get_deets(c, current_industry, driver):
    #resulting data struture is [ company_name, industry,  website, phone, postal code, territory code, rep name, city, province, address ]
    todays_date = datetime.datetime.today().strftime('%Y-%m-%d')
    whose_postal = [
      ["Tony", 'x13', ['M6P', 'M6', 'M8','M8W', 'M8Y', 'M8Z', 'L4V', 'L4W', 'L4X','L4Y', 'L5A', 'L5B', 'L5E', 'L5G', 'L5P', 'M9C']], 
      ["Sierra",'x11', ['L5C', 'L5H', 'L5J', 'L5K', 'L5L', 'L5M', 'L6J', 'L6K', 'L6L', 'L6M']], 
      ["Karen",'x14', ['L0J', 'L4H', 'L5N', 'L5R', 'L5V', 'L5W', 'L6P', 'L6R', 'L6S', 'L6V', 'L6W', 'L6X', 'L6Y', 'L6Z', 'L7A']],
      ["Galen", 'x17',['L4T', 'L4Z', 'L5S', 'L5T', 'L6T']],
      ["Brandon", 'x18',['M6L','M6M', 'M6N', 'M2H', 'M8X', 'M2J', 'M9A', 'M9B', 'M9N', 'M9P', 'M9R', 'M2K', 'M2M', 'M2N', 'M2R', 'M3H', 'M3J']],
      ["Daniel", 'x20', ['L4K' 'L4L', 'M3K', 'M3L', 'M3M', 'M3N', 'M9L', 'M9M', 'M9V', 'M9W']]
    ]
    
    try:
        c.click()
    except:
        try:
            sleep(1)
            c.click()
        except:
            #holy fuck 
            pass
            

    
    deets = []
    
    #keep here to ensure that the driver gets a new value and not the old pane
    xpath_company_name = "//div[@data-attrid='title']//span" #.text
    xpath_address = "//span[@class='LrzXr']" #break down into postal and street
    xpath_website = "//a[@class='CL9Uqc ab_button']" #.get_attribute("href")
    xpath_phone = "//span[@data-dtype='d3ifr']//span"

    
    details_list = [xpath_company_name, xpath_website, xpath_phone, xpath_address]
    
    valid=False
    try:
        pane = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[@data-attrid='title']//span"))
        )
    except TimeoutException:
        condition = False
        print('I am lost for how this even can occur -if this continues happening then try printing body of response')
        
        
    sleep(0.8)

    for i in details_list:
        try:
            x = driver.find_element_by_xpath(i)
            if i == xpath_website:
                tag = x.get_attribute("href")
                
            else:
                tag = x.text
                if i == xpath_address:
                    tag_postal = tag[-7:]
                    
                    
                    current_territory_code='ctc nf'
                    current_rep_name = 'crn nf'
                    for w in whose_postal:
                        for j in w[2]:
                            if tag_postal[0:3] == j:
                            
                                valid = True
                        
                                current_territory_code = w[1]
                                current_rep_name = w[0]
                                
                            
                    
                    deets.append(tag_postal)
                    
                    deets.append(current_territory_code)
                    deets.append(current_rep_name)
                    
                    tag = tag[:-7]
                    a_pieces = tag.split(',')
                    print('a pieces', a_pieces)
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
            
            if i == xpath_company_name:
              deets.append(tag)
              deets.append(current_industry)
            else:  
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
        
        
        
    return deets, valid 
  
  
def navigate_to_linkedin_search(driver):
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
    driver.execute_script("document.body.style.zoom='60%'")
    
#    driver.get('https://www.linkedin.com/search/results/people/?keywords=THOMSON%20TERMINALS%20LTD.&origin=GLOBAL_SEARCH_HEADER&page=20')
#    driver.execute_script("document.body.style.zoom='50%'")


def add_linkedin_contacts(master_list_this_run, starting_index, driver, output_filename):

    
        
    linkedin_list = give_me_starting_linkedin_list(master_list_this_run)
    
    #companies that have multiple locations are grouped into a list
    
    has_linkedin_stopped = False
    idx = 0
    iter_length = len(linkedin_list)
    while idx < iter_length and has_linkedin_stopped == False:
      
      if isinstance(linkedin_list[idx][0], list):
        linkedin_list[idx][0], has_linkedin_stopped = search_contacts_for_company(linkedin_list[idx][0], driver, starting_index)
        for location in linkedin_list[idx]:
          location[starting_index: starting_index+5] = linkedin_list[idx][0][starting_index: starting_index+5]
          write_to_file(location, output_filename)
      else:
        linkedin_list[idx], has_linkedin_stopped = search_contacts_for_company(linkedin_list[idx])
        write_to_file(linkedin_list[idx], output_filename)
        
      idx+=1
    
    return idx, iter_length
  
def give_me_starting_linkedin_list(list_of_lists):
    #logic to not search for the same company twice 
    #sort the list so that any companies with the same name are in the same group 
      #use isinstance 
    new_list = []
    
    #if the value of this index is the same as another one(or more) coming in the list then with the matches build a "company"
    idx = 0
    
    name_cell_idx = 0
    while idx < len(list_of_lists):
      print(idx)
      new_group = []
      for later_row in list_of_lists[idx:]:
        if list_of_lists[idx][name_cell_idx].lower() == later_row[name_cell_idx].lower():
          new_group.append(later_row)
      if len(new_group) > 0:
        new_group.append(list_of_lists[idx])
        new_list.append(new_group)
      else:
        new_list.append(csv[idx])
      
      idx+=1
        
        
    return new_list
  
 
      
  
          
        #=======================================================================================================#
def search_contacts_for_company(company, driver, starting_index, first_index_for_contacts=None): #remember to pass in 19 when running for scott
    print('got here')
    if first_index_for_contacts == None:
      #default to end of line
      first_index_for_contacts = len(company)
      
    name = company[1]  
    if name =='':
      print(company)
      name = company[0]
      
    if (company[0] == '') or (re.search(r'[0-9]{7}\s(Ontario|ONTARIO)', company[0])):
      name = company[0]
    else:
      name = company[1]
      
    simple_name =re.sub(r'( ltd| LTD| Ltd| \.| inc| Inc| INC|\.| limited| Limited| incorporated| Incorporated| INCORPORATED| ULC| ulc)', '', name) 
    search_name = '"' + simple_name + '"'
    print('\n\n\n\n\n\n', search_name, '\n\n\n\n\n\n\n')
    
    linkedin_condition = True
    while linkedin_condition == True:
#        search_string = 'https://www.linkedin.com/search/results/people/?authorCompany=%5B%5D&authorIndustry=%5B%5D&contactInterest=%5B%5D&facetCity=%5B%5D&facetCompany=%5B%5D&facetConnectionOf=%5B%5D&facetCurrentCompany=%5B%5D&facetCurrentFunction=%5B%5D&facetGeoRegion=%5B%5D&facetGroup=%5B%5D&facetGuides=%5B%5D&facetIndustry=%5B%5D&facetNetwork=%5B%5D&facetNonprofitInterest=%5B%5D&facetPastCompany=%5B%5D&facetProfessionalEvent=%5B%5D&facetProfileLanguage=%5B%5D&facetRegion=%5B%5D&facetSchool=%5B%5D&facetSeniority=%5B%5D&facetServiceCategory=%5B%5D&facetState=%5B%5D&groups=%5B%5D&keywords='+ str(search_name) +'&origin=GLOBAL_SEARCH_HEADER&page=1&refresh=false&skillExplicit=%5B%5D&topic=%5B%5D'
        
        
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
            
            driver.get('https://www.linkedin.com/search/results/people/?authorCompany=%5B%5D&authorIndustry=%5B%5D&contactInterest=%5B%5D&facetCity=%5B%5D&facetCompany=%5B%5D&facetConnectionOf=%5B%5D&facetCurrentCompany=%5B%5D&facetCurrentFunction=%5B%5D&facetGeoRegion=%5B%5D&facetGroup=%5B%5D&facetGuides=%5B%5D&facetIndustry=%5B%5D&facetNetwork=%5B%5D&facetNonprofitInterest=%5B%5D&facetPastCompany=%5B%5D&facetProfessionalEvent=%5B%5D&facetProfileLanguage=%5B%5D&facetRegion=%5B%5D&facetSchool=%5B%5D&facetSeniority=%5B%5D&facetServiceCategory=%5B%5D&facetState=%5B%5D&groups=%5B%5D&keywords='+ str(search_name) +'&origin=GLOBAL_SEARCH_HEADER&page='+str(page) +'&refresh=false&skillExplicit=%5B%5D&topic=%5B%5D')
          
            
            
            driver.execute_script("document.body.style.zoom='67%'")
            sleep(2)
            #get and analyze data ; job title
            
            yield_page, data_avail, has_linkedin_stopped =  analyze_linkedin_page(simple_name, driver)
            
            if has_linkedin_stopped:
              break
            
            if(len(people_at_company) > 5):
                print('This happened (5 contacts) with ', name)
                break
              
            
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
          
                            
        people_at_company.sort(key=lambda x: x[0])
        if len(people_at_company) <5:
            #needed = 5-len(p@c)
            for i in range(5-len(people_at_company)):
                people_at_company.append('NA')
        else:
            #greater than 5 -> prioritize
            people_at_company = people_at_company[:5]
            
        #===============================================================================================#
        
        for item in people_at_company:
            #2 cases generally: 5 NA's or a list of lists
            if(isinstance(item, list)):
                #build contact 
                processed_item = item[1] + " - " + item[2]    
              
            else:
                processed_item = item
              
            
            company.insert(starting_index, processed_item)
            starting_index +=1
            
        #===============================================================================================#
        
        linkedin_condition = False
        print(company)
    return company, has_linkedin_stopped
        #=======================================================================================================#    
    
def analyze_linkedin_page(name, driver):
    has_linkedin_stopped = False
    #check if there are actually contacts on this page 
    important_titles = [['ceo','chief executive officer', 'broker of record', 'broker', 'partner', 'owner'], 'president',
                        ['cfo', 'chief financial officer'], 
                        ['coo','chief operating officer'], ['cto', 'chief technology officer'], 
                        ['cmo', 'chief marketing officer'], ['cio', 'chief information officer'], 'director',
                        'controller', 'office manager', 'head of', 'operations', 'warehouse manager', 'manager', 'business development manager']
    """
    
    future:
        find list of important titles by industry
    
    
    
    """
    
    people_at_company = []
    try:
        contact_name_elems = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//span[@class='name-and-icon']"))
        )
#        print(len(contact_name_elems))
        contact_roles_elems = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//p[@class='subline-level-1 t-14 t-black t-normal search-result__truncate']//span[@dir='ltr']"))
        )
#        print(len(contact_roles_elems))
        data_avail = True
    except TimeoutException:
        data_avail = False
        
        try:
          linkedin_stopped = driver.find_element_by_xpath("//div[@@class='search-no-results__image-container']//h1[@class='t-20 t-black t-normal mb2']").text
          if linkedin_stopped == 'Search Limit Reached.':
            has_linkedin_stopped = True
              
        except:
          pass
          
          
    if data_avail:
        i = 0
    #                contact_name_elems = driver.find_elements_by_xpath("//span[@class='name actor-name']")
        contact_names = []

        while i < len(contact_name_elems):

            try:
                contact_name_elems=driver.find_elements_by_xpath("//span[@class='name-and-icon']")
                contact_names.append(contact_name_elems[i].text.split('\n')[0])
#                print(i)
               
            except:
                
#                del contact_name_elems
                print('Excepted at ',i)
                contact_name_elems = driver.find_elements_by_xpath("//span[@class='name-and-icon']")
                sleep(1)
                contact_names.append(contact_name_elems[i].text.split('\n')[0])
            i+=1 
        print('yielded contact names: ', len(contact_names), 'from ', len(contact_name_elems))      
        i = 0
#        contact_roles_elems = driver.find_elements_by_xpath("//p[@class='subline-level-1 t-14 t-black t-normal search-result__truncate']//span[@dir='ltr']")
        contact_roles = []
        while i < len(contact_roles_elems):
            try:
                contact_roles_elems=driver.find_elements_by_xpath("//p[@class='subline-level-1 t-14 t-black t-normal search-result__truncate']//span[@dir='ltr']")
                contact_roles.append(contact_roles_elems[i].text.lower())
                print(i)
#                i +=1
            except:
#                del contact_roles_elems
                print('Excepted at ',i)
                contact_roles_elems = driver.find_elements_by_xpath("//p[@class='subline-level-1 t-14 t-black t-normal search-result__truncate']//span[@dir='ltr']")
                sleep(1)
                contact_roles.append(contact_roles_elems[i].text)
            i+=1 
        print('yielded contact roles: ', len(contact_roles), 'from ', len(contact_roles_elems))
        
        
        print('\n\n')
        
        #build contacts with the extracted information
        i = 0
        while i < len(contact_names):
            contact = []
            contact.append(contact_names[i])
            contact.append(contact_roles[i])
            useful = regex_parse(important_titles, contact, name)
            
    #                    print(useful)
            if useful != False:
                people_at_company.append(useful)
                print(people_at_company)
            
            i+=1
            
            
            
    return people_at_company, data_avail, has_linkedin_stopped
                
        
def write_to_file(_input, file, mode='w'):
    with open(file, mode=mode) as file:
      csv_writer = csv.writer(file, delimiter=',', lineterminator='\n')
      if isinstance(_input[0], list):
        for line in _input:
          csv_writer.writerow(line)
      
      elif isinstance(_input[0], (int, str)):
        csv_writer.writerow(_input)
      
    file.close()

def get_whose_postal(rep_name): #for a change - dont forget to change in get_deets() 
    whose_postal = [
      ["Tony", 'x13', ['M6P' , 'M6', 'M8','M8W', 'M8Y', 'M8Z', 'L4V', 'L4W', 'L4X','L4Y', 'L5A', 'L5B', 'L5E', 'L5G', 'L5P', 'M9C']],
      ["Sierra",'x11', ['L5C', 'L5H', 'L6H', 'L5J', 'L5K', 'L5L', 'L5M', 'L6J', 'L6K', 'L6L', 'L6M']], 
      ["Karen",'x14', ['L0J', 'L4H', 'L5N', 'L5R', 'L5V', 'L5W', 'L6P', 'L6R', 'L6S', 'L6V', 'L6W', 'L6X', 'L6Y', 'L6Z', 'L7A']],
      ["Galen", 'x17',['L4T', 'L4Z', 'L5S', 'L5T', 'L6T'], 'Scott'],
      ["Brandon", 'x18',['M6L','M6M', 'M6N', 'M2H', 'M8X', 'M2J', 'M9A', 'M9B', 'M9N', 'M9P', 'M9R', 'M2K', 'M2M', 'M2N', 'M2R', 'M3H', 'M3J']],
      ["Daniel", 'x20', ['L4K' 'L4L', 'M3K', 'M3L', 'M3M', 'M3N', 'M9L', 'M9M', 'M9V', 'M9W']],
      ["Daniel K", 'tcd', ['M4Y', 'M5J', 'M5S', 'M5T', 'M5C', 'M5H', 'M5X']]
    ]
    
    
    for terr in whose_postal:
      if terr[0].lower() == rep_name.lower():
        return terr


def get_postal_codes(): #NOT SURE IF NECESSARY FOR HUB
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
  
  return postal_codes

def get_default_industries():
  industries = [
  'Consulting',
  'Financial Services',  
  'Banking', 
  'Accounting',
  'Insurance',
  'Legal',
  'Recruiting',
  'Schools',
  'Churches',
  'Mosques',
  'Synagogues'
  'retirement home'
  'Advertising',
  'Graphic Communications',
  'Communications',
  'Public Relations',
  'Marketing',
  'Media',
  'Entertainment',
  'Construction',
  'Engineering',
  'Architecture',
  'Interior Design', 
  'Mining',
  'Environmental',
  'Biotech',
  'Energy ',
  'Chemicals',
  'Machinery',
  'Manufacturing', 
#  'Electronics',
  'Software',
#  'Technology',
  'Telecommunications',
#  'IT',
#  'Education',
  'School'
  'Religious Organization',
  'Non-profit',
  'Member Organizations',
  'Government',
  'Health Care',
  'Tourism',
  'Travel',
  'Restaurant ',
  'Hospitality',
  'Recreation',
  'Apparel',
  'Retail',
  'Property Management',
  'Real Estate',
  'Shipping',
  'Transportation',
  'Automotive'
  ]
  return industries




#architected for an easy portal to access -- this is control flow here -- for a given use case :: steps needed for output
def main_script(use_case, rep_name, path_to_database=None, path_to_csv=None, linkedin_search=True, desired_industries=None, desired_postal=None, num_desired_accounts=1000000): #linkedin credentials

    search_term_index = 0
    running_total = 0
  
    time_start_process = time.time()
    today = datetime.date.today().strftime('%m/%d/%Y') 
    directory = '/home/galensprout/Documents/LeadGenOutput/' 
    output_filename =  str(use_case) + '-' + 'linkedin_search_' + str(linkedin_search) + 'created' + today + '.csv'
    if rep_name != None:
      repfile_ref = str(rep_name)
    else:
      repfile_ref = 'NoName'
    
    output_filename = directory + repfile_ref + output_filename
      
    
    opts = Options()
    opts.add_argument("--user-data-dir=/home/galensprout/.config/google-chrome")
    opts.add_argument("--start-maximized")
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=opts)
    
    if use_case == 'competitive': #or really the competitor data too -- unless you will start with a csv for that
      print(desired_postal)
      print(desired_industries)
      
      if (desired_industries == None) and (desired_postal==None):  
        search_terms = build_search_terms(get_default_industries(), get_whose_postal(rep_name)[2])
      
      elif (desired_industries == None) and (desired_postal):  
        search_terms = build_search_terms(get_default_indDocumentsustries(), desired_postal)
        
      elif (desired_industries) and (desired_postal==None):
        search_terms = build_search_terms(desired_industries, get_whose_postal(rep_name)[2])
      
      elif (desired_industries) and (desired_postal):
        search_terms = build_search_terms(desired_industries, desired_postal)
        
      else:
        print('you goof')
      
      search_terms = search_terms[:num_desired_accounts] #make sure in the docs to show how to produce certain outputs
      
      
        
   
#      running_total = 0 
      search_term_index = 0
      while (search_term_index < len(search_terms)) and (search_term_index < num_desired_accounts): #in case of list getting too large for working memory 
          
              
          driver.get('https://www.google.com/search?source=hp&ei=TtleXfv5JeSI_QaZ44_YBQ&q=m3h%20realtors&oq=m3h+realtors&gs_l=psy-ab.3..33i160l2.1798.4372..4439...0.0..0.113.934.9j2......0....1..gws-wiz.......0i131j0j38j0i22i30j0i22i10i30.8QpbyNqCNcI&ved=2ahUKEwif24G9iJfkAhXuQ98KHUGsC4MQvS4wAHoECAsQIA&uact=5&npsic=0&rflfq=1&rlha=0&rllag=43779574,-79469222,752&tbm=lcl&rldimm=13008810070858663899&rldoc=1&tbs=lrf:!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2#rlfi=hd:;si:13008810070858663899;mv:!1m2!1d43.7944211!2d-79.41743699999999!2m2!1d43.6476987!2d-79.6166288!3m12!1m3!1d71126.18765552614!2d-79.51703289999999!3d43.7210599!2m3!1f0!2f0!3f0!3m2!1i291!2i296!4f13.1;tbs:lrf:!2m1!1e2!2m1!1e3!3sIAE,lf:1,lf_ui:2')
  
          """insert multiprocessing here - change linkedin code to def get_contacts(driver, company_names): """
          main_mem = google_search_with_multiple_terms(search_terms, driver, get_whose_postal(rep_name))
          
          #==================================================================================#
                    
#          contig_major_rep = get_whose_postal(rep_name)[3]
#          
#          if sys.plaform == 'windows':
#            contig_str = r'\\' + contig_major_rep + '_accounts'
#          elif sys.platform == 'linux':
#            contig_str = '/' + contig_major_rep + '_accounts'
#            
#          mypath = path_to_database + contig_str
#          filenames = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#          
#          locations_of_names = [] #will apppend list(name, postal)
#          for file in filenames:
#            
#          
#          
#          for lead in main_mem:
#            #validate not a duplicate 
#            
#          
          
          
          write_to_file(main_mem, 'daniel_klugman_accounts.csv')
          
          
          if linkedin_search:
            navigate_to_linkedin_search(driver)
            idx, iter_length = add_linkedin_contacts(main_mem, len(main_mem[0]), driver, output_filename) #returns the idx in case that it doesnt complete 
            if idx < iter_length:
              write_to_file([rep_name, idx, iter_length, main_mem[idx][0]], '/home/galensprout/Documents/LINKEDIN_STOPPED_AT_INDEX.csv')


        
      
          #===============================================================================#
          
           #reset to 0 after the data has been offloaded into a csv
#      pass
#      do 
#      
        #define the globals in google_search_with_multiple_terms
#      
##      
##      need a system to ensure that the data is not duplicated  EXCEPT IF DEALING WITH UPDATE CSV -- this is done on a per line basis
##      to do so with the new incoming competitive accounts:
##
##        confirm not a major account --> cross reference with data in database
##        
##        will need to hold each file in a "database": a folder of csv's 
##            then: for csv in folder:
##              for line in csv:
##                confirm not already had 
##    
##                check if in destination already -- DO THIS CSV FIRST BUT THEN CONFIRM ITS NOT ELSEWHERE
##                  IF NOT IN ANY CSV:  
##                    then append to destination csv 
##                  
#      name_index = ''
#      for filename in os.listdir('CSV_Database'):
#        #===========================================================#
#        
#        #ADD IN LOGIC TO USE THE TERRITORY CODE TO SHORTCUT SEARCHING THROUGH COMMERCIAL REPS
#        
#        #===========================================================#
#        if filename.endswith('.csv'):
#          with open(filename, mode='r') as f:
#            reader=csv.reader(f)
#            data = [line for line in reader]
#            for row in main_mem:
#              
#              #good idea to ensure data format 
#              for line in data:
#                if row[name_index].lower() == line[name_idx]:
#                  #===============================================================================++++++++++#
#                              #insert 'playing with data'
#                  #=========================================================================================#
#                  
#                  #check first if there are any missing values to add
#                  #then after the existing entry has received the data -> delete from main mem
#                       
#                    
    if use_case == 'update_csv': #this will include xpert and siebel 
      if path_to_csv == None:
        print(' I need a csv for this function')
        
      #open and read csv
      #for each line :
        #confirm missing data 
          #google search with one term for each in missing_Data list
        
        #add linked in contacts for all in list
          #group the same companies in csv    
            #LINKED IN TO OCCUR AFTER IF/ELSE     
      main_mem = [] 
      with open(path_to_csv) as csvfile:
          reader = csv.reader(csvfile)
          for line in reader:
    
              main_mem.append(line)
                   
          csvfile.close()
      
      headers = main_mem[0]
      main_mem = main_mem[1:]
      
      
      #==========================================================#
            #google search --- comment out if unwanted -- add as option later
            
      for company in main_mem:
        company = google_search_with_one_term(company, driver)
      print(main_mem)
      #==========================================================#
      
      
      if linkedin_search:
        
        navigate_to_linkedin_search(driver)
        idx, iter_length = add_linkedin_contacts(main_mem, len(headers), driver, output_filename) #returns the idx in case that it doesnt complete 
        if idx < iter_length:
          write_to_file([rep_name, idx, iter_length, main_mem[idx][0]], '/home/galensprout/Documents/LINKEDIN_STOPPED_AT_INDEX.txt')
      
      else:
        
        write_to_file(main_mem)
  
    time_end_process = time.time()
          
    process_time = (time_end_process - time_start_process)/60
    print("Process time for the list to be appended to file was " + str(process_time))

    
main_script('competitive', path_to_csv ='/home/galensprout/Documents/daniel-klugman.csv', rep_name = 'Daniel K', linkedin_search=True)

    
#  """  
#  
#  for linkedin:
#      extract names (re-append after)
#      ensure that list to search names for is not duplicated 
#        ideally build system to add to each instance of the name for the contacts found with the name
#      
#    add linkedin contacts 
#      for any case do this last after the base contact info is determined and the line is known to be not duplicated 
#    
#    
#    
#    
#    then with updated data --> write to the csv     
#    
#  """
        
        
        
        
        
        

        
        
        
        
        
        
      #==========================================================================================================+++#
  
  
   
#    print(names)
    

    


"""


ALL OF THE BELOW IS TO DETERMINE THE FORMATTING RULES FOR THE TABLE

could also write rule to remove spaces in the string(s) being checked if the regex pattern fails
"""



#
#def regex_derived_format_of_tabular_data(csv, headers_length):
#    #returns a row with n columns of [Regex Cell > regex_group1, regex group2...]
#    regex_rule = []
#    list_for_analysis = setup_for_regex_analysis(csv, headers_length)
#    regex_string_table = [regex_of_this_line(line) for line in list_for_analysis]
#    null_regex_rule = regex_string_table[0]
#    #======================================================================================================================#
#    idx_vert = 0
#    idx_horiz = 0
#    while idx_horiz < headers_length:
#      first = check_for_groups(regex_string_table[0][idx_horiz]) #list 
#      first_groups = [i for i in first if isinstance(i, list)] 
#      num_groups = len(first)
#      #tries to invalidate and peel back for n in sample
#      #check each column for validity 
#      for row in regex_string_table:
#        
#        
#        
#        
#        
#        
#        
#        
#        item_to_compare = check_for_groups(row[idx_horiz]) 
#        item_as_groups = [i for i in item_to_compare if isinstance(i, list)]
#        
#        is_same_length = sum([len(i) for i in item_as_groups]) - sum([len(i) for i in first_groups]) #if same length this equals 0
#        
#        if len(item_as_groups) != len(first_groups) and is_same_length == 0:
#          #then another character type caused inconsistency which lead to another group
#            #most likely to happen with postal codes eg M9B 0C3 vs M9B0C3
#            
#            
#            #best solution is to check the rest of the rows and take the most common format
#            favor_first = 0
#            favor_this = 0 
#            for row in regex_string_table:
#              if len(row[idx_horiz]) == len(first):
#                favor_first +=1
#              elif len(row[idx_horiz]) == len([i for i in row[idx_horiz] if isinstance(i, list)):
#                favor_this +=1
#            
#            #find the differential cause 
#            temp_idx = 0
#            if favor_first > favor_this:
#              if len(first_groups) > len(item_as_groups):
#                #then we want to break apart item into structure of the first group
#                  #note: in this case we would also need to add in '\W' for non alphanumeric 
#                while temp_idx < len(first_groups):
#                  try:
#                    
#                    #try to break apart with the len of the index from "first" so that the current and next indices line up length is the same 
#                    pass
#                  
#                  except AssertionError:
#                    pass
#                  
#                  temp_idx +=1
#              else:
#                
#                
#            
#            else: #favor this 
#            
#            
#            
#                
#                
#             
#                              
##======================================================================================================================#         
#        
#        
#          #at this point, the rest of the algorithm must be dealing with an equal number of groups        
#        
#        
#        
##======================================================================================================================#
##        if len(row[idx_horiz]) == len(regex_string_table[0][idx_horiz]): #compares two lists of characters that are formatted as lists 
#        group_idx = 0
#        while group_idx < num_groups:
#          for i in item_to_compare:
#            if isinstance(item_to_compare[group_idx], list):
#              do 
#              then increment group idx
#            else: #is string and must be special character or space 
#              pass 
#          
#          
#          if_update_group = [] 
#          
#          #change will happen per group -> Maximize discrimination on format
#            #effectively looping through each possible invalidation and if invalidation found on this idx then peel back the current regex string for this group 
#            
#            #3 conditions on groups:
#              #1: regex is starting string 
#                ## return starting string or updated to any case
#              #2: regex has been updated but not necessarily finished 
#                # -> has '\w' but not {0,10} 
#                  #return current iteration or '\w' with {0,X}
#                # -> has {0,X} but is for set([0-9] or [A-Za-z])
#              #3: regex wouldn't be updated from this point on ; '\w'{0,10} is the case 
#          if ('\w' not in item_to_compare[group_idx]) and ('{' not in item_to_compare[group_idx]):
#            
#            if len(first[group_idx]) == len(item_to_compare[group_idx]):
#              #then check if the discrimination holds
#              char_idx = 0
#              while char_index < len(first[group_idx]): #len gives the number of characters
#                
#                if first[group_idx][char_idx] == item_to_compare[group_idx][char_idx]:
#                  #nothing needs to be done
#                  pass 
#                
#                else:
#                  #then discrimination per character failed on this group
#                  """ replace me with method to change char from [0-9], [A-Za-z] to '\w' """
#                  string.replace('[A-Za-z]', '\w')
#                  string.replace('[0-9]')
#                char_idx +=1
#              
#              #then easily comparable
#              if first[group_idx] == item_to_compare[group_idx]:
#                #then discrimination worked @ sub index 
#                
#                
#            else: #BUILD CI 
#              #CI is not specific to any char or char set but rather all 
#                #should reasonably be larger range for '\w'
#              #the two groups are not equal length -> need condidence interval 
#              #can only check if all the char's in the group are the same as each other and same with reference object
#                
#              
#                #check if length at this index is larger than the previous one found 
#                  #if yes, update max 
#                
#              
#                
#                to_check = first[group_idx] + item_to_compare[group_idx] #adding lists of lists since groups/words are in list format
#                length = 0
#                for char in to_check:
#                  if char != to_check[0]:
#                    #are all the chars the same type?
#                    #random between letters and numbers 
#                    """replace me with method to change group from list of chars that equal [0-9], [A-Za-z] to '\w' """
#                    
#                #now we check for proper confidence interval 
#                  #goal is to compute max once in this block
#                    #get all groups at this group index ; 
#                      #find max lengths of all groups at this index 
#                      
#                
#                
#                    """ and method for confidence interval  """
#                    
#                  
#                  
#          elif ('\w' in item_to_compare[group_idx]) and ('{' not in item_to_compare[group_idx]):
#            
#          
#                
#          group_idx += 1
#      idx_horiz +=1
#            
#        
#          
#          
#      
#      
#      idx_horiz+=1
#    
#        for string in line:
#          #iteration structure:
#            #columns from left to right 
#              #at that index/column value -> check that each row is equal to row 0 at that index 
#          
#          
#          
#          
#          
#          #check if all the strings are equal length 
#            #if true then check for groups being equal length 
#              #if equal length: 
#                #for each char:
#                  #check if each index/char is the same type 
#                    #if all are same type 
#                      #return a regex pattern that discriminates for these types at these indexes
#                    #else ; not the same type at the same index
#                      #replace discriminatory chars with \w and return 
#                      
#              #else (the equal index groups are not equal lengths):
#                #check if the group is all the same character 
#                  #if yes then return [char type]{CI} where confidence interval is {1, MAX(Sample[Index]) + 2}
#                  
#          
#            #else (the string is not equal length)
#              #check for each group's length 
#                #if each group is same length
#                  #check index for index 
#                    #if at each index: types are the same -> return discriminatory string
#                    #else (not same at each index) -> replace discr. with '\w' and return
#                    
#                #else;   each group is not the same length:
#                  #check if each char is same type
#                  #if (same type):
#                    #return [char type]{CI} where confidence interval is {1, MAX(Sample[Index]) + 2}
#                  #else ; not the same type in the group 
#                    #replace discr. terms with '\w' and return pattern
#            
#          
#          for char in string: #string is actually formatted as a list 
#            #get temp char-string of alphanumeric 
#              #compare length 
#                #compare same index for all strings 
#                      #maybe compare string_one[this_index] to other strings[this_index]
#                      #if match -> increment match ?
#                      
#                    #note: [0-9][0-9] is the same as [0-9]+ or [0-9]{0, 2}
#                    
#                      #because in the case that you have an address, if some numbers are 2 digits and some are 3 -> then the rest of the indexes following that one will be thrown off 
#                      #idea : find groups (seperated by non alphanumeric) and determine length +/- CI 
#                        #then check if the groups are the same length
#                          #so ... if group-words #1 == group-words #2 -> easy solve ; analyze as whole string 
#                            #else: analyze as groups 
#                              #for group in groups:
#                                #is the group the same length as equivalent groups?
#                                  #yes -> simple analysis
#                                  #no/else ->    it is probably not a uniform-feature object such as an ID # 
#                                    #so just check if all chars in the group are the same 
#                                    
#                                    
#                      #return string= group 1 + group 2 + group 3 ...
#                        # -> regex_rule_string_complete = group1(+/- CI) + [special char] + group 2(+/- CI) ...
#                              #groups value will either be CASE 1: letters and numbers or CASE 2: word chars
#                                #example r'[0-9]{0, 5}[A-Za-z]{3,4}' or r'\w{0,7}'
#                                
#                                
#                      #length computation: max of sample - min of sample = range + 2 on both sides
#            
#            
#            
##            print(string_for_compare)
#        alphanumeric.append(line)
#    #======================================================================================================================#
#
##    print(regex_rule)
#    return regex_rule
##            
##    print(regex_string_table)
#    
#    
#regex_derived_format_of_tabular_data(main_mem, 86)
#
#def check_for_groups(sal):
#    groups = []
#    group = []
#    i = 0 #need to start comparison to previous from the 2nd index 
#    while i < len(sal):
#      print(len(sal))
#      print(sal[i])
#      if (sal[i] == r'[A-Za-z]') or (sal[i] == r'[0-9]'):
#        group.append(sal[i])
#        i+=1
#        in_group = True
#        while in_group:
##          print(sal[i])
#          try:
#            if sal[i] == sal[i-1]:
#              group.append(sal[i])
#              i+=1
#            else:
#              in_group = False
#              groups.append(group)
#              group = [] #reset 
#          except IndexError:
#            i +=300
#            in_group = False
#      else:
#        print('made it here')
#        groups.append(sal[i])
#        i+=1
#    
#    return groups
#  
#print(check_for_groups([r'[0-9]',r'[0-9]', r'\\.']))  
#    
#def setup_for_regex_analysis(csv, headers_length):
#    list_for_analysis = []
#    new_list_length = 0
#    idx=0
#    while (new_list_length < 10) and (idx < len(csv)):
#        is_na = False
#        if len(csv[idx]) == headers_length:
#          cell_idx = 0
#          while cell_idx < headers_length:
##            print(cell_idx)
#            
#            print(csv[idx][cell_idx])
#            x=re.search(r'n/a', csv[idx][cell_idx].lower())
#            print(x)
#            if x==None:
#              #need to skip this entry and move to next one 
#              pass
#            elif x!=None and is_na == False:   
#              is_na = True
#              print('is_na')
#            
#            cell_idx +=1
#            
#        if is_na == False:
#          list_for_analysis.append(csv[idx])
#          print(csv[idx])
#          new_list_length +=1
#              
#            
#        idx+=1
#    
#    idx_horiz = 0
#    idx_vert = 0
#    while idx_horiz < headers_length:
#      exp_inconsist = r"&.A-Za-z0-9'"
#      this_column = 0
#      for row in list_for_analysis:
#        print(row[idx_horiz])
#        #======================================================Unsure if this effectively handles periods in emails================#
#        if (row[idx_horiz] != '') or (row[idx_horiz] != N) or (row[idx_horiz].lower() != 'n/a')
#          this_column += len(re.findall(r'[^%s]' % exp_inconsist, row[idx_horiz]))
#        #======================================================Unsure if this effectively handles periods in emails================#
#      x = this_column % len(list_for_analysis)
#      if x != 0:
#        print('inconsistency found', idx_horiz, idx_vert, 'number=', x)
#        for row in list_for_analysis:
#          for char in row[idx_horiz]:
#            if re.match('\W', char):
#              del char
#      idx_horiz +=1
#        
#      default_non_words = len([i for i in list_for_analysis[idx_vert][idx_horiz] if re.search('\W', i)])
#      
#      print(default_non_words)
#      while idx_vert < len(list_for_analysis):
#        if 
#    
#    print('List for Analysis')
#    for i in list_for_analysis:
#      print(i)
##    
#    
#    return list_for_analysis
#
#l=setup_for_regex_analysis(main_mem, len(headers))
#
#def regex_of_this_line(line):
#    return [regex_pattern_read(string) for string in line]
#    
#    
#def regex_pattern_read(string): 
#    regex_pattern_read = []
#    last_outcome = ''
#    
#    for char in string:
# 
#        if re.search(r'[A-Za-z]', char):
#            #letter 
##            print('shiit')
#            regex_pattern_read.append(r'[A-Za-z]')
#            
#            #need to be flexible in how many characters it looks for ; ie. finding 5 letters doesn't mean all will necessary have 5 letters, could be 2-10 letters in a row for example 
#        elif re.search(r'[0-9]', char):
#            #digit 
#            regex_pattern_read.append(r'[0-9]')
#        
#        elif re.search('\s', char):
#            #whitespace
#            regex_pattern_read.append(r'\s')
#            
#        elif re.search(re.escape("^\/|`~!@#$%&*()-_+={}[]<>?\"';:"), char):
#            #return this exact special character
#            
#            regex_pattern_read.append(re.escape(char))
#            
#        else:
#            regex_pattern_read.append(re.escape(char))
#            #likely encode error 
#                #return this exact char     
#        
#        
##        """
##        Next: find how many in a row for numbers and letters ->NextNext : factor in a confidence interval for length
##        
##        
##        """
#        
#    return regex_pattern_read
#
#print(regex_pattern_read('word 48 #$%^&*() '))
#
#print(re.match(r'[A-Za-z][A-Za-z][A-Za-z][A-Za-z]', 'Word'))
#
#
#
#
#
#
#
#
##        
##    regex_encoded_format = [regex_pattern_read(string) for string in line[1]]
##    for line in main_mem:
##        if len(line) != len(headers):
##            idx = 0
##            while idx < len(headers):
##                rpr = regex_pattern_read(line[idx])
##                try:
##                    assert rpr == regex_encoded_format[idx]
##                    idx+=1
##                    
##                except AssertionError:
##                    found = False
##                    sub_idx = idx 
##                    while ((found==False) and (sub_idx < len(line))):
##                        try:
##                            assert regex_encoded_format[idx] == line[sub_idx]
###                                    error_cells_len = sub_idx - idx
##                            del line[idx:sub_idx] #deletes from idx up to but not including sub_idx
##                            found = True
##                        except AssertionError:
##                            sub_idx +=1
##                
##                idx+=1
##            
##            
##            num_line_errors = len(line)-len(headers) ?
##                    #fixing algorithm
##                    
##                    #check for regex pattern of ID's  -> if false -> check rest of line for 
#   
#
#
#
