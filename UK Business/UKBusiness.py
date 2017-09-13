# -*- coding: utf-8 -*-

from databaker.framework import *
import zipfile, datetime, sys
import pandas as  pd


"""
Dictionary storing extraction details

-------
EXAMPLE
-------

optDict = {             
           '<Name of spreadsheet>.xlsx': {
                                          'LEFT':<dimension name for whevers going down column A>,
                                          'ABOVE_R2':<dimension name for whatevers on row 2>,
                                          'ABOVE_R3':<"None" to ignore/switch off, or whatevers on row 3>,
                                          'obI':'<row in column B where the observations start>,
                                          'gOver':<if there no georaphy in the sheet, specifiy it here (K02000001) otherwise None>
                                          'Entity Type':<"enterprise" or "local units", depends on the sheet>
                           },
"""

# Options for all extractions
optDict = {
            'Table 1 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'SIC07',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':None,
                            'Entity Type':'Enterprise'
                           },
            'Table 2 TAU.xlsx': {
                            'LEFT':'SIC07',
                            'ABOVE_R2':'Geography',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':None,
                            'Entity Type':'Enterprise'
                           },
            'Table 3 TAU.xlsx': {
                            'LEFT':'SIC07',
                            'ABOVE_R2':'Geography',
                            'ABOVE_R3':'Employment size band',
                            'obI':'5',
                            'gOver':None,
                            'Entity Type':'Enterprise'
                           },
            'Table 4 TAU.xlsx': {
                            'LEFT':'SIC07',
                            'ABOVE_R2':'Employment size band',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':"K02000001",
                            'Entity Type':'Enterprise'
                           },
            'Table 5 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'Employment size band',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':None,
                            'Entity Type':'Enterprise'
                        },
            'Table 6 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'SIC07',
                            'ABOVE_R3':None,
                            'obI':'5',
                            'gOver':None,
                            'Entity Type':'Enterprise'
                           },
            'Table 7 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'Turnover size Band',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':None,
                            'Entity Type':'Enterprise'
                           },
            'Table 8 TAU.xlsx': {
                            'LEFT':'SIC07',
                            'ABOVE_R2':'Geography',
                            'ABOVE_R3':'Turnover Size Band',
                            'obI':'5',
                            'gOver':None,
                            'Entity Type':'Enterprise'
                           },
            'Table 9 TAU.xlsx': {
                            'LEFT':'SIC07',
                            'ABOVE_R2':'Size band',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':"K02000001",
                            'Entity Type':'Enterprise'
                           },
            'Table 10 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'Employment size band',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':None,
                            'Entity Type':'Enterprise'
                           },
            'Table 11 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'Turnover Size Band',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':None,
                            'Entity Type':'Enterprise'
                           },
            'Table 12 TAU.xlsx': {
                            'LEFT':'SIC07',
                            'ABOVE_R2':'Legal status',
                            'ABOVE_R3':"Size Band",
                            'obI':'4',
                            'gOver':"K02000001",
                            'Entity Type':'Enterprise'
                           },
            'Table 13 TAU.xlsx': {
                            'LEFT':'SIC07',
                            'ABOVE_R2':'Legal status',
                            'ABOVE_R3':"Size Band",
                            'obI':'4',
                            'gOver':"K02000001",
                            'Entity Type':'Enterprise'
                           },
            'Table 14 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'Legal status',
                            'ABOVE_R3':"Size Band",
                            'obI':'4',
                            'gOver':None,
                            'Entity Type':'Enterprise'
                           },
            'Table 15 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'Legal status',
                            'ABOVE_R3':"Size Band",
                            'obI':'4',
                            'gOver':None,
                            'Entity Type':'Enterprise'
                           },
            'Table 16 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'SIC07',
                            'ABOVE_R3':None,
                            'obI':'5',
                            'gOver':None,
                            'Entity Type':'Local Units'
                           },
            'Table 17 TAU.xlsx': {
                            'LEFT':'SIC07',
                            'ABOVE_R2':'Geography',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':None,
                            'Entity Type':'Local Units'
                            },
            'Table 18 TAU.xlsx': {
                            'LEFT':'SIC07',
                            'ABOVE_R2':'Geography',
                            'ABOVE_R3':'Employment size band',
                            'obI':'5',
                            'gOver':None,
                            'Entity Type':'Local Units'
                           },
            'Table 19 TAU.xlsx': {
                            'LEFT':'SIC07',
                            'ABOVE_R2':'Employment size band',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':"K02000001",
                            'Entity Type':'Local Units'
                           },
            'Table 20 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'Employment size band',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':None,
                            'Entity Type':'Local Units'
                           },
            'Table 21 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'SIC07',
                            'ABOVE_R3':None,
                            'obI':'5',
                            'gOver':None,
                            'Entity Type':'Local Units'
                           },
            'Table 22 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'Employment size band',
                            'ABOVE_R3':None,
                            'obI':'3',
                            'gOver':None,
                            'Entity Type':'Local Units'
                           },
            'Table 23 TAU.xlsx': {
                            'LEFT':'SIC07',
                            'ABOVE_R2':'Legal status',
                            'ABOVE_R3':"Size Band",
                            'obI':'4',
                            'gOver':"K02000001",
                            'Entity Type':'Local Units'
                           },
            'Table 24 TAU.xlsx': {
                            'LEFT':'Geography',
                            'ABOVE_R2':'Legal status',
                            'ABOVE_R3':"Size Band",
                            'obI':'4',
                            'gOver':None,
                            'Entity Type':'Local Units'
                           },
            }


