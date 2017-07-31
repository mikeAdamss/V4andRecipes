# CRIME 'recipe'

Takes 6 files. Outputs 35 datasets.

* input1 - Household Crime Incidence
* input2 - Household Crime Prevalence 
* input3 - Personal Crime Incidence
* input4 - Household Crime Prevalence
* input5 - Characteristis reference
* input6 - Measurement reference

## description:
each dataset is filtered to one characteristic, and contains data from both Incidence and Prevalence
i.e - 'Household' in a filename means the data is drawn from input 1 AND 2 from the above.

all output files make use f the measure and characteristics reference data.

## usage: 
```python crime.py input1 input2 input3 input4 input5 input6```

## details
full details are provided in the form of the attached details.json

uses pandas dataframes. Does not use databaker python library.
