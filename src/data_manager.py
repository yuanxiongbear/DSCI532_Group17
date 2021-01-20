import pandas as pd
import numpy as np


"""
Class for data wrangling
"""
class DataManager():

    # retreieve data
    def get_data(self):
        df = pd.read_csv('../data/processed/data.csv')
        print(df['Value'])
        return df

    # make initial table, land-on page
    def make_table(self, df):
        table = df[['Name', 'Nationality', 'Age', 'Value', 'Overall']]
        table = table.sort_values('Overall', ascending=False)[:10]
        table['Ranking'] = np.arange(table.shape[0]) + 1
        return table

    
    # Updates table from given parameters
    #
    # df : dataframe, processed dataset
    # by : str, column to sort by
    # order : bool, determines ascending or not
    # cols : list(str), columns to include in table
    #
    # return : dataframe, top ten rows of the sorted dataset
    def update_table(self, df, by, order, cols):
        # column conditions
        if not(by in cols):
            cols.append(by)
        if not('Name' in cols):
            cols.append('Name')

        # update table
        table = df[cols]
        table = table.sort_values(by=by, ascending=False)
        table['Ranking'] = np.arange(table.shape[0]) + 1
        table = table.sort_values(by=by, ascending=order)[:10]

        # Re-arrange columns
        cols.append('Ranking')
        cols.insert(0, cols.pop(cols.index('Name')))
        cols.insert(0, cols.pop(cols.index('Ranking')))
        table = table[cols]
        return table