# Look for year explicitly passed to script
# If we dont have it, take it from the server clock
try:
    time = sys.argv[2]
except:
    time = datetime.datetime.now()
    time = time.year
    print('No time specified. Auto-setting year from server clock as: ', time)

# Extract everything    
z = zipfile.ZipFile(sys.argv[1])
allFiles = z.namelist()
# z.extractall() .... FOR NOW


# Extracts all the data from 1 sheet into a simple dataframe. Uses the filename to specifiy options from the dictionary.
def extract(file):
    
    tabs = loadxlstabs(file)
    
    # should only ever be 1 tab
    assert len(tabs) == 1, "Error, expecting one tab per sheet but getting {c}.".format(c=len(tabs))
    tab = tabs[0]

    # selections = always the same
    left = tab.excel_ref('A2').expand(DOWN).is_not_blank().is_not_whitespace()
    above = tab.excel_ref('B2').expand(RIGHT).is_not_blank().is_not_whitespace()
    
    # select observations. row that obs start on is gotten from the optDict
    obs = tab.excel_ref('B' + optDict[file]['obI']).expand(RIGHT).expand(DOWN).is_not_blank().is_not_whitespace()

    # Standard Dimensions. Names taken from optDict
    dimensions = [
            HDimConst("TIME", time),
            HDim(left, optDict[file]['LEFT'], DIRECTLY, LEFT),
            HDim(above, optDict[file]['ABOVE_R2'], CLOSEST, LEFT),  # also works as direcetly above in some cases
            HDimConst("Entity Type", optDict[file]['Entity Type'])
            ]
    
    # optionally have a third dimension if needed
    if optDict[file]['ABOVE_R3'] != None:
        thirdDim = tab.excel_ref('B3').expand(RIGHT).is_not_blank().is_not_whitespace()
        dimensions.append(HDim(thirdDim, optDict[file]['ABOVE_R3'], CLOSEST, LEFT))
        
    # Insert Geography where specified
    if optDict[file]['gOver'] != None:
        dimensions.append(HDimConst("Geography", optDict[file]['gOver']))
    
    # Convert selection into a conversionsegment option and bump straight into a simple pandas dataframe
    allData = ConversionSegment(tab, dimensions, obs).topandas()

    return allData
    

# Take 2 files, extract from them, merge and populate _codelist column where appropriate
def joinMerge(file1, file2):

    # iniital extractions, uses 1 or both files.
    if file2 == None:
        data = [extract(file1)]
    else:
        data = [extract(file1), extract(file2)]

    # use databaker writeCSV with hidden to-dataframe option
    # this'll concatente them into a single dataframe set out in a V4 structure.
    df = writeCSV('', data, toFrame=True)
    df.fillna('', inplace=True)
    
    # Fill in codelist columns
    if 'Legal status' in df.columns.values:
        df['Legal status_codelist'] = df['Legal status'].map(lambda x: x.split('-')[0].strip())
        # overWrite where its totol
        df['Legal status_codelist'][df['Legal status'] == 'Total'] = 'Total'
        
    if 'SIC07' in df.columns.values:
        df['SIC07_codelist'][df['SIC07'].map(lambda x: ':' not in x)] = df['SIC07'].str[:4].map(lambda x: x.split(' ')[0].strip())
        df['SIC07_codelist'][df['SIC07'].map(lambda x: ':' in x)] = df['SIC07'].str[:5].map(lambda x: x.split(':')[0].replace(':', '').strip())
        # overWrite where its totol
        df['SIC07_codelist'][df['SIC07'] == 'Total'] = 'Total'
        
    return df

# ------------------------------------
# Joining Files Ready for Publication
    

# UKBAA01a-Enterprise/local units by 4 Digit SIC and UK Regions
name = "UKBAA01a-Enterprise-local units by 4 Digit SIC and UK Regions.csv"
comboFrame = joinMerge("Table 2 TAU.xlsx", "Table 17 TAU.xlsx")
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAA01b-Enterprise/local units by Broad Industry Group and GB Local Authority Districts (including UK total)
name = "UKBAA01b-Enterprise-local units by Broad Industry Group and UK Local Authority Districts.csv"
comboFrame = joinMerge("Table 1 TAU.xlsx", "Table 16 TAU.xlsx")
# Business Area have spit the labels over multiple lines which messes with the dimensions..fix it
fixIt = {
    "01-03": "01-03 : Agriculture, forestry & fishing",
    "49-53" :"49-53 : Transport & Storage (inc. postal)",
    "55-56":"55-56 : Accommodation & food services",
    "58-63":"58-63 : Information & communication",
    "64-66":"64-66 : Finance & insurance",
    "69-75":"69-75 : Professional, scientific & technical",
    "77-82":"77-82 : Business administration & support services",
    "84":"84 : Public administration & defence",
    "90-99":"90-99 : Arts, entertainment, recreation & other"
      }
