# V4andRecipes

A master repo for recipes/scripts transforming ONS outputs into a V4 structured CSV.

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

The idea is we can (perhaps) pull some needed details out automatically at a future date. NOTE - "uses" is intended as a quick insight into how the transformation was approached and is in no way intended as a requirements.txt.

# Install

Download this repo and ```pip install -r requirments.txt```.

This will include our branched (V4 enabled) version of databaker, along with all python libraries used in the wider data transformation proceses.


# Technology Overview

![alt tag](/technology_overview_pic.png)

### Databaker

Branched here: https://github.com/MikeData/databaker

## Pandas

Standard, just ``` pip install pandas```

## SDMXtoV4

A wrapper/helper script. Included in repo.

## V3toV4

A helper script. Included in repo.

## WDAtoV4

A helper script included in repo.

