import pickle
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

dataset = pd.read_csv("freelancer\\web_interface_song\\static\\r_songs.csv", header=None)
X = dataset.iloc[:, 1:].values

X

transactions = []
for i in range(100):
    transactions.append([str(dataset.values[i,j]) for j in range(0,15)])

transactions

flat_data = [song for playlist in transactions for song in playlist if song != 'nan']

mlb = MultiLabelBinarizer()
X = mlb.fit_transform([[song] for song in flat_data])


from sklearn.cluster import KMeans
wcss = []
for i in range(1, 5):
    kmeans = KMeans(n_clusters = i, init = 'k-means++', random_state = 42)
    kmeans.fit(X)
    wcss.append(kmeans.inertia_)


plt.plot(range(1, 5), wcss)
plt.title('The Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()


kmeans = KMeans(n_clusters = 4, init = 'k-means++', random_state = 42)
kmeans.fit(X)
y_kmeans = kmeans.fit_predict(X)

y_kmeans


plt.scatter(X[y_kmeans == 0, 0], X[y_kmeans == 0, 1], s = 100, c = 'red', label = 'Cluster 1')
plt.scatter(X[y_kmeans == 1, 0], X[y_kmeans == 1, 1], s = 100, c = 'blue', label = 'Cluster 2')
plt.scatter(X[y_kmeans == 2, 0], X[y_kmeans == 2, 1], s = 100, c = 'green', label = 'Cluster 3')
plt.scatter(X[y_kmeans == 3, 0], X[y_kmeans == 3, 1], s = 100, c = 'cyan', label = 'Cluster 4')
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 300, c = 'yellow', label = 'Centroids')
plt.show()
file2 = open("freelancer\\web_interface_song\\static\\kmeans.pkl",'wb')
pickle.dump(kmeans,file2)
file2.close()

file2 = open("freelancer\\web_interface_song\\static\\mlb.pkl",'wb')
pickle.dump(mlb,file2)
file2.close()