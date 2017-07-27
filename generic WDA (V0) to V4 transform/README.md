
# Generic WDA->V4 Converter

## Usage:


```python WDAtoV4.py <filename.csv>```



## Caveats:

Not every old file if suitable for automatic conversion to V4. If your source is unsuitable the script will throw an appropriate error, the source file will then need looking at in more detail and restructuring.

This is just a command line tool. Errors etc will need redirecting before if can be utilised as part of a pipeline process.



## Important:


Not all old WDA load files have geography in them. This is because if the dataset was high level data (UK or Great Britain typically) that information was perviously added by the dataset manangement system.

IF processing one of these files you'll need to pass the geographic code explicitly, as follows:

``` python WDAtoV4.py <filename.csv> K20000001 ```


Any WDA/V0 file with more than one geographic level will already have the codes in it.


## Note

Uses python pandas. Does not utilise the databaker python library.
