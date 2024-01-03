import pandas as pd
import sqlite3 
conn = sqlite3.connect('data/melusine_database.db') #Outil permettant d'exploiter la base de donnée

###  RECUPERATION DES COLONNES INTERESSANTES DE CEN EN DATAFRAME
sql_request = 'SELECT id_saisie, date, nom_regroupement, unite_oeuvre, hours FROM CEN WHERE id_saisie NOT NULL'
data = pd.read_sql(sql_request, conn)
print(data.info())
print(data)