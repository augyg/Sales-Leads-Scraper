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
    while search_term_index < len(search_terms) and sizeof_list < 3500:
#    for term in search_terms:    
        search_bar = driver.find_element_by_xpath("//input[@title='Search']")
        update_search_bar(search_bar, search_terms[search_term_index])
        current_industry = search_terms[search_term_index][6:] #grabs the piece after postal and spaces
        test_counter = 0
        condition = True
            
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
                deets.append(current_industry)
                
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
    updated_master = []
    for company in master_list_this_run:
        company = search_contacts_for_company(company)
        updated_master.append(company)
        
    return updated_master
        
        

        
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
    """
    
    future:
        find list of important titles by industry
    
    
    
    """
    
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




if __name__ == "__main__":
    main_mem = [] #to save with at the end 
    with open('/home/galensprout/Documents/Accounts.csv') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
  
            main_mem.append(line)
                 
        csvfile.close()
    
    headers = main_mem[0]
    main_mem = main_mem[1:]
    i=0
    for line in main_mem:
      i+=1
      if len(line) != 86:
        print(i)
        
    
    
    
    
    
    names = []
    for i in main_mem:
        names.append(['useless placeholder string', i[0]])
    print(names)
    
    opts = Options()
    opts.add_argument("--user-data-dir=/home/galensprout/.config/google-chrome")
    driver = webdriver.Chrome('/usr/bin/chromedriver', options=opts)
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
    new_list = add_linkedin_contacts(names)
    index =0
    while index < len(main_mem)-1:
        main_mem[i] = main_mem[i] + names[i][-5:]
        print(main_mem[-10:])
        index+=1
        
        
    
    
    
        #linkedin do 
        
        
    
    
    if len(names) != len(main_mem) != len(new_list):
        raise("Error, you're lists are not the same length, you need to fix something")
    else:
        write_to_file(new_list, 'test_file.csv')
            #if trying to write to same file then throw error
        


"""


ALL OF THE BELOW IS TO DETERMINE THE FORMATTING RULES FOR THE TABLE

could also write rule to remove spaces in the string(s) being checked if the regex pattern fails
"""




