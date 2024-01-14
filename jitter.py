import numpy as np
import pandas as pd
import pickle
import time
from apyori import apriori
import math

dataset = pd.read_csv("freelancer\\web_interface_song\\static\\r_songs.csv", header=None) #we are specifying there is no header
transactions = []
for i in range(100):
    transactions.append([str(dataset.values[i,j]) for j in range(0,15)])

dataset
def one_hot_encode_data(data):
    unique_items = set(item for transaction in data for item in transaction)
    encoded_data = []
    for transaction in data:
        encoded_transaction = [1 if item in transaction else 0 for item in unique_items]
        encoded_data.append(encoded_transaction)
    return encoded_data

encoded_data = one_hot_encode_data(transactions)

encoded_data


num_repetitions = 10

execution_times = []

for i in range(num_repetitions):
    start_time = time.time()

    rules = apriori(transactions = transactions , min_confidence = 0.1,min_support = 0.003,min_lift = 1,min_length = 2,max_length=3)

    end_time = time.time()

    execution_time = end_time - start_time
    execution_times.append(execution_time)


print(execution_times)
mean_execution_time = sum(execution_times) / num_repetitions
variance = sum((t - mean_execution_time) ** 2 for t in execution_times) / (num_repetitions - 1)
std_deviation = math.sqrt(variance)
print("{:.5f}".format(mean_execution_time))
print(variance)
print(std_deviation)