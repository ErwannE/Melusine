import pandas as pd
from sqlalchemy import create_engine
import os
import sqlite3

from datetime import date, timedelta
from proba_discrete import *
from plannification import *
from discretisation import *

### Paths to the files
path = "doc_eop/"
doc_manif = path + "LIST_MANIF.xlsx"
doc_qty = path + 'RECP_QTY.csv'
nombre_ouvrier = 15


current_day = date.today()
#print(current_day)
day_of_week = current_day.strftime("%A")
#print(day_of_week)


def data_df():
    """Returns a dataframe with the manifest data and the quantity data"""
    df_manif = pd.read_excel(doc_manif)
    df_qty = pd.read_csv(doc_qty)
    return df_manif, df_qty

def create_local_database(): # create a database (useful for calculations)
    database = path + 'database_eop.db'
    engine = create_engine('sqlite:///' + database)
    df_manif = pd.read_excel(doc_manif)
    df_qty = pd.read_csv(doc_qty)
    df_manif.to_sql("Manifs", engine, index=False, if_exists='replace')
    df_qty.to_sql("Recp_Qty", engine, index=False, if_exists='replace')
    print("The database has been created")

def delete_database():
    database = path + 'database_eop.db'
    if os.path.exists(database):
        os.remove(database)
        print("The database has been deleted")
    else:
        print("The database does not exist")






def main_end_of_prod():
    """OBJECTIF : Pour chaque manifeste, calculer la date de fin de production. Pour cela, on associe à chaque tâche de chaque manifeste une variable 
    aléatoire à l'aide de la table de probabilité conditionnelle. """
    connect = sqlite3.connect('doc_eop/database_eop.db') #Outil permettant d'exploiter la base de donnée

    # La commande suivante permet de récuppérer toutes les informations nécessaires. L'ordre de priorité est donné par la date
    request = 'SELECT Manifs.MNFID AS Manif, ITEMID AS ItemID, SUM(RECPQTY_COLIS) AS Qty, CAT AS Cat, strftime("%m",END_DATE) AS Mois FROM Recp_Qty JOIN Manifs ON Recp_Qty.MNFID = Manifs.MNFID GROUP BY Manif, ITEMID ORDER BY END_DATE' 
    df = pd.read_sql(request, connect)

    table_proba = table_proba_condi() #table des probas conditionnelles

    discret_unite(df,colonne="Qty") #Discrétisation de la variable "unite_oeuvre"

    liste_var_alea = [table_proba[row["Cat"]][row["Mois"]][row["cat_Qty"]] for index, row in df.iterrows() ] #liste des variables aléatoires
    #print(liste_var_alea[0]) première variable aléatoire
    with open('output.txt', 'w') as f:
        c=0
        while not df.empty:
            c=c+1
            f.write("Planning de la journée : " + str(c) + "\n")
            planning_du_jour = planning_jour_V2(liste_var_alea, nombre_ouvrier, index=df.index)
            f.write(str(planning_du_jour) + "\n") #Planning de la journée
            f.write("Jour " + str(c) + " terminé\n")
            df = df.loc[planning_du_jour[-1]] #On supprime les lignes correspondant aux tâches effectuées
    

#create_local_database()
main_end_of_prod()