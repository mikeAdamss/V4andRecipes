# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import requests, sys, re

    
# The different 'modes; you can run the tool in from the command lone. This choice is passed on the command line by sys argument 1.
modes = {
    '-tran':"Return a simple 'observation per row' CSV of all data and metadata fields with all codes translated",
    '-raw ':"Return a simple 'observation per row' CSV of all data and metadata fields with none of the codes translated",
    '-list':"Prints a list of possible dimensions within the SDMX source file.",
    '-v4  ':"Create a V4 verion of the SDMX file - required dimensions to be specified"
         } 
         
        
# simple output to the user if they get the commands wrong.
def callHelp(modes=modes):
    
    print('\n------------------\nCommand Line Error\n------------------\nSomething has been entered incorectly on the command line.\n')
    print('Valid modes of operation are as follows:\n')
    for m in modes:
        print(m, '  -  ', modes[m])
    print('\nFor all modes you required your choice of mode (i.e -all) as the first argument and the SDMX file as the second.')
    print('When creating V4 files (-v4) you also need to include a third argument specifiying which dimensions you require.')
    sys.exit()

    
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
        
        print(url)
        
        # parse it
        soup = BeautifulSoup(data, 'lxml')
        codes = soup.html.body.find_all("str:code")

        for c in codes:
            lookup.update({c.attrs['value']:c.text.strip()})
    
    return lookup
    

# given a dataframe, a specific column and the mapping of columns->codelists. Translates all the column codes to labels
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
    appropriate codelists for any dimensions we choose to use.
    
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
                    assert entry.attrs['name'] == nameMapping[entry.attrs['type']], "{wtf} is mapping to more than one type in the DSD".format(wtf=entry.attrs['name'])
                
                # if the name and type are different, its a codelist, we want it
                if entry.attrs['name'] != entry.attrs['type']:
                    nameMapping.update({entry.attrs['name'].lower():entry.attrs['type']})
      
                # TODO - probably needs an else here for extensions that are not just codelists.    
                
    return nameMapping
    

# make sure the parameters supplied are as expected. Otherwise educate.
def policeInput(mode, modes, file):
    
    # ugly but necessary as added spaces to keys for cleaner help output
    cleanKeys = [x.strip() for x in modes.keys()]
    
    if sys.argv[1] not in cleanKeys:
        callHelp()
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
    return allCols, None # failed to find


# Finds the time dimension from a list of columns headers taken from the dataframe
# returns that heading as time, and returns the list without that entry.
def wheresGeo(allCols):
    
    geoNames = ['ref_area']

    for g in geoNames:
        if g in allCols:
            return [x for x in allCols if x != g], g
    return allCols, None # failed to find
            

# Finds the time dimension from a list of columns headers taken from the dataframe
# returns that heading as time, and returns the list without that entry.
def wheresObs(allCols):
    
    obsNames = ['obs_value']

    for o in obsNames:
        if o in allCols:
            return [x for x in allCols if x != o], o
    return allCols, None # failed to find

 
# ######################
# PANDAS FUNCTION WRAPS
# ######################
# The following are applied to individual series (columns) in pandas dataframes


# Get the time "type" out of whatever SDMX is using
def ONStype(cell):
    if re.match('\d{4}(?:\.0)?$', cell):
        return 'Year'
    if re.match('\d{4}(?:\.0)?\s*[Qq]\d$', cell):
        return 'Quarter'
    if re.match('[Qq]\d\s*\d{4}(?:\.0)?$', cell):
        return 'Quarter'
    if re.match('[12][0-9]{3}-[Qq][1-4]$', cell):
        return 'Quarter'
    if re.match('[A-Za-z]{3}\s*\d{4}(?:\.0)?$', cell):
        return 'Month'
    raise ValueError("Cannot identify the time type of", cell)
    
    
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
def BUILDtran(file):
    
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
    df.to_csv('CSVtranSDMX_' + "".join(file.split('.')[:-1]) + '.csv', index=False)
    
    
# Builds a "raw" CSV with no codes translated.
def BUILDraw(file):
    
    # create base dataframe
    df = makeDataframeFromSDMX(file)

    # output CSV
    df.to_csv('CSVrawSDMX_' + "".join(file.split('.')[:-1]) + '.csv', index=False)  
    
    
# we need to parse the provided options string into something we can use
def parseChoices(optString):
    
    """
    The option string is basically our "recipe". 
    Example:
    "time=Q4 2014 dimensions=[time,age,industry] geo="K000000001 obs=obs_col"
    """

    time = None   # assumed.
    geo = None    # ...
    obs = None    # .
    dimensions = []

    # Look for optional "time=" in optString
    if "time=" in optString:
        
        # if "time=" appears more than once in the options string they're doing it wrong
        assert len(optString.split("time=")) ==2, "You can only specifiy the time (with time=) once."
        
        # Time may be in two parts (e.g Q1 2014) so split by eliminting the other options (which dont include whitespace delimeters)
        tString = optString
        tString = [x for x in tString.split("obs=") if "time=" in x][0]
        tString = [x for x in tString.split("dimensions=") if "time=" in x][0]
        tString = [x for x in tString.split("geo=") if "time=" in x][0]
        time = tString[5:] # get rid of "time="


    # look for optional obs= in optString
    if "obs=" in optString:
        obs = optString.split("obs=")
        assert len(obs) == 2, "You can only specify the obs column (with obs=) once"


    # look for optional geo= in optString
    if "geo=" in optString:
        obs = optString.split("geo=")
        assert len(obs) == 2, "You can only specify the obs column (with geo=) once"

        
    # Finds MANDATORY dimensions= in optString        
    assert "dimensions=" in optString, "You MUST provide the required dimensions when trying to convert to V4"

    
    # Find the sub-string. Assertion for stupidity.
    dimText = [x for x in optString.split(" ") if "dimensions=" in x]
    assert len(dimText) == 1, "You should only be specifiying 'dimensions=' once!"

    # Build the list of wanted dimensions    
    dimText = dimText[0].replace("dimensions=", "").replace("[", "").replace("]", "")
    dimText = dimText.split(" ")[0].strip()
    dimensions = dimText.split(",")

    return time, geo, obs, dimensions
    
    
    
