import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import sys
import fiona.crs
import numpy as np
from random import random
# For spreadsheets
import xlrd
# For making plot and legend align
from mpl_toolkits.axes_grid1 import make_axes_locatable
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

countriesWithNonCompatibleNames = [
    "Bahamas, The",
    "Bosnia and Herzegovina",
    "Brunei Darussalam",
    "Central African Republic",
    "Congo, Dem. Rep.",
    "Congo, Rep.",
    "Czech Republic",
    "Cote d'Ivoire",
    "N. Cyprus",
    "Dominican Republic",
    "Egypt, Arab Rep.",
    "Equatorial Guinea",
    "Gambia, The",
    "Iran, Islamic Rep.",
    "Korea, Rep.",
    "Korea, Dem. People’s Rep.",
    "Kyrgyz Republic",
    "Russian Federation",
    "South Sudan",
    "Slovak Republic",
    "Solomon Islands",
    "Syrian Arab Republic",
    "Venezuela, RB",
    "Yemen, Rep."
]

def changeCountryNames(countries):
    for i in range(len(countries)):
        if countries[i] in countriesWithNonCompatibleNames:
            countries[i] = getNewCountryName(countries[i])
    
def getNewCountryName(country): # TODO: Make this into a dictionary
    if country == "Bahamas, The":
        return "Bahamas"
    elif country == "Bosnia and Herzegovina":
        return "Bosnia and Herz."
    elif country == "Brunei Darussalam":
        return "Brunei"
    elif country == "Central African Republic":
        return "Central African Rep."
    elif country == "Congo, Rep.":
        return "Congo"
    elif country == "N. Cyprus":
        return "Cyprus"
    elif country == "Czech Republic":
        return "Czech Rep."
    elif country == "Cote d'Ivoire":
        return "Côte d'Ivoire"
    elif country == "Congo, Dem. Rep.":
        return "Dem. Rep. Congo"
    elif country == "Korea, Dem. People’s Rep.":
        return "Dem. Rep. Korea"
    elif country == "Dominican Republic":
        return "Dominican Rep."
    elif country == "Egypt, Arab Rep.":
        return "Egypt"
    elif country == "Equatorial Guinea":
        return "Eq. Guinea"
    elif country == "Gambia, The":
        return "Gambia"
    elif country == "Iran, Islamic Rep.":
        return "Iran"
    elif country == "Korea, Rep.":
        return "Korea"
    elif country == "Kyrgyz Republic":
        return "Kyrgyzstan"
    elif country == "Russian Federation":
        return "Russia"
    elif country == "South Sudan":
        return "S. Sudan"
    elif country == "Slovak Republic":
        return "Slovakia"
    elif country == "Solomon Islands":
        return "Solomon Is."
    elif country == "Syrian Arab Republic":
        return "Syria"
    elif country == "Venezuela, RB":
        return "Venezuela"
    elif country == "Yemen, Rep.":
        return "Yemen"
    
# countriesToIgnore = [
# Falkland Is.
# Fr. S. Antarctic Lands
# Macedonia
# N. Cyprus
# Palestine
# Somaliland
# Swaziland
# Taiwan
# ]

# Initialize our data
# World is Pandas datasheet
world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
world = world[(world.pop_est>0)&(world.name!="Antarctica")]

# List of country names in 'world', alphabetized
countryNames = world["name"].tolist()
countryNamesCopy = []
for i in range(len(countryNames)):
    countryNamesCopy.append(countryNames[i])
countryNamesCopy.sort()
# countryData is our xls sheet
countrtDataWorkBook = xlrd.open_workbook("data/countryData.xls")
countryData = countrtDataWorkBook.sheet_by_index(0)

# get rows of our data
rows = countryData.get_rows()

# get headers of columns and number of columns as parameters
colHeaders = countryData.row_values(0)
numCols = len(colHeaders)

# our useful column indexes
countryColIndex = 1
indicatorColIndex = 2



