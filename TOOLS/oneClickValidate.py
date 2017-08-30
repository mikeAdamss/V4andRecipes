# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 12:25:46 2017

@author: Mike
"""

from tkinter import filedialog
import tkinter as tk
from databaker.helpers import validateV4
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
    
    feedback = validateV4(df)
    
    if len(feedback) == 0:
        print("Validation Complete,file is ok: ", source, '\n')
    else:
        print('--------------------\nProblems Detected\n--------------------')
        print('File:', source)
        print('--------------------\\n')
        for issue in feedback:
            print(issue)
        print('-------End--------')

    
"""
THE FOLLOWING CODE IS JUST FOR THE GUI
"""
            
root = tk.Tk()
file1 = tk.StringVar()

description = 'Script Launcher: Vaidation, V1.0'
label = tk.Label(root, text=description)
label.pack()

description = 'A simple file dialogue to us the databaker validation scripts on lone CSV files'
label = tk.Label(root, text=description)
label.pack()

tk.Button(text='Select Source File', command=get_file1).pack()
tk.Label(root, textvariable=file1).pack()

tk.Button(text='Validate', command=run).pack()
# tk.Button(text='Compare', command=convert).pack()
root.mainloop()

