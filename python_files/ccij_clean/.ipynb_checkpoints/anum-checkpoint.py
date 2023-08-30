import pandas as pd

def fix(df):
    df.loc[~df['a_number'].isna(), 'a_number'] = df.loc[~df['a_number'].isna(), 'a_number'].astype(str)
    for x, y in df[~df['a_number'].isna()]['a_number'].items():
        if len(y) == 8:
            df.loc[x, 'a_number'] = '0'+y
    return df