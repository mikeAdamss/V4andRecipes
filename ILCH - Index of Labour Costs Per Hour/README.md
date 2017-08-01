# ILCH

Takes 2 input file (seasonally adjusted and non seasonally adjusted), creates 2 output files ("growth" and "level").

## description
Each output file contains data from both inputs. The "Growth" output is made using growth data from both the Seasonally Adjusted and Non Seasonally Adjusted spreadsheets.
 
# usage

```python ILCH.py <NSA input> <SA input>```


## details
full details are provided in the form of the attached details.json. Contents shown below

```json
{"transformName":"ILCH: Index of Labout Costs Per Hour",
             "inputs":{
                        "1": {
                            "name":"Non Seasonally Adjusted File",
                            "distinctiveText":"nsa",
                            "format":"xls"
                            },
                        "2": {
                            "name":"Seasonally Adjusted File",
                            "disctinctiveText":"",
                            "format":"xls"
                            }
                        },
               "Outputs":["ILCH-Growth.csv", "ILCH-Level.csv"],
               "transformType":"many-to-many",
               "decription":"Creates two output files, each combines data from both input files.",
               "uses":["pandas", "databaker"]
             }
```

