import numpy as np
import os
import pandas as pd
import random
import time

random.seed(time.time())

class DataSet(object):
    def __init__(self, stock_ID, input_size=1, num_steps=30,
                 test_ratio=0.1, normalized=True, close_price_only=True):
        self.stock_ID = stock_ID
        self.input_size = input_size
        self.num_steps = num_steps
        self.test_ratio = test_ratio
        self.close_price_only = close_price_only
        self.normalized = normalized

        # read csv file
        raw_df = pd.read_csv(os.path.join("data", "%s.csv" % stock_ID))

        # merge into one sequence
        if close_price_only:
            self.raw_seq = raw_df['Close'].tolist()
        else:
            self.raw_seq = [price for tup in raw_df[['Open', 'Close']].values for price in tup]

        self.raw_seq = np.array(self.raw_seq)
        self.train_X, self.train_y, self.test_X, self.test_y = self._prepare_data(self.raw_seq)

    def info(self):
        return "StockDataSet [%s] train: %d test: %d" % (
            self.stock_ID, len(self.train_X), len(self.test_y)
        )

    def _prepare_data(self, seq):
        # split into items of input_size
        seq = [np.array(seq[i * self.input_size: (i+1) * self.input_size])
               for i in range(len(seq) // self.input_size)]

        if self.normalized:
            seq = [seq[0] / seq[0][0] - 1.0] + [
                curr / seq[i][-1] - 1.0 for i, curr in enumerate(seq[1:])
            ]

        # split into groups of num_steps