# Command line wrapper. Turn the options string into something we can use
def BUILDV4(file, opString):
    time, geo, obs, dimensions = parseChoices(opString)
    SDMXtoV4(file, dimensions, obs=obs, time=time, geo=geo)
    

# MAIN TRANSFORM FUNCTION
def SDMXtoV4(file, dimensions, obs=None, time=None, geo=None):

    # create base dataframe
    df = makeDataframeFromSDMX(file)
    
    # if our 3 constant dimensons arent specified. Go get them, error on fail
    allCols = df.columns.values
    if time == None:
        allCols, time = wheresTime(allCols)  # identify TIME, and remove it from the list
    
    if geo == None:
        allCols, geo = wheresGeo(allCols) # identify GEOGRAPHY and remove it from the list
    
    if obs == None:
        allCols, obs = wheresObs(allCols) # identify OBS and remove it from the list
    
    # Make sure they havnt provided the same info twice
    for eachDim in [time, geo, obs]:
        assert eachDim not in dimensions, "The dimension {ec} shouldnt be in the dimensions= list. Its already accounted for.".format(ec=eachDim)
        
    # get DSD, then codelists from it
    DSD = getDSD(file)
    allCodeLists = identifyCodelists(DSD)
    
    # Now build the V4 file
    V4 = pd.DataFrame()
    
    # Standarad Dims
    V4['V4_0'] = df[obs]

    # Time is fidly. We'll use pandas apply (the argument is a function applied to and returning each cell. think "big lambda")
    V4['Time_codelist'] = df[time].apply(ONStype)
    V4['Time'] = df[time]

    V4['Geography_codelist'] = df[geo]
    V4['Geography'] = df[geo]
    V4 = translateColumn(V4, "Geography", allCodeLists[geo])
    
    # -----------
    # IMF UK Code
    # If they're using the IMF national level geography codlist
    imf = "https://registry.sdmx.org/FusionRegistry/ws/rest/codelist/IMF/CL_AREA/1.1/?detail=full&references=none&version=2.0"
    if geo == imf:
        assert df[geo].unique()[0] == 'GB', "IMF Level Geography included. We can only accept UK level data. Codelist: {gcl}".format(imf=imf)
        V4['Geography_codelist'] = 'K02000001'
        V4['Geography'] = ''
    else:    
        V4['Geography_codelist'] = df[geo]
        V4['Geography'] = df[geo]
        V4 = translateColumn(V4, "Geography", allCodeLists[geo])    
        
    # Topic dims
    for dim in dimensions:
        V4[dim+'_codelist'] = df[dim]
        V4[dim] = df[dim]
        V4 = translateColumn(V4, dim, allCodeLists[dim])
        
    # output CSV
    V4.to_csv('V4fromSDMX_' + "".join(file.split('.')[:-1]) + '.csv', index=False)
    
    
# ###################
# COMMAND LINE ONLY #
# ###################

# TODO argparser of some kind
if __name__ == '__main__':

    # Police the standard parameters a bit
    try:
        mode, file = policeInput(sys.argv[1], modes, sys.argv[2])
    except:
        callHelp()
    
    # -tran  
    # Create a CSV of all fields, with everything translated
    if sys.argv[1] == '-tran':
        BUILDtran(file)
        
    # -raw
    # Create a CSV of all fields, with nothing translated
    elif sys.argv[1] == '-raw':
        BUILDraw(file)
        
    # -list
    # Identifies time and geography, provides a list of other dimensions
    elif sys.argv[1] == '-list':
        PRINTlist(file)
    
        
    # -V4...see below
    elif sys.argv[1] == '-v4' or sys.argv[1] == '-V4':
        """
        The main trasformation function. Requires an options string, example shown below.
        
        "time=Q4 2014 dimensions=time,age,industry geo="K000000001 obs=obs_col"
        
        It looks python-esque but its just a text string that comes from sys.argv[3].
        The ONLY mandatory part is dimensions, order doesnt matter.
        """
        try:
            
            # Make sure they've provided an options string as instructed.
            opString = sys.argv[3]
    
           # Now look for a 4th arg. If you get one they've probably forgotten to wrap the options string in quotes...
            try:
                opString = sys.argv[4]
                print("Too many arguments provided. Did you forget to wrap your options string in quotes?")
                callHelp()
            except:
                pass #coolio
                
        except:
            # they didnt provide an options string....
            callHelp()
            
        # Everything seems to have been provided ok. Lets make a V4
        BUILDV4(file, opString)
            
    # They've used an incorrect argument 1
    else:
        callHelp()
    
            
    
    
