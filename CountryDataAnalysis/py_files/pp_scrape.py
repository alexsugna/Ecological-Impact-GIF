"""
This file scrapes the protectedplanet site for information
on protected areas by country.

It writes a dictionary object named 'land_sea_protection' to a file named
'land_sea_storage'. 'land_sea_protection' is a dictionary with the following format:

name : [protected_area_float, land_effectiveness_float,
        protected_sea_float, sea_effectiveness_float]

Make sure this file is in the directory where you want the storage file written to.

Alex Angus

May 15, 2019
"""
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from country_data_functions import objToFile

starting_url = "https://www.protectedplanet.net/c/unep-regions"
           
session = HTMLSession()
request = session.get(starting_url)
links = request.html.links
trimmed_links = links.copy()

for link in links:
    if("/country/" not in link):
        trimmed_links.remove(link)
session.close()

land_sea_data = {}

for page in trimmed_links:
    new_session = HTMLSession()
    new_request = new_session.get('https://www.protectedplanet.net' + page)
    
    
    name_object = new_request.html.find('.hero__title', first = True) #get country name
    name_list = []
    for char in name_object.text: #get rid of the region
        if(char == ','):
            break
        name_list.append(char)
        
    name = ''.join(name_list)
    
    area_object = new_request.html.find('.value__number--xxlarge')
    
    #get protected land area
    protected_area_percentage = area_object[1].text
    protected_area_float = float(protected_area_percentage[:-1])
    
    #get protected sea
    protected_sea_percentage = area_object[2].text
    protected_sea_float = float(protected_sea_percentage[:-1])
    
    #get effectivenesses (is that a word?)
    effectiveness_object = new_request.html.find('.value__number')
    land_effectiveness_float = None
    
    if(protected_area_float != 0.0): #if there's no protected area, then there's no effectiveness
        land_effectiveness_percentage = effectiveness_object[6].text 
        land_effectiveness_float = float(land_effectiveness_percentage[:-1])
    sea_effectiveness_float = None
    
    if(protected_sea_float != 0.0):
        sea_effectiveness_percentage = effectiveness_object[-2].text
        if("km" not in sea_effectiveness_percentage[:-1]):
            sea_effectiveness_float = float(sea_effectiveness_percentage[:-1])
    
    land_sea_data.update({name : [protected_area_float, land_effectiveness_float,
                                  protected_sea_float, sea_effectiveness_float]})
                                  
objToFile(land_sea_data, "land_sea_storage")
print("Land/Sea protection and effectivenesses stored to file: land_sea_storage")

