# ASHE Table 10 'recipe'

Takes a zip of 22 files as input. Outputs 2 datasets.


## usage: 
```python ASHE10.py <Zip File>```

## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{
          "uses": ["pandas"],
          "description": "Creates 2 load files from a zip containing 22 xls files",
          "inputs": {
                     "1": {
                           "format": "zip",
                           "distinctiveText": "",
                           "name": "ASHE Table 10 Zip"
                           },
                    },
          "transformName": "ASHE Table 10",
          "outputs": [
                      "ASHE Hours <year>.csv",
                      "ASHE Earnings <year>.csv"
                      ],
          "transformType": "many-to-many"}
```