for fix in fixIt.keys():
    comboFrame['SIC07'][comboFrame['SIC07'].map(lambda x: fix in x)] = fixIt[fix]
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAA01b-Enterprise/local units by Broad Industry Group and GB Local Authority Districts (including UK total)
name = "UKBAA03-Enterprise-local units by Industry and Parliamentary Constituency.csv"
comboFrame = joinMerge("Table 6 TAU.xlsx", "Table 21 TAU.xlsx")
comboFrame.to_csv(name, encoding="utf-8", index=False)
# Business Area have spit the labels over multiple lines which messes with the dimensions..fix it
fixIt = {
    "01-03": "01-03 : Agriculture, forestry & fishing",
    "49-53" :"49-53 : Transport & Storage (inc. postal)",
    "55-56":"55-56 : Accommodation & food services",
    "58-63":"58-63 : Information & communication",
    "64-66":"64-66 : Finance & insurance",
    "69-75":"69-75 : Professional, scientific & technical",
    "77-82":"77-82 : Business administration & support services",
    "84":"84 : Public administration & defence",
    "90-99":"90-99 : Arts, entertainment, recreation & other"
      }
for fix in fixIt.keys():
    comboFrame['SIC07'][comboFrame['SIC07'].map(lambda x: fix in x)] = fixIt[fix]
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBABa-Enterprise/local units by 2 Digit SIC, Employment size band and Region
name = "UKBABa-Enterprise3local units by 2 Digit SIC, Employment size band and Region.csv"
comboFrame = joinMerge("Table 3 TAU.xlsx", "Table 18 TAU.xlsx")
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBABb-Enterprise/local units by 4 Digit SIC and Employment size band 4 19
name = "UKBABb-Enterprise-local units by 4 Digit SIC and Employment size band.csv"
comboFrame = joinMerge("Table 4 TAU.xlsx", "Table 19 TAU.xlsx")
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAC-Enterprise/local units by Industry, Employment size band and Legal status 12 23
name = "UKBAC-Enterprise-local units by Industry, Employment size band and Legal status.csv"
comboFrame = joinMerge("Table 12 TAU.xlsx", "Table 23 TAU.xlsx")
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAD01-Enterprise/local units by Employment size band and GB Local Authority Districts (including UK total)
name = "UKBAD01-Enterprise-local units by Employment size band and UK Local Authority Districts.csv"
comboFrame = joinMerge("Table 10 TAU.xlsx", "Table 22 TAU.xlsx")
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAD03-Enterprise/local units by Employment size band and Parliamentary Constituency
name = "UKBAD03-Enterprise-local units by Employment size band and Parliamentary Constituency.csv"
comboFrame = joinMerge("Table 5 TAU.xlsx", "Table 20 TAU.xlsx")
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAE-Enterprise/local units by Employment size band, Legal status and Region
name = "UKBAE-Enterprise-local units by Employment size band, Legal status and Region.csv"
comboFrame = joinMerge("Table 14 TAU.xlsx", "Table 24 TAU.xlsx")
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAF01-Enterprise by Turnover size band and UK Local Authority Districts (including UK total)
name = "UKBAF01-Enterprise by Turnover size band and GB Local Authority Districts.csv"
comboFrame = joinMerge("Table 11 TAU.xlsx", None)
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAF03-Enterprise by Turnover size band and Parliamentary Constituency
name = "UKBAF03-Enterprise by Turnover size band and Parliamentary Constituency.csv"
comboFrame = joinMerge("Table 7 TAU.xlsx", None)
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAGa-Enterprise by 2 Digit SIC, Turnover size band and Region
name = "UKBAGa-Enterprise by 2 Digit SIC, Turnover size band and Region.csv"
comboFrame = joinMerge("Table 8 TAU.xlsx", None)
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAGb-Enterprise by 4 Digit SIC and Turnover size band
name = "UKBAGb-Enterprise by 4 Digit SIC and Turnover size band.csv"
comboFrame = joinMerge("Table 9 TAU.xlsx", None)
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAF01-Enterprise by Turnover size band and GB Local Authority Districts (including UK total)
name = "UKBAH-Enterprise by Turnover size band, Legal status and Region.csv"
comboFrame = joinMerge("Table 15 TAU.xlsx", None)
comboFrame.to_csv(name, encoding="utf-8", index=False)


# UKBAF01-Enterprise by Turnover size band and GB Local Authority Districts (including UK total)
name = "UKBAI-Enterprise by Industry, Turnover size band and Legal status.csv"
comboFrame = joinMerge("Table 13 TAU.xlsx", None)
comboFrame.to_csv(name, encoding="utf-8", index=False)

 
















