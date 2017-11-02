# V4andRecipes

A master repo for recipes/scripts transforming ONS outputs into a V4 structured CSV.


# Current Status

| Output | Dataset | Description | Filename  | Folder | Status | Actions |
| ------ | ------- | ----------- | ------------------- | --- | --- | --- |
| ASHE | Table 7 | Combined Timeseries (5 years). Does not inlcude percentages. | MASTER_ASHE7.zip | "ASHE Table 7" | Ok to load | Further |
| ASHE | Table 8 | Combined Timeseries (5 years) | MASTER_ASHE8.zip | "ASHE Table 8" | Ok to load | Further |
| ASHE | Table 9 | Combined Timeseries (5 years) | MASTER_ASHE9.zip | "ASHE Table 9" | Ok to load | Further |
| ASHE | Table 10 | Combined Timeseries (5 years) | MASTER_ASHE10.zip | "ASHE Table 10" | Ok to load | Further |
| ASHE | Table 11 | Combined Timeseries (5 years) | MASTER_ASHE11.zip | "ASHE Table 11" | Ok to load | Further |
| ASHE | Table 12 |  Combined Timeseries (5 years) | MASTER_ASHE12.zip | "ASHE Table 12" | Ok to load | Further |


# Details

All folder with the exceptions of 'SDMX to V4', 'generic V3 to V4 transforms', 'generic WDA (V0) to V4 transform' and 'TOOLS' contain V4 load files and the scripts needed to generate them.

They will also include a details.json file, example below:

```json
{
          "uses": ["pandas", "WDAtoV4"],
          "description": "Takes 1 csv file, outputs 1 V4 CSV file",
          "inputs": {
                     "1": {
                           "format": "csv",
                           "distinctiveText": "",
                           "name": "Filename"
                           },
                    },
          "transformName": "ThisTransform",
          "outputs": [
                      "Output_V4_Filename.csv"
                      ],            
          "transformType": "one-to-one"
          }
```

The idea is we can (perhaps) pull some needed details out automatically at a future date. NOTE - "uses" is intended as a quick insight into how the transformation was approached. For own installation and usage see below.

# Install

Download this repo and ```pip install -r requirements.txt```.

This will include our branched (V4 enabled) version of databaker, along with all python libraries used in the wider data transformation processes.


# Technology Overview

![alt tag](/technology_overview_pic.png)

### Databaker

Branched here: https://github.com/MikeData/databaker

## Pandas

Standard.

## SDMXtoV4

A wrapper/helper script. Included in repo.

## V3toV4

A helper script. Included in repo.

## WDAtoV4

A helper script included in repo.

