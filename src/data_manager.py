import pandas as pd
import numpy as np
import altair as alt


"""
Class for data wrangling
"""
class DataManager():

    # retreieve data
    def get_data(self):
        df = pd.read_csv('../data/processed/data.csv')
        return df

    # make initial table, land-on page
    def make_table(self, data):
        table = data[['Name', 'Nationality', 'Age', 'Value', 'Overall']]
        table = table.sort_values('Overall', ascending=False)[:10]
        table['Ranking'] = np.arange(table.shape[0]) + 1
        return table

    # make initial charts, land-on page
    def make_chart(self, data, group_col):
        df = (data.groupby(group_col).sum()['Value']
             ).sort_values(ascending=False)[:10].reset_index()

        chart = alt.Chart(df).mark_bar().encode(
                x=alt.X(group_col, sort='-y'),
                y=alt.Y('Value', title='Player Value')
        ).properties(
            width=200,
            height=150
        )
        return chart
    
    # Updates table from given parameters
    #
    # df : dataframe, processed dataset
    # by : str, column to sort by
    # order : bool, determines ascending or not
    # cols : list(str), columns to include in table
    # filter_natn: str, column to filter Nationality on
    # filter_club: str, column to filter Club on
    #
    # return : dataframe, top ten rows of the sorted dataset
    def update_table(self, data, by, order, cols,
                     filter_natn, filter_club):

        # column conditions
        # 1. by (sort by) column must be present
        # 2. player Name must be present
        if not(by in cols):
            cols.append(by)
        if not('Name' in cols):
            cols.append('Name')

        # update table
        if filter_natn:
            data = data[data['Nationality'] == filter_natn]
        if filter_club:
            data = data[data['Club'] == filter_club]
        table = data[cols]
        table = table.sort_values(by=by, ascending=False)
        table['Ranking'] = np.arange(table.shape[0]) + 1
        table = table.sort_values(by='Ranking', ascending=order)[:10]

        # Re-arrange columns
        cols.append('Ranking')
        cols.insert(0, cols.pop(cols.index('Name')))
        cols.insert(0, cols.pop(cols.index('Ranking')))
        table = table[cols]
        return table

