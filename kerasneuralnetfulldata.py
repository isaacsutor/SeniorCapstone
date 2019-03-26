from keras import backend as K
import os
from importlib import reload
import numpy as np
import pandas as pd
# import cntk as C
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from sklearn.model_selection import train_test_split # cross_validation
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import math
from keras.models import model_from_json



np.random.seed(7)
msft_dataset = pd.read_csv('SP500.csv')
msft_dataset.head()

msft_dataset['Date'] = pd.to_datetime(msft_dataset['Date'])
msft_dataset['Close'] = pd.to_numeric(msft_dataset['Close'], downcast='float')

msft_dataset.set_index('Date', inplace=True)
# msft_dataset.info()

msft_dataset.sort_index(inplace=True)

msft_close = msft_dataset['Close']
msft_close = msft_close.values.reshape(len(msft_close), 1)
plt.plot(msft_close)
# plt.show()


scaler = MinMaxScaler(feature_range=(0, 1))
msft_close = scaler.fit_transform(msft_close)
# print(msft_close)

# ::::::::: Original Train_size ::::::::::
# train_size = int(len(msft_close)*0.7)
train_size = int(len(msft_close)*0.85)
test_size = len(msft_close) - train_size

msft_train, msft_test = msft_close[0:train_size, :], msft_close[train_size:len(msft_close), :]

# print('Data Split : ', len(msft_train), len(msft_test))

def create_ts(ds, series):
    X, Y = [], []
    for i in range(len(ds)-series - 1):
        item = ds[i:(i+series), 0]
        X.append(item)
        Y.append(ds[i+series, 0])
    return np.array(X), np.array(Y)


series = 7

trainX, trainY = create_ts(msft_train, series)
testX, testY = create_ts(msft_test, series)

trainX = np.reshape(trainX, (trainX.shape[0], trainX.shape[1], 1))
testX = np.reshape(testX, (testX.shape[0], testX.shape[1], 1))

model = Sequential()
model.add(LSTM(4, input_shape=(series, 1)))
model.add(Dense(1))
model.compile(loss='mse', optimizer='adam')
model.fit(trainX, trainY, epochs=100, batch_size=32)
# serialize model to JSON
model_json = model.to_json()
with open("model_1.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model_1.h5")
print("Saved model to disk")

trainPredictions = model.predict(trainX)
testPredictions = model.predict(testX)
trainPredictions = scaler.inverse_transform(trainPredictions)
testPredictions = scaler.inverse_transform(testPredictions)
trainY = scaler.inverse_transform([trainY])
testY = scaler.inverse_transform([testY])

trainScore = math.sqrt(mean_squared_error(trainY[0], trainPredictions[:, 0]))
testScore = math.sqrt(mean_squared_error(testY[0], testPredictions[:, 0]))
print('Train score: %.2f rmse', trainScore)
print('Test score: %.2f rmse', testScore)

#lets plot the predictions on a graph and see how well it did
train_plot = np.empty_like(msft_close)
train_plot[:,:] = np.nan
train_plot[series:len(trainPredictions)+series, :] = trainPredictions

test_plot = np.empty_like(msft_close)
test_plot[:,:] = np.nan
test_plot[len(trainPredictions)+(series*2)+1:len(msft_close)-1, :] = testPredictions

#plot on graph
plt.plot(scaler.inverse_transform(msft_close))
plt.plot(train_plot)
plt.plot(test_plot)
plt.show()


