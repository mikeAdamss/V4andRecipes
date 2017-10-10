# -*- coding: utf-8 -*-

from WDAtoV4 import makeV4
import pandas as pd
import sys


# divide by a 1000
def div1000(cell):
    
    cell = int(cell)
        
    # Divide by 1000, lost the decimal
    cell = cell / 1000
    decimals = cell % 1
    cell = cell-decimals
    return int(cell)
    

ukFile = sys.argv[1]
gbFile = sys.argv[2]

df1 = makeV4(ukFile, geo="K02000001", presentation="labelsToCodes", dropDims=[1,4,5,6,7,8], asDataFrame=True)
df2 = makeV4(gbFile, geo="K03000001", presentation="labelsToCodes", dropDims=[1,4,5,6,7,8], asDataFrame=True)

df = pd.concat([df1, df2])

# divide by 1000
df['V4_0'] = df['V4_0'].apply(div1000)

# Output File
df.to_csv('Output-WFJ-JOBS03.csv', index=False)
