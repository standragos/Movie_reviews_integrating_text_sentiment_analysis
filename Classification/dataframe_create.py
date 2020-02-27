import pandas as pd
import numpy as np
import os
from pathlib import Path
import pyprind as pyprind

basePath = Path('E:\Proiect Licenta\movie classifier\data\\aclImdb')

labels = {'pos': 1, 'neg': 0}
pBar = pyprind.ProgBar(50000)
df = pd.DataFrame()
for s in ('test', 'train'):
    for l in ('pos', 'neg'):
        path = os.path.join(basePath, s, l)
        for file in os.listdir(path):
            with open(os.path.join(path, file), 'r', encoding='utf-8') as infile:
                txt = infile.read()
            df = df.append([[txt, labels[l]]], ignore_index=True)
            pBar.update()

df.columns = ['review', 'sentiment']

# randomize df and save as csv
np.random.seed(0)

df = df.reindex(np.random.permutation(df.index))
# save data frame to csv file called movie_data.csv
df.to_csv('movie_data.csv', index=False, encoding='utf-8')
# read file and check first rows
df = pd.read_csv('movie_data.csv',encoding='utf-8')
df.head()