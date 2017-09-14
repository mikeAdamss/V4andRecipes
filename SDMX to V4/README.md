# SDMX to V4 tool

Intended to allow us to quickly create simple SDMX to V4 pipelines for CMD.

SDMX is a very well structured data source with fully providionsed codelists begind it and while we could convert *everything* from within an SDMX dataset into V4 to be exposed on CMD, what you end up with is an awful lot of one item dimensions containing what we regard as metadata.

The point of this tool then is to let you work with SDMX easily and specify only those dimensions we want to expose via CMD for inclusion in a V4 output.



# Usage

```python SDMXtoV4.py -v4 <SOURCE SDMX> "dimensions=Industry,Age"```

The "dimension=" part of the above is how you specify which dimensions you want to convert (observation, time and geography are included automatically).


# Other Functionality

The rest of the functionality is based around getting you to the point where you can run a transform like the above example,
