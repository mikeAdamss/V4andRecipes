# Weekly Deaths 'recipe'

Takes 1 xls as input. Outputs 1 dataset.


## usage: 
```python weeklyDeaths.py <inputFile>```


## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{
          "uses": ["databaker"],
          "description": "Takes 1 xls input file, produces 1 csv output files.",
          "inputs": {
                     "1": {
                           "format": "xls",
                           "distinctiveText": "",
                           "name": "Weekly Deaths by Age Group"
                           },
                    },
          "transformName": "Weekly Deaths",
          "outputs": [
                      "Weekly Deaths By Age Group <year>.csv"
                      ],
          "transformType": "one-to-one"}
```
