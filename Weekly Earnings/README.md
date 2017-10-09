# Weekly Earnings 'recipe'

Takes 1 excel spreadsheet as input. Outputs 3 datasets.


## usage: 
```python WeeklyEarnings.py <input.xls>```

## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{
          "uses": ["databaker"],
          "description": "Takes 1 csv file, outputs 3 V4 CSV file",
          "inputs": {
                     "1": {
                           "format": "csv",
                           "distinctiveText": "",
                           "name": "Average Weekly Earnings Excel Spreadsheet."
                           },
                    },
          "transformName": "WeeklyEarnings",
          "outputs": [
                      "Weekly Earnings - Pay Index.csv",
                      "Weekly Earnings - Summary as percentage changes",
                      "Weekly Earnings - Summary"
                      ],
                      
          "transformType": "one-to-many"}
```
