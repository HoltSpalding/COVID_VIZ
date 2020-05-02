import pandas as pd
import json

#get corona data corresponding to particular date
def getConfirmedGivenDate(df,date):
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
    return df_filtered_by_date

def assignColors(df,min_confirmed,max_confirmed):
    color_unit = 225 / max_confirmed
    # print(df)
    # newdf = pd.DataFrame([df.FIPS])
    # print(newdf)
    # df["Confirmed"] = df["Confirmed"].apply(lambda x: "rgb(255," + str(round(255-x*color_unit)) + "," + str(round(255-x*color_unit)) + ")")
    print(df)
    df =  json.loads(df)
    print(type(df))
    for key,value in df.items():
        df[key] =  "rgb(255," + str(int(round(255-value*color_unit))) + "," + str(int(round(255-value*color_unit))) + ")"
    return df



