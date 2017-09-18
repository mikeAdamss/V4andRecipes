
from databaker.framework import *
from databaker.jupybakeutils import pdguessforceTIMEUNIT
import pandas as pd
import sys

# Set the inputfile
inputFile = sys.argv[1]

# Switch - BY default we dont want the sparce combinations (chatted with Darren)
# If we're feeling brave we can flick this switch.
Clean = True


#####################
# Functions


# filter out what we dont need for the Median Housing Dataset
def applyHousingFilters(housing, measure):
    
    if measure == 'Median':
        housing = housing.filter(contains_string("Median"))
        housing = housing - housing.filter(contains_string("Percentage"))
        housing = housing - housing.filter(contains_string("Rank"))
        
        # if we want the clean and simple (non sparse) version
        if Clean:
            housing = housing - housing.filter(contains_string("All property types"))
        
    if measure == 'Percentage':
        housing = housing.filter(contains_string("%"))
    
        # if we want the clean and simple (non sparse) version
        if Clean:
            housing = housing.filter(contains_string("Q2 2015:"))
    
    return housing



# filter out what we dont need for the Median Housing Dataset
def applyIMDFilters(housing, measure):
    
    if measure == 'Rank':
        housing = housing.filter(contains_string("Rank"))
        
    if measure == 'Proportion':
        housing = housing.filter(contains_string("%"))
    
    return housing



# sort out the time and clean the housing dimensions
def timeAndClean(df, measure):
    
    for i, row in df.iterrows():
           
        # #####
        # TIME
        # #####
        
        time = row['Housing'].split(' Q')

        if len(time) == 2: # it only has 1 date in the title
            time = 'Q' + time[1][:6]
        else:
            twoTimes = 'Q' + time[1][:6]
            time = 'Q' + time[2][:6] 
        
        df.iloc[i, df.columns.get_loc('TIME')] = time
        
        
        # ########
        # HOUSING
        # ########
        
        # tidy up the housing label.
        if measure == 'Median':
            # i.e "Median House Price, year ending Q2 2015: Detached" becaomes "Detached"
            housing = row['Housing'].split(': ')[1]
            if housing == ['All property types']:
                housing = 'All properties'
            df.iloc[i, df.columns.get_loc('Housing')] = housing
            
        if measure == 'Percentage':
            if 'Percentage change' in row['Housing']:
                df.iloc[i, df.columns.get_loc('Housing')] = 'Percentage Change since ' + twoTimes
            else:
                housing = row['Housing'].split(',')[0] + ':' + row['Housing'].split(':')[1]
                df.iloc[i, df.columns.get_loc('Housing')] = housing.replace(' (%)', '')
                
    return df
    


#############################################################
############## EXTRACTING THE HOUSING TAB ###################
#############################################################


tabsWeWant = ['Housing']
tabs = loadxlstabs(inputFile, tabsWeWant)


for measure in ['Median', 'Percentage']:

    tab = tabs[0]

    # TCITY15CD
    geo = tab.excel_ref('A2').fill(DOWN)
    geo = geo - tab.excel_ref('A').filter(contains_string("Source")).expand(RIGHT).expand(DOWN)
    
    # Housing
    housing = tab.excel_ref('D2').expand(RIGHT).is_not_blank().is_not_whitespace()

    # Apply filters
    housing = applyHousingFilters(housing, measure)
    
    # obs
    obs = geo.waffle(housing)

    dimensions = [
        HDim(geo, "Geography", DIRECTLY, LEFT),
        HDim(housing, "Housing", DIRECTLY, ABOVE),
        HDimConst(TIME, '')
    ]
    df = ConversionSegment(tab, dimensions, obs).topandas()

    # Now we need to tidy up the Housing dimension items and extract the time
    df = timeAndClean(df, measure)
    df = pdguessforceTIMEUNIT(df)  # borrowed from inner databaker

    if measure == 'Median':
        writeCSV("Towns and Cities - Median House Prices.csv", df)
    else:
        # clean the label, no need to repeat what already in the title
        df['Housing'] = df['Housing'].map(lambda x: x.replace('Proportion of property sales: ',''))
        writeCSV("Towns and Cities - Proportion of property sales.csv", df)



#########################################################
############## EXTRACTING THE IMD TAB ###################
#########################################################

tabsWeWant = ['IMD']
tabs = loadxlstabs(inputFile, tabsWeWant)

for measure in ['Rank', 'Proportion']:
    
    tab= tabs[0]
    
    # Geography
    geo = tab.excel_ref('A2').fill(DOWN)
    geo = geo - tab.excel_ref('A').filter(contains_string("Source")).expand(RIGHT).expand(DOWN)
    
    # Housing
    housing = tab.excel_ref('D2').expand(RIGHT).is_not_blank().is_not_whitespace()

    # Apply filters
    housing = applyIMDFilters(housing, measure)
    
    # obs
    obs = geo.waffle(housing)

    dimensions = [
        HDim(geo, "Geography", DIRECTLY, LEFT),
        HDim(housing, "Housing", DIRECTLY, ABOVE),
        HDimConst(TIME, tab.excel_ref('A1').value[-4:])
    ]
    
    df = ConversionSegment(tab, dimensions, obs).topandas()

    # Now we need to tidy up the Housing dimension items and extract the time
    #df = timeAndClean(df, measure)
    df = pdguessforceTIMEUNIT(df)  # borrowed from inner databaker

    if measure == 'Rank':
        df['Housing'] = df['Housing'].map(lambda x: x.replace('Rank',''))
        writeCSV("Towns and Cities - IMD Rankings.csv", df)
    else:
        df['Housing'] = df['Housing'].map(lambda x: x.replace(': Proportion of LSOAs in most deprived 20%',''))
        writeCSV("Towns and Cities - Proportion of LSOAs in most deprived 20%.csv", df)

