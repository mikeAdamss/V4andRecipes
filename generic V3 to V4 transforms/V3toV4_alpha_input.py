# coding: utf-8
import pandas as pd
import json, sys

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
    
    newDf['Time_codelist'] = df['Dimension_Value_1']
    newDf['Time'] = df['Dimension_Name_1']
    
    newDf['Geography_codelist'] = df['Dimension_Value_2']
    newDf['Geography'] = ''

    return newDf


# calculate how many topic dimensions we have
def howManyTopics(df):

    topics = len(df.columns.values)
    topics = topics - 9    
    assert topics % 3 == 0, "V3 Dataset has missing or additional columns. Not a valid source."
    topics = topics / 3
    return topics
    

# check a Hierarchy column, to see if it has a hierarchy entry. Returns True/False
# if get=True, returns the name of the hierarchy
def hasHierarchy(df, col, get=False):
    
    if len(df[col].unique()) > 1:
        raise ValueError('Columns {col} appears to have more than one value. File invalid.'.format(col=col))
    else:
        h = df[col].unique()[0]
        if get==True:
            return h
        if h == '':
            return False
        else:
            return True
    
    
# check the item column. Is it labels or is it all WDA codes?
def hasCIcodes(df, col):
    
    items = df[col].unique()
    items = [x for x in items if x[:3] != 'CI_']
    if len(items) == 0:
        return True
    else:
        return False


# checks there is only one name in a Dimension_Name_x columna nd returns it
def getSingleName(df, col):
    
    names = df[col].unique()
    assert len(names) == 1, "More then one Dimension name in '{col}', invalid file".format(col=col)
    
    return names[0]
    

# get the labels for the provided cdoes from the alpha scraped .json files
def copyInCodes(newDf, df, value, name, hierName):
    
    lookups = {}
    
    # loops iteself to build lookup dict of code:name
    def updateCodes(level, lookups):
        if type(level) == dict:
            if 'options' in level.keys():
                lookups = updateCodes(level['options'], lookups)

            for opt in level['options']:
                lookups.update({opt['code']:opt['name']})
        
        if type(level) == list:
            for opt in level:
                lookups.update({opt['code']:opt['name']})
                
        return lookups
    
    # copy the codes into the names columne
    newDf[name] = df[value]
    
    # create a code lookup dictionary
    with open('ALPHA/{CL}.json'.format(CL=hierName)) as json_data:
        d = json.load(json_data)
        lookups = updateCodes(d, lookups)
        
    # sanity check
    assert len(lookups) > 0, "Error, the Lookup dictionary for Codes appears to be empty."
    
    # Apply the lookups
    newDf[name] = newDf[name].map(lambda x: x.replace(x, lookups[x]))
        
    return newDf
    
    
# create the topic dimensions
def createTopicDims(newDf, df):
    
    topics = howManyTopics(df)
    
    for i in range(3, int(topics)+3):
        
        hier = 'Dimension_Hierarchy_{h}'.format(h=str(i))
        name = 'Dimension_Name_{n}'.format(n=str(i))
        value = 'Dimension_Value_{v}'.format(v=str(i))
        
        # does the file have a stated hierarchy
        if hasHierarchy(df, hier):
            thisHierarchy = df[hier].unique()[0] # list of 1. anything else was flagged during hasHierarchy
        
        # if it has codes or a hieracht it MUST have both, throw an error it not
        if hasCIcodes(df, value) and hasHierarchy(df, hier) == False:
            raise ValueError ("Dataset has codes but no codelist. Invalid Source File")
            

        # get the dim name. Error if more than one
        name = getSingleName(df, name)
        
        # populate with EITHER codes or labels
        if hasCIcodes(df, value):
            hierName = hasHierarchy(df, hier, get=True)
            newDf[hierName] = df[value]
            newDf = copyInCodes(newDf, df, value, name, hierName)
        else:
            newDf[name + '_codelist'] = ''
            newDf[name] = df[value]
        
    return newDf
    
# load input file into dataframe, get rid of nan values
inputFile = sys.argv[1]
df = pd.read_csv(inputFile)
df.fillna('', inplace=True)

# Create new dataframe and start columns
newDf = initialColumns(df)

# time and geography
newdf = timeAndGeography(newDf, df)

# topic dimensions
newDf = createTopicDims(newDf, df)

newDf.to_csv('V3toV4_' + inputFile, index=False)

