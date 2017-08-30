# ASHE Pensions Tables 6 & 10 'recipe'

Takes 4 input files. One each of data and CV values for table 6 and table 10. Outputs a value file and a percentages file, each uses all 4 inpupts in its creation.

# usage

```python ASHEpensions6and10.py <values1.xls> <CV1.xls> <values2.xls> <CV2.xls>```


## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{
          "transformName": "ASHE Pensions: Tables 6 & 10",
          "inputs": {
                    "1": {
                              "distinctiveText": "6.1a",
                              "format": "xls",
                              "name": "ASHE Pensions 6 data"
                    },
                    "2": {
                              "format": "xls",
                              "name": "ASHE Pensions 6 CV",
                              "distinctiveTexat": "6.1b"
                    },
                    "3": {
                              "distinctiveText": "10.1a",
                              "format": "xls",
                              "name": "ASHE Pensions 10 data"
                    },
                    "4": {
                              "format": "xls",
                              "name": "ASHE Pensions 10 CV",
                              "distinctiveTexat": "10.1b"
                    }
                    },
          "description": "Takes 4 files: Values for tables 6 and 10, and CVs for tables 6 and 10. Generates a 1 percentage and 1 values output. Both outputs require all 4 inputs.",
          "outputs": [
                    "ASHE Pensions Tables 6 and 10 Values <year>.csv",
                    "ASHE Pensions Tables 6 and 10 Percentages <year>.csv"
                    ],
          "uses": [
                    "databaker",
                    "pandas"
                    ],
          "transformType": "many-to-many"
}
```
