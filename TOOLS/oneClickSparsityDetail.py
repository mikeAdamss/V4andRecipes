# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 12:25:46 2017

@author: Mike
"""

from tkinter import filedialog
import tkinter as tk
from databaker.helpers import detailSparsity
import pandas as pd


def get_file1():
    global file1
    path = filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
    file1.set(path)    
        
def run():
    runfiles(file1.get())

def runfiles(source):  

    df = pd.read_csv(source)
    df.fillna('', inplace=True)
    
    detailSparsity(df)

    
"""
THE FOLLOWING CODE IS JUST FOR THE GUI
"""
            
root = tk.Tk()
file1 = tk.StringVar()

description = 'Script Launcher: Detail Sparsity, V1.0'
label = tk.Label(root, text=description)
label.pack()

description = 'A simple file dialogue for printing cause of sparsity details.'
label = tk.Label(root, text=description)
label.pack()

tk.Button(text='Select Source File', command=get_file1).pack()
tk.Label(root, textvariable=file1).pack()

tk.Button(text='Get Details', command=run).pack()
# tk.Button(text='Compare', command=convert).pack()
root.mainloop()

