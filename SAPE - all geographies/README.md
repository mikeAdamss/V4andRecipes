# SAPE 'recipe'

Consist of one script that should work for any combination of SAPE source files.

## Inputs

Give the large (50?!) input files in some cases the script is set to pull in all csvs in its current directory when run. So put your source files in a directory, copy in this file and run.


# Usage

```python SAPE.py <Output Name>```

"Output Name" in this case is typically the geographical hierarchy, so PCON, CCS etc.


# Dealing with large data sources

SAPE data can get rather large so the script can accept one or both of the additional arguments show below.

```python SAPE.py <Output Name> chunksize=100000 chunkcutoff=100000```


### chunksize
The maximum size in bytes you wish to process at a time. Requires an integer.

### chunkcutoff
The number of rows that will trigger an output. Reguires an Integer.

## IMPORTANT

The chunkcutoff is checked every time a chunk is finished processing. Whenever an output is required (whenever the current row numbers exceed the cut off) a csv with be written with a suitable file number appended - file1 then file2, file3, file4 etc - then processing will continue.

You typically need to supply BOTH the arguments to effectively control processing resource. 

For example if you specify procssing in chunks of 100000 bytes but dont set a chunkcutoff it may be self defeating - all those chunks you're carefully processing will be adding to a giant not-yet-output file in memmory.


By default both optional arugmnts are set to 99999999999



