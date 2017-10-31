# National Population Projections 'recipe'

Takes 1 input file (a .zip file containing .xml files). Created one output file.


# IMPORTANT!

This is an experimental dataset, combining all outputs into a single explorable datacube.

In order to do this we took the following steps.

We have not used cross border rates.
We have removed age ranges above 104, as there are conflicting ranges above that number.
Periods with 2 year values i.e 2014-2015 have been sliced to the first value, i.e 2014.
Dates after 2039 have been removed (these only exist for the main population estimates)..

This may be the way to go, or we may need to create multiple seperate datasets (or something in between).
Either way the process *MUST* be signed off by the business area before publication.

Instructions on how to turn off this special handling (as part of creating a different pipeline) is included in usage instructions should we need to adopt a different approach.


# usage

To convert from a zip to the experimental combined cube on the command line.
```python npp.py <Input.zip>```


To extract as above within a script
```
from npp import 
extractFromZip(<inputFile.zip>)
```

To extract as above but without the custom slicing described earlier.
To create alternative dataset you would create this datacube, and slice out the new datasets.
```
from npp import 
extractFromZip(<inputFile.zip>, oneCube=False)
```


## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{
          "uses": ["pandas"],
          "description": "Takes 1 input file (a .zip file containing .xml files). Created one output file.",
          "inputs": {
                     "1": {
                           "format": "zip",
                           "distinctiveText": "",
                           "name": "National Population Projections. Zip of Xml files."
                           }
                    },
          "transformName": "National Population Projections",
          "outputs": [
                      "Experimental-National Population Projections.csv"
                      ],
          "transformType": "many-to-one"}
```
