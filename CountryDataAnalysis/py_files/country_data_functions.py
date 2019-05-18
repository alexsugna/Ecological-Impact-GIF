"""
This file contains useful functions for the country data analysis project.

Alex Angus

May 5, 2019
"""
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from country_class import Country
import matplotlib.pyplot as plt
import pickle
import simpleaudio as sa
import numpy as np
#from requests_html import HTMLSession

"""
The function downloadExcelFiles downloads worldbank country data. It will download 
max_files number of files to the current directory.
"""

def downloadExcelFiles(starting_url, max_files):
    page = requests.get(starting_url)
    soup_object = BeautifulSoup(page.text, 'html.parser')
    soup_object.find(class_="sidebar").decompose()
    soup_object.find(class_="header").decompose()
    body = soup_object.find(class_ = "overviewArea body")
    ind_types = body.find_all(class_="nav-item")

    indicator_links = []

    for ind_type in ind_types:
        indicators = ind_type.find_all('h3')        
        for indicator in indicators:
            link = indicator.find('a')
            indicator_links.append("https://data.worldbank.org" + link.get('href'))
    i = 0
    for link in indicator_links:
        indicator_page = requests.get(link)
        indicator_soup = BeautifulSoup(indicator_page.text, 'html.parser')
        #print(link)
        downloads = indicator_soup.find(class_="btn-item download").find_all('a')
    
        for download in downloads:
            if("EXCEL" in download):
                csv_link = download.get('href')
        csv_download = requests.get(csv_link, allow_redirects = True)
        open("country_download" + str(i) + ".xls", 'wb').write(csv_download.content)
        
        i += 1
        if(i == max_files):
            break
        
            
"""
The function checkFormat makes sure the excel files are formatted how I think they are.           
"""
def checkFormat(data_frame, file_format, file_name, sheet):
    i = 0
    for col in data_frame.columns:
        if(col != file_format[i]):
            raise Exception(file_name + ", sheet: "+ sheet, "does not fit format")
            continue
        i += 1
        
"""
The function indicatorByYear formats indicator data by year. It returns a dictionary
where the key is the indicator name and the value is a list of data points from 
1960 to 2018 where the index 0 is 1960 and the index 58 is 2018. 
        
data_frame must be in the format that satisfies the function checkFormat
"""
def indicatorByYear(data_frame, row):
    indicator_name = data_frame.iloc[row,2]
    indicator_data = []
    for col in range(4, data_frame.shape[1]):
        indicator_data.append(data_frame.iloc[row,col])
    return indicator_name, indicator_data

"""
The function fillStorage fills the CountryStorage object with indicator by 
country data from world bank data.
"""

def fillStorage(indicators_directory, file_format, storage):
    for file_name in os.listdir(indicators_directory): #iterate through files in directory
    
        if("country_download" not in file_name): #we only want the ones that we downloaded
            continue
        
        #if there are more than 1 data sheet, do this for each data sheet
        sheets = pd.ExcelFile(file_name).sheet_names
        data_sheet_number = 1
        for sheet in sheets:
            if("Data" in sheet):
                if(data_sheet_number < 2):
                    data_frame = pd.read_excel(file_name, sheet_name = sheet, 
                                               skiprows = [0,1,2]) #read in excel file as pandas dataframe
                    checkFormat(data_frame, file_format, file_name, sheet) #make sure the format is correct
                else:
                    data_frame = pd.read_excel(file_name, sheet_name = sheet)
                
                for row in range(0, data_frame.shape[0]): #iterate through rows of file
                    
                    name_of_country = data_frame.iloc[row,0] #get the name of the country
                    #construct country object for that country, if it doesn't exist already in storage, and add to storage
                    if((not storage.contains(name_of_country)) and 
                       (name_of_country not in storage.not_countries)):
                        country_object = Country()
                        setattr(country_object, 'country_name', 
                                name_of_country)
                        storage.addCountry(country_object)
                        country = True
                        
                    elif(name_of_country not in storage.non_countries):
                        country_object = Country()
                        setattr(country_object, 'non_country_name', 
                                name_of_country)
                        storage.addNonCountry(country_object)
                        country = False
                        
                    indicator, indicator_data = indicatorByYear(data_frame, 
                                                                row) #get the indicator/data in the row
                    
                    if(country == True):
                        country_row = storage.getCountry(name_of_country) #retrieve the country object from storage
                    
                    else:
                        country_row = storage.getNonCountry(name_of_country) #retrieve the country object from storage
                        
                    for keyword in storage.keywords:
                        if((keyword in indicator) and (indicator not in country_row.indicators.keys())):
                            country_row.indicators.update({indicator:indicator_data})  #set indicator as attribute with data as value
                        
                data_sheet_number += 1
                
        print("The file " + file_name + " has been formatted into country objects ("
              + str(data_sheet_number - 1) + ")")
    
    print("All files have been formatted into country objects")

