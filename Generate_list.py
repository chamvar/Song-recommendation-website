from SqlAlchemy import get_songs
import random
import pickle

file2 = open("freelancer\\web_interface_song\\static\\song_pairs.pkl",'rb')
results = pickle.load(file2)
file2.close()


# generate random 5songs to display in music_list
def generate_random_music_list():
    songs = get_songs()
    s = list(songs.keys())
    l = []
    while len(l) < 5:
        x = s[random.randint(0, len(songs) - 1)]
        if x not in l:
            l.append(x)

    return songs,l

# recommend pairs using apriori algorithm and kmeans
def recommend_pairs(music):
    song_pairs = []
    for record in results:
        items = set(record.items)
        song_pairs.append(items)
    predictions = set()
    for i in song_pairs:
        for j in music:
            if j in i and len(i)>1:
                predictions.update(i)
    predictions = list(predictions)
    return predictions[:5]



# for generating random dataset
# lis = ["Best Songs Hip Hop RB Mix","Stereo hearts","Just the two of us"]

# print(kmean_recommendation(lis))


# songs = get_songs()

# songs = list(songs.keys())



# import pandas as pd
# import numpy as np
# import random
# lis = []

# for i in range(100):
#     lis.append([])

# lis

# for q in range(100):
#     x = lis[q]
#     y = random.randint(0,20)
#     for i in range(y):
#         z = random.randint(0,len(songs)-1)
#         if z not in x:
#             x.append(z)

# lis
# len(songs)

# data = []
# for i in range(100):
#     data.append([])

# for q in range(len(lis)):
#     x = lis[q]
#     y = data[q]
#     for i in x:
#         y.append(songs[i])

# data

# max_len = max(len(sublist) for sublist in data)

# # Create a new list of lists with the same length for all inner lists
# padded_data = [sublist + [np.nan] * (max_len - len(sublist)) for sublist in data]

# # Convert the padded list of lists to a DataFrame
# df = pd.DataFrame(padded_data, index=None )


# # Display the resulting DataFrame
# print(df)
# df.to_csv("C:\\Users\\vramt\\Desktop\\Programming\\freelancer\\web_interface_song\\r_songs.csv")
