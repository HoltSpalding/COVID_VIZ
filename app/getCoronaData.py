import json
import pandas as pd
import numpy as np


#get corona data corresponding to particular date
def getConfirmedGivenDate(df,date):
    #get all rows of a certain date
    df_filtered_by_date = df.loc[df['Date'] == date]
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

def assignColors(df,min_confirmed,max_confirmed,mean_confirmed,std_confirmed):
    df =  json.loads(df)
    for key,value in df.items():
        if value == 0:
            color_p = 0
        else:
            color_p = (np.log(value) - min_confirmed)/np.log(max_confirmed)
        color_val = str(int(round(color_p*255)))
        df[key] = "rgb(255," + color_val + "," + color_val + ")"

    return df



