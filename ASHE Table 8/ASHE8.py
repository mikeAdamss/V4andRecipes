# -*- coding: utf-8 -*-

"""
Databaker script to create dataset: ASHE Table 7

Uses all tabs from an ASHE table zip file, 16 files for Earnings, the remaining 6 for Hours

example zip url: 


Logic
------
ASHE is amost perfect structure wise with all visual relationships being shown in columns A and B.

Therefore rather than databaking the wholelot cell by cell, we're loading each tab into a dataframe then using databaker 
to establish those viusal relationships and "correct" the dataframe. Once fully described its far more 
efficient to flatten (1000's of cells per operation rather than 1000's of individual operations)

"""

from databaker.framework import *
import pandas as pd
from collections import OrderedDict



# Codes for where we just have a place name
# The presence of "England" in "England and Wales" can cause replacment confusion so using two passes
codeNames = OrderedDict({
          "United Kingdom":"K02000001",
          "Great Britain":"K03000001",
          "England and Wales":"K04000001",
          "Wales / Cymru":"W92000004",
          "Northern Ireland":"N92000002",
          "Scotland":"S92000003",
          "North East":"E12000001",
          "North West":"E12000002",
          "Yorkshire and The Humber":"E12000003",
          "East Midlands":"E12000004",
          "West Midlands":"E12000005",
          "London":"E12000007",
          "South East":"E12000008",
          "South West":"E12000009"
        })

smallCodes = OrderedDict({
                        "East":"E12000006",
                        "England":"E92000001",
                            })

# probably easier to derive but this keeps the code simpler
# also, can compare tabs to this for validation
findGenderWork = {
    'All':{'gender':'All', 'work':'All'},
    'Male':{'gender':'Male', 'work':'All'},
    'Female':{'gender':'Female', 'work':'All'},
    'Full-Time':{'gender':'All', 'work':'Full-Time'},
    'Part-Time':{'gender':'All', 'work':'Part-Time'},
    'Male Full-Time':{'gender':'Male', 'work':'Full-Time'},
    'Male Part-Time':{'gender':'Male', 'work':'Part-Time'},
    'Female Full-Time':{'gender':'Female', 'work':'Full-Time'},
    'Female Part-Time':{'gender':'Female', 'work':'Part-Time'}
}

headers = [
    'delete1',
    'Geography',
    'Number of Jobs (thousands)',
    'Median',
    'Annual Percentage Change',
    'Mean',
    'Annual Percentage change',
    '10', '20', '25', '30', '40', '60', '70', '75', '80', '90',
    'drop1', 'drop2', 'drop3'
]


# functions


# the number of column headers bring picked up can vary slightly over time
# nothing serious but + or - 1 junk column does happen. Need to accomdate it
def tryHeaders(df, headers):

    if len(df.columns.values) < len(headers):
        headers = headers[:-1]
    
    if len(df.columns.values) > len(headers):
        headers.append('dopr4')

    return headers

    
    
# get the uqiue descriptor of this spreadsheet
# i.e ' Get 'Working Pay - Gross' out of the filename 'Work Geography Table 7.1a   Weekly pay - Gross 2013.csv' 
def unique_me(filename):
    filenames = filename.split('.')
    del filenames[0]
    filenames = filenames[0]
    filenames = filenames[3:-5]
    filenames = filenames.strip()
    return filenames


# take a clean dataframe of observations and another of CVs and build a v3 output
def makeV4(cvDf, df):

    obs_file_parts = []
    wanted = [ '10', '20', '25', '30', '40', '60', '70', '75', '80', '90']
    wanted.append('Mean')
    wanted.append('Median')
    
    # get rid of headers
    df = df[4:]
    
    for col in wanted:
        newDf = pd.DataFrame()
        newDf['V4_2'] = df[col]
        newDf['Data_Marking'] = ''
        newDf['CV'] = cvDf[col]
        
        newDf['Time_codelist'] = 'Year'
        newDf['Time'] = df['Time']
        
        newDf['Geography_codelist'] = df['Geography']
        newDf['Geography'] = ''
        
        newDf['Earnings_codelist'] = ''
        newDf['Earnings'] = df['Earnings']
        
        newDf['Gender_codelist'] = ''
        newDf['Gender'] = df['Gender']
        
        newDf['Working Pattern_codelist'] = ''
        newDf['Working Pattern'] = df['Working Pattern']
        
        newDf['Earnings Statistics_codelist'] = ''
        newDf['Earnings Statistics'] = col

        obs_file_parts.append(newDf)
        
    obs_file = pd.concat(obs_file_parts)
    obs_file.fillna('', inplace=True)
    
    # remove any blank obs (data makers and obs are still in one column at this point)
    oldLen = len(df)
    obs_file = obs_file[obs_file['V4_2'].astype(str) != '']
                        
    # split obs and data markers
    dMarkers = ['x', '..', ':', '-']
    obs_file['Data_Marking'][obs_file['V4_2'].map(lambda x: x in dMarkers)] = obs_file['V4_2']
    obs_file['V4_2'][obs_file['V4_2'].map(lambda x: x in dMarkers)] = ''
    
    return obs_file
    
    
import requests, zipfile, io, sys

z = zipfile.ZipFile(sys.argv[1])
allFiles = z.namelist()

# get the non cv files for the EARNINGS dataset
nonCvFiles = [x for x in allFiles if 'CV.' not in x]
hoursFiles = [x for x in nonCvFiles if '.9' in x or '.10' in x or '.11' in x]
earningsFiles = [x for x in nonCvFiles if '.9' not in x and '.10' not in x and '.11' not in x]

   
        
hoursRun=True
for dset in [hoursFiles, earningsFiles]:
    
    doneTabs = []
    for ncf in dset:

        # load into databaker
        xl = pd.ExcelFile(z.open(ncf))
        tabs = xl.sheet_names

        # clip the year out of the name (last 4 letters not counting the file extension)
        time = ncf.split(' ')[-1][:-4]

        for tab in tabs:

            if 'notes' not in tab.lower():

                # load the current tab into a dataframe
                df = xl.parse(tab)
                
                # headers +/- 1 (some inconsistencies over time)
                df.columns = tryHeaders(df, headers)

                # get rid of footer and below
                footer = df[df['delete1'] == 'Not Classified']
                assert len(footer) == 1, "Cannot find 'Not Classified'. Unable to find end of data table"
                footY = footer.index[0] # its a tuple-like object (int, type)
                df = df[:footY]
                
                df.fillna('', inplace=True)  # get rid of the nans

                # Add gender and working pattern
                df['Gender'] = findGenderWork[tab]['gender']
                df['Working Pattern'] = findGenderWork[tab]['work']

                # iterate rows
                # TODO = kinda slow
                df['Geography'][df['Geography'] == ''] = df['delete1']
                for code in codeNames.keys():
                    df['Geography'] = df['Geography'].map(lambda x: x.replace(code, codeNames[code]))
                    
                for code in smallCodes.keys():
                    df['Geography'] = df['Geography'].map(lambda x: x.replace(code, smallCodes[code]))


                # add the time
                df['Time'] = time

                # get hours worked
                hoursOrEarnings = unique_me(ncf)
                df['Earnings'] = hoursOrEarnings

                """
                Use the Special Phrase(i.e "Weekly Pay Gross") to split to the table number
                use that to load the CV version of the table
                """
                Cvfile = ncf.split(hoursOrEarnings)[0]
                replaceText = Cvfile.split(' ')[-4]
                Cvfile = ncf.replace(replaceText, replaceText.replace('a', 'b'))
                Cvfile = Cvfile.replace('.x', ' CV.x')

                # load Cv excel
                xl2 = pd.ExcelFile(z.open(Cvfile))
                cvDf = xl2.parse(tab)
                cvDf = cvDf[4:footer.index[0]]
                cvDf.columns = tryHeaders(cvDf, headers)


                olDf = df

                df = makeV4(cvDf, df)

                doneTabs.append(df)

    df = pd.concat(doneTabs)

    if hoursRun:
        ds = 'Hours'
        hoursRun = False
    else:
        ds = 'Earnings'
    
    if 'provisional' in sys.argv[1].lower():
        prov = '_Provisional_'
    else:
        prov = ''
        
    df.to_csv('ASHE_8_{ds}{p}{t}.csv'.format(ds=ds, t=time, p=prov), encoding="utf-8", index=False)
