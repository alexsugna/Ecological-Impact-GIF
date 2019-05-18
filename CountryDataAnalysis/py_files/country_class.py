"""
This program defines the country class for storing data about the worlds countries
and the CountryStorage class for storing the country objects.

22/04/2019

Alex Angus
"""

"""
The Country class can have attributes added to it indefinitely.
"""

class Country: 
    def __init__(self, country_name):
        self.indicators = {}
        self.indicators.update({'Name' : country_name})
        
    def addIndicator(self, indicator_key, value):
        if(indicator_key not in self.indicators.keys()):
            self.indicators.update({indicator_key : value})
    
    def PrintIndicators(self):
        print(self.indicators.keys())
        
    def Print(self):
        print(self.country_name, self.indicators)
    
    def getName(self):
        return self.indicators.get('Name')

"""
The CountryStorage class holds all the country objects and a list of 
string country names.        
"""

class CountryStorage:
    def __init__(self):
        self.country_names = [] #list to store names for checking if an object is in here
        self.countries = [] #list to store country objects
        self.non_country_names = [] #list to store non-country names for checking is an object is in here
        self.non_countries = []
        self.not_countries = ['Arab World', 'East Asia & Pacific', 
                              'Europe & Central Asia', 'High income',
                              'World']
        
        self.file_format = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code', #format of the downloaded excel files
                            '1960', '1961', '1962', '1963', '1964', '1965', '1966', '1967', '1968',
                            '1969', '1970', '1971', '1972', '1973', '1974', '1975', '1976', '1977',
                            '1978', '1979', '1980', '1981', '1982', '1983', '1984', '1985', '1986',
                            '1987', '1988', '1989', '1990', '1991', '1992', '1993', '1994', '1995',
                            '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004',
                            '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013',
                            '2014', '2015', '2016', '2017', '2018']
        
        self.indicator_weights = {'Total greenhouse gas emissions (kt of CO2 equivalent)': [1.0, -1],
                                  'Livestock production index (2004-2006 = 100)' : [0.4, -1],
                                  'PM2.5 air pollution, mean annual exposure (micrograms per cubic meter)' : [0.5, -1],
                                  'Fertilizer consumption (kilograms per hectare of arable land)' : [0.1, -1],
                                  'Total threatened species' : [0.25, -1],
                                  'Alternative and nuclear energy (% of total energy use)' : [1.0, 1],
                                  'Combined forest indicator' : [0.4, 1],
                                  'Protected area indicator' : [0.2, 1]
                                  }
        
        self.keywords = ["greenhouse", "Livestock", "pollution", "Fertilizer", 
                         "species", "Forest", "Alternative"]
        
        self.anti_keywords = ["household"]
        
    def addCountry(self, country_name): #add to the lists
        country = Country(country_name)
        self.country_names.append(country.indicators.get('Name'))
        self.country_names.sort()
        self.countries.append(country)
        self.countries.sort(key = lambda country: country.indicators.get('Name'))
        if(self.country_names[0] != self.countries[0].indicators.get('Name')):
            raise Exception('Country objects and country names are out of order.')
            
    def addNonCountry(self, non_country_name):
        non_country = Country(non_country_name)
        self.non_country_names.append(non_country.indicators.get('Name'))
        self.non_country_names.sort()
        self.non_countries.append(non_country)
        self.non_countries.sort(key = lambda non_country: non_country.indicators.get('Name'))
        if(self.non_country_names[0] != self.non_countries[0].indicators.get('Name')):
            raise Exception('Non-country objects and non-country names are out of order.')
        
    def contains(self, country_name):
        if(country_name in self.country_names):
            return True
        elif(country_name in self.non_country_names):
            return True
        else:
            return False
            
    def getCountry(self, country_name):
        index = self.country_names.index(country_name) #if country_names and countries have same order, this will work.
        return self.countries[index]
    
    def getNonCountry(self, non_country_name):
        index = self.non_country_names.index(non_country_name) #if country_names and countries have same order, this will work.
        return self.non_countries[index]
        
    def Print(self):
        print(self.country_names)
        print(self.non_country_names)

        
        
        
        
        
        
        