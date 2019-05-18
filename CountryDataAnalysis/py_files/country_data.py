"""
This file scrapes The World Bank Website for country data and constructs 
country objects with all the data.
"""
from country_class import CountryStorage
from country_data_functions import downloadExcelFiles, fillStorage, plotIndicator, objToFile, getStorage 
from country_data_functions import playSound, normalizeIndicator, sumThreatenedSpecies#, scrapeLandSea
import matplotlib.pyplot as plt

def main():
    starting_url = 'https://data.worldbank.org/indicator'
    indicators_directory = '/Users/alexangus/Desktop/Projects/CountryDataAnalysis' #where it's all taking place
    max_files = 1000
    WorldBankDownloaded = True
    WorldBankStored = True
    #LandSeaDownloaded = False #this also stores it
    SumThreatenedSpecies = True
    
    if(not WorldBankDownloaded):
        downloadExcelFiles(starting_url, max_files) #get excel files
        print("Excel files downloaded!")
    
    if(not WorldBankStored):
        
        storage = CountryStorage() #storage constructor
        
        fillStorage(indicators_directory, storage.file_format, storage)
        
        objToFile(storage, 'storage_file')

    if(not SumThreatenedSpecies):
        sumThreatenedSpecies(storage)
        objToFile(storage, 'storage_file')
        
    storage = getStorage('storage_file')
    
    #if(not LandSeaDownloaded):
        
        #scrapeLandSea(storage)

        
    print(storage.getCountry('United States').indicators.keys())
        
    
    """
    plotIndicator(storage, 'United States', 
            'General government final consumption expenditure (current US$)')
    
    normalizeIndicator('General government final consumption expenditure (current US$)',
                       storage)
    
    plotIndicator(storage, 'United States', 
            'General government final consumption expenditure (current US$)')
    """
    
    playSound()
    
if __name__ == "__main__":
    main()