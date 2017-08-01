# encoding: utf-8

# imports
from databaker.framework import *
import pandas as pd
import sys


# we want one seasonal adjustment source file
sourceNSA = sys.argv[1]

# and one non seasonal adjustment source file
sourceSA = sys.argv[2]


# Get the growth period
def get_growthPeriod(tab):
    tab_title = tab.excel_ref('A1')
    
    if tab_title.filter(contains_string("year on year")):
        gp = "Annual"
    elif tab_title.filter(contains_string("quarter on quarter")):
        gp = "Quarterly"
    elif tab_title.filter(contains_string("growth rates")):
        gp = "Annual"
    else:
        gp = 'Quarterly'
    
    return gp


# Get the measure type
def get_measureType(tab):
    tab_title = tab.excel_ref('A1')
                       
    if "year on year" in tab_title:
        mt = "Percent"
    elif "quarter on quarter" in tab_title:
        mt = "Percent"
    elif "growth rates" in tab_title:
        mt = "Percent"
    else:
        mt = "Index"
    return mt
    

"""
The recipe for the 'level' tabs, returns a list of conversionSegments (in this case - contents of one extracted tab).
we're not writing to file yet. 
"""

def level_recipe(saOrNsa, tabs):
    
    conversionsegments = []

    for tab in tabs:

        # Set anchor one to the left of cell with "Agriculture" 
        anchor = tab.filter(contains_string("eriod")).assert_one()

        # set up a waffle
        datarows = anchor.fill(DOWN).is_not_blank()
        datacols = anchor.shift(DOWN).fill(RIGHT).is_not_blank()
        obs = datarows.waffle(datacols).is_not_blank()
        
        # set the measuretype
        mt = get_measureType(tab) # todo - where does measure type fit in now?

        dimensions = [
                HDim(datarows, TIME, DIRECTLY, LEFT),
                HDimConst("Geography", "K02000001"),
                HDim(datacols, "Costs", DIRECTLY, ABOVE),
                HDim(anchor.fill(RIGHT).is_not_blank().is_not_whitespace(), "SIC", CLOSEST, LEFT),
                HDimConst("SA / NSA", saOrNsa)
                     ]

        # TIME has wierd data markings, get them out
        time = dimensions[0]
        assert time.name == 'TIME', "Time needs to be dimension 0"
        for val in time.hbagset:
            if '(r)' in val.value or ('p') in val.value:
                time.cellvalueoverride[val.value] = val.value[:6]

        conversionsegment = ConversionSegment(tab, dimensions, obs).topandas()
        conversionsegment['SIC'] = conversionsegment['SIC'].map(lambda x: x.replace('\n', ' '))
        conversionsegments.append(conversionsegment)     
    
    return conversionsegments


"""
The recipe for the 'growth' tabs, returns a list of conversionSegments (in this case - contents of one extracted tab).
we're not writing to file yet. 
"""

def growth_recipe(saOrNsa, tabs):
    
    conversionsegments = []

    for tab in tabs:

        # Set anchor one to the left of cell with "Agriculture" 
        anchor = tab.filter(contains_string("eriod")).assert_one()

        # set up a waffle
        datarows = anchor.fill(DOWN).is_not_blank()
        datacols = anchor.shift(DOWN).fill(RIGHT).is_not_blank()
        obs = datarows.waffle(datacols).is_not_blank()

        # set the growth period & measuretype
        gp = get_growthPeriod(tab)
        mt = get_measureType(tab)  # TODO - where does measure type fit in now?

        dimensions = [
                HDim(datarows, TIME, DIRECTLY, LEFT),
                HDimConst("Geography", "K02000001"),
                HDim(datacols, "Costs", DIRECTLY, ABOVE),
                HDim(anchor.fill(RIGHT).is_not_blank().is_not_whitespace(), "SIC", CLOSEST, LEFT),
                HDimConst("Growth Period", gp),
                HDimConst("SA / NSA", saOrNsa)
        ]
        
        # TIME has wierd data markings, get them out
        time = dimensions[0]
        assert time.name == 'TIME', "Time needs to be dimension 0"
        for val in time.hbagset:
            if '(r)' in val.value or ('p') in val.value:
                time.cellvalueoverride[val.value] = val.value[:6]

        conversionsegment = ConversionSegment(tab, dimensions, obs).topandas()
        conversionsegment['SIC'] = conversionsegment['SIC'].map(lambda x: x.replace('\n', ' '))
        conversionsegments.append(conversionsegment)
    
    return conversionsegments

    
"""
EXTRACTNG FROM THE NSA SPREADSHEET
"""

# load and select tabs
tabs = loadxlstabs(sourceNSA)
    
# NSA level tabs
level_tabs = [x for x in tabs if 'level' in x.name.lower()]
level_from_NSA = level_recipe("Not seasonally adjusted", level_tabs)

# NSA growth tabs
growth_tabs = [x for x in tabs if 'growth' in x.name.lower()]
growth_from_NSA = growth_recipe("Seasonally adjusted", growth_tabs)


"""
EXTRACTNG FROM THE SA SPREADSHEET
"""

# laod and select tabs
tabs = loadxlstabs(sourceSA)
    
# NSA level tabs
level_tabs = [x for x in tabs if 'level' in x.name.lower()]
level_from_SA = level_recipe("Not seasonally adjusted", level_tabs)

# NSA growth tabs
growth_tabs = [x for x in tabs if 'growth' in x.name.lower()]
growth_from_SA = growth_recipe("Seasonally adjusted", growth_tabs)


"""
COMBINING THE LEVEL AND GROWTH EXTRACTIONS FROM EACH
"""

writeCSV('ILCH-Growth.csv', growth_from_SA + growth_from_NSA)

writeCSV('ILCH-Level.csv', level_from_SA + level_from_NSA)

