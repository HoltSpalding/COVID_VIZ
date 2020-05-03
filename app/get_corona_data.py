import json
import pandas as pd
import numpy as np

#returns county-by-county and state-by-state
#confirmed cases for a given date
def county_state_confirmed_stats(df,date):
    #get all rows of a certain date
    df = df.loc[df['Date'] == date]
    #drop all Nan values
    df= df.dropna(subset=["FIPS", "Confirmed"])
    #Only get the FIPS and Confirmed columns
    df = df[["FIPS", "Confirmed"]]
    #cast FIPS as ints
    df["FIPS"] = pd.to_numeric(df["FIPS"], downcast="integer")
    #group duplicate territories (very few)
    df = df.groupby(["FIPS"], as_index = False).agg("sum")
    #assert there are no duplicates
    assert not (df["FIPS"].duplicated().any())
    #convert to json, where FIPS is key and Confirmed is value
    df = df.set_index('FIPS')["Confirmed"].to_json()
    return df


def county_state_assign_colors(df,min_confirmed,max_confirmed):
    df =  json.loads(df)
    state_df = {}
    for key,value in df.items():
        if value == 0:
            normalized_color_val = 1
        else:
            normalized_color_val = 1 - (np.log(value) - min_confirmed)/np.log(max_confirmed)
        color_val = int(round(normalized_color_val*255))
        df[key] = "rgb(255," + str(color_val) + "," + str(color_val) + ")"
        if len(key) == 4 or len(key) == 5:
            state_key = key[:-3]
            # print(state_key)
            # print(state_df)
            if state_key not in state_df:
                state_df[state_key] = [color_val]
            else:
                state_df[state_key].append(color_val)
                # curr_stat_col_list = state_df[state_key]
                # print(curr_stat_col_list)
                # state_df[state_key] = curr_stat_col_list.append(color_val)
    for key,value in state_df.items():
        color_val_list = state_df[key]
        state_color = int(round(sum(color_val_list) / len(color_val_list)))
        state_df[key] = "rgb(255," + str(state_color) + "," + str(state_color) + ")"
    # print(state_df)
    return df,state_df

# def state_assign_colors(df):
#     df = json.loads(df)
#     state_df = {}
#     for key,value in df.items():
#         if len(key) == 4 or len(key) == 5:
#             state_key = key[:-3]
#             color_val = value.split(",")[1]
#             if state_key not in state_df:
#                 state_df[state_key] = [color_val]
#             else:
#                 state_df[state_key].append(color_val)
#     for key,value in state_df.items():
#         state_color = sum(value) / len(value)
#         state_df[key] = "rgb(255," + str(state_color) + "," + str(state_color) + ")"