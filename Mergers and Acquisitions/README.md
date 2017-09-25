# Mergers and Acquisitions 'recipe'


NOTE - this is a first pass at a complicated data source. 

As such I've built 4 datasets, though there are possibly/potentially more to be had from this source these intial 4 are by far the
most signifcant.


## description:
One input CSV becomes 4 datasets.


## usage: 
```python mergAcq.py```

## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{
          "uses": ["pandas"],
          "description": "Takes 1 csv file, outputs 4 V4 files..",
          "inputs": {
                     "1": {
                           "format": "csv",
                           "distinctiveText": "",
                           "name": "Mergers and Acquisitions data as CSV."
                           },
                    },
          "transformName": "Mergers and Acquisitions",
          "outputs": [
                      "Mergers and Acquisition, Number of by County.csv",
                      "Mergers and Acquisition, Value of by County.csv",
                      "Mergers and Acquisition - Numbers.csv",
                      "Mergers and Acquisition - Values.csv"
                      ],
                      
          "transformType": "one-to-many"}
```