def regex_derived_format_of_tabular_data(csv, headers_length):
    #returns a row with n columns of [Regex Cell > regex_group1, regex group2...]
    regex_rule = []
    list_for_analysis = setup_for_regex_analysis(csv, headers_length)
    regex_string_table = [regex_of_this_line(line) for line in list_for_analysis]
    null_regex_rule = regex_string_table[0]
    #======================================================================================================================#
    idx_vert = 0
    idx_horiz = 0
    while idx_horiz < headers_length:
      first = check_for_groups(regex_string_table[0][idx_horiz]) #list 
      first_groups = [i for i in first if isinstance(i, list)] 
      num_groups = len(first)
      #tries to invalidate and peel back for n in sample
      #check each column for validity 
      for row in regex_string_table:
        
        
        
        
        
        
        
        
        item_to_compare = check_for_groups(row[idx_horiz]) 
        item_as_groups = [i for i in item_to_compare if isinstance(i, list)]
        
        is_same_length = sum([len(i) for i in item_as_groups]) - sum([len(i) for i in first_groups]) #if same length this equals 0
        
        if len(item_as_groups) != len(first_groups) and is_same_length == 0:
          #then another character type caused inconsistency which lead to another group
            #most likely to happen with postal codes eg M9B 0C3 vs M9B0C3
            
            
            #best solution is to check the rest of the rows and take the most common format
            favor_first = 0
            favor_this = 0 
            for row in regex_string_table:
              if len(row[idx_horiz]) == len(first):
                favor_first +=1
              elif len(row[idx_horiz]) == len([i for i in row[idx_horiz] if isinstance(i, list)):
                favor_this +=1
            
            #find the differential cause 
            temp_idx = 0
            if favor_first > favor_this:
              if len(first_groups) > len(item_as_groups):
                #then we want to break apart item into structure of the first group
                  #note: in this case we would also need to add in '\W' for non alphanumeric 
                while temp_idx < len(first_groups):
                  try:
                    
                    #try to break apart with the len of the index from "first" so that the current and next indices line up length is the same 
                    pass
                  
                  except AssertionError:
                    pass
                  
                  temp_idx +=1
              else:
                
                
            
            else: #favor this 
            
            
            
                
                
             
                              
#======================================================================================================================#         
        
        
          #at this point, the rest of the algorithm must be dealing with an equal number of groups        
        
        
        
#======================================================================================================================#
#        if len(row[idx_horiz]) == len(regex_string_table[0][idx_horiz]): #compares two lists of characters that are formatted as lists 
        group_idx = 0
        while group_idx < num_groups:
          for i in item_to_compare:
            if isinstance(item_to_compare[group_idx], list):
              do 
              then increment group idx
            else: #is string and must be special character or space 
              pass 
          
          
          if_update_group = [] 
          
          #change will happen per group -> Maximize discrimination on format
            #effectively looping through each possible invalidation and if invalidation found on this idx then peel back the current regex string for this group 
            
            #3 conditions on groups:
              #1: regex is starting string 
                ## return starting string or updated to any case
              #2: regex has been updated but not necessarily finished 
                # -> has '\w' but not {0,10} 
                  #return current iteration or '\w' with {0,X}
                # -> has {0,X} but is for set([0-9] or [A-Za-z])
              #3: regex wouldn't be updated from this point on ; '\w'{0,10} is the case 
          if ('\w' not in item_to_compare[group_idx]) and ('{' not in item_to_compare[group_idx]):
            
            if len(first[group_idx]) == len(item_to_compare[group_idx]):
              #then check if the discrimination holds
              char_idx = 0
              while char_index < len(first[group_idx]): #len gives the number of characters
                
                if first[group_idx][char_idx] == item_to_compare[group_idx][char_idx]:
                  #nothing needs to be done
                  pass 
                
                else:
                  #then discrimination per character failed on this group
                  """ replace me with method to change char from [0-9], [A-Za-z] to '\w' """
                  string.replace('[A-Za-z]', '\w')
                  string.replace('[0-9]')
                char_idx +=1
              
              #then easily comparable
              if first[group_idx] == item_to_compare[group_idx]:
                #then discrimination worked @ sub index 
                
                
            else: #BUILD CI 
              #CI is not specific to any char or char set but rather all 
                #should reasonably be larger range for '\w'
              #the two groups are not equal length -> need condidence interval 
              #can only check if all the char's in the group are the same as each other and same with reference object
                
              
                #check if length at this index is larger than the previous one found 
                  #if yes, update max 
                
              
                
                to_check = first[group_idx] + item_to_compare[group_idx] #adding lists of lists since groups/words are in list format
                length = 0
                for char in to_check:
                  if char != to_check[0]:
                    #are all the chars the same type?
                    #random between letters and numbers 
                    """replace me with method to change group from list of chars that equal [0-9], [A-Za-z] to '\w' """
                    
                #now we check for proper confidence interval 
                  #goal is to compute max once in this block
                    #get all groups at this group index ; 
                      #find max lengths of all groups at this index 
                      
                
                
                    """ and method for confidence interval  """
                    
                  
                  
          elif ('\w' in item_to_compare[group_idx]) and ('{' not in item_to_compare[group_idx]):
            
          
                
          group_idx += 1
      idx_horiz +=1
            
        
          
          
      
      
      idx_horiz+=1
    
        for string in line:
          #iteration structure:
            #columns from left to right 
              #at that index/column value -> check that each row is equal to row 0 at that index 
          
          
          
          
          
          #check if all the strings are equal length 
            #if true then check for groups being equal length 
              #if equal length: 
                #for each char:
                  #check if each index/char is the same type 
                    #if all are same type 
                      #return a regex pattern that discriminates for these types at these indexes
                    #else ; not the same type at the same index
                      #replace discriminatory chars with \w and return 
                      
              #else (the equal index groups are not equal lengths):
                #check if the group is all the same character 
                  #if yes then return [char type]{CI} where confidence interval is {1, MAX(Sample[Index]) + 2}
                  
          
            #else (the string is not equal length)
              #check for each group's length 
                #if each group is same length
                  #check index for index 
                    #if at each index: types are the same -> return discriminatory string
                    #else (not same at each index) -> replace discr. with '\w' and return
                    
                #else;   each group is not the same length:
                  #check if each char is same type
                  #if (same type):
                    #return [char type]{CI} where confidence interval is {1, MAX(Sample[Index]) + 2}
                  #else ; not the same type in the group 
                    #replace discr. terms with '\w' and return pattern
            
          
          for char in string: #string is actually formatted as a list 
            #get temp char-string of alphanumeric 
              #compare length 
                #compare same index for all strings 
                      #maybe compare string_one[this_index] to other strings[this_index]
                      #if match -> increment match ?
                      
                    #note: [0-9][0-9] is the same as [0-9]+ or [0-9]{0, 2}
                    
                      #because in the case that you have an address, if some numbers are 2 digits and some are 3 -> then the rest of the indexes following that one will be thrown off 
                      #idea : find groups (seperated by non alphanumeric) and determine length +/- CI 
                        #then check if the groups are the same length
                          #so ... if group-words #1 == group-words #2 -> easy solve ; analyze as whole string 
                            #else: analyze as groups 
                              #for group in groups:
                                #is the group the same length as equivalent groups?
                                  #yes -> simple analysis
                                  #no/else ->    it is probably not a uniform-feature object such as an ID # 
                                    #so just check if all chars in the group are the same 
                                    
                                    
                      #return string= group 1 + group 2 + group 3 ...
                        # -> regex_rule_string_complete = group1(+/- CI) + [special char] + group 2(+/- CI) ...
                              #groups value will either be CASE 1: letters and numbers or CASE 2: word chars
                                #example r'[0-9]{0, 5}[A-Za-z]{3,4}' or r'\w{0,7}'
                                
                                
                      #length computation: max of sample - min of sample = range + 2 on both sides
            
            
            
#            print(string_for_compare)
        alphanumeric.append(line)
    #======================================================================================================================#

#    print(regex_rule)
    return regex_rule
#            
#    print(regex_string_table)
    
    
regex_derived_format_of_tabular_data(main_mem, 86)

def check_for_groups(sal):
    groups = []
    group = []
    i = 0 #need to start comparison to previous from the 2nd index 
    while i < len(sal):
      print(len(sal))
      print(sal[i])
      if (sal[i] == r'[A-Za-z]') or (sal[i] == r'[0-9]'):
        group.append(sal[i])
        i+=1
        in_group = True
        while in_group:
#          print(sal[i])
          try:
            if sal[i] == sal[i-1]:
              group.append(sal[i])
              i+=1
            else:
              in_group = False
              groups.append(group)
              group = [] #reset 
          except IndexError:
            i +=300
            in_group = False
      else:
        print('made it here')
        groups.append(sal[i])
        i+=1
    
    return groups
  
print(check_for_groups([r'[0-9]',r'[0-9]', r'\\.']))  
    
def setup_for_regex_analysis(csv, headers_length):
    list_for_analysis = []
    new_list_length = 0
    idx=0
    while (new_list_length < 10) and (idx < len(csv)):
        is_na = False
        if len(csv[idx]) == headers_length:
          cell_idx = 0
          while cell_idx < headers_length:
#            print(cell_idx)
            
            print(csv[idx][cell_idx])
            x=re.search(r'n/a', csv[idx][cell_idx].lower())
            print(x)
            if x==None:
              #need to skip this entry and move to next one 
              pass
            elif x!=None and is_na == False:   
              is_na = True
              print('is_na')
            
            cell_idx +=1
            
        if is_na == False:
          list_for_analysis.append(csv[idx])
          print(csv[idx])
          new_list_length +=1
              
            
        idx+=1
    
    idx_horiz = 0
    idx_vert = 0
    while idx_horiz < headers_length:
      exp_inconsist = r"&.A-Za-z0-9'"
      this_column = 0
      for row in list_for_analysis:
        print(row[idx_horiz])
        #======================================================Unsure if this effectively handles periods in emails================#
        if (row[idx_horiz] != '') or (row[idx_horiz] != N) or (row[idx_horiz].lower() != 'n/a')
          this_column += len(re.findall(r'[^%s]' % exp_inconsist, row[idx_horiz]))
        #======================================================Unsure if this effectively handles periods in emails================#
      x = this_column % len(list_for_analysis)
      if x != 0:
        print('inconsistency found', idx_horiz, idx_vert, 'number=', x)
        for row in list_for_analysis:
          for char in row[idx_horiz]:
            if re.match('\W', char):
              del char
      idx_horiz +=1
        
      default_non_words = len([i for i in list_for_analysis[idx_vert][idx_horiz] if re.search('\W', i)])
      
      print(default_non_words)
      while idx_vert < len(list_for_analysis):
        if 
    
    print('List for Analysis')
    for i in list_for_analysis:
      print(i)
#    
    
    return list_for_analysis

l=setup_for_regex_analysis(main_mem, len(headers))

def regex_of_this_line(line):
    return [regex_pattern_read(string) for string in line]
    
    
def regex_pattern_read(string): 
    regex_pattern_read = []
    last_outcome = ''
    
    for char in string:
 
        if re.search(r'[A-Za-z]', char):
            #letter 
#            print('shiit')
            regex_pattern_read.append(r'[A-Za-z]')
            
            #need to be flexible in how many characters it looks for ; ie. finding 5 letters doesn't mean all will necessary have 5 letters, could be 2-10 letters in a row for example 
        elif re.search(r'[0-9]', char):
            #digit 
            regex_pattern_read.append(r'[0-9]')
        
        elif re.search('\s', char):
            #whitespace
            regex_pattern_read.append(r'\s')
            
        elif re.search(re.escape("^\/|`~!@#$%&*()-_+={}[]<>?\"';:"), char):
            #return this exact special character
            
            regex_pattern_read.append(re.escape(char))
            
        else:
            regex_pattern_read.append(re.escape(char))
            #likely encode error 
                #return this exact char     
        
        
#        """
#        Next: find how many in a row for numbers and letters ->NextNext : factor in a confidence interval for length
#        
#        
#        """
        
    return regex_pattern_read

print(regex_pattern_read('word 48 #$%^&*() '))

print(re.match(r'[A-Za-z][A-Za-z][A-Za-z][A-Za-z]', 'Word'))








#        
#    regex_encoded_format = [regex_pattern_read(string) for string in line[1]]
#    for line in main_mem:
#        if len(line) != len(headers):
#            idx = 0
#            while idx < len(headers):
#                rpr = regex_pattern_read(line[idx])
#                try:
#                    assert rpr == regex_encoded_format[idx]
#                    idx+=1
#                    
#                except AssertionError:
#                    found = False
#                    sub_idx = idx 
#                    while ((found==False) and (sub_idx < len(line))):
#                        try:
#                            assert regex_encoded_format[idx] == line[sub_idx]
##                                    error_cells_len = sub_idx - idx
#                            del line[idx:sub_idx] #deletes from idx up to but not including sub_idx
#                            found = True
#                        except AssertionError:
#                            sub_idx +=1
#                
#                idx+=1
#            
#            
#            num_line_errors = len(line)-len(headers) ?
#                    #fixing algorithm
#                    
#                    #check for regex pattern of ID's  -> if false -> check rest of line for 
   



