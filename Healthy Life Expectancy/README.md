# IMPORTANT !!!

The non-summary datasets in this repo are using a 2 year time period. We'll need to resolve if we could/should handlt that on CMD before loading.

## Healthy Life Expectancy 'recipe'

Takes 1 input file. Creates 3 output file consisting of: 1 summary. 1 HLE by number of years, 1 Proportion of life as HLE.

```python HealthyLifeExpectancy.py <InptFile.csv>```


## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{
          "uses": ["databaker","pandas"],
          "description": "Takes 1 Excel of Healthy Life Expectancy as input. Creates 3 datasets. One is a summary of HLE and LE. Then one                           LE in years, and one proportion of healthy healthy life.",
          "inputs": {
                     "1": {
                           "format": "xls",
                           "distinctiveText": "",
                           "name": "Healthy Life Expectancy Spreadsheet"
                           }
                    },
          "transformName": "Healthy Life Expectancy",
          "outputs": [
                      "V4-HLE Healthy Life Expectancy in years.csv",
                      "V4-HLE Proportion of life spent in good health.csv",
					  "V4-HLE Summary of Life and Healthy Expectancy.csv"
                      ],
          "transformType": "one-to-many"}
```
