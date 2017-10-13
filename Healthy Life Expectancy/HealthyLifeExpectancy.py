# coding: utf-8


from databaker.framework import *
import sys

inputfile = sys.argv[1]


# ################
# Common Functions
# ################

# Get the gender from the tab name
def getGender(tab):

    if 'female' in tab.name.lower():
            return 'Female'
    elif 'male' in tab.name.lower():
            return 'Male'
    else:
        ValueError("Cannot identify gender")
    
    

# ########
# Summary
# ########

outputfile = 'V4-HLE Summary of Life and Healthy Expectancy.csv'

# load the tabs that we want
tabs_we_want = ['UTLA males', 'UTLA females']
tabsNational = loadxlstabs(inputfile, tabs_we_want)


conversionsegments = []
for tab in tabsNational:
    
    geo = tab.excel_ref('A10').fill (DOWN).is_not_blank() - tab.excel_ref('A161').expand(DOWN)

    # Select the HLE an LE colimns    
    HorLE = tab.excel_ref('A10').expand(RIGHT).filter(contains_string('LE')) - tab.excel_ref('H10').expand(RIGHT)
    
    gender = getGender(tab)
    
    obs = geo.waffle(HorLE)
        
    # make a dict to override the acronyms in HorLE with something plain english
    lifeLookup = {
        'LE':'Life Expectancy',
        'HLE':'Healthy Life Expectancy',
    }
        
    dimensions = [
        HDim(tab.excel_ref('A4'), TIME, CLOSEST,ABOVE),
        HDim(geo, "Geography", DIRECTLY, LEFT),
        HDimConst("Gender", gender),
        HDim(HorLE, "Life Measure", DIRECTLY, ABOVE, cellvalueoverride=lifeLookup)
            ]
    
    conversionsegment = ConversionSegment(tab, dimensions, obs)
    conversionsegments.append(conversionsegment)
    
writeCSV(outputfile, conversionsegments)
    


# ################################################
# HLE in years & Proportion of Life in good Heakth
# ################################################

"""
These transformations re virtually identicial, the first has obs in column D, the second column G.
Other than that its just the output file name
"""

# differentiate via options
dSetOps = (
        {'name':'V4-HLE Healthy Life Expectancy in years.csv','obsCol':'D'},
        {'name':'V4-HLE Proportion of life spent in good health.csv','obsCol':'G'}
        )
    

for ops in dSetOps:
    outputfile = ops['name']
    
    # load the tabs that we want
    tabs_we_want = ['Male lower than SPA', 'Male higher than SPA', 'Female lower than SPA', 'Female higher than SPA']
    tabsNational = loadxlstabs(inputfile, tabs_we_want)
    
    conversionsegments = []
    
    for tab in tabsNational:
        
        geo = tab.excel_ref('A9').expand(DOWN).is_not_blank() - tab.excel_ref('A9').expand(DOWN).is_blank().by_index(1).expand(DOWN)
        
        obs = tab.excel_ref(ops['obsCol'] + '9').expand(DOWN).is_not_blank().is_not_whitespace()
    
        gender = getGender(tab)
    
        dimensions = [
            HDimConst(TIME, "2011-2013"),
            HDim(geo, "Geography", DIRECTLY, LEFT),
            HDimConst("Gender", gender)
                ]
        
        conversionsegment = ConversionSegment(tab, dimensions, obs)
        conversionsegments.append(conversionsegment)
        
    writeCSV(outputfile, conversionsegments)
    
