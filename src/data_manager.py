import pandas as pd
import numpy as np


"""
Class for data wrangling
"""
class DataManager():

    def get_data(self):
        df = pd.read_csv('../data/data.csv')
        return df

    def make_table(self, df):
        table = df[['Name', 'Nationality', 'Age', 'Value', 'Overall']]
        table = table.sort_values('Overall', ascending=False)[:10]
        table['Ranking'] = np.arange(table.shape[0]) + 1
        return table

    def update_table(self, df, by, order):
        table = df[['Name', 'Nationality', 'Age', 'Value', 'Overall']]
        table = table.sort_values(by=by, ascending=order)[:10]
        table['Ranking'] = np.arange(table.shape[0]) + 1
        return table


