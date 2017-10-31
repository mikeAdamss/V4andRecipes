# -*- coding: utf-8  -*-
from bs4 import BeautifulSoup
import pandas as pd
import zipfile, sys


"""
Beta Build
----------
For the purposes of the CMD beta we've combined bearly all NPP data into a single dataset.

We have not used cross border rates.
We have also ended the age ranges at 104, as there are conflicting ranges above that number.
Periods with 2 year values i.e 2014-2015 have been slisced to the first value, i.e 2014.

Dates after 2039 (main population estimates) have been removed.

"""

# Apply the conditions explained above to the data
def betaBuild(v4):

    # Remove cross border rates
    remove = ['En_Wa', 'En_Sc', 'En_Ni', 'Wa_En', 'Wa_Sc', 'Wa_Ni', 'Sc_En', 'Sc_Wa', 'Sc_Ni', 'Ni_En', 'Ni_Wa', 'Ni_Sc']
    v4 = v4[v4['Time'].map(lambda x: x.strip() not in remove)]
            
    # Same thing for age
    unwantedAge = ['Birth', '105+', '105 - 109', '110 and over']
    v4 = v4[v4['Age'].map(lambda x: x.strip() not in unwantedAge)]
    v4 = v4[v4['Age'].map(lambda x: int(x) < 105)]

    # sort out time
    v4['Time'] = v4['Time'].map(lambda x: x.split(' ')[0].strip())
    
    # dicey .....
    v4 = v4[v4['Time'].map(lambda x: int(x) < 2040)]
    
    # Drop gender "3"
    v4 = v4[v4['Sex'].map(lambda x: x != "3" and x != 3)]
    
            
    return v4
    
    
    

# get the proje tion tyoe for a given xml
def getProjectionType(XMLsoup):
    
    allTabs = XMLsoup.find_all("worksheet")
    for at in allTabs:
        if at.attrs['ss:name'] == 'Contents':
            contents = at
            
    rows = contents.find_all('row')
    
    for r in rows:
        if 'Projection type:' in r.text:
            return r.find_all('data')[1].text
            
         

# TODO - DRY, this is basically same as the above
# get the geographic coverage for a given xml
def getGeoCoverage(XMLsoup):
    
    allTabs = XMLsoup.find_all("worksheet")
    for at in allTabs:
        if at.attrs['ss:name'] == 'Contents':
            contents = at
            
    rows = contents.find_all('row')
    
    for r in rows:
        if 'Coverage' in r.text:
            return r.find_all('data')[1].text  
    
    

# Returns a list of dictionaries, one for each tab. 
# Each dict has the projection type and a dataframe equating to one "tab" worth of data
def dataFramesFromXML(XMLsoup, tabDict):
    
    # get the projection type for the XML file
    projectionType = getProjectionType(XMLsoup)  
    
    geoCoverage = getGeoCoverage(XMLsoup)
    
    if geoCoverage == "United Kingdom (uk)":
        geoCoverage = "K02000001"
    else:
        raise ValueError('Expecting geographic area of "United Kingdom (uk)" in the contents tab but its not there. Aborting.')
    
    
    allFrames = []
    for tab in tabDict:

        currentSheet = XMLsoup.find("worksheet",{"ss:name":tab['name']})
        cells = currentSheet.find_all('cell')
              
        currentRow = 0
        dFrame = {}
        mapValues = {}
            
        for c in cells:
                
            # First run down the row is getting column headers mapped. Then we fill them.
            if currentRow < int(tab['rowCount']):
                mapValues.update({currentRow:c.text.strip()})
                dFrame.update({c.text.strip():[]})
            else:
                colName = mapValues[currentRow % int(tab['rowCount'])]
                dFrame[colName].append(c.text.strip())
            currentRow += 1 
        
        allFrames.append({'df':pd.DataFrame.from_dict(dFrame), 'coverage':geoCoverage, 'projection':projectionType, 'tab':tab['name']})       
        
    return allFrames
    
    
    
"""
Extracts name and number of rows for each "tab" of data in the xml file

return [
        {'name':'Births', 'rowCount':27},
        etc..
        ]
"""
def tabDetailsFromXML(XMLsoup):
    
    sheets = XMLsoup.find_all('namedrange')
    
    tabs = []
    for sheet in sheets:
        
        ref = sheet.attrs['ss:refersto'].split(':')[-1]
        ref = ref.split('C')[1]

        details = {
            'name':sheet.attrs['ss:name'].strip(),
            'rowCount':ref
                  }
        tabs.append(details)
    
    return tabs
    
    


# Build a v4 file from our list of dataframes
def buildV4(dfList):
    
    v4ToJoin = []
    for dfItem in dfList:
        v4Pieces = []
        
        df = dfItem['df']
        tabName = dfItem['tab']
        projection = dfItem['projection']
        coverage = dfItem['coverage']
        
        for col in df.columns.values:
            if col.lower().strip() != 'sex' and col.lower().strip() != 'age' and  col.lower().strip() != 'flow':
                
                newDf = pd.DataFrame()
                newDf['V4_0'] = df[col]
                
                newDf['Time'] = col
                newDf['Time_codelist'] = 'Year'

                newDf['Geography'] = ''
                newDf['Geography_codelist'] = coverage
                
                newDf['Sex_codelist'] = ''
                newDf['Sex'] = df['Sex']
                newDf[newDf['Sex'] == 1] = 'Male'
                newDf[newDf['Sex'] == 2] = 'Female'
                
                newDf['Age_codelist'] = ''
                newDf['Age'] = df['Age']
                
                newDf['Projection Type_codelist'] = ''
                newDf['Projection Type'] = projection
                    
                newDf['Population Measure_codelist'] = ''
                newDf['Population Measure'] = tabName
                
                if 'migration' in tabName.lower() and len(newDf) > 1:
                    newDf['Population Measure'] = newDf['Population Measure']  + "(" + df['Flow'] + ")"

                v4Pieces.append(newDf)
        v4ToJoin.append(pd.concat(v4Pieces))
        print(v4ToJoin[-1]['Time'].unique())
        
    return pd.concat(v4ToJoin)



def oneFileToV4(inFile): 

    with open(inFile, 'r') as f:

        # Parse with bs4
        soup = BeautifulSoup(f, 'lxml')
        
        # Get the tabs
        tabDict = tabDetailsFromXML(soup)
        
        # Get the data for each tab into a dataframe
        dfList = dataFramesFromXML(soup, tabDict)
        
        # Build V4
        v4 = buildV4(dfList)
    
    return v4


def extractFromZip(filename, oneCube=False):
    
    z = zipfile.ZipFile(filename)
    z.extractall()
    xmlFiles = [x for x in z.namelist() if '.xml' in x]
    
    allV4 = []
    for xml in xmlFiles: 
        v4 = oneFileToV4(xml)
        allV4.append(v4)
        
    final = pd.concat(allV4)
    
    
    # ##################################################
    # IMPORTANT !!!!!
    # Ad-hoc alterations/removals to make a better cube.
    # Needs BA apprival for anything beyond tesing
    # ##################################################
    if oneCube:
        final = betaBuild(final)
    

    final.to_csv('Experimental-National Population Projections.csv', index=False)
    

if __name__ == "__main__":
    inFile = sys.argv[1]
    extractFromZip(inFile)





    
    
    