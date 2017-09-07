# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 13:50:31 2017

@author: Mike

Simple SDMX to V3CSV builder
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests, sys


# creates a CSV-like dataframe of one-row=per-observation out of the SDMX file.
# this is "raw" so its everything and with no codes translated.
def makeDataframeFromSDMX(inputFile):

    with open(inputFile, 'r') as f:
        soup = BeautifulSoup(f, 'lxml')
    
        # for each data series
        dataSeries = soup.html.body.compactdata.find_all('na_:series')
        
        # build dict
        finalDict = {}
        initial_keys = ['obs_value', 'time_period', 'obs_status', 'conf_status']
        for ik in initial_keys:
            finalDict.update({ik:[]})
        
        # add the keys is use per series
        series_keys = dataSeries[0].attrs.keys()
        for sk in series_keys:
            finalDict.update({sk:[]})
            
        # EXTRACT
        for dSeries in dataSeries:
            for ob in dSeries.findChildren():    
                for ik in initial_keys:
                    finalDict[ik].append(ob[ik])
                for sk in series_keys:
                    finalDict[sk].append(dSeries[sk])
                    
        obs_file = pd.DataFrame.from_dict(finalDict)
        
        return obs_file
    
            
# Uses info at the top of the SDMX file to create a url and requests the DSD from registry.SDMX.org
def getDSD(inputFile):

    with open(inputFile, 'r') as f:
        soup = BeautifulSoup(f, 'lxml')

        # We're going to parse the info we need for the GET out of the dataet schemalocation attribute (top of SDMX file)
        infoString = soup.html.body.compactdata.attrs['xsi:schemalocation']

        # Get the key family section 
        keyString = [x for x in infoString.split() if '.KeyFamily' in x]
        assert len(keyString) == 1, "Cannot find reference to key family in the 'xsi:schemalocation' attribute"
        keyString = keyString[0]
        
        # Now split further, we want all 3 parts of the keyFAMILY, divded by "/" for the request
        keyString = keyString.split('KeyFamily=')[1].replace(':', '/').replace('/compact', '')
        
        # Create a version string for scheme version
        versionString = [x for x in infoString.split() if 'schemas' in x]
        assert len(versionString) == 1, "Cannot find reference to 'schemas' family in the 'xsi:schemalocation' attribute"
        versionString = versionString[0]
        
        versionString = versionString.split('schemas')[1].replace('/message', '').replace('/v', '').replace('_', '.')
        
        url = 'https://registry.sdmx.org/FusionRegistry/ws/rest/schema/datastructure/{kf}/?version={v}'.format(kf=keyString, v=versionString)   

        # get and return
        DSDdata = requests.get(url).content
        
        return DSDdata
    
# given the organisation.codelist.verion for a given codelist, return lookup dictionary
# includes alternate hanlding for prefixed items
def mapCodes(codeList):
    
    lookup = {}

    """
    Need non-standard handling if the codeList string contains a prefix
    i.e has a colon in it.
    """
    if ':' in codeList:
        pass
    else:
            
        # get the XML
        codeList = codeList.replace('.', '/')
        
        # replace _ with . in the verion
        codeList = codeList.split('/')
        codeList[2] = codeList[2].replace('_', '.')
        codeList = "/".join(codeList)
        
        # create url and GET the xml
        url = "https://registry.sdmx.org/FusionRegistry/ws/rest/codelist/{CL}/?detail=full&references=none&version=2.0".format(CL=codeList)
        data = requests.get(url).content
        
        # parse it
        soup = BeautifulSoup(data, 'lxml')
        codes = soup.html.body.find_all("str:code")

        for c in codes:
            lookup.update({c.attrs['value']:c.text.strip()})
    
    return lookup
    

# given a dataframe, a specofic column and the mapping of columns->codelists. Translates all the column codes to labels
def translateColumn(df, column, codeList):
    
    lookup = mapCodes(codeList)
    
    for key in lookup.keys():
        df[column][df[column] == key] = lookup[key]
    
    return df
    
    
# get details of the codelists sitting behind each of the dimensions in the dataset
# returns dictioary of {name:organisation.codelist.version}
def identifyCodelists(data):
    
    """    
    SDMX uses strictly defined codelists that sit behind the more user-friendly labels typically shown.
    For example the dimensions "Accounting Entry" in na_:main is actually of type "IMF.CL_ACCOUNT_ENTRY.1_0",
    signifying it uses version 1 of the IMF defined codelist "ACCOUNT ENTRY".
    
    The nameMapping dictionary will map the common-place name to these names, we can then query the
    appropriate coelists for any dimensions we choose to use.
    
    """
    nameMapping = {}
    soup = BeautifulSoup(data, 'xml')
    extensionData = soup.find_all("extension")
        
    for extension in extensionData:
        for entry in extension:
            if 'name' in entry.attrs and 'type' in entry.attrs:
                # we only care about the name and type attributes
                # where the type is referenced more that once the name should always match - error catch just in case

                if entry.attrs['type'] in nameMapping.keys():
                    print(entry.attrs['name'],nameMapping[entry.attrs['type']])
                    assert entry.attrs['name'] == nameMapping[entry.attrs['type']], "{wtf} is mapping to more than one type in the DSD".format(wtf=entry.attrs['name'])
                
                # if the name and type are different, its a codelist, we want it
                if entry.attrs['name'] != entry.attrs['type']:
                    nameMapping.update({entry.attrs['name'].lower():entry.attrs['type']})
      
                # TODO - probably needs an else here for extensions that are not just codelists.    
                
    return nameMapping
    

