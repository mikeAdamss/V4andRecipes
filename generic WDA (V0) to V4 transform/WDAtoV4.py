# encoding: utf-8
import pandas as pd
import sys

CONSTANTDIMS = ('Time_codeList', 'Time', 'Geography_codelist', 'Geography')

HEADERS = [
        'observation',
        'data_marking',
        'statistical_unit_eng',
        'statistical_unit_cym',
        'measure_type_eng',
        'measure_type_cym',
        'observation_type',
        'empty',
        'obs_type_value',
        'unit_multiplier',
        'unit_of_measure_eng',
        'unit_of_measure_cym',
        'confidentuality',
        'empty1',
        'geographic_area',
        'empty2',
        'empty3',
        'time_dim_item_id',
        'time_dim_item_label_eng',
        'time_dim_item_label_cym',
        'time_type',
        'empty4',
        'statistical_population_id',
        'statistical_population_label_eng',
        'statistical_population_label_cym',
        'cdid',
        'cdiddescrip',
        'empty5',
        'empty6',
        'empty7',
        'empty8',
        'empty9',
        'empty10',
        'empty11',
        'empty12'
        ]
        
TOPIC = [
        'dim_id_',
        'dimension_label_eng_',
        'dimension_label_cym_',
        'dim_item_id_',
        'dimension_item_label_eng_',
        'dimension_item_label_cym_',
        'is_total_',
        'is_sub_total_',
           ]

           
# we also need to check we dont have completly empty dimensions....apparently
# funtion will Error and flag an instance of completely empty dimension item columns
def FlagEmptyDims(df):
    headers = [x for x in df.columns.values if 'dim_item_id' in x]
    for h in headers:
        if df[h].unique()[0] == '':
            raise ValueError ("Column '{c}' is required and appears to be blank. Needs to be populated or removed.".format(c=h))

            
# unfortunetly the labelling convention is out on some files
# we need to reqrite the headers to standard as a precausion
def rewriteHeaders(df):
    
    numDims = numberOfDims(df)
    newHeaders = HEADERS
    
    for i in range(0, numDims):
        for subCol in TOPIC:
            newHeaders.append(subCol + str(i+1).replace('.0', ''))        
        
    assert len(newHeaders) == len(df.columns.values), "Cannot write. Column header mismatch when overwriting standard WDA headings"

    df.columns = newHeaders

    return df
    


# checks the Dimension columns, looking for invalid multi-cube files
def checkValidTuple(df, colTuple):

    # colTuple = ('dim_id_1', 'dimension_label_eng_1', 'dim_item_id_1', 'dimension_item_label_eng_1')
    
    # dim id
    uniqueIn1 = df[colTuple[0]].unique()
    if len(uniqueIn1) != 1:
        raise ValueError ("Dimension identified by multiple IDs, this appears to be a multiple-datacube dataset and cannot be conoverted in this manner.", uniqueIn1)

    # dim label
    uniqueIn2 = df[colTuple[1]].unique()
    if len(uniqueIn2) != 1:
        raise ValueError ("Dimension identified by multiple Lables, this appears to be a multiple-datacube dataset and cannot be conoverted in this manner", uniqueIn2)


        
# Works out number of dimensions based on standard WDA column spread
def numberOfDims(df):
    
    # get number of topic dimensions
    numDims = len(df.columns.values) - 35

    # check correct column count
    if numDims % 8 != 0:
        raise ValueError ("Input Dataset does not have a valid number of columns")

    numDims = int(numDims / 8)
    
    return numDims

    

# What optional fields do we need pre-time?
def discoverFields(df):
    
    # initial
    fieldsNeeded = []

    # Do we have data markings?
    if len(df['data_marking'][df['data_marking'] != ''].unique()) > 0:
        fieldsNeeded.append('Data Marking')

    # Do we have quality measures in play?
    QAcount = df['observation_type'][df['observation_type'] != ''].unique()
    if len(QAcount) > 0: 
        
        # if should be 1!
        assert QAcount == 1, "You should not have more than one type of quality measure in a WDA/V0 file!?" 
        fieldsNeeded.append(QAcount[0])

    return fieldsNeeded



# Populate the standard dimensions
def populateStandardDims(df):

    # list of additional fields (data marking, CV etc ...)
    fieldsNeeded = discoverFields(df)
    
    # create new dataframe and add obs
    newDf = pd.DataFrame()
    newDf['V4_' + str(len(fieldsNeeded))] = df['observation']
    
    # add data marking if applicable
    if 'Data Marking' in fieldsNeeded:
        newDf['Data Marking'] = df['data_marking']

    # add other pre-time fields
    for newField in fieldsNeeded:
        if newField != 'Data Marking':
            newDf[newField] = df['obs_type_value']

    return newDf



# populate time and geaography
def timeAndGeography(df, V4):
    
    # copy in wanted columns
    V4['Time_codelist'] = df['time_type']
    V4['Time'] = df['time_dim_item_label_eng']
    V4['Geography_codelist'] = df['geographic_area']
    V4['Geography'] = ''
    
    return V4
    

    
# return col headers as tuples for WDA 8 col dimension 
# example return: ('dim_id_1', 'dimension_label_eng_1', 'dimension_item_id_1', 'dimension_item_label_eng_1')
def range8Index(df, i):    
    
    # get the x index for each "first" column of each 8 columns dimension pattern
    dimIndex = 35 + (8 * (i))
    
    # use this to slice the 8 columsn we want
    headers = list(df.columns.values)[dimIndex:dimIndex+8]
    
    # put the lot into a tuple
    colTuple = (headers[0], headers[1], headers[3], headers[4])
    
    return colTuple



