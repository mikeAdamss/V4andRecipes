"""
Average Weekly Earnings
-----------------------

Essentially 3 transformation scripts, one on top of the other. As follows:
    
    
1.) Summary (values)
2.) Summary (percentages)
3.) Pay Index 

There's a fair amount of cross over between the different extractions but I've kept them seperated out (and easier to read).
    
"""

# imports
from databaker.framework import *
import pandas as pd
import sys

inputFile = sys.argv[1]



# ##################################
# WEEKLY EARNINGS - Summary (Values)
# ##################################

# laod and select tabs
tabsWeWant = ['1. AWE Total Pay','2. AWE Bonus Pay','3. AWE Regular Pay']
tabs = loadxlstabs(inputFile, tabsWeWant)

conversionsegments = []

myDict = {}
for tab in tabs:

        # get the date
        time = tab.excel_ref('A8').fill(DOWN).is_not_blank().is_not_whitespace()
        
        
        # get observations. use waffled in case of footers
        obs = tab.excel_ref('A6').fill(RIGHT).is_not_blank().filter(contains_string("Weekly Earnings")).waffle(time)
        obs = obs.is_not_blank().is_not_whitespace()
    
        # Get the pay type
        payType = " ".join(tab.name.split(' ')[2:])
        
        # category
        category = tab.excel_ref('A5').expand(RIGHT).is_not_blank()
        
        # tidy up horrible footnotes
        """
        i.e create this kinda thing:
        categoryOverride = {
                            'Public sector2 4 5':Public Sector'
                            }
        """
        
        categoryOverrides = {}
        for cell in category:
            if 'Public sector excluding financial services'.lower() in cell.value.lower():
                categoryOverrides.update({cell.value:'Public sector excluding financial services'})
            elif 'Public sector'.lower() in cell.value.lower():
                categoryOverrides.update({cell.value:'Public sector'})
            elif 'Private sector'.lower() in cell.value.lower():
                categoryOverrides.update({cell.value:'Private sector'})
        
        # define relationships
        dimensions = [
            HDim(time, TIME, DIRECTLY, LEFT),
            HDimConst("Geography", "K03000001"),
            HDimConst("Pay Type", payType),
            HDim(category, "Category", DIRECTLY, ABOVE, cellvalueoverride=categoryOverrides)
        ]
        
        
        myDict.update({tab.name:{}})
        for dimension in dimensions:
            if dimension.hbagset != None:
                myDict[tab.name].update({dimension.name:[]})
                for cell in dimension.hbagset:
                    myDict[tab.name][dimension.name].append(cell)
        
        
        conversionsegment = ConversionSegment(tab, dimensions, obs).topandas()
        
        # Get rid of mid-sentence forced line break
        conversionsegment['Category'] = conversionsegment['Category'].map(lambda x: " ".join([t.replace('\r','').replace('\n', '').strip() for t in x.split(' ')]))    
        
        conversionsegments.append(conversionsegment)

        
writeCSV("Weekly Earnings - Summary.csv", pd.concat(conversionsegments))




# ###############################################
# WEEKLY EARNINGS - Summary of Percentage Changes
# differences: "month" in text.
# dimension in 2 things.
# ##################################

# laod and select tabs
tabsWeWant = ['1. AWE Total Pay','2. AWE Bonus Pay','3. AWE Regular Pay']
tabs = loadxlstabs('earn01jun2017 (2).xls', tabsWeWant)


conversionsegments = []

for tab in tabs:

        # get the date
        time = tab.excel_ref('A8').fill(DOWN).is_not_blank().is_not_whitespace()
        
        # percentages tsype
        perc = tab.excel_ref('A7').fill(RIGHT).is_not_blank().filter(contains_string("month"))
        
        # obs
        obs = perc.waffle(time).is_not_blank().is_not_whitespace()
    
        # Get the pay type
        payType = " ".join(tab.name.split(' ')[2:])
        
        # category
        category = tab.excel_ref('A5').expand(RIGHT).is_not_blank()
        
        # tidy up horrible footnotes
        """
        categoryOverride = {
                            'Public sector2 4 5':Public Sector'
                            }
        """
        
        categoryOverrides = {}
        for cell in category:
            if 'Public sector excluding financial services'.lower() in cell.value.lower():
                categoryOverrides.update({cell.value:'Public sector excluding financial services'})
            elif 'Public sector'.lower() in cell.value.lower():
                categoryOverrides.update({cell.value:'Public sector'})
            elif 'Private sector'.lower() in cell.value.lower():
                categoryOverrides.update({cell.value:'Private sector'})
                
                
        perOverrides = {}
        for cell in perc:
            if '3 month average'.lower() in cell.value.lower():
                perOverrides.update({cell.value:'3 month average'})
        
        # define relationships
        dimensions = [
            HDim(time, TIME, DIRECTLY, LEFT),
            HDimConst("Geography", "K03000001"),
            HDim(perc, "Percentage Change", DIRECTLY, ABOVE, cellvalueoverride=perOverrides),
            HDimConst("Pay Type", payType),
            HDim(category, "Category", CLOSEST, LEFT, cellvalueoverride=categoryOverrides)
        ]
        
        conversionsegment = ConversionSegment(tab, dimensions, obs).topandas()
        
        # Get rid of mid-sentence forced line break
        conversionsegment['Category'] = conversionsegment['Category'].map(lambda x: " ".join([t.replace('\r', '').replace('\n', '').strip() for t in x.split(' ')])) 
        
        conversionsegments.append(conversionsegment)

        
writeCSV("Weekly Earnings - Summary as percentage changes.csv", pd.concat(conversionsegments))




# ##########
# Pay Index 
# ##########

# laod and select tabs
tabsWeWant = ['4. AWE Total Pay Index','5. AWE Regular Pay Index']
tabs = loadxlstabs(inputFile, tabsWeWant)


TabsAsDataFrames = []
for tab in tabs:

        anchor = tab.excel_ref('A8')
        
        obs = anchor.shift(DOWN).fill(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace()
    
        # get the date
        time = anchor.fill(DOWN).is_not_blank().is_not_whitespace()
        
        # get CDIDs
        cdid = anchor.expand(RIGHT).is_not_blank().is_not_blank()
        
        # Pay type
        payType = " ".join(tab.name.split(' ')[1:-1])
        
        # industry
        industry = anchor.shift(0, -2).expand(RIGHT).is_not_blank().is_not_whitespace()
        
        # define relationships
        dimensions = [
            HDim(time, TIME, DIRECTLY, LEFT),
            HDimConst("Geography", "K03000001"),
            HDimConst("Pay Type", payType),
            HDim(cdid, "CDID", DIRECTLY, ABOVE),
            HDim(industry, "Industry", DIRECTLY, ABOVE)
        ]

        # bounce to a dataframe
        df = ConversionSegment(tab, dimensions, obs).topandas()

        # get rid of any numbersin industry
        for i in range(0, 10):
            df['Industry'] = df['Industry'].map(lambda x: x.replace(str(i), ''))
        df['Industry'] = df['Industry'].map(lambda x: x.replace('\n', '').strip())    

        TabsAsDataFrames.append(df)
        
writeCSV("Weekly Earnings - Pay Index.csv", pd.concat(TabsAsDataFrames))

