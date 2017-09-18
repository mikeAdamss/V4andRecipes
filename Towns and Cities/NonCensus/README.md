# Towns and Cities 'recipe'

Takes a 1 xls file as input. Outputs 4 datasets.


## usage: 
```python Towns&Cities.py <inputFile>```


## details
full details are provided in the form of the attached details.json. Contents shown below.

```json
{
          "uses": ["databaker","pandas"],
          "description": "Takes 1 xls input file, produces 4 csv output files.",
          "inputs": {
                     "1": {
                           "format": "xls",
                           "distinctiveText": "",
                           "name": "Housing, IMD and Census data using Towns and Cities Hierarchy"
                           },
                    },
          "transformName": "UK Business",
          "outputs": [
                      "Towns and Cities - IMD Rankings.csv",
                      "Towns and Cities - Median House Prices.csv",
                      "Towns and Cities - Proportion of LSOAs in most deprived 20%.csv",
                      "Towns and Cities - Proportion of property sales.csv"
                      ],
          "transformType": "one-to-many"}
```
