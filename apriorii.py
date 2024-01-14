
import numpy as np
import pandas as pd
import pickle
import time
from apyori import apriori


dataset = pd.read_csv("freelancer\\web_interface_song\\static\\r_songs.csv", header=None) #we are specifying there is no header
transactions = []
for i in range(100):
    transactions.append([str(dataset.values[i,j]) for j in range(0,15)])

start_time = time.time()
rules = apriori(transactions = transactions , min_confidence = 0.1,min_support = 0.003,min_lift = 1,min_length = 2,max_length=3)
end_time = time.time()

runtime = end_time - start_time

print(runtime)

results = list(rules)

results

song_pairs = []
for record in results:
    items = set(record.items)
    song_pairs.append(items)

for i in song_pairs:
   print(i)

len(song_pairs)  

file2 = open("freelancer\\web_interface_song\\static\\song_pairs.pkl",'wb')
pickle.dump(results,file2)
file2.close()