
# Generic WDA->V4 Converter

## In-script Usage

As per the following example.

```
from WDAtoV4 import makeV4
import sys

makeV4(sys.argv[1], geo="K03000001", presentation="labelsToCodes")
```

The geo and presentation keywords will not always be used (you cant even use the presentation one at the comment line at the moment), their usage is explained below.


## Command Line Usage:


```python WDAtoV4.py <filename.csv>```



## Caveats:

Not every old file if suitable for automatic conversion to V4. If your source is unsuitable the script will throw an appropriate error, the source file will then need looking at in more detail and restructuring.



## Keyword Arguments


### Geo 
Not all old WDA load files have geography in them. This is because if the dataset was high level data (UK or Great Britain typically) that information was previously added by the dataset manangement system.

If processing one of these files you'll need to pass the geographic code explicitly. Any WDA/V0 file with more than one geographic level will already have the codes in it.



### Presentation

Special handling is triggered by using the "presentation=" keyword
This cannot currently be applied on the command line.
    
This is for dealing with non standard appraoched to dimensions/labels that needed to be taken with some WDA inputs. 
    
Example, cases where the files are mapped WDACodes:InternalCodes rather than codes:labels.

Options are:
    
None:              default. No special handling triggered.
justCodes:         as expected then blank the labels column
justLabels:        as expected then blank the codes column
labelToCodes:      put the labels column in codes then blank the labels column
codesToLabels:     put the codes column in labels then blank the codes column
    
These circumstances are all rare but can occur. In 99%+ of use-cases the default "None" will be fine, no keyword will be needed
and the function will never be called.

## Note

Uses python pandas. Does not utilise the databaker python library.
