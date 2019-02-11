import tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt


data = pd.read_csv('_data_stocks.csv')

data = data.drop(['DATE'], 1)

n = data.shape[0]
p = data.shape[1]

data = data.values
# hello

plt.plot(data['SP500'])
