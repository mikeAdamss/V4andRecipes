
from databaker.framework import *
import sys

inputFile1 = sys.argv[1]
inputFile2 = sys.argv[2]

year = inputFile1.split(' ')[-1][:-4]
year = int(year.strip())

tabs = loadxlstabs(inputFile1)


lastRow = "85"
focus = "Occupation"


# get rid of notes and glossary tabs
tabs = [tab for tab in tabs if tab.name.lower().strip() not in ['notes','glossary']]


# PRocess values Dset then a percentage one
for i in range(0, 2):
    
    if i == 0: percent = True
    if i == 1: percent = False

    conversionsegments = []
    for tab in tabs:

        pension = tab.excel_ref('C3').expand(RIGHT).is_not_blank().is_not_whitespace()

        ageGroup = tab.excel_ref('A6:A' + lastRow).is_bold()

        provision = tab.excel_ref('A6:A' + lastRow)


        # cell value overrides for agegroup (i.e bold values to Total)
        cvProv = {
            'All employees':'Total',
            '16 - 21':'Total',
            '22 - 29':'Total',
            '30 - 39':'Total',
            '40 - 49':'Total',
            '50 - 54':'Total',
            '55 - 59':'Total',
            '60 - 64':'Total',
            '65 and over':'Total'
        }

        # Get all ons (including blanks and whistespace!)
        obs = pension.waffle(tab.excel_ref('A6:A' + lastRow))

        if percent:
            obs = obs.shift(RIGHT)

        dimensions = [
            HDimConst(TIME, "2016"),
            HDimConst("Geography", "K02000001"),
            HDim(pension, "Provision", CLOSEST, LEFT),  # slower, but allows conditional percentage obs
            HDim(ageGroup, focus, CLOSEST, ABOVE),
            HDim(provision, "Earnings", DIRECTLY, LEFT, cellvalueoverride=cvProv),
            HDimConst("Gender", tab.name)
        ]

        # Convet to dataframe
        conversionsegment = ConversionSegment(tab, dimensions, obs).topandas()
        conversionsegment['Earnings'] = conversionsegment['Earnings'].map(lambda x: x.strip())
        conversionsegment['Provision'] = conversionsegment['Provision'].map(lambda x: x.replace('No pension provisiond', 'No pension provision'))
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

    if 'PROV' in inputFile1:
        prov = ' PROV '
    else:
        prov = ''
        
        
    if percent:
        writeCSV('ASHE Pensions Table 3 Percentages {p}{y}.csv'.format(y=year,p=prov), conversionsegments)
    else:
        writeCSV('ASHE Pensions Table 3 Values {p}{y}.csv'.format(y=year, p=prov), conversionsegments)
