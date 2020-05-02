import pandas as pd


df = pd.read_csv("app/static/us_corona_counties.csv")

df = df.drop("UID",axis=1).drop("iso2",axis=1).drop("iso3",axis=1).drop("code3",axis=1).drop("Country_Region",axis=1)

#get all rows of a certain date
df_filtered_by_date = df.loc[df['Date'] == "1/22/20"]
#drop all Nan values
df_filtered_by_date = df_filtered_by_date.dropna(subset=["FIPS", "Confirmed"])
#Only get the FIPS and Confirmed columns
df_filtered_by_date = df_filtered_by_date[["FIPS", "Confirmed"]]
#cast FIPS as ints
df_filtered_by_date["FIPS"] = pd.to_numeric(df_filtered_by_date["FIPS"], downcast="integer")
#group duplicate territories (very few)
df_filtered_by_date = df_filtered_by_date.groupby(["FIPS"], as_index = False).agg("sum")
#assert there are no duplicates
assert not (df_filtered_by_date["FIPS"].duplicated().any())
#convert to json, where FIPS is key and Confirmed is value
df_filtered_by_date = df_filtered_by_date.set_index('FIPS')["Confirmed"].to_json()
print(df_filtered_by_date)