"""
This file contains functions that calculate various ecological impact indices
from web scraped data through the Country Data Analysis project. More information
on the indices can be found at alexangus.com/projects/

Alex Angus

May 17, 2019
"""
import numpy as np
from country_data_functions import weightedAverageDifferential

def Vindex(country_name, storage, SV = False, DV = False, gdp_scale = False):
    TV = False
    country = storage.getCountry(country_name)
    if(SV and DV):
        TV = True
    if(SV):
        SV_value = calculateSV(country, storage)
        if(not TV):
            return SV_value
    if(DV and (not TV)):
        DV_value = calculateDV(country, storage)
        if(not TV):
            return DV_value
    if(TV):
        return SV_value + DV_value
        
def sortVV(storage):
    vices, virtues = [], [] #initialize vice and virtue lists
    indicators_list = storage.indicator_weights #important Vindex indicators
    for indicator_key in indicators_list.keys(): #iterate through indicators
        if(indicators[indicator_key][1] < 0): #if it's a vice
            vices.append(indicator_key) #add to vice list
        else: #if it's a virtue
            virtues.append(indicator_key)
    
    return vices, virtues
    
def calculateSV(country, storage):
    weights = storage.indicator_weights
    vices, virtues = sortVV(storage)
    vices_sum_weighed = 0
    virtues_sum_weighed = 0
    for vice in vices:
        vice_weight = weights.get(vice)[0]
        vice_array = np.array(country.indicators.get(vice))
        vice_weighed = vice_array * vice_weight
        vices_sum_weighed += vice_weighed
        
    for virtue in virtues:
        virtue_weight = weights.get(virtue)[0]
        virtue_array = np.array(country.indicators.get(virtue))
        virtue_weighed = virtue_array * virtue_weight
        virtues_sum_weighed += virtue_weighed
        
    return virtue_sum_weighed - vice_sum_weighed 
    
def calculateDV(country, storage):
    weights = storage.indicator_weights
    vices, virtues = sortVV(storage)
    d_vices_sum_weighed = 0
    d_virtues_sum_weighed = 0
    
    for vice in vices:
        vice_weight = weights.get(vice)[0]
        vice_array = np.array(country.indicators.get(vice))
        d_vice_array = weightedAverageDifferential(vice_array)
        d_vice_weighed = d_vice_array * vice_weight
        d_vices_sum_weighed += d_vice_weighed
        
    for virtue in virtues:
        virtue_weight = weights.get(virtue)[0]
        virtue_array = np.array(country.indicators.get(virtue))
        d_virtue_array = weightedAverageDifferential(virtue_array)
        d_virtue_weighed = d_virtue_array * virtue_weight
        d_virtues_sum_weighed += d_virtue_weighed
    
    return d_virtue_sum_weighed - d_vice_sum_weighed


    
    
    
    
    
    
    
            
    
        
    