# make sure the parameters supplied are as expected. Otherwise educate.
def policeInput(mode, file):
    
    modes = {
         '-all':"Return a simple 'observation per row' CSV of all data and metadata fields with all codes translated",
         '-raw':"Return a simple 'observation per row' CSV of all data and metadata fields with none of the codes translated",
         '-list':"Prints a list of possible dimensions within the SDMX source file."
         } 
    if sys.argv[1] not in modes.keys():
        print("\nMandatory parameter missing. The first argument must be one of the following:\n")
        for m in modes:
            print(m, '   ', modes[m])
    else:
        mode = sys.argv[1]
    
    if '.sdmx' not in sys.argv[2].lower() and '.xml' not in sys.argv[2].lower():
        print("The second argument for this scipt needs to be a .SDMX or .XML file")
    else:
        file = sys.argv[2]
    
    return mode, file
    

# Finds the time dimension from a list of columns headers taken from the dataframe
# returns that heading as time, and returns the list without that entry.
def wheresTime(allCols):
    
    timeNames = ['time_period']

    for t in timeNames:
        if t in allCols:
            return [x for x in allCols if x != t], t


# Finds the time dimension from a list of columns headers taken from the dataframe
# returns that heading as time, and returns the list without that entry.
def wheresGeo(allCols):
    
    geoNames = ['ref_area']

    for g in geoNames:
        if g in allCols:
            return [x for x in allCols if x != g], g
            

# Finds the time dimension from a list of columns headers taken from the dataframe
# returns that heading as time, and returns the list without that entry.
def wheresObs(allCols):
    
    obsNames = ['obs_value']

    for o in obsNames:
        if o in allCols:
            return [x for x in allCols if x != o], o

# #######################
# THE INDIVIDUAL COMMANDS
# #######################

def PRINTlist(file):
    
    # create base dataframe
    df = makeDataframeFromSDMX(file)
    
    allCols = df.columns.values
    allCols, time = wheresTime(allCols)  # identify TIME, and remove it from the list
    allCols, geo = wheresGeo(allCols) # identify GEOGRAPHY and remove it from the list
    allCols, obs = wheresObs(allCols) # identify GEOGRAPHY and remove it from the list
    
    print('\n\n------------------\nMandatory Dimensions\n----------------')
    print('These will be included automatically in the V4 transformation.\n')
    print('Time Column:      ', time)
    print('Geography Column: ', geo)
    print('Observations:     ', obs)
    
    print('\n\nOptional Dimensions\n-----------------------')
    print('OCCURANCES  | ITEM')
    print('-----------------------')
    for col in allCols:
        entries = len(df[col].unique())
        padding = int(11-len(str(entries).replace('.0', '')))
        print(entries, ' '*padding + '|' , col)
    
    print('\n')

    
# Builds a CSV from the SDMX with all codes translated.
def BUILDall(file):
    
    # create base dataframe
    df = makeDataframeFromSDMX(file)
    
    # get DSD, then codelists from it
    DSD = getDSD(file)
    allCodeLists = identifyCodelists(DSD)
    
    # translate the codes in all columns of the dataframe that have an associated codelist
    for col in df.columns.values:        
        if col in allCodeLists: # i.e if it has codes behind it
                df = translateColumn(df, col, allCodeLists[col])
    
    # output CSV
    df.to_csv('CSVallSDMX_' + "".join(file.split('.')[:-1]) + '.csv', index=False)
    
    
# Builds a "raw" CSV with no codes translated.
def BUILDraw(file):
    
    # create base dataframe
    df = makeDataframeFromSDMX(file)

    # output CSV
    df.to_csv('CSVrawSDMX_' + "".join(file.split('.')[:-1]) + '.csv', index=False)  
    
    
    
    
    
# ####
# MAIN
# ####

# Police the parameters a bit
mode, file = policeInput(sys.argv[1], sys.argv[2])
    
# -all    
# Create a CSV of all fields, with everything translated
if sys.argv[1] == '-all':
    BUILDall(file)
    
# -raw
# Create a CSV of all fields, with nothing translated
if sys.argv[1] == '-raw':
    BUILDraw(file)
    
# -list
# Identifies time and geogrpahy, provides a list of other dimensions
if sys.argv[1] == '-list':
    PRINTlist(file)



    


