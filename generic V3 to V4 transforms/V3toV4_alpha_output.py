# -*- coding: utf-8 -*-
import pandas as pd
import sys

# Looks for any entries in Data_Marking and Obs_type_value
def initialColumns(df, qm=False):
    
    newDf = pd.DataFrame()
    count = 0
    dmNeeded = False
    qmNeeded = False
    
    # if there's data makrings, return True
    if len(df['Data_Marking'].unique()) > 1:
        dmNeeded = True
        colCount += 1
        
    # if there are Cv values flag it - do we want to do this?
    # else return true
    if len(df['Observation_Type_Value'].unique()) > 1:
        if qm == False:
            raise ValueError ("Quality measure detected. Pass specific name i.e 'CV' on command line to process")
        else:
            qmNeeded = True
            count += 1    
    
    # Add the coluns needed
    newDf['V4_' + str(count).replace('.0', '')] = df['Observation']
    if dmNeeded:
        newDf['Data Marking'] = df['Data_Marking']
    if qmNeeded:
        newDf[qm] = df['Observation_Type_Value']
    
    return newDf
    

 
# add time and geography related columns
def timeAndGeography(newDf, df):
    
    newDf['Time_codelist'] = df['Dimension_1_Name']
    newDf['Time'] = df['Dimension_1_Code']
    
    newDf['Geography_codelist'] = df['Dimension_2_Code']
    newDf['Geography'] = ''

    return newDf


# calculate how many topic dimensions we have
def howManyTopics(df):

    topics = len(df.columns.values)
    topics = topics - 10 
    assert topics % 2 == 0, "V3 Dataset has missing or additional columns. Not a valid source."
    topics = topics / 2
    return topics


# checks there is only one name in a Dimension_Name_x columna nd returns it
def getSingleName(df, col):
    
    names = df[col].unique()
    assert len(names) == 1, "More then one Dimension name in '{col}', invalid file".format(col=col)
    
    return names[0]
    
    
# create the topic dimensions
def createTopicDims(newDf, df):
    
    topics = howManyTopics(df)
    
    for i in range(3, int(topics)+3):
        
        name = 'Dimension_{n}_Name'.format(n=str(i))
        value = 'Dimension_{v}_Value'.format(v=str(i))
        
        newDf[getSingleName(df,name) + '_codelist'] = ''
        newDf[getSingleName(df,name)] = df[value]
        
    return newDf
    

infile = sys.argv[1]
    
df = pd.read_csv(infile)
df.fillna('', inplace=True)

# Create new dataframe and start columns
newDf = initialColumns(df)

# time and geography
newdf = timeAndGeography(newDf, df)

# add any topic dimensions
newDf = createTopicDims(newDf, df)

newDf.to_csv('V4fromV3_' + infile, index=False)

