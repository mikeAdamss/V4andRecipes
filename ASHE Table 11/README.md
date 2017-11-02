# ASHE Table 11 'recipe'

Takes a zip of 22 files as input. Outputs 2 datasets.


## usage: 
```python ASHE11.py <Zip File>```


## example source sample(s)

https://www.ons.gov.uk/employmentandlabourmarket/peopleinwork/earningsandworkinghours/datasets/workbasedtraveltoworkareaashetable11


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
                           "name": "ASHE Table 11 Zip"
                           },
                    },
          "transformName": "ASHE Table 11",
          "outputs": [
                      "ASHE 11 Hours <year>.csv",
                      "ASHE 11 Earnings <year>.csv"
                      ],
          "transformType": "many-to-many"}
```
