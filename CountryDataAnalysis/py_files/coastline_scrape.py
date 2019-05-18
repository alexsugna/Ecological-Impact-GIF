"""
This file contains a program that scrapes the ChartsBin site for coastlines by country.
It writes a dictionary object named 'coasts' to a file named 'coastline_storage'.
'coasts' has country_names as keys and coastline in km as values (floats).
Make sure this file is in the directory where you want the storage file written to.

Alex Angus

May 17, 2019 
"""
from requests_html import HTMLSession
from bs4 import BeautifulSoup
from country_data_functions import objToFile

starting_url = "http://chartsbin.com/view/ofv"

session = HTMLSession()
request = session.get(starting_url)

country_names = request.html.find('.cname')
coastlines = request.html.find('.tvalue')

coasts = {}
first = True
for name, coastline in zip(country_names, coastlines):
    if(first):
        first = False
        continue
    print(name.text, coastline.text)
    coasts.update({name.text : float(coastline.text[:-3].replace(',', ''))})
    
objToFile(coasts, "coastline_storage")
print("Country by coastline dictionary stored to file: coastline_storage")
