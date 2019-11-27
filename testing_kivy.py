  #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 27 10:59:36 2019

@author: galensprout
"""

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.dropdown import DropDown
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty
from kivy.factory import Factory 
import os
import sys
#kivy.require("1.10.1")
from process_csv_from_hubview import *



class startPage(GridLayout):
  def __init__(self, **kwargs):
    super().__init__(**kwargs) #get kwargs from kivyApp()
    self.industries = [
          'Consulting',
          'Financial Services',  
          'Banking', 
          'Accounting',
          'Insurance',
          'Legal',
          'Recruiting',
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
          'Electronics',
          'Software',
          'Technology',
          'Telecommunications',
          'IT',
          'Education',
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
    
    self.industries_chosen = []
    self.postals_chosen = []
    self.rep_name = ''
    self.path_to_database = ''
    #data ^^^^^^^^^^^^^^^
    #==============================================================#
    
    
    
    self.cols = 2
    
    self.logo = Image(source='/home/galensprout/Pictures/hubTGI-weblogo.png')
    self.add_widget(self.logo)
    
    self.title = Label(text='Hub Lead Gen System')
    self.add_widget(self.title)
    
    self.add_widget(Label(text='Who is you??'))
    self.name_input = TextInput()
    self.add_widget(self.name_input)
    
    self.choose_newleads = Button(text='Generate New Leads')
    self.choose_newleads.bind(on_press=self.new_leads_form)
    self.add_widget(self.choose_newleads)
    
    self.choose_updatecsv = Button(text='Update Existing Contacts/Leads')
    self.choose_updatecsv.bind(on_press=self.update_csv_form)
    self.add_widget(self.choose_updatecsv)
    
  def get_whose_postal(self, rep_name): #for a change - dont forget to change in get_deets() 
    whose_postal = [
      ["Tony", 'x13', ['M6P' , 'M6', 'M8','M8W', 'M8Y', 'M8Z', 'L4V', 'L4W', 'L4X','L4Y', 'L5A', 'L5B', 'L5E', 'L5G', 'L5P', 'M9C']],
      ["Sierra",'x11', ['L5C', 'L5H', 'L6H', 'L5J', 'L5K', 'L5L', 'L5M', 'L6J', 'L6K', 'L6L', 'L6M']], 
      ["Karen",'x14', ['L0J', 'L4H', 'L5N', 'L5R', 'L5V', 'L5W', 'L6P', 'L6R', 'L6S', 'L6V', 'L6W', 'L6X', 'L6Y', 'L6Z', 'L7A']],
      ["Galen", 'x17',['L4T', 'L4Z', 'L5S', 'L5T', 'L6T']],
      ["Brandon", 'x18',['M6L','M6M', 'M6N', 'M2H', 'M8X', 'M2J', 'M9A', 'M9B', 'M9N', 'M9P', 'M9R', 'M2K', 'M2M', 'M2N', 'M2R', 'M3H', 'M3J']],
      ["Daniel", 'x20', ['L4K' 'L4L', 'M3K', 'M3L', 'M3M', 'M3N', 'M9L', 'M9M', 'M9V', 'M9W']]
    ]
    
    p='None'
    print(p)
    for terr in whose_postal:
      if terr[0].lower() == rep_name.lower():
        p=terr
    print(p)
    return p


  def new_leads_form(self, instance):
    self.rep_name = self.name_input.text
    
    #add industry dropdown
    self.add_widget(Label(text='Select Industries'))
    self.industry_dropdown = DropDown()
    for i in self.industries:
      btn = Button(text='%s' % i, size_hint_y=None, height=44)
      btn.bind(on_release=lambda btn: self.industry_dropdown.select(btn.text)) #may not need - may only retain one value
      btn.bind(on_release=lambda btn: self.industries_chosen.append(btn.text))       # self.industries_chosen.append(btn.text))
      self.industry_dropdown.add_widget(btn)
      
    self.add_widget(self.industry_dropdown)
    
    self.ind_button = Button(text='Industries...')
    self.ind_button.bind(on_release=self.industry_dropdown.open)
    
    self.add_widget(self.ind_button)
    
    
    #add postal dropdown 
    self.add_widget(Label(text='For which Postal Codes'))
    self.postal_dropdown = DropDown()
    for i in self.get_whose_postal(self.rep_name)[2]:
      bttn = Button(text='%s' % i, size_hint_y=None, height=44)
      bttn.bind(on_release=lambda bttn: self.postal_dropdown.select(bttn.text)) #may not need - may only retain one value
      bttn.bind(on_release=lambda bttn: self.postals_chosen.append(bttn.text))
      self.postal_dropdown.add_widget(bttn)
      
    self.add_widget(self.postal_dropdown)
    
    self.postal_button = Button(text='Your Postal Codes...')
    self.postal_button.bind(on_release=self.postal_dropdown.open)
    
    self.add_widget(self.postal_button)
    
    
    self.add_widget(Label(text='Check this box once you have confirmed that in your documents folder there is a folder called "Lead_GEN" with your Siebel, Xpert and Hubview accounts as well as Major Reps Accounts all as individual .csv files'))     
  
    self.confirm_dir_struct = CheckBox()
    self.confirm_dir_struct.bind(active=self.validate_dir)

    
    #linkedin
    self.add_widget(Label(text='Include Linkedin Search?'))
    self.linkedin_opt = CheckBox()
    self.linkedin_opt.bind(active=self.get_linkedin_info)
    self.add_widget(self.linkedin_opt)
    
    self.add_widget(Label(text='Due to LinkedIn policies, this will use up all available searches for the day. \n You will also need to return at a later date to this app if you plan on getting more than 100 leads today \n (again due to LinkedIn policies...lame I know)'))
    self.add_widget(Label(text='Do not click the above box if this is not ok'))

    self.submit_button = Button(text='Submit')
    self.submit_button.bind(on_release=self.submit_newleads)
    
  
  def update_csv_form(self, instance):
    self.add_widget(Label(text='What is the name of the file you wish to update? \n\n Make sure the file is in your documents folder'))
    self.csv_input = TextInput()
    
    self.add_widget(Label(text='Run Google Update? \n\n gets basic contact info'))
    self.do_google = CheckBox()
    self.add_widget(self.do_google)
    
    self.add_widget(Label(text='Run Linkedin Update? \n\n gets up to five contacts per company'))
    self.linkedin_opt = CheckBox()
    self.linkedin_opt.bind(active=self.get_linkedin_info)
    
    self.submit_button.bind(on_release=self.submit_update_csv)

  def submit_update_csv(self, instance):    
    #check form conditions and build main()
    
    main_script('')
    pass
  
  def submit_newleads(self, instance):
    
    pass
  
  def get_linkedin_info(self, instance):
    self.add_widget(Label(text='Enter Your Linkedin Email'))
    self.linkedin_username = TextInput()
    self.add_widget(self.linkedin_username)
    
    self.add_widget(Label(text='Enter Your LinkedIn Password \n (this is not saved and will never leave your computer, dontchu worry)'))
    self.linkedin_password = TextInput()
    self.add_widget(self.linkedin_password)
    

  def validate_dir(self, instance, active):
    if self.confirm_dir_struct.active:
      try:
        if sys.platform == 'windows':
          directory = os.path.expanduser('~\Lead_GEN')[:len('~\Lead_GEN')] + r'\Documents\Lead_GEN'
        elif sys.platform == 'linux':  
          directory = os.path.expanduser('~/Lead_GEN')[:len('~/Lead_GEN')] + '/Documents/Lead_GEN'
        
        if os.path.exists(directory):
          self.path_to_database = directory
        else:
          raise(IOError)
          
      except IOError:
        p = Popup(title='Folder was not found', text="Make sure you have a folder named 'Lead_GEN' otherwise you'll duplicate accounts")

        p.open()
        self.confirm_dir_struct.active=False
        close = Button(text='close')
        close.bind(on_release=p.dismiss())
        
  def main_script():
    pass
  
  def subfunctions():
    pass

        
    
  
  
class kivyApp(App):  
  def build(self):
    return startPage()
    


if __name__ == "__main__":
    kivyApp().run()
    



#class LoadDialog(FloatLayout):
#    load = ObjectProperty(None)
#    cancel = ObjectProperty(None)
#
#
#class SaveDialog(FloatLayout):
#    save = ObjectProperty(None)
#    text_input = ObjectProperty(None)
#    cancel = ObjectProperty(None)
#    
#    
#class file_popup(FloatLayout):
#  loadfile = ObjectProperty(None)
#  savefile = ObjectProperty(None)
#  text_input = ObjectProperty(None)
#
#  def dismiss_popup(self):
#      self._popup.dismiss()
#
#  def show_load(self):
#      content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
#      self._popup = Popup(title="Load file", content=content,
#                          size_hint=(0.9, 0.9))
#      self._popup.open()
#
#  def show_save(self):
#      content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
#      self._popup = Popup(title="Save file", content=content,
#                          size_hint=(0.9, 0.9))
#      self._popup.open()
#
#  def load(self, path, filename):
#      with open(os.path.join(path, filename[0])) as stream:
#          self.text_input.text = stream.read()
#
#      self.dismiss_popup()
#
#  def save(self, path, filename):
#      with open(os.path.join(path, filename), 'w') as stream:
#          stream.write(self.text_input.text)
#
#      self.dismiss_popup()