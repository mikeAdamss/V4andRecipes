# UK Business 'recipe'

Takes a zip of 24 files as input. Outputs 15 datasets.


## usage: 
```python UKBusiness.py <Zip File>```

Will take the year from the current time of the server.

```python UKBusiness.py <Zip File> <time>```

Will let you specifiy a 4-digit integer as the time (these datasets are yearly).

## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{
          "uses": ["databaker","pandas"],
          "description": "Takes 1 zip file (containing 24 files). Creates 15 output files.",
          "inputs": {
                     "1": {
                           "format": "zip",
                           "distinctiveText": "",
                           "name": "UK Business Data, Zipfile of 24 xlsx spreadsheets."
                           },
                    },
          "transformName": "UK Business",
          "outputs": [
                      "UKBAA01a-Enterprise-local units by 4 Digit SIC and UK Regions.csv",
                      "UKBAA01b-Enterprise-local units by Broad Industry Group and UK Local Authority Districts.csv",
                      "UKBAA03-Enterprise-local units by Industry and Parliamentary Constituency.csv",
                      "UKBABa-Enterprise-local units by 2 Digit SIC, Employment size band and Region.csv",
                      "UKBABb-Enterprise-local units by 4 Digit SIC and Employment size band.csv",
                      "UKBAC-Enterprise-local units by Industry, Employment size band and Legal status.csv",
                      "UKBAD01-Enterprise-local units by Employment size band and UK Local Authority Districts.csv",
                      "UKBAD03-Enterprise-local units by Employment size band and Parliamentary Constituency.csv",
                      "UKBAE-Enterprise-local units by Employment size band, Legal status and Region.csv",
                      "UKBAF01-Enterprise by Turnover size band and GB Local Authority Districts.csv",
                      "UKBAF03-Enterprise by Turnover size band and Parliamentary Constituency.csv",
                      "UKBAGa-Enterprise by 2 Digit SIC, Turnover size band and Region.csv",
                      "UKBAGb-Enterprise by 4 Digit SIC and Turnover size band.csv",
                      "UKBAH-Enterprise by Turnover size band, Legal status and Region.csv",
                      "UKBAI-Enterprise by Industry, Turnover size band and Legal status.csv"
                      ],
          "transformType": "many-to-many"}
```
