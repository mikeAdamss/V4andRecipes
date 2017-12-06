# V4andRecipes

A master repo for recipes/scripts transforming ONS outputs into a V4 structured CSV.


# Install

You'll need to install python3 and a virtual environment. A python virtual environment exists entirely in a single folder chosen by you, holding a unique copy of python3 and all its libraries and dependencies. 

Its entirely up to you what you call you virtual environment but they tend to be purpose specific, so something informatiive like "databaker_env", "pyEnvDatabaker" is good practice. Be aware it'll also appear before your command prompt once activated. 


### Part 1: Install Python3 and Virtual Environment

Databaker v2 is a python3 application, macOS uses python2. We'll need to install python3 then setup the virtual environment.
* `brew install python3`
* `python3 -m venv <virtual env name>`
* Activate your new environment with `source ./<virtual env name>/bin/activate`

  When activated your env name should appear to the left of your command prompt in the terminal.
  
  Enter `deactivate` (no path required) to return to the usual shell.
  
  
### Part 2: Clone this Repo and Install
* Clone this repo (anywhere....doesn't need to be relative to your env).
* Navigate into /V4andRecipes and run ```pip install -r requirements.txt```

This will include our branched (V4 enabled) version of databaker, along with all python libraries and helper scipts/tools used in the wider data transformation processes.

If you want to test via a full transforamtion, start with the ASHE Table 7 script (source data is linked in its repo).


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

