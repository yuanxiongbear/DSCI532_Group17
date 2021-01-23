# script to clean raw data and store into processed dataset
import pandas as pd
import numpy as np

def get_raw():
    df = pd.read_csv('../data/raw/data.csv')
    return df

def clean(df):
    cols = ['ID', 'Name', 'Age', 'Nationality', 'Height', 'Weight', 
       'Overall', 'Potential', 'Club', 'Value', 'Wage', 'Special',
       'Preferred Foot', 'International Reputation', 'Weak Foot',
       'Skill Moves', 'Work Rate', 'Body Type', 'Real Face', 'Position',
       'Jersey Number', 'Joined', 'Loaned From', 'Contract Valid Until',
       'Crossing',
       'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling',
       'Curve', 'FKAccuracy', 'LongPassing', 'BallControl', 'Acceleration',
       'SprintSpeed', 'Agility', 'Reactions', 'Balance', 'ShotPower',
       'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression',
       'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure',
       'Marking', 'StandingTackle', 'SlidingTackle', 'GKDiving', 'GKHandling',
       'GKKicking', 'GKPositioning', 'GKReflexes', 'Release Clause']
    df = df[cols]

    # data formats
    def convert_num(string):
        string = string[1:]
        num = 0
        if string[-1] == 'K':
            num = int(float(string[:-1]) * 1000)
        if string[-1] == 'M':
            num = int(float(string[:-1]) * 1000_000)
        return num
    df['Value'] = df['Value'].apply(convert_num)
    df['Wage'] = df['Wage'].apply(convert_num)

    return df


if __name__ == '__main__':
    df = get_raw()
    df = clean(df)
    df.to_csv('../data/processed/data.csv')
