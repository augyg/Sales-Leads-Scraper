#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 05:50:04 2019

@author: gsprout






Notes

Xerox 


Hub 
    Major
        XTI
        CTI
    Commercial
        XTI : starts with 5
        CTI : starts with 7
        
        
        commercial always start with 5 or 7
        major starts with 8 
        
Major really just needs a contact

ID number is important for CRM matching         

"""


import csv
import re
        
def write_to_file(master_list_this_run, prospects_file):
    with open(prospects_file, mode='a') as prospects_file:
        csv_writer = csv.writer(prospects_file, delimiter=',', lineterminator='\n')
        for i in master_list_this_run:
            csv_writer.writerow([s.decode("utf-8") for s in i]) #needs to be fixed

    prospects_file.close()







main_mem = []
with open('/home/galensprout/Documents/Hub_West_CTI_XPERT_List.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        line[4] = re.sub(r"(unit|suite)", '#', line[4])
        line[4] = re.sub(r"[^a-zA-Z0-9]", '', line[4])
        line[8] = line[8][0:3] + ' ' + line[8][3:]
        line[9] = '(' + line[9][0:3] + ') ' +  line[9][3:6] + '-' + line[9][6:]   #(519)498-4976
#        print(line)
        main_mem.append(line)
    
    csvfile.close()
        
        
print(main_mem[3])
    
headers_main = main_mem[0]
main_mem = main_mem[1:]

cross_ref_mem = []
with open('/home/galensprout/Documents/prospects_westsmallslice_two.csv', 'r', newline='\n') as csvfile:
    reader = csv.reader(csvfile)
    for line in reader:
        #following assumes b'string '  problem is solved
#        if "b'" or 'b"' in line[0]:
#            for string in line:
#                string = string[2:-1]
#        else: 
#            print("Do you need this code block anymore?")
        if line[0][:1] == "b'" and True:
            pass                                    #figure out what you were doing here
        if '+' in line[7]:
            line[7] = re.sub(r"\+", "", line[7])
        
        cross_ref_mem.append(line)
    
    csvfile.close()

print(cross_ref_mem[3])



#=========================================================================================================================#

format_list = [name, ]

with open('/home/galensprout/Documents/constant_contacts.csv', 'r', newline='\n') as csvfile:
    reader=csv.reader(csvfile)
    for line in reader:
        if line[1] != '':
            line [0] = line[0] + line[1]
        del line[1]
    















#=========================================================================================================================#


may not need later - figure out how to avoid this for incoming data
cross_cleaned = []
for row in cross_ref_mem:
    new_row = []
    for string in row:
        x = string[2:-1]
        new_row.append(x)
    cross_cleaned.append(new_row)
    
del cross_ref_mem
print(cross_cleaned)


headers_cross_cleaned = ['industry', 'name', 'territory designation', 'rep name', 'postal code', 'address', 'website', 'phone', 'contact1', 'contact2', 'contact3', 'contact4', 'contact5']


def primary_check_with_name(main_mem, new_mem):
    i=0
    j=0
    results = []
    while i < len(new_mem):
        while j < len(main_mem):
            """ 
            
            regex parse 
            
            """
            if new_mem[i][1] == main_mem[j][4]:
                results.append(new_mem[i], main_mem[j])
            j +=1
        i +=1
    return results

def piecewise_check(main_mem, new_mem): #may define regex checker -> returns %match
    #break up into pieces: words and symbols 
        #determine if noun is pronoun or common word
            #check if each word is in the other list > string
    i=0
    j=0
    results = []
    #architected in this manner to deal with continually incoming data into established database
    while i < len(new_mem):
        while j < len(main_mem):
            """ 
            
            regex parse 
            
            """
            word_i_sep = new_mem[i][1].lower().split(' ')
            name_j = main_mem[j][4].lower()
            
            num_words_i = len(word_i_sep)
            num_matches = 0
            for word in word_i_sep:
                if word in name_j:
                    num_matches +=1 
                    
                    
                if num_matches == num_words_i:
                    #then there was a random ass reason it didn't match yet
                elif num_matches > 0: #Partial find
                    name_match = num_matches/num_words_i
                    phone_match = False
                    postal_match = False
                    address_match
                    
                    #enforce proper formatting
                        #check if postal is same
                        
                             #check for postal code first
                        #check if address is same
                            #street -> building number -> unit 
                        #check if phone is AVAILABLE TO CHECK then if same
                        
                else:
                    continue
                
                        #is common?
                            #match + small
                        #is non-common
                            #match + large
            
            #need to deal with & and 'and'
            
            
            if cross_cleaned[i][1] == main_mem[j][4]:
                results.append(cross_cleaned[i], main_mem[j])
            j +=1
        i +=1
    return results
    



if __name__ == "__main__":
#    for row in incoming_file:
    pass
#        parse_compare(row)
        
    """ consider doing all 3 search types while match != found then going to next index """
    
    indeterminant = []
    print(indeterminant)
    


"""
DO 3 Hierarchical searches 

1. Full string
2. For word in string -> is string there? -> how many out of total? -> score 
    Based on Score: (score > x_min)
        check other fields to see if they match
            can do so with:
                !!!after checking that there is a value != NF
                Postal Code
                Phone
                Address - parsed with regex patterns; unit numbers
                
3. Regex search ?
Else: this is a newly found account that must not be in database


"""