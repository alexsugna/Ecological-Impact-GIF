
"""
The function fillStorage fills the CountryStorage object with indicator by 
country data from world bank data.
"""
from country_class import CountryStorage, Country
import os
import pandas as pd


def fillStorage(indicators_directory, file_format, storage):
    for file_name in os.listdir(indicators_directory): #iterate through files in directory
    
        if("country_download" not in file_name): #we only want the ones that we downloaded
            continue
        
        #if there are more than 1 data sheet, do this for each data sheet
        sheets = pd.ExcelFile(file_name).sheet_names
        data_sheet_number = 1
        print('Currently on ' + file_name)
        for sheet in sheets:
            if("Data" in sheet):
                if(data_sheet_number < 2):
                    data_frame = pd.read_excel(file_name, sheet_name = sheet, 
                                               skiprows = [0,1,2]) #read in excel file as pandas dataframe
                    checkFormat(data_frame, file_format, file_name, sheet) #make sure the format is correct
                else:
                    data_frame = pd.read_excel(file_name, sheet_name = sheet)
                print('Now iterating through rows')
                for row in range(0, data_frame.shape[0]): #iterate through rows of file
                    indicator_name = data_frame.iloc[row, 2]
                    if(not doWeWantIt(indicator_name, storage)): #if we don't want the indicator, skip the row
                        continue
                    else:
                        country_name = data_frame.iloc[row, 0]
                        if(not storage.contains(country_name)): #if the country is not already in storage
                            country = Country(country_name)
                            if(countryOrNot(country_name, storage)): #if its a country
                                storage.addCountry(country_name)
                                country_bool = True
                            else: #its a region
                                storage.addNonCountry(country_name)
                                country_bool = False
                        else: #still need to determine whether or not its a country or non country
                            if(country_name in storage.not_countries):
                                country_bool == False
                            else:
                                country_bool == True
                        indicator_name, indicator_data = indicatorByYear(data_frame, row)
                        print(indicator_name)
                        if(country_bool):
                            country_object = storage.getCountry(country.indicators.get('Name'))
                        else:
                            country_object = storage.getNonCountry(country.indicators.get('Name'))
                        print(country_object.getName())
                        country_object.addIndicator(indicator_name, indicator_data)
                data_sheet_number += 1
                
        print("The file " + file_name + " has been formatted into country objects ("
              + str(data_sheet_number - 1) + ")")
    
    print("All files have been formatted into country objects")

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
The function doWeWantIt determines if the given indicator is relevant based on the 
keywords defined in storage   
"""
    
def doWeWantIt(indicator_name, storage):
    for keyword in storage.keywords:
        if(keyword in indicator_name):
            print(indicator_name)
            return True
    return False
            
"""
The function countryOrNot determines if the given country name is a country, or some
other region or group based on the list specified in storage.            
"""

def countryOrNot(country_name, storage):
    for non_country in storage.not_countries:
        if(country_name == non_country):
            return False
    return True
    
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
        
    
storage = CountryStorage()
fillStorage('/Users/alexangus/Desktop/Projects/CountryDataAnalysis', storage.file_format, storage)
storage.getCountry('Zimbabwe').PrintIndicators()
    

    
    
    
    

