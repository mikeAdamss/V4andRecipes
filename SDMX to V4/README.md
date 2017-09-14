# SDMX to V4 tool

Intended to allow us to quickly create simple SDMX to V4 pipelines for CMD.

SDMX is a very well structured data source with fully provisioned codelists begind it. While we could convert *everything* from within an SDMX dataset into V4 for loading onto CMD, what you end up with is an awful lot of one-item-only dimensions containing what we regard metadata, inside a structurally sound but user-unfriendly mess of a datacube.

The point of this tool then is to help us identify and quickly transform datasets using only those dimensions we want to expose as V4.



# Usage

```python SDMXtoV4.py -v4 <SOURCE SDMX> "dimensions=Industry,Age"```

The "dimension=" part of the above is how you specify which dimensions you want to convert (observation, time and geography are included automatically).


# Other Functionality

The rest of the functionality is based around getting you to the point where you can run a transform like the above example.
