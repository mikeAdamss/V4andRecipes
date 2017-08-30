
from databaker.framework import *
import pandas as pd
import sys


# DETAILS ==============================

# THESE DICTS ARE THE ONLY DIFFERENCES IN THE "Duel" DATASETS (any pensions dataset made form multiple tables)

# table 5
details1 = {
    "lastRow":"41",
    "focus":"Size of Company",
    "extraDim":"Contributor",
    "extraItem":"Employee"
         
    }
# table 9  
details2 = {
    "lastRow":"41",
    "focus":"Size of Company",
    "extraDim":"Contributor",
    "extraItem":"Employer"
           }
           
# ================================

           
# you cant mix provisional and revised tables for the same period.
# make sure all the files are either one or the other
def checkprov(files):
    
    prov = False
    revised = False
    
    for f in files:
        if 'prov' in f.lower():
            prov = True
        else:
            revised = True
            
    if prov and revised:
        raise ValueError("You cannot use a mixture of Provisional and Revised data in the same dataset!")
        
    if prov:
        return prov
    else:
        return revised


     
# Process values Dset then a percentage one
def processOne(valxls, cvXls, details, year, percent=False):
    
    lastRow = details["lastRow"]
    focus = details["focus"]
    extraDim = details["extraDim"]
    extraItem = details["extraItem"]

    tabs = loadxlstabs(inputFile1)
    tabs = [tab for tab in tabs if tab.name.lower().strip() not in ['notes','glossary']]

    conversionsegments = []
    for tab in tabs:
    
        pension = tab.excel_ref('C3').expand(RIGHT).is_not_blank().is_not_whitespace()

        boldGroup = tab.excel_ref('A6:A' + lastRow).is_bold()

        contribution = tab.excel_ref('A6:A' + lastRow)

        # build vaue overrides based on bold values that appear elsewhere
        def buildCvOverrides(boldGroup, contribution):
            Cv = {}
            for val in [x.value for x in boldGroup]:
                if val in [x.value for x in contribution]:
                    Cv.update({val:'All'})    
            return Cv

        # cell value overrides for agegroup (i.e bold values to Total)
        cvProv = buildCvOverrides(boldGroup, contribution)

        # Get all ons (including blanks and whistespace!)
        obs = pension.waffle(tab.excel_ref('A6:A' + lastRow))

        if percent:
            obs = obs.shift(RIGHT)
    
        dimensions = [
            HDimConst(TIME, "2016"),
            HDimConst("Geography", "K02000001"),
            HDim(pension, "Contribution", CLOSEST, LEFT),  # slower, but allows conditional percentage obs
            HDim(boldGroup, focus, CLOSEST, ABOVE),
            HDimConst(extraDim, extraItem),
            HDim(contribution, "Provision", DIRECTLY, LEFT, cellvalueoverride=cvProv),
            HDimConst("Gender", tab.name)
            ]
    
        # Convet to dataframe
        conversionsegment = ConversionSegment(tab, dimensions, obs).topandas()
        conversionsegment['Provision'] = conversionsegment['Provision'].map(lambda x: x.strip())
        conversionsegment['Contribution'] = conversionsegment['Contribution'].map(lambda x: x.replace('No pension provisiond', 'No pension provision'))
        # now we just need the CV values from the other file .........
    
    
        ######################################################
        # this WHOLE section is just the minimum code needed to extract the "obs" from the CV file
        # those "cvObs" will becomes the CV values in our principle/original dataframe
    
        # load specific tab based on current one being processed
        cvTab = loadxlstabs(inputFile2, [tab.name])[0]  # CV file should a tab with an identical name
    
        # get the cvObs
        cvObs = cvTab.excel_ref('C3').expand(RIGHT).is_not_blank().is_not_whitespace()
        cvObs = cvObs.waffle(tab.excel_ref('A6:A' + lastRow))
        if percent:
            cvObs = cvObs.shift(RIGHT)
    
        # nonsensical dimension just so we can trigger the extraction
        dimensions = [
            HDimConst('Holding', "Value")
            ]
    
        CVsegment = ConversionSegment(cvTab, dimensions, cvObs).topandas()
    
        # pull them in
        conversionsegment['CV'] = CVsegment['OBS']
    
        ######################################################
    
        # This tab is done - append to list of done tabs
        conversionsegments.append(conversionsegment)
            
    return conversionsegments
    
            
# #####
# MAIN
# #####

inputFile1 = sys.argv[1]
inputFile2 = sys.argv[2]
inputFile3 = sys.argv[3]
inputFile4 = sys.argv[4]

year = inputFile1.split(' ')[-1][:-4]
year = int(year.strip())
     
# find out if its provisional or not
prov = checkprov([inputFile1, inputFile2, inputFile3, inputFile4])

# additional label for putput
if prov:
    addLab = 'PROV '
else:
    addLab = ''
       
# ######
# VALUES
# ######

# Process values Dset then a percentage one
valFirst = processOne(inputFile1, inputFile2, details1, year)
valSecond = processOne(inputFile3, inputFile4, details2, year)
valDset = pd.concat(valFirst + valSecond)
writeCSV('ASHE Pensions Tables 8 and 12 Values {p}{y}.csv'.format(y=year, p=addLab), valDset)
        

# ############
# Percentages
# ############

# Process values Dset then a percentage one
perFirst = processOne(inputFile1, inputFile2, details1, year, percent=True)
perSecond = processOne(inputFile3, inputFile4, details2, year, percent=True)
perDset = pd.concat(valFirst + valSecond)
writeCSV('ASHE Pensions Tables 8 and 12 Percentages {p}{y}.csv'.format(y=year, p=addLab), perDset)
  
