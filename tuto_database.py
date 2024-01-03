#Petit tuto pour apprendre à utiliser la base de donnée stats_pokemons.db 
#La lecture de la base de donnée se fait via des commandes en SQL et les deux bibliothèques suivantes :
import pandas as pd
import sqlite3 
conn = sqlite3.connect('data/melusine_database.db') #Outil permettant d'exploiter la base de donnée

#On peut ensuite récupérer dans un format dataframe (le même format que pour la STNum) les données via des commandes SQL
request = 'SELECT * FROM "PRépa CEN" WHERE RAYID=67' 
dataframe_requested = pd.read_sql(request, conn)
print(dataframe_requested.info())
print(dataframe_requested)

#A vous de vous amuser, à savoir qu'on travaille sous l'environnement SQLite
#NB : Pour l'instant, les usages ne sont pas dispo (j'ai pas réussi à les mettres dans la db)