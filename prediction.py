import json
from math import sqrt

import plotly
import plotly.graph_objs as go
import pandas as pd
from pandas import concat
import calendar
import chart_studio.plotly as py
import numpy as np
from plotly.subplots import make_subplots
from statsmodels.tsa.stattools import pacf, acf
import plotly.express as px
from keras.models import Sequential
from keras.layers import Dense, concatenate
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder


class Visual():
    def create_dataset(dataset, look_back):
        dataX, dataY = [], []
        for i in range(len(dataset) - look_back - 1):
            a = dataset[i:(i + look_back), 0]
            dataX.append(a)
            dataY.append(dataset[i + look_back, 0])
        return np.array(dataX), np.array(dataY)

    def series_to_supervised(self, data, n_in=1, n_out=1, dropnan=True):
        print(type(data))
        n_vars = 1 if type(data) is list else data.shape[1]
        df = pd.DataFrame(data)
        cols, names = list(), list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(df.shift(i))
            names += [('var%d(t-%d)' % (j + 1, i)) for j in range(n_vars)]
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
            cols.append(df.shift(-i))
            if i == 0:
                names += [('var%d(t)' % (j + 1)) for j in range(n_vars)]
            else:
                names += [('var%d(t+%d)' % (j + 1, i)) for j in range(n_vars)]
        # put it all together
        agg = concat(cols, axis=1)
        agg.columns = names
        # drop rows with NaN values
        if dropnan:
            agg.dropna(inplace=True)
        return agg

    def LSTM(self, df, features, split, begin, end, disease):
        dfTest = df
        df = df.groupby(['year', 'month', 'province_code'], as_index=False).mean()
        df = df.groupby(['year', 'month'], as_index=False).sum()
        df = df.drop(['province_code'], axis=1)
        print(df)
        np.random.seed(42)
        values = df.values
        encoder = LabelEncoder()
        values[:, 1] = encoder.fit_transform(values[:, 1])
        values = values.astype('float32')
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled = scaler.fit_transform(values)

        reframed = self.series_to_supervised(scaled, 1, 1)
        reframed.drop(reframed.columns[[0, 1, 2, 3, 4, 6, 7]], axis=1, inplace=True)
        print(reframed.head())
        values = reframed.values
        trainSplit = (split - begin) * 12
        train = values[:trainSplit, :]
        test = values[trainSplit:, :]
        print(len(train))
        train_X, train_y = train[:, :-1], train[:, -1]
        test_X, test_y = test[:, :-1], test[:, -1]
        # reshape input to be 3D [samples, timesteps, features]
        train_X = train_X.reshape((train_X.shape[0], 1, train_X.shape[1]))
        test_X = test_X.reshape((test_X.shape[0], 1, test_X.shape[1]))
        print(train_X.shape, train_y.shape, test_X.shape, test_y.shape)
        ...
        # design network
        model = Sequential()
        model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
        model.add(Dense(1))
        model.compile(loss='mae', optimizer='adam')
        # fit network
        history = model.fit(train_X, train_y, epochs=50, batch_size=72, validation_data=(test_X, test_y), verbose=2,
                            shuffle=False)
        # plot history
        yhat = model.predict(test_X)
        test_X = test_X.reshape((test_X.shape[0], test_X.shape[2]))
        # invert scaling for forecast
        inv_yhat = concatenate((yhat, test_X[:, 1:]), axis=1)
        print(inv_yhat)
        inv_yhat = scaler.inverse_transform(inv_yhat)
        inv_yhat = inv_yhat[:, 0]
        # invert scaling for actual
        test_y = test_y.reshape((len(test_y), 1))
        inv_y = concatenate((test_y, test_X[:, 1:]), axis=1)
        inv_y = scaler.inverse_transform(inv_y)
        inv_y = inv_y[:, 0]
        # calculate RMSE
        rmse = sqrt(mean_squared_error(inv_y, inv_yhat))
        print('Test RMSE: %.3f' % rmse)
        return 0



    def LSTM(self, df, disease):
        df = df.groupby(['year', 'month', 'province_code'], as_index=False).mean()
        df = df.groupby(['year', 'month'], as_index=False).sum()
        df = df.drop(['province_code'], axis=1)