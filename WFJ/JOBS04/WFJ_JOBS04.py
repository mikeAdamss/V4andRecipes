# -*- coding: utf-8 -*-

from WDAtoV4 import makeV4
import sys


# divide by a 1000
def div1000(cell):
    
    cell = int(cell)
    
    # Divide by 1000, lost the decimal
    cell = cell / 1000
    decimals = cell % 1
    cell = cell-decimals
    return int(cell)
    

df = makeV4(sys.argv[1], geo="K03000001", presentation="labelsToCodes", dropDims=[1,4,5,6,7,8], asDataFrame=True)

# divide by 1000
df['V4_0'] = df['V4_0'].apply(div1000)

# Output File
df.to_csv('Output-WFJ-JOBS04.csv', index=False)
