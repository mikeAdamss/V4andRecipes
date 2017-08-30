# ASHE Pensions Tables 7 & 11 'recipe'

Takes 4 input files. One each of data and CV values for table 7 and table 11. Outputs a value file and a percentages file, each uses all 4 inpupts in its creation.

# usage

```python ASHEpensions7and11.py <values1.xls> <CV1.xls> <values2.xls> <CV2.xls>```


## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{
          "transformName": "ASHE Pensions: Tables 7 & 11",
          "inputs": {
                    "1": {
                              "distinctiveText": "7.1a",
                              "format": "xls",
                              "name": "ASHE Pensions 7 data"
                    },
                    "2": {
                              "format": "xls",
                              "name": "ASHE Pensions 7 CV",
                              "distinctiveTexat": "7.1b"
                    },
                    "3": {
                              "distinctiveText": "11.1a",
                              "format": "xls",
                              "name": "ASHE Pensions 11 data"
                    },
                    "4": {
                              "format": "xls",
                              "name": "ASHE Pensions 11 CV",
                              "distinctiveTexat": "11.1b"
                    }
                    },
          "description": "Takes 4 files: Values for tables 7 and 11, and CVs for tables 7 and 11. Generates a 1 percentage and 1 values output. Both outputs require all 4 inputs.",
          "outputs": [
                    "ASHE Pensions Tables 7 and 11 Values <year>.csv",
                    "ASHE Pensions Tables 7 and 11 Percentages <year>.csv"
                    ],
          "uses": [
                    "databaker",
                    "pandas"
                    ],
          "transformType": "many-to-many"
}
```
