# -*- coding: utf-8 -*-

from databaker.framework import *
import pandas as pd
import sys

# specify the file in question
inputFile = sys.argv[1]

# load 1 tab only into databaker
tabs = loadxlstabs(inputFile, ["Weekly figures 2017"])


#######################
# Deaths by age group #
#######################

TabsAsDataFrames = []
for tab in tabs:   # not really necesary but doesn't hurt as the tabs are loaded as a list (even when there's just 1 tab like now)
    
    # obs
    obs = tab.excel_ref('C15').expand(DOWN).expand(RIGHT).is_not_blank().is_not_whitespace()
    obs = obs - tab.excel_ref('B42').expand(RIGHT).expand(DOWN)
    
    # time
    time = tab.excel_ref('C5').expand(RIGHT).is_not_blank().is_not_blank()
    
    # too amny bold cells, select then filter to what we want
    gender = tab.excel_ref('B13').expand(DOWN).is_bold().is_not_blank().is_not_whitespace()
    gender = gender.filter(lambda x: x.value.split(' ')[0].lower() in ['males', 'females', 'persons'])
    
    # age overrides
    # horrible on-the-fly creation of key:value pairs to override footnote markers.
    # i.e turn cell content "Persons 5" into "Persons"
    genderOverrides = {}
    for cell in gender:
        if 'females' in cell.value.lower():
            genderOverrides.update({cell.value:'Female'})
        elif 'males' in cell.value.lower():
            genderOverrides.update({cell.value:'Male'})
        elif 'persons' in cell.value.lower():
            genderOverrides.update({cell.value:'Person'})
        else:
            raise ValueError("Cannot identify Gender")
            
    # age - whole column. valid values are always to the left of obs
    age = tab.excel_ref('C15').expand(DOWN).is_not_blank().is_not_whitespace()
              
    # define relationships
    dimensions = [
        HDim(time, TIME, DIRECTLY,ABOVE),
        HDimConst("Geography", "K04000001"),
        HDim(gender, "Gender", CLOSEST, ABOVE, cellvalueoverride=genderOverrides),
        HDim(age, "Age", DIRECTLY, LEFT)
    ]
        
    df = ConversionSegment(tab, dimensions, obs).topandas()
    
    df['TIMEUNIT'] = 'Week'
    df['Age'] = df['Age'].map(lambda x: str(x.strip('.0')))
    
    TabsAsDataFrames.append(df)


# get file name time from C5 (first time cell), plus assertion
time = tab.excel_ref('C5').value
time = time.today().year
assert int(time) > 2010 and time < 2030, 'Error: Cant find a year in the strting "{str}"'.format(time)
time = str(time).strip('.0')
    
writeCSV("Weekly deaths by age group {t}.csv".format(t=time), pd.concat(TabsAsDataFrames))