def getYearColumn(year):
    year = str(year)
    assert year in colHeaders, "No data for this year!"
    for col in range(numCols):
        if colHeaders[col] == year:
            return col

def buildIndicatorColName(indicator, year):
    return indicator + "_" + str(year)

# Orders data in list1data to align with that of list2 to fix order
# of countries
def fixListOrder(list1, list1data, list2, badNames):
    assert len(list1) == len(list2)
    
    for i in range(len(list1)):
        print(list1[i])
        print(list1data[i])
            
            
            
    goodCountries = []
    badCountriesAdded = 0
    goodCountriesAdded = 0
    list1good = []

    for i in range(len(list1)):
        if list1[i] == None:
            list1good.append(badNames[badCountriesAdded])
            badCountriesAdded += 1
        else:
            goodCountries.append(list1[i])
            list1good.append(goodCountries[goodCountriesAdded])
            goodCountriesAdded += 1
    dict1 = dict(zip(list1good, list1data))
    
    list2data = [None]*len(list2)
    for i in range(len(list2)):
        country = list2[i]
        list2data[i] = dict1[country]
    return list2data

def getCountriesWithIndicator(indicator, yearColumn):
    # initialize lists of countries we find with this indicator
    # as well as their data
    commonCountriesWithIndicator = []
    indicatorData = []
    i = 0
    for row in rows:
        # if country has our desired indicator
        if indicator in countryData.cell_value(i, indicatorColIndex):
            # get the country
            country = countryData.cell_value(i, countryColIndex)
            # change country name if not compatible with world
            if country in countriesWithNonCompatibleNames:
                country = getNewCountryName(country)
            # if the country is in World
            if country in countryNamesCopy:
                # add to our list of countries with indicator
                commonCountriesWithIndicator.append(country)
                # add data for desired indiicator and year
                indicatorData.append(countryData.cell_value(i, yearColumn))
        i += 1
    return (commonCountriesWithIndicator, indicatorData)

def buildSeries(indicator, year, commonCountriesWithIndicator, indicatorData):
    # initialize lists to add to 'world'
    countriesToAddToWorld = []
    indicatorDataToAddToWorld = []
    countriesFound = 0
    
    countriesToIgnore = []
    # For each country in World
    for country in range(len(countryNamesCopy)):
        # If we haven't found the country to have the indicator
        if countryNamesCopy[country] not in commonCountriesWithIndicator:
            countriesToAddToWorld.append(None)
            indicatorDataToAddToWorld.append(None)
            countriesToIgnore.append(countryNamesCopy[country])
        else:
            countriesToAddToWorld.append(countryNamesCopy[country])
            indicatorDataToAddToWorld.append(indicatorData[countriesFound])
            countriesFound += 1
            
    sortedIndicatorDataToAddToWorld = fixListOrder(countriesToAddToWorld,
                                                   indicatorDataToAddToWorld,
                                                   countryNames,
                                                   countriesToIgnore)
    series = [None]
    for i in range(len(sortedIndicatorDataToAddToWorld)-1):
        series.append(sortedIndicatorDataToAddToWorld[i])
    
    for i in range(len(indicatorDataToAddToWorld)):
        print(countriesToAddToWorld[i])
        print(series[i])
    return pd.Series(series)

def printMap(indicator, year):
    
    # Get the column with the data we want based on year
    yearColumn = getYearColumn(year)
    
    # Find every country that has our shit
    countriesTuple = getCountriesWithIndicator(indicator, yearColumn)
    commonCountriesWithIndicator = countriesTuple[0]
    commonCountriesWithIndicator.sort()
    indicatorData = countriesTuple[1]

        
    # Make column name for our new series
    colName = buildIndicatorColName(indicator, year)
    
    series = buildSeries(indicator, year, commonCountriesWithIndicator, indicatorData)
    world[colName] = series
    
#     plot grey so nans aren't white
    ax = world.plot(color="grey")
    world.dropna().plot(ax=ax, column=colName)
    plt.show()
printMap("Land area (sq. km)", 1975)