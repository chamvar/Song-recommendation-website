import pickle
import pandas as pd
import numpy as np
import re


df = pd.read_csv("freelancer\\web_interface_song\\static\\df.csv")

file = open("C:\\Users\\vramt\\Desktop\\Programming\\freelancer\\web_interface_song\\static\\similarity.pkl",'rb');
similarity = pickle.load(file)
file.close()

def recommendation(song_df):
    song_df = song_df.lower()
    idx = df[df['song'] == song_df].index[0]
    distances = sorted(list(enumerate(similarity[idx])),reverse=True,key=lambda x:x[1])
    
    songs = []
    for m_id in distances[1:6]:
        songs.append(df.iloc[m_id[0]].song)
        
    return songs

recommendation('Believer'.lower())