# populate topic dimensions
def populateTopics(df, V4):
 
    hasCodeList = {}
    for i in range(0, numberOfDims(df)): # for each topic

        # example return: ('dim_id_1', 'dimension_label_eng_1', 'dimension_item_id_1', 'dimension_item_label_eng_1')
        splitCols = range8Index(df, i)
        
        checkValidTuple(df, splitCols) # validate, because a multicube dataset wont work
        
        # dimension ID. Should always be one but check anyway
        uniqueItems = df[splitCols[0]].unique()
        if len(uniqueItems) > 1:
            raise ValueError ('Multiple dimension Ids identified in column: ', splitCols[0])
        else:
            CL_header = uniqueItems[0]
                
        # dimension Label. Should always be one but check anyway
        uniqueItems = df[splitCols[1]].unique()
        if len(uniqueItems) > 1:
            raise ValueError ('Multiple dimension Labels identified in column: ', splitCols[1])
        else:
            dim_header = uniqueItems[0]
        
        # if dim id and label are identical, add the _codelist postfix
        if dim_header != CL_header:
            hasCodeList.update({dim_header:CL_header})
            CL_header = dim_header + '_codelist'
            
        # if the item_id and item_label cols match blank the codelist. Otherwise just output
        if df[splitCols[2]].all() == df[splitCols[3]].all():
            V4[CL_header] = ''
        else:
            V4[CL_header] = df[splitCols[2]]
        V4[dim_header] = df[splitCols[3]]   
   
    # if we encountered codelsits, print them to screen
    # ... this is just to make documenting easy the first time. Usually commented out.
    #if len(hasCodeList) > 0:
    #    print(hasCodeList)
                
    return V4
    

    
# Main conversion functions, holds an call all of the above
def conversion(df, geo=None):
    
    # obs and optional columns
    V4 = populateStandardDims(df)

    # time and geography
    V4 = timeAndGeography(df, V4)
    
    # topic dimensions
    V4 = populateTopics(df, V4)
    
    if geo is not None:
        V4['Geography_codelist'] = geo
    
    return V4


# Dealing with deviations from the typical code:label pattern
def presentationChange(myV4, presentation):
    """
    Special handling triggered by using the "presentation" keyword
    cannot be applied on the command line.
    
    ---------------------------------------------------------------
    This is for dealing with non standard appraoched to dimensions/labels that needed to be taken with some
    WDA inputs. 
    
    Example, cases where the files are mapped WDACodes:InternalCodes rather than codes:labels.
    
    Options are:
    
    None:              default. This function is not triggered.
    justCodes:         as expected then blank the labels column
    justLabels:        as expected then blank the codes column
    labelToCodes:      put the labels column in codes then blank the labels column
    codesToLabels:     put the codes column in labels then blank the codes column
    
    These circumstances are all rare but can occur. In 99%+ of use-cases the default "None" will be fine
    and this function will never be called.
    """
    
    # For every dimension (defined as two columns) after "Geography"
    for i in range(myV4.columns.get_loc('Geography')+1, len(myV4.columns.values), 2):
        
        codeCol = myV4.columns.values[i]
        labelCol = myV4.columns.values[i+1]
    
        if presentation == 'justCodes':
            myV4[labelCol] = ''
            
        elif presentation == 'justLabels':
            myV4[codeCol] = ''
            
        elif presentation == 'labelsToCodes':
            myV4[codeCol] = myV4[labelCol]
            myV4[labelCol] = ''
            
        elif presentation == 'codesToLabels':
            myV4[labelCol] = myV4[codeCol]
            myV4[codeCol] = ''

        else:
            raise ValueError("Invalid argument passed for keyword 'presentation='.")
        
    return myV4
    
 
# drop any unwanted dimensions from the dataset
def dropUnwanted(oldDf, dropDims):
    
    dimNos = numberOfDims(oldDf)
    
    for i in range(1, dimNos+1):
        if i in dropDims:
            for T in TOPIC:
                oldDf = oldDf.drop(T, inplace=True)
    return oldDf
    
    
    
# ####
# MAIN
# ####

# kwargs:
# -------
# geo = add a speciic geographic code for this dataset
# presentation = non-standard shaping of output (see "presentationChange()" function)
# asDataframe = if true, returns a dataframe rather than a CSV
# dropDims = LIST of dimensions (just the number) to drop during the transformation process. i.e [2,5]

def makeV4(inputFile, geo=None, presentation=None, asDataFrame=False, dropDims=False):
    
    oldDf = pd.read_csv(inputFile)

    oldDf = oldDf[:-1] # get rid of ********* footer
    oldDf.fillna('', inplace=True)  # clean na's
    
    oldDf = rewriteHeaders(oldDf)
    FlagEmptyDims(oldDf) # basic validation
    
    # drop unwanted dimensions
    if dropDims is not False:
        oldDf = dropUnwanted(oldDf, dropDims)
    
    if geo is not None: 
        myV4 = conversion(oldDf, geo)
    else:
        myV4 = conversion(oldDf)
        
    # deal with wierdness
    if presentation:
        myV4 = presentationChange(myV4, presentation)
    
    if asDataFrame:
        myV4.to_csv('Output_V4-{i}'.format(i=inputFile), index=False)
    else:
        return myV4
        
    
# use from command line
if __name__ == "__main__":
    
    inputFile = sys.argv[1]    

    try:
        geo = sys.argv[2]
    except:
        geo = None
        
    makeV4(inputFile, geo)

