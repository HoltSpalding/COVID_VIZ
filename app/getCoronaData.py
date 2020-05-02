import pandas as pd
import json
from scipy.stats import lognorm
import numpy as np
# from scipy.stats.expon import logpdf
from scipy.stats import expon
from scipy.stats import logistic
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
    # color_unit = 225 / max_confirmed
    # print(df)
    # newdf = pd.DataFrame([df.FIPS])
    # print(newdf)
    # df["Confirmed"] = df["Confirmed"].apply(lambda x: "rgb(255," + str(round(255-x*color_unit)) + "," + str(round(255-x*color_unit)) + ")")
    # print(df)
    df =  json.loads(df)
    # rv = expon(scale=0.01)
    # rv2 = logistic(loc=mean_confirmed,scale=std_confirmed)
    # rv = expon(loc=mean_confirmed,scale=std_confirmed)
    # print(type(df))
    # s = 0.001
    # dist=lognorm(s,loc=mean_confirmed,scale=std_confirmed)
    
    for key,value in df.items():
        #normalize_color_val
        # color_z = (value - mean_confirmed)/std_confirmed
        # color_p = scipy.stats.norm.sf(abs(color_z))*2
        # print(color_p)
        # color_p = dist.pdf(value)
        # color_p = rv.pdf(value)
        # color_p = rv2.pdf(value)
        # if np.log(value) 
        if value == 0:
            color_p = 0
        else:
            color_p = (np.log(value) - min_confirmed)/np.log(max_confirmed)
        print(color_p)
        color_val = str(int(round(color_p*255)))
        # df[key] =  "rgb(255," + str(int(round(255-value*color_unit))) + "," + str(int(round(255-value*color_unit))) + ")"
        # print(color_val)
        df[key] = "rgb(255," + color_val + "," + color_val + ")"

    return df



