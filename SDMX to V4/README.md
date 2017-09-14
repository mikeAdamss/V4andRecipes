# SDMX to V4 tool

Intended to allow us to quickly create simple SDMX to V4 pipelines for CMD.

SDMX is a very well structured data source with fully provisioned codelists begind it. While we could convert *everything* from within an SDMX dataset into V4 for loading onto CMD, what you end up with is an awful lot of one-item-only dimensions containing what we regard metadata, inside a structurally sound but user-unfriendly mess of a datacube.

The point of this tool then is to help us identify and quickly transform datasets using only those dimensions we want to expose as V4.



# Usage

```python SDMXtoV4.py -v4 <SOURCE SDMX> "dimensions=Industry,Age"```

The "dimension=" part of the above is how you specify which dimensions you want to convert (observation, time and geography are included automatically).



# Other Functionality

The rest of the functionality is based around getting you to the point where you can run a transform like the above example.

```python SMXtoV4.py -raw <SOURCE SDMX>```


Writes the whole SDMX file to simple flat file CSV.

```python SMXtoV4.py -tran <SOURCE SDMX>```


Writes the whole SDMX file to simple flat file CSV and uses codelists hosted on sdmx.org to translate the codes into labels.

```python SMXtoV4.py -list <SOURCE SDMX>```

Prints to screen a summary of the dimensions inside the SDMX dataset. This inludes whether or not the observations, time and geography dimensions have been automatically identified (if not - see below) as well as a list of all optional dimensions along with a count of the number of unique items in each.



# Obs, Time and Geography

The aim is for these to be automatially detected by the tool (you can check by using the -list swtich).

If for any reason they arent you can pass this information in the the options string (the bit that contains "dimensions=X,Y").

Example:

```python SDMXtoV4.py -v4 <SOURCE SDMX> "time=my_time_column obs=obs_column dimensions=Industry,Age geo=K2000001"```

The order does not matter but they must be delimited by spaces and no other spaces should be included in the string.

