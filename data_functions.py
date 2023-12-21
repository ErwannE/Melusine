import readcsv
import pandas as pd
import math

def merch_types(df):
    '''Returns the list of the different 
    types of merchandise in dataframe df'''
    res = []
    for i in range(len(df)):
        if df['nom_regroupement'][i] not in res:
            if type(df['nom_regroupement'][i]) == str:
                res.append(df['nom_regroupement'][i])
    return res

def get_agents_nb_by_circuit(df,hours_work_per_day_per_agent):
    '''Returns a dictionary of the number of agents 
    by date and circuit'''
    # Order df by date
    ordered_df = df.sort_values(by='date')
    # Creation of the dictionary
    res = {}
    current_date = ordered_df['date'][0]
    merch = merch_types(df)
    for type in merch:
        res["agents_{0}".format(str(type) + '_' + str(current_date))] = 0

    for i in range(len(ordered_df)):
        if ordered_df['date'][i] == current_date:
            if ordered_df['hours'][i] > 0:
                res["agents_" + str(ordered_df['nom_regroupement'][i]) + '_' + str(current_date)] += ordered_df['hours'][i]
            else:
                0
        else:
            previous_date = current_date
            for type in merch:
                res["agents_" + str(type) + '_' + str(previous_date)] /= hours_work_per_day_per_agent
                res["agents_" + type + '_' + str(previous_date)] = math.ceil(res["agents_" + type + '_' + str(previous_date)])
            current_date = ordered_df['date'][i]
            #creation of the new attributes in the dictionary
            merch = merch_types(df)
            for type in merch:
                res["agents_{0}".format(str(type) + '_' + str(current_date))] = 0
            if ordered_df['hours'][i] > 0:
                res["agents_" + str(ordered_df['nom_regroupement'][i]) + '_' + str(current_date)] += ordered_df['hours'][i]
    final_date = current_date
    for type in merch:
        res["agents_" + str(type) + '_' + str(final_date)] /= hours_work_per_day_per_agent
        res["agents_" + str(type) + '_' + str(final_date)] = math.ceil(res["agents_" + str(type) + '_' + str(final_date)])

    return res

print(get_agents_nb_by_circuit(readcsv.df.head(100),6.5))