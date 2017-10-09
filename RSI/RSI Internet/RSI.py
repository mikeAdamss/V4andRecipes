# -*- coding: utf-8 -*-

from WDAtoV4 import makeV4
import sys

df = makeV4(sys.argv[1], geo="K03000001", presentation="labelsToCodes", dropDims=[2,4,6], asDataFrame=True)

headers = [x.replace('RSI Series type_codelist', 'Series type_codelist').replace('RSI Series type','Series type') for x in df.columns.values]
df.columns = headers

df.to_csv('Output_V4-WDADataset_Internet.csv', index=False)