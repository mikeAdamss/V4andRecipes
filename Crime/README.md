# CRIME 'recipe'

Takes 6 files. Outputs 35 datasets.

* input1 - Household Crime Incidence
* input2 - Household Crime Prevalence 
* input3 - Personal Crime Incidence
* input4 - Perrsonal Crime Prevalence
* input5 - Characteristis reference
* input6 - Measurement reference

## description:
each dataset is filtered to one characteristic, and contains data from both Incidence and Prevalence
i.e - 'Household' in a filename means the data is drawn from input 1 AND 2 from the above.

all output files make use f the measure and characteristics reference data.

## usage: 
```python crime.py input1 input2 input3 input4 input5 input6```

## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{            
             "transformName":"CRIME",
             "inputs":{
                        "1": {
                            "name":"Household Crime Incidence",
                            "distinctiveText":"Household crime_Incidence",
                            "format":"csv"
                            },
                        "2": {
                            "name":"Household Crime Prevalence",
                            "distinctiveText":"Household crime_Prevalence",
                            "format":"csv"
                            },
                        "3": {
                            "name":"Personal Crime Incidence",
                            "distinctiveText":"Personal crime_Incidence",
                            "format":"csv"
                            },
                        "4": {
                            "name":"Personal Crime Prevalence",
                            "distinctiveText":"Personal crime_prevalence",
                            "format":"csv"
                            },
                        "5": {
                            "name":"Charactersics Reference",
                            "distinctiveText":"characteristicvar",
                            "format":"csv"
                            },
                        "6": {
                            "name":"Measurement Reference",
                            "distinctiveText":"measurementvar",
                            "format":"csv"
                            },
                        },
               "outputs":[
                            "V4_Household Crime_HRP Age.csv",
                            "V4_Household Crime_Accommodation type.csv",
                            "V4_Household Crime_HRP Employment status.csv",
                            "V4_Household Crime_Employment deprivation index.csv",
                            "V4_Household Crime_HRP occupation.csv",
                            "V4_Household Crime_Region.csv",
                            "V4_Household Crime_Output area classification.csv",
                            "V4_Household Crime_Level of physical disorder in immediate area.csv",
                            "V4_Household Crime_Structure of household.csv",
                            "V4_Household Crime_Tenure.csv",
                            "V4_Household Crime_HRP Sex.csv",
                            "V4_Personal Crime_Accommodation type.csv",
                            "V4_Household Crime_Type of area (urban rural).csv",
                            "V4_Personal Crime_Age group (7 bands).csv",
                            "V4_Household Crime_Total.csv",
                            "V4_Household Crime_Total household income.csv",
                            "V4_Personal Crime_Employment deprivation index.csv",
                            "V4_Personal Crime_Highest qualification.csv",
                            "V4_Personal Crime_Employment status.csv",
                            "V4_Personal Crime_Ethnic group.csv",
                            "V4_Personal Crime_Level of physical disorder in immediate area.csv",
                            "V4_Personal Crime_Marital status.csv",
                            "V4_Personal Crime_Number of visits to a nightclub last month.csv",
                            "V4_Personal Crime_Number of hours out of home on an average weekday.csv",
                            "V4_Personal Crime_Sex.csv",
                            "V4_Personal Crime_Long-standing illness or disability .csv",
                            "V4_Personal Crime_Region.csv",
                            "V4_Personal Crime_Occupation.csv",
                            "V4_Personal Crime_Output area classification.csv",
                            "V4_Personal Crime_Number of evening visits to a bar in the last month.csv",
                            "V4_Personal Crime_Total household income.csv",
                            "V4_Personal Crime_Structure of household.csv",
                            "V4_Personal Crime_Tenure.csv",
                            "V4_Personal Crime_Total.csv",
                            "V4_Personal Crime_Type of area (urban rural).csv"
                          ],
               "transformType":"many-to-many",
               "decription":"Creates 35 output files, each combines data from two input files and utilises both reference csvs.",
               "uses":["pandas"]
             }
```
