import pandas as pd
import sqlite3 
conn = sqlite3.connect('data/melusine_database.db') #Outil permettant d'exploiter la base de donnée
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures # For (polynomial) feature engineering
from statsmodels.api import OLS # For the linear regression
from statsmodels.tools import add_constant # To add the constant in a model
import numpy as np

#Dataframe des valeurs exploitable
sql_request = "SELECT hours, unite_oeuvre, strftime('%m',date), nom_regroupement, COUNT(*) FROM CEN WHERE id_saisie NOT NULL GROUP BY hours, unite_oeuvre, strftime('%m',date) ORDER BY COUNT(*) DESC"
data = pd.read_sql(sql_request, conn)

print(data['feur'])