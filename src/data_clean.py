# author: Yuan Xiong
# date: 2020-01-22

# The purpose of this script is to do the data wrangling on
# the raw data and turn it into processed data based on the study purpose of our project.

import pandas as pd
import numpy as np
import pycountry_convert as pc

def raw_import():
    df = pd.read_csv('../data/raw/data.csv', index_col=0)
    return df

def column_filter(df):
    df_filtered = df[['Name', 'Age', 'Nationality', 'Overall', 'Potential', 'Club', 'Value', 'Wage', 'Height', 'Weight']]
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
    df['Weight'] = df['Weight'].str.replace('lbs','')
    df["Weight"] = pd.to_numeric(df["Weight"], downcast="float")
    df = df.rename(columns={'Weight': 'Weight(lbs)', 'Value': 'Value(€)', 'Wage': 'Wage(€)'})
    return df

def add_continent(df):
    s1 = list()
    df = df.replace(['England', 'Wales', 'Scotland', 'Northern Ireland', ], ['United Kingdom','United Kingdom','United Kingdom',  'United Kingdom', ])
    df = df.replace(['Korea Republic', 'Central African Rep.','Kosovo'],['Korea, Republic of', 'Central African Republic','Serbia'])
    df = df.replace(['DR Congo', 'Republic of Ireland', 'FYR Macedonia', 'China PR', 'Guinea Bissau'],['Congo, The Democratic Republic of the', 'Ireland', 'North Macedonia', 'China', 'Guinea-Bissau'])
    df = df.replace(['São Tomé & Príncipe', 'Korea DPR', 'St Kitts Nevis'], ['Sao Tome and Principe', "Korea, Democratic People's Republic of", 'Saint Kitts and Nevis'])
    df = df.replace(['Antigua & Barbuda', 'Curacao','Trinidad & Tobago','Bosnia Herzegovina','St Lucia'],['Netherlands','Antigua and Barbuda','Trinidad and Tobago', 'Bosnia and Herzegovina','Saint Lucia'])
    for i in df['Nationality']:
        country_code = pc.country_name_to_country_alpha2(i, cn_name_format="default")
        continent_name = pc.country_alpha2_to_continent_code(country_code)
        s1.append(continent_name)
    df['Continent'] = s1
    df = df.replace(['SA', 'EU', 'AF', 'NA', 'AS', 'OC'], ['South America', 'Europe', 'Africa', 'North America', 'Asia', 'Oceania'])
    return df
   
if __name__ == "__main__":
    df = raw_import()
    df = column_filter(df)
    df = num_transform(df)
    df = add_continent(df)
    df.to_csv('../data/processed/processed_data.csv')
    



