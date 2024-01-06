import pandas as pd
import sqlite3 
conn = sqlite3.connect('data/melusine_database.db') #Outil permettant d'exploiter la base de donnée

# Etude des données des colis par type de produit 

    # Construction de tables contenant seulement les ML, TEX, PARF et calcul de leur moyenne (pas de fct variance, à faire)
request = 'SELECT "Circuit de préparation" AS ML, AVG("Colis / UM") FROM (SELECT * FROM "Colis moyens par UM par circuit CEN" WHERE "Circuit de préparation" LIKE "%ML%")'
df_AVG_ML = pd.read_sql(request, conn)
print(df_AVG_ML)

request = 'SELECT "Circuit de préparation" AS TEX, AVG("Colis / UM") FROM (SELECT * FROM "Colis moyens par UM par circuit CEN" WHERE "Circuit de préparation" LIKE "%TEX%")'
df_AVG_TEX = pd.read_sql(request, conn)
print(df_AVG_TEX)

request = 'SELECT "Circuit de préparation" AS PARF, AVG("Colis / UM") FROM (SELECT * FROM "Colis moyens par UM par circuit CEN" WHERE "Circuit de préparation" LIKE "%PARF%")'
df_AVG_PARF = pd.read_sql(request, conn)
print(df_AVG_PARF)