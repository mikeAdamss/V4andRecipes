
from databaker.framework import *
import pandas as pd
import sys

# Set the inputfile
inputFile = sys.argv[1]


tabsWeWant = ['Census']
tabs = loadxlstabs(inputFile, tabsWeWant)


# The datasets we're getting from this tab of data
# -specifies their row 2 columns
dSets = {
    'EVERYTHING':'D2:W2',
    'Age Group':'D2:G2',
    'Health':'H2:J2',
    'Tenure':'K2:N2',
    'Qualifications':'P2:Q2',
    'Industry':'R2:U2',
    'Commuting':'V2:W2'
}


for censusMeasure in dSets.keys():
    
    tab = tabs[0]

    # TCITY15CD
    geo = tab.excel_ref('A2').fill(DOWN)
    geo = geo - tab.excel_ref('A').filter(contains_string("Source")).expand(RIGHT).expand(DOWN)
    
    # Whatever we're measuring
    census = tab.excel_ref(dSets[censusMeasure])
    
    # obs
    obs = geo.waffle(census)

    dimensions = [
        HDim(geo, "Geography", DIRECTLY, LEFT),
        HDim(census, censusMeasure, DIRECTLY, ABOVE),
        HDimConst(TIME, tab.excel_ref('A1').value[-4:])
    ]
    df = ConversionSegment(tab, dimensions, obs).topandas()
    df['TIMEUNIT'] = 'Deccenial'  # Overright databaker assumed 'year'
    
    
    # Clean clunky and/or redundant strings then output
    
    # EVERYTHING
    # Included just in case
    if censusMeasure == 'EVERYTHING':
        writeCSV('EVERYTHING - Cities and Houses, Census 2011 data.csv', df)
    
    
    # Age Group
    if censusMeasure == 'Age Group':
        df[censusMeasure] = df[censusMeasure].map(lambda x: x.replace('Population aged ',''))
        writeCSV('Percentage of Population by Age Group (2011 Census).csv', df)
    
    
    # Health and Age Group
    if censusMeasure == 'Health':
        """
        These headers, eg: "Population "limited a lot" by a health problem or disability, aged 16-64"
        Works much better as two dimensions. We'll split them out here.
        """
        df['Age Group'] = df['Health'].map(lambda x: x.split('aged')[1].strip())
        df['Health or Disability Impact'] = df['Health'].map(lambda x: x.split('"')[1].strip()) # better name
        df = df.drop('Health', axis =1)
        
        writeCSV('Percentage of Population by Health and Age Group (2011 Census).csv', df)
    
    
     # Tenure
    if censusMeasure == 'Tenure':
        writeCSV('Percentage of Population by Tenure - All Households (2011 Census).csv', df)
    
    
    # Qualifications
    if censusMeasure == 'Qualifications':
        df['Qualifications'] = df['Qualifications'].map(lambda x: x.replace('Proportion of resident population with ', '').replace(', aged 16+',''))
        df['Qualifications'] = df['Qualifications'].map(lambda x: x.title())
        writeCSV('Qualifications by Proportion of resident qualifications, 16+ (2011 Census).csv', df)
        
        
    # Industry
    if censusMeasure == 'Industry':
        df['Industry'] = df['Industry'].map(lambda x: x.split(",")[0].replace('Proportion of workday population in ', '').strip()) 
        writeCSV('Proportion of workday population by Industry, aged 16-74 (2011 Census).csv', df)
        

    # Commputing
    if censusMeasure == 'Commuting':
        writeCSV('Net Communiting for ages 16-74 (2011 Census).csv', df)
    
