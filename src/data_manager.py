import pandas as pd
import numpy as np


"""
Class for data wrangling
"""
class DataManager():

    def get_data(self):
        df = pd.read_csv('../data/data.csv')
        df['Ranking'] = np.arange(df.shape[0]) + 1
        return df