"""
The function plotIndicator plots an indicator by year for a given country
and a given indicator.
"""

def plotIndicator(storage, country_name, indicator):
    country = storage.getCountry(country_name) #get country
    indicator_data = country.indicators.get(
            'General government final consumption expenditure (current US$)') #get indicator
    plt.plot(indicator_data) #plot
    plt.title(indicator + ' of ' + country_name)
    plt.xlabel("Years since 1960")
    plt.legend(indicator)
    plt.figure(figsize = (20,20))
    plt.show()
    
"""
The function objToFile writes the storage object into a file so I don't have to 
fill the storage every time I want to do something.

WARNING: This takes a long time. Do it before you go to sleep.
"""

def objToFile(storageObject, filename):
    with open(filename, 'wb') as storage_file:
        pickle.dump(storageObject, storage_file, protocol=pickle.HIGHEST_PROTOCOL)
        print('storage object written to file: ' + filename)

"""
The funciton getStorage reads the storage object from it's file. filename is 
the file that the storage object is in.
"""

def getStorage(filename):
    with open(filename, 'rb') as storage_file:
        print('storage object retrieved from file: ' + filename)
        return pickle.load(storage_file)
    
"""
The function playSound plays a .wav file. Intended to let the user know that 
the program is finished running.
"""
    
def playSound():
    wave_obj = sa.WaveObject.from_wave_file("Crash-Cymbal-1.wav")
    play_obj = wave_obj.play()
    play_obj.wait_done()
    
"""
The function weightedAverageDifferential returns the derivative array of an array
of values. 
    
COMBINE WITH AVERAGE
"""

def weightedAverageDifferential(array):
    return np.mean(yearWeight(np.diff(array), 1/10))
    
"""
The function averageValue returns the unweighted average of an array    
"""
def average(array):
    return np.mean(array)
    
"""
The funciton yearWeight scales an array so that points closer to
the maximum value are worth more. Used to scale differential averages
so that more recent years count for more.

baseline_frac: minimum value of smallest x value as a fraction of maximum
    Ex: baseline_frac = 1/10 causes minimum weight to be 0.1 of max y value
"""
def yearWeight(array, baseline_frac):
    c = array.max() * baseline_frac #baseline value
    return array.max() * np.exp(array - len(array)) + c #weight function
    
"""
The function normalizeIndicator normalizes the specified indicator to 
the global (out of all the countries) maximum value of that indicator type.
The maximum value is set to 1, all other values are between 0 and 1.    
"""
    
def normalizeIndicator(indicator, storage):
    max_value = 0
    for country in storage.countries: #iterate through countries
        indicator_list = country.indicators.get(indicator) #get indicator list
        for value in indicator_list: #iterate through values of list
            if(value >= max_value): #if value is the biggest so far, replace highest
                max_value = value
    
    print(country.country_name + " has the highest " + indicator)
    
    #normalize to max_value
    for country in storage.countries:
        indicator_list = country.indicators.get(indicator)
        normalized_list = []
        for value in indicator_list: #for each value
            normalized_list.append(value/max_value) #normalize the value and append to the normalized list
        country.indicators[indicator] = normalized_list #replace indicator value with normalized list
        
def normalizeAllIndicators(storage):
    first_country_name = storage.country_names[0]
    first_country = storage.getCountry(first_country_name)
    indicator_list = first_country.indicators
    for indicator in indicator_list:
        normalizeIndicator(indicator, storage)
    
    print('All indicators have been normalized')
            
            
"""
The function scrapeLandSea web scrapes the protectedplanet site for information
on protected areas by country. It retrieves country name, percentage of total
land and sea protected, and how effective those areas are managed. It adds these 
values to the storage object.
"""

def scrapeLandSea(storage):
    starting_url = "https://www.protectedplanet.net/c/unep-regions"
               
    session = HTMLSession()
    request = session.get(starting_url)
    links = request.html.links
    trimmed_links = links.copy()
    
    for link in links:
        if("/country/" not in link):
            trimmed_links.remove(link)
    session.close()
    
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
                
        country = storage.getCountry(name) #add it to storage
        setattr(country, 'Protected Land (% of total land area)', protected_area_float)
        setattr(country, 'Protected Sea (% of total sea area)', protected_sea_float)
        setattr(country, 'Protected Land Management Effectiveness (%)', land_effectiveness_float)
        setattr(country, 'Protected Sea Management Effectiveness (%)', sea_effectiveness_float)
    
"""
The function sumThreatenedSpecies finds all indicators with information on
the number of various threatened species. It sums these indicators to yeild a
total  threatened species count. It then adds an attribute called 
'Total threatened species' to each country object.
"""
    
def sumThreatenedSpecies(storage):
    country_names = storage.country_names
    first_country = storage.getCountry(country_names[0])
    threatened_species_indicators = []
    for indicator in first_country.indicators.keys(): #find the threatened species indicators
        if("species" in indicator):
            threatened_species_indicators.append(indicator)
    
    for country_name in country_names:
        country = storage.getCountry(country_name)
        total_threatened_species_count = \
        np.empty(len(country.indicators.get(threatened_species_indicators[0])),
                 dtype = np.float)
        for target_indicator in threatened_species_indicators:
            total_threatened_species_count += np.array(country.indicators.get(target_indicator))

        setattr(country, 'Total threatened species', total_threatened_species_count)
                
        
        
"""
The function calculateForestIndicator calculates the forest indicator described 
in the documentation for a given country.
"""

def calculateForestIndicator(country_name, storage):
    country = storage.getCountry(country_name) #get the country
    normalizeIndicator('Forest area (% of land area)', storage) #normalize the indicators
    normalizeIndicator('Forest area (sq. km)', storage)
    percentForest = np.array(country.indicators.get('Forest area (% of land area)'))
    totalForest = np.array(country.indicators.get('Forest area (sq. km)'))
    
    return 0.5 * percentForest + 0.5 * totalForest
        
"""
The function calculateProtectedAreasIndicator calculates the protected areas 
indicator described in the documentation for a given country.
"""

def calculateProtectedAreasIndicator(country_name, storage):
    country = storage.getCountry(country_name) #get the country
    percent_land = np.array(country.indicators.get('Protected Land (% of total land area)'))
    effective_land = np.array(country.indicators.get('Protected Land Management Effectiveness (%)'))
    percent_sea = np.array(country.indicators.get('Protected Sea (% of total sea area)'))
    effective_sea = np.array(country.indicators.get('Protected Sea (% of total sea area)'))
    total_land = np.array(country.indicators.get('Land area (sq. km)'))
    total_sea = np.array(country.indicators.get('Sea area (sq. km)'))
    real_land = percent_land * effective_land / 100
    real_sea = percent_sea * effective_sea / 100
    real_total = real_land + real_sea
    total_total = total_land + total_sea
    
    return real_total/total_total
    
"""
The function calculateTotalSeaArea calculates the total sea area in km^2 
that the specified country is responsible for.
"""
    
def calculateTotalSeaArea(country_name, storage):
    country = storage.getCountry(country_name, storage)
    coastline = country.indicators.get('Coastline (km)')
    return 22.2 * coastline 


    
    
    
    
    
    
    