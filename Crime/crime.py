
# coding: utf-8

# In[15]:

"""
CRIME datasets
--------------

Takes 6 files. Outputs 35 datasets.

input1 - Household Crime Incidence
input2 - Household Crime Prevalence 
input3 - Personal Crime Incidence
input4 - Household Crime Prevalence
input5 - Characteristis reference
input6 - Measurement reference

description:
each dataset is filtered to one characteristic, and contains data from both Incidence and Prevalence
i.e - 'Household' in a filename means the data is drawn input 1 AND 2 from the above.

usage: 
python crime.py input1 input2 input3 input4 input5 input6

"""

import pandas as pd
import sys

houInc = sys.argv[1]
houPre2 = sys.argv[2]
perInc = sys.argv[3]
perPrev = sys.argv[4]
charVarFile = sys.argv[5]
measVarFile = sys.argv[6]


# In[12]:

import pandas as pd

# Lookup the cell value in the variable dict
def varLookup(cell):
    cell = varDict[cell]
    return cell


# Create initial Household file
def createInitialFrameHousehold(filterBy):
    files = [
        'Household crime_Incidence_England and Wales_2017Q1.csv',
        'Household crime_Prevalence_England and Wales_2017Q1.csv',
    ]

    dfList = []
    for f in files:

        obs_file = pd.read_csv(f)
        dfList.append(obs_file)

    df = pd.concat(dfList)
    df.fillna('', inplace=True)
    df = df[df['CharacteristicVar'] == filterBy]
    
    return df


# Create initial personal file
def createInitialFramePersonal(filterBy):
    files = [
        'Personal crime_Incidence_England and Wales_2017Q1.csv',
        'Personal crime_Prevalence_England and Wales_2017Q1.csv'
    ]

    dfList = []
    for f in files:

        obs_file = pd.read_csv(f)
        dfList.append(obs_file)

    df = pd.concat(dfList)
    df.fillna('', inplace=True)
    df = df[df['CharacteristicVar'] == filterBy]
    
    return df


def addGeographyCodes(cell):
    
    codes = {
          "United Kingdom":"K02000001",
          "Great Britain":"K03000001",
          "England and Wales":"K04000001",
          "England":"E92000001",
          "Wales":"W92000004",
          "Northern Ireland":"N92000002",
          "Scotland":"S92000003",
          "North East":"E12000001",
          "North West":"E12000002",
          "Yorkshire and The Humber":"E12000003",
          "East Midlands":"E12000004",
          "West Midlands":"E12000005",
          "East of England":"E12000006",
          "London":"E12000007",
          "South East":"E12000008",
          "South West":"E12000009"
        }
            
    if cell not in codes.keys():
        raise ValueError ("Unexpected geography, need the code for: ", cell)
    
    cell = codes[cell]
    
    return cell
    
    
# created the intial dataframe and populates the standard dims (obs, optional, time, geography)
def buildDims(df, charDim, ageAndSex=False):
    
    newDf = pd.DataFrame()
    newDf['V4_1'] = df['Estimate']
    newDf['Standard Error'] = df['StandardError']
    newDf['Time_codelist'] = 'Quarter'
    newDf['Time'] = df['Year'].astype(str) + ' Q' + df['Quarter'].astype(str)

    
    if charVar == 'gor': #i.e by regions
        newDf['Geography_codelist'] = df['Characteristic'].apply(addGeographyCodes)
        newDf['Geography'] = ''
    else:   
        newDf['Geography_codelist'] = df['Geography'].apply(addGeographyCodes)
        newDf['Geography'] = ''

    newDf[charDict[charDim] + '_codelist'] = '' # df['CharacteristicVar']
    newDf[charDict[charDim]] =  df['Characteristic']
        
    newDf['Measurement Type_codelist'] = ''
    newDf['Measurement Type'] = df['MeasurementType']
    
    newDf['Crime Type_codelist'] = ''
    newDf['Crime Type'] = df['MeasurementVar'].apply(varLookup)

    if ageAndSex:
        newDf['Age_codelist'] = ''
        newDf['Age'] = df['Age']
        
        newDf['Sex_codelist'] = ''
        newDf['Sex'] = df['Sex']
    else:
        newDf['Household Type_codelist'] = ''
        newDf['HouseholdType'] = df['HouseholdType']
    

    # Catch and remove Age after we've filtered out duplicates arising from generic '16+' age grouping
    if 'Age group' in charDict[charDim]:
        newDf = newDf[newDf['Age'] != '16+']
        newDf = newDf.drop('Age', axis=1)
        newDf = newDf.drop('Age_codelist', axis=1)

    if charDict[charVar] == 'Sex':
        newDf = newDf[newDf['Sex'] != 'All adults']

    if charDict[charVar] == 'Region':
        newDf = newDf.drop('Region_codelist', axis=1)
        newDf = newDf.drop('Region', axis=1)
        
    return newDf


"""
Creates a dictionary of <variable:English Label> from the charactersitics reference
"""
def read_characteristicsVar(varFile):
    df = pd.read_csv(varFile)
    dicto = pd.Series(df.CharacteristicLabel.values,index=df.CharacteristicVar).to_dict()
    return dicto


"""
Creates a dictionary of <variable:English Label> from the measure reference
"""
def read_measurementVar(varFile):
    df = pd.read_csv(varFile)
    dicto = pd.Series(df.MeasurementLabel.values,index=df.MeasurementVar).to_dict()
    return dicto


# Load the dictionanaries we'll need
charDict = read_characteristicsVar(charVarFile)
varDict = read_measurementVar(measVarFile)


# In[13]:

"""
Households - Executing the actual code
"""
# household
houInc = pd.read_csv('Household crime_Incidence_England and Wales_2017Q1.csv')
houPrev = pd.read_csv('Household crime_Prevalence_England and Wales_2017Q1.csv')
df = pd.concat([houInc, houPrev])

dsets = df['CharacteristicVar'].unique()
for charVar in dsets:
    df = createInitialFrameHousehold(charVar)
    newDf = buildDims(df, charVar)
    newDf.to_csv('V4_Household Crime_{c}.csv'.format(c=charDict[charVar].replace('/', ' ')), index=False)
    
    newDf['dup'] = newDf.duplicated()
    newDf = newDf[newDf['dup'] == True]    
    
    if len(newDf) > 0:
            print(charVar)


# In[14]:

"""
Personal - Executing the actual code
"""
perInc = pd.read_csv('Personal crime_Incidence_England and Wales_2017Q1.csv')
perPrev = pd.read_csv('Personal crime_Prevalence_England and Wales_2017Q1.csv')
df = pd.concat([perInc, perPrev])

dsets = df['CharacteristicVar'].unique()
for charVar in dsets:
    df = createInitialFramePersonal(charVar)
    newDf = buildDims(df, charVar, ageAndSex=True)
    
    newDf.to_csv('V4_Personal Crime_{c}.csv'.format(c=charDict[charVar].replace('/', ' ')), index=False)
    
    newDf['dup'] = newDf.duplicated()
    newDf = newDf[newDf['dup'] == True]    
    
    if len(newDf) > 0:
            print(charVar)
    

