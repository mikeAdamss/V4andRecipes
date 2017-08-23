# coding: utf-8

"""
CRIME datasets
--------------

Takes 6 files. Outputs 35 datasets.

input1 - Household Crime Incidence
input2 - Household Crime Prevalence 
input3 - Personal Crime Incidence
input4 - Personal Crime Prevalence
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

# collect the files from the execution command
houInc = sys.argv[1]
houPrev = sys.argv[2]
perInc = sys.argv[3]
perPrev = sys.argv[4]
charVarFile = sys.argv[5]
measVarFile = sys.argv[6]


# Lookup the cell value in the variable dict
def varLookup(cell):
    cell = varDict[cell]
    return cell


# Create initial dataframe. Filtered down to a single characteristic
def createInitialFrame(df, filterBy):
    df = df[df['CharacteristicVar'] == filterBy]    
    return df


# TODO - off the API, ...maybe better
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
    
    
# created the intial dataframe and populates the dimensions
def buildDims(df, charDim, ageAndSex=False):
    
    newDf = pd.DataFrame()
    newDf['V4_2'] = df['Estimate']
    newDf['Standard Error'] = df['StandardError']
    newDf['Unweighted Count'] = df['UnweightedCount']
    newDf['Time_codelist'] = 'Quarter'
    newDf['Time'] = df['Year'].astype(str) + ' Q' + df['Quarter'].astype(str)

    # geography in regions datafile needs different treatment  
    if charVar == 'gor': #i.e by region
        newDf['Geography_codelist'] = df['Characteristic'].apply(addGeographyCodes)
        newDf['Geography'] = ''
    else:   
        newDf['Geography_codelist'] = df['Geography'].apply(addGeographyCodes)
        newDf['Geography'] = ''

    newDf[charDict[charDim] + '_codelist'] = ''
    newDf[charDict[charDim]] =  df['Characteristic']
    
    newDf['Measurement Type_codelist'] = ''
    newDf['Measurement Type'] = df['MeasurementType']
    
    newDf['Crime Type_codelist'] = ''
    newDf['Crime Type'] = df['MeasurementVar'].apply(varLookup)
    newDf['Crime Type'] = newDf['Crime Type'].map(lambda x: x.strip())

    # ageAndSex = True, just means its a personal datafile not households
    if ageAndSex:
        newDf['Age_codelist'] = ''
        newDf['Age'] = df['Age']
        
        newDf['Sex_codelist'] = ''
        newDf['Sex'] = df['Sex']
    else:
        newDf['Household Type_codelist'] = ''
        newDf['Household Type'] = df['HouseholdType']
    
    # Catch and remove Age from "age group" dataset.
    # also filtered out duplicates arising from generic '16+' age grouping
    if 'Age group' in charDict[charDim]:
        newDf = newDf[newDf['Age'] != '16+']
        newDf = newDf.drop('Age', axis=1)
        newDf = newDf.drop('Age_codelist', axis=1)

    # drop 'All adults' in sex dimension as huge duplication otherwise
    if charDict[charVar] == 'Sex':
        newDf = newDf[newDf['Sex'] != 'All adults']

    # drop the specific "region" dimension" (as we've out the codes into geography_codelist already)
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


"""
Households - Executing the actual code
"""
# household
houInc = pd.read_csv(houInc)
houPrev = pd.read_csv(houPrev)
df = pd.concat([houInc, houPrev])

dsets = df['CharacteristicVar'].unique()
for charVar in dsets:
    oneDf = createInitialFrame(df, charVar)
    newDf = buildDims(oneDf, charVar)
    newDf.to_csv('V4_Household Crime_{c}.csv'.format(c=charDict[charVar].replace('/', ' ')), index=False)
    
    # check for duplication and throw an error if we find it
    newDf['dup'] = newDf.duplicated()
    newDf = newDf[newDf['dup'] == True]    
    if len(newDf) > 0:
            raise ValueError("Error, duplication found in dimension: ", charVar)

                             
"""
Personal - Executing the actual code
"""
perInc = pd.read_csv(perInc)
perPrev = pd.read_csv(perPrev)
df = pd.concat([perInc, perPrev])

dsets = df['CharacteristicVar'].unique()
for charVar in dsets:
    oneDf = createInitialFrame(df, charVar)
    newDf = buildDims(oneDf, charVar, ageAndSex=True)
    
    newDf.to_csv('V4_Personal Crime_{c}.csv'.format(c=charDict[charVar].replace('/', ' ')), index=False)
    
    # check for duplication and throw an error if we find it
    newDf['dup'] = newDf.duplicated()
    newDf = newDf[newDf['dup'] == True]    
    if len(newDf) > 0:
            raise ValueError("Error, duplication found in dimension: ", charVar)
            
    
