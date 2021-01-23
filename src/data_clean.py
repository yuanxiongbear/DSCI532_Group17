# author: Yuan Xiong
# date: 2020-01-22

# The purpose of this script is to do the data wrangling on the raw data and turn it into processed data based on the study purpose of our project.

import pandas as pd
import numpy as np

def raw_import():
    df = pd.read_csv ('../data/raw/data.csv')
    return df

def column_filter(df):
    df_filtered = df[['Name', 'Age', 'Nationality', 'Overall', 'Potential', 'Club', 'Value', 'Wage']]
    return df_filtered

def num_transform(df):
    df['Value'] = df['Value'].str.replace('€','')
    df['Wage'] = df['Wage'].str.replace('€','')
    df.Value = (df.Value.replace(r'[KM]+$', '', regex=True).astype(float) * \
                df.Value.str.extract(r'[\d\.]+([KM]+)', expand=False)
                  .fillna(1)
                  .replace(['K','M'], [10**3, 10**6]).astype(int))
    df.Wage = (df.Wage.replace(r'[KM]+$', '', regex=True).astype(float) * \
               df.Wage.str.extract(r'[\d\.]+([KM]+)', expand=False)
                  .fillna(1)
                  .replace(['K','M'], [10**3, 10**6]).astype(int))
    return df

if __name__ == "__main__":
    df = raw_import()
    df = column_filter(df)
    df = num_transform(df)
    df.to_csv('../data/processed/processed_data.csv')
    



