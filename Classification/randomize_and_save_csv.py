import numpy as np
import pandas as pd

np.random.seed(0)

df = pd.reindex(np.random.permutation(pd.index))
# save data frame to csv file called movie_data.csv

df.to_csv('movie_data.csv', index=False, encoding='utf-8')

# read file and check first rows

df = pd.read_csv('movie_data.csv',encoding='utf-8')
df.head()