# to show what has stored in h5 file. 

import pandas as pd
import sys,os 
sys.path.append(os.getcwd())
store = pd.HDFStore('ether.h5')
print(store)
df = store['ether']
print(df)