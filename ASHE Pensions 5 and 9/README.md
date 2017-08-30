# ASHE Pensions Tables 5 & 9 'recipe'

Takes 4 input files. One each of data and CV values for table 5 and table 9. Outputs a value file and a spercentages file, each uses all 4 inpupts in its creation.

# usage

```python ASHEpensions5and9.py <values1.xls> <CV1.xls> <values2.xls> <CV2.xls>```


## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{
          "transformName": "ASHE Pensions: Tables 5 & 9",
          "inputs": {
                    "1": {
                              "distinctiveText": "5.1a",
                              "format": "xls",
                              "name": "ASHE Pensions 5 data"
                    },
                    "2": {
                              "format": "xls",
                              "name": "ASHE Pensions 5 CV",
                              "distinctiveTexat": "5.1b"
                    },
                    "3": {
                              "distinctiveText": "9.1a",
                              "format": "xls",
                              "name": "ASHE Pensions 9 data"
                    },
                    "4": {
                              "format": "xls",
                              "name": "ASHE Pensions 9 CV",
                              "distinctiveTexat": "9.1b"
                    }
                    },
          "description": "Takes 4 files: Values for tables 5 and 9, and CVs for tables 5 and 9. Generates a 1 percentage and 1 values output. Both outputs require all 4 inputs.",
          "outputs": [
                    "ASHE Pensions Tables 5 and 9 Values <year>.csv",
                    "ASHE Pensions Tables 5 and 9 Percentages <year>.csv"
                    ],
          "uses": [
                    "databaker",
                    "pandas"
                    ],
          "transformType": "many-to-many"
}
```
