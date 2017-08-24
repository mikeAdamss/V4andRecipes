# -*- coding: utf-8 -*-
"""
Created on Thu Aug 24 10:48:37 2017

@author: Mike


SAPE script. 

These files get rather large so script is set to read (and check) the file in chunks.

"""

import pandas as pd
import os, sys


# Turn off "setting with copy" wanrings to mute false positives
pd.options.mode.chained_assignment = None  # default='warn'

# Actually do the processing
def processChunk(chunk, df, time, fileCount, cutOff):
    newDf = pd.DataFrame()
    
    # Find which column is age and sex etc
    for i in range(0, len(chunk.columns.values)):
        
        # find age
        if chunk.columns.values[i].lower().strip() == 'age':
            ageCol = i
        
        # find sex
        if chunk.columns.values[i].lower().strip() == 'sex':
            sexCol = i
        
    newDf['V4_0'] = chunk[chunk.columns.values[3]]
    newDf['Time_codelist'] = 'Year'
    newDf['Time'] = time
    newDf['Geography_codelist'] = chunk[chunk.columns.values[0]]
    newDf['Geography'] = ''
    newDf['Age_codelist'] = ''
    newDf['Age'] = chunk[chunk.columns.values[ageCol]]
    newDf['Sex_codelist'] = ''
    newDf['Sex'] = chunk[chunk.columns.values[sexCol]]

    df = pd.concat([df, newDf])
    
    if len(df) > cutOff:
        tidyandOutput(df, fileCount)
        df = pd.DataFrame()
        fileCount += 1
    
    return df, fileCount



# main file processing
def process(chunksize=99999999999, cutOff=9999999999):

    # simple feedback
    print('Processing in chunks sized:', chunksize, 'bytes.')
    print('Output chunks after:', cutOff, 'rows processed.')
    
    # Out blank dataframe
    df = pd.DataFrame()
    
    # filecount for outputs
    fileCount = 0
    
    # Gather all appropriate CSVs in our directory
    files = [f for f in os.listdir('.') if os.path.isfile(f) and '.csv' in f and 'SAPE_Output' not in f]
    
    for filename in files:
        
        headers = pd.read_csv(filename, nrows=1)
        headers = headers.columns.values
    
        for i in range(2010, 2030):
            if str(i) in filename:
                time = str(i).replace('.0', '') # replace, just in case
    
        for chunk in pd.read_csv(filename, chunksize=chunksize, usecols=headers):    
            df, fileCount = processChunk(chunk, df, time, fileCount, cutOff=cutOff)
                
    return df, fileCount



# helper to run main script with first, second or both arguments provided
def runSplitCommands(commands):
    
    hasChunk = False
    hasMax = False

    # If both arguments specified
    if len(commands.split(' ')) == 2:
        for com in commands.split(' '):
            if 'chunksize' in com:
                hasChunk = True
                chunksize = int(com.split('=')[1].strip())
            elif 'chunkcutoff' in com:
                hasMax = True
                cutOff = int(com.split('=')[1].strip())
            
        # run or throw error for bad arguments
        if hasChunk and hasMax:
            df, fileCount = process(chunksize=int(chunksize), cutOff=int(cutOff))
        else:
            raise ValueError ("Arguments can only be be 'chucksize=xxxx' and/or 'rowmax=xxxxx'")
        
    elif 'chunksize' in commands:
        df, fileCount = process(chunksize=int(commands.split('=')[1]))
    elif 'chunkcutoff' in commands:
        df, fileCount = process(cutOff=int(commands.split('=')[1]))
    else:
        raise ValueError ("Arguments can only be be 'chucksize=xxxx' and/or 'rowmax=xxxxx'")
    
    return df, fileCount



# tidy up labels - much quicker per output df than pre chunk
def tidyandOutput(df, fileCount):

    try:
        # Here, as its quicker than doing per-chunk    
        df['Sex'][df['Sex'] == 1] = 'Male'
        df['Sex'][df['Sex'] == 2] = 'Female'
        df['Sex'][df['Sex'] == 3] = 'All'
    except:
        print('Failed on: ', df.columns.values, fileCount)
        
    if fileCount > 0:
        df.to_csv('SAPE_Output_{na}{no}.csv'.format(na=name,no=fileCount), index=False)
    else:
        df.to_csv('SAPE_Output_{na}.csv'.format(na=name), index=False)



# #####
# MAIN
# #####

name = sys.argv[1]

# filecount (for multiple outputs)
fileCount = 1
    
# use manually-chosen chunksize if provided
chucksize = ''
maxrows = ''

# TODO ...bleurgh
try:
    commands = sys.argv[2]
    try:
        commands = commands + ' ' + sys.argv[3]
        df, fileCount = runSplitCommands(commands)
    except:
        df, fileCount = runSplitCommands(commands)
except:
    print('Default Parameters Used.')
    df, fileCount = process()

# Output any leftover rows
if len(df) > 0:
    tidyandOutput(df, fileCount)

