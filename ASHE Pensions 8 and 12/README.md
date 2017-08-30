# ASHE Pensions Tables 8 & 12 'recipe'

Takes 4 input files. One each of data and CV values for table 8 and table 12. Outputs a value file and a percentages file, each uses all 4 inpupts in its creation.

# usage

```python ASHEpensions8and12.py <values1.xls> <CV1.xls> <values2.xls> <CV2.xls>```


## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{
          "transformName": "ASHE Pensions: Tables 8 & 12",
          "inputs": {
                    "1": {
                              "distinctiveText": "8.1a",
                              "format": "xls",
                              "name": "ASHE Pensions 8 data"
                    },
                    "2": {
                              "format": "xls",
                              "name": "ASHE Pensions 8 CV",
                              "distinctiveTexat": "8.1b"
                    },
                    "3": {
                              "distinctiveText": "12.1a",
                              "format": "xls",
                              "name": "ASHE Pensions 12 data"
                    },
                    "4": {
                              "format": "xls",
                              "name": "ASHE Pensions 12 CV",
                              "distinctiveTexat": "12.1b"
                    }
                    },
          "description": "Takes 4 files: Values for tables 8 and 12, and CVs for tables 8 and 12. Generates a 1 percentage and 1 values output. Both outputs require all 4 inputs.",
          "outputs": [
                    "ASHE Pensions Tables 8 and 12 Values <year>.csv",
                    "ASHE Pensions Tables 8 and 12 Percentages <year>.csv"
                    ],
          "uses": [
                    "databaker",
                    "pandas"
                    ],
          "transformType": "many-to-many"
}
```
