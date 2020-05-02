import pandas as pd


df = pd.read_csv("app/static/us_corona_counties.csv")

df = df.drop("UID",axis=1).drop("iso2",axis=1).drop("iso3",axis=1).drop("code3",axis=1).drop("Country_Region",axis=1)
# print(df.iloc[4534])