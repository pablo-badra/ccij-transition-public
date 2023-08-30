import pandas as pd

def age(df):
    z = []
    for x, y in df.lawlab_opened.items():
        date = y
        bday = df['DOB'][x]
        age = date.year - bday.year - ((date.month, date.day) < (bday.month, bday.day))
        z.append(age)
    df['age_open'] = z
    return df