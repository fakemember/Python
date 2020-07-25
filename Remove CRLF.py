# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 14:52:15 2020

@author: CHAO
"""


import pandas as pd
import os 

# set working directory or enter the absolute path with double slash
# example "C:\\Users\\CHAO\\downloads"

filepath=os.getcwd()


# list all files in the folder
allfiles=pd.Series(os.listdir(filepath))

# select csv files, can change to xlsx
selected=allfiles[allfiles.str.endswith('.csv')]

# loop through all selected files
for file in selected:
    readfile=pd.read_csv(os.path.join(filepath,file),dtype=object)
    for column in readfile.columns:
        readfile[column]=readfile[column].str.replace('\n',' ').replace('\r',' ')
    readfile.to_csv(os.path.join(filepath,file),index=False)


