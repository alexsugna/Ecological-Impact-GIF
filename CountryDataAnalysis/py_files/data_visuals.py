"""
This file contains functions for creating visuals with CountryDataAnalysis data.

Alex Angus

May 10, 2019
"""
#**********BUG*************#
import matplotlib
matplotlib.use('TkAgg')
#**********FIX*************#

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

fig = plt.figure(figsize=(8, 8))
m = Basemap(projection='lcc', resolution='h', 
            lat_0=37.5, lon_0=-119,
            width=1E6, height=1.2E6)
m.shadedrelief()
m.drawcoastlines(color='gray')
m.drawcountries(color='gray')
m.drawstates(color='gray')

plt.show()