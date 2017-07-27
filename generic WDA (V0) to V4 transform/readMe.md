
# Generic WDA->V4 Converter

usage:


```python WDAtoV4.py <filename.csv>```


## Important


Not all old WDA load files have geography in them. This is because if the dataset was high level data (UK or Great Britain typically) that information was perviously added by the dataset manangement system.

IF processing one of these files you'll need to pass the geographic code explicitlt, as follows:

``` python WDAtoV4.py <filename.csv> K20000001 ```


Any WDA/V0 file with more than one geographic level will already have the codes in it.
