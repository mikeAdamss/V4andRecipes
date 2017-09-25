# Splits the heaer value into seperate dimension items
def spreadHeader(header):
    header = str(header)
    
    # ...sigh
    header = header.replace('Ouward', 'Outward')
    
    
    cells = header.split(' ')
    
    # Drop pointless things
    cells = [x for x in cells if x != ':£m']  # dont care. 'Value' in a paired dimension covers it.

    
    # if their are any colons left its fully delimited, use it
    if len([x for x in header.split(' ') if ':' in x]) > 1:
        dimRow = header.split(':')
        dimRow = [x for x in dimRow if x != '£m'] # still dont care
    
    
    # From here its just text pasrsing to match up the different pattersn
    elif 'Total' in cells and '&' in cells:
        dimRow = [cells[0] + ' ' + cells[1] + ' ' + cells[2], cells[3] + ' ' + cells[4], cells[5], cells[6]]
        #assert len(cells) == 7, "Parse 1 wasting"
    
    
    elif '&' in cells:
        dimRow = [cells[0] + ' ' + cells[1] + ' ' + cells[2], cells[3], cells[4], cells[5]]
        #assert len(cells) == 6, "Parse 2 wasting"
    
    
    elif 'Other' in cells[0]:
        dimRow = [cells[0] + ' ' + cells[1], cells[2], cells[3], cells[4]]
        
        
    elif 'Total' in cells:
        dimRow = [cells[0] + ' ' + cells[1], cells[2], cells[3], cells[4]]
        #assert len(cells) == 5, "Parse 3 wasting"
    
    else:
        dimRow = [cells[0], cells[1], cells[2], cells[3]]
    
    return dimRow


# Spread the dim items from the header into V4 style
def colToV4(df, col):
    
    """
    The actual obsCol taken from the DF is the observation
    The header text is spread to create the dims
    """
    dimRow = spreadHeader(col)
    
    newDf = pd.DataFrame()
    
    newDf['V4_0'] = df[col][6:] # skip the CDID
    
    newDf['Time_codelist'] = 'Year'
    newDf['Time'] = df['Title'][6:]
    
    # Switch the time type if quartes are involved
    newDf['Time_codelist'][newDf['Time'].str.contains('Q')] = 'Quarter'
    
    newDf['Geography_codelist'] = 'K02000001'
    newDf['Geography'] = ''
    
    newDf['d1#_codelist'] = ''
    newDf['d1#'] = dimRow[0]
    
    newDf['d2#_codelist'] = ''
    newDf['d2#'] = dimRow[1]
    
    newDf['d3#_codelist'] = ''
    newDf['d3#'] = dimRow[2]
    
    # Optional. Not all columns have 4 dims so set to 'unspecified' to keep the shape
    if len(dimRow) < 4:
        newDf['d4#_codelist'] = ''
        newDf['d4#'] = 'UnSpecified'
    else:
        newDf['d4#_codelist'] = ''
        newDf['d4#'] = dimRow[3]
        
    
    newDf.fillna('', inplace=True)
    
    #newDf['sanityCheck'] = col

    return newDf


# Takes a dataframe and a dict of what we want the column headers
def buildHeaders(df, Ovr):
    newHeaders = []
    
    for key in Ovr.keys():
        if Ovr[key] == 'DROPME':
            df = df.drop(key, axis=1)
            df = df.drop(key + '_codelist', axis=1)
    
    # Replace/fix headers
    for col in df.columns.values:  # 1 at a time for order
        for key in Ovr.keys():
            if key in col:
                col = col.replace(key, Ovr[key])
        newHeaders.append(col)
    df.columns = newHeaders
    return df
        
                
import pandas as pd
import sys


##########
## MAIN ##
##########

"""
Create an inlcudes-everything "main" dataframe with holding dimensions d1#, d2#, d3#, d4# for topics.
Everything we want can be sliced out of that.
"""

inFile = sys.argv[1]

df = pd.read_csv(inFile)

mainDf = []
for col in df.columns.values[1:]:
    newDf = colToV4(df, col)
    mainDf.append(newDf)

mainDf = pd.concat(mainDf)
mainDf.fillna('', inplace=True) # pesky nans

# Get rid of blank observations
mainDf = mainDf[mainDf['V4_0'] != '']



###########################################################
### Getting Countries based Values and Numbers Datasets ###
###########################################################

#  Countries is all rows that dont have 'M&A' for topic d1#
df = mainDf[mainDf['d1#'].map(lambda x: x.strip() != 'M&A')]
Ovr = {
    'd1#':'Country',
    'd2#':'Flow',
    'd3#':'M&A',
    'd4#':'Measure',
}
df = buildHeaders(df, Ovr)

# Tidy up "Value:" into "Value" for the measure dimension
df['Measure'][df['Measure'] == 'Value:'] = 'Value'


