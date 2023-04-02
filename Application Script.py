import pandas as pd
import numpy as np
import os
import glob
import re
from tqdm import tqdm
from all_function import *
import retrying

path = os.getcwd()+"\\new"
csv_files = glob.glob(os.path.join(path, "*.csv"))
df = pd.read_csv(csv_files[0])


for csv_file in csv_files:
    df = pd.read_csv(csv_file)
    print (csv_file)
    csv_file.split('\\')[-1]

    df = basic_cleaning(df)
    #Saving all the cleaned files
    df.to_csv('./Cleaned_Test/CLEANED__{}'.format(csv_file.split('\\')[-1]),index=False)


path = os.getcwd()+"\\Cleaned_Test"
csv_files = glob.glob(os.path.join(path, "*.csv"))

#File Combiner : To combine all the Cleaned File
file_names = []
for filename in csv_files:
    df = pd.read_csv(filename, index_col=None, header=0)
    file_names.append(df)
    
frame = pd.concat(file_names, ignore_index=True)
frame.to_csv("Final Combined.csv",index=False)
