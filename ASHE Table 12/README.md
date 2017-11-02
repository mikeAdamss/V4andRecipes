# ASHE Table 12 'recipe'

Takes a zip of 22 files as input. Outputs 2 datasets.


## usage: 
```python ASHE12.py <Zip File>```


## example source file(s)

https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/residencebasedtraveltoworkareaashetable12

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
                           "name": "ASHE Table 12 Zip"
                           },
                    },
          "transformName": "ASHE Table 12",
          "outputs": [
                      "ASHE 12 Hours <year>.csv",
                      "ASHE 12 Earnings <year>.csv"
                      ],
          "transformType": "many-to-many"}
```