# Now we split them into "Values" and "Numbers" dataset based on whats in the 'measure' dimension

# -- Value
valDf = df[df['Measure'] == 'Value']
valDf = valDf.drop('Measure', axis=1)  # drop 'measure', its served its purpose
valDf.to_csv('Mergers and Acquisition, Value of by County.csv')


# -- Numbers
valDf = df[df['Measure'] == 'Number']
valDf = valDf.drop('Measure', axis=1) # drop 'measure', its served its purpose
valDf.to_csv('Mergers and Acquisition, Number of by County.csv')



###############################
### Other Numeric Measures  ###
###############################

# Mergers and Acquisitions, Numbers
df = mainDf[mainDf['d3#'].map(lambda x: 'number' in x.strip().lower())]
Ovr = {
    'd1#':'DROPME',   # M&A
    'd2#':'Flow',   # 
    'd3#':'Transactions',   # 
    'd4#':'DROPME',
}
df = buildHeaders(df, Ovr)


# Split out mergers from disposals. Doing it here as some are not clearly delimited.
df['Merger or Acquisition_codelist'] = ''
df['Merger or Acquisition'] = ''
df['Merger or Acquisition'][df['Transactions'].map(lambda x: 'acqui' in x.lower())] = 'Acquisition'
df['Merger or Acquisition'][df['Transactions'].map(lambda x: 'disposal' in x.lower())] = 'Disposal'

# Get rid of' Number of companies acquired'. Its the sole romainint domestic item
df = df[df['Transactions'] != ' Number of companies acquired']

# Clean the text
removeCrap = [' Number of acquisitions ', ' Number of disposals ']
for rc in removeCrap:
    df['Transactions'] = df['Transactions'].map(lambda x: x.replace(rc,''))
df['Transactions'] = df['Transactions'].map(lambda x: x.replace('-', '').strip().title())

# Since I used title-caxe I need to correct the national acronyms
df['Transactions'][df['Transactions'] == 'In Eu'] = 'In EU'
df['Transactions'][df['Transactions'] == 'In Usa'] = 'In USA'
df['Transactions'][df['Transactions'] == 'Indirect Funded In Uk'] = 'Indirect Funded In UK'

# Get rid of (some of the) sparsity
df['Transactions'][df['Transactions'] == 'Number Of Acquisitions'] = 'Number Of'
df['Transactions'][df['Transactions'] == 'Number Of Disposals'] = 'Number Of'


# whitespace
df['Flow'] = df['Flow'].map(lambda x: x.strip())

listo = df['Flow'].unique()
assert '' not in listo, "Flow is blank! Should be acquisition or disposal, contains: " + df['Flow'].unique()

df.to_csv('Mergers and Acquisitions - Numbers.csv', index=False)



#############################
### Other Value Measures  ###
#############################

# Mergers and Acquisitions, Value
df = mainDf[mainDf['d3#'].map(lambda x: 'value' in x.strip().lower())]
Ovr = {
    'd1#':'DROPME',   # M&A
    'd2#':'DROPME',   # 
    'd3#':'Transactions',   # 
    'd4#':'DROPME',
}
df = buildHeaders(df, Ovr)


# Need to get Acqusitions and Displosals from text as its not a dimension in all cases
df['Flow_codelist'] = ''
df['Flow'] = ''
df['Flow'][df['Transactions'].map(lambda x: 'acqui' in x.lower())] = 'Acquisition'
df['Flow'][df['Transactions'].map(lambda x: 'disposal' in x.lower())] = 'Disposal'

# Get rid of generic stock data. Doesn't the the cube structure
for rm in [' Value of ordinary shares ', ' Value of preference & loan stock ']:
    df = df[df['Transactions'] != rm]

# Clean the text
removeCrap = [' Value of acquisitions ', ' Value of disposals ']
for rc in removeCrap:
    df['Transactions'][df['Transactions'] == rc] = 'Total Value'  # it its *just* something from the list its a total
    df['Transactions'] = df['Transactions'].map(lambda x: x.replace(rc,''))  # otherwise its in the way
df['Transactions'] = df['Transactions'].map(lambda x: x.replace('-', '').strip().title())

# Since I used title-caxe I need to correct the national acronyms
df['Transactions'][df['Transactions'] == 'In Eu'] = 'In EU'
df['Transactions'][df['Transactions'] == 'In Usa'] = 'In USA'
df['Transactions'][df['Transactions'] == 'Indirect Funded In Uk'] = 'Indirect Funded In UK'

listo = df['Flow'].unique()
assert '' not in listo, "Flow is blank! Should be acquisition or disposal, contains: " + df['Flow'].unique()

df.to_csv('Mergers and Acquisitions - Values.csv', index=False)


