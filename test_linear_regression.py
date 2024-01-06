import pandas as pd
import sqlite3 
conn = sqlite3.connect('data/melusine_database.db') #Outil permettant d'exploiter la base de donnée
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures # For (polynomial) feature engineering
from statsmodels.api import OLS # For the linear regression
from statsmodels.tools import add_constant # To add the constant in a model
import numpy as np

###  RECUPERATION DES COLONNES INTERESSANTES DE CEN EN DATAFRAME
sql_request = 'SELECT id_saisie, date, nom_regroupement, unite_oeuvre, hours FROM CEN WHERE id_saisie NOT NULL'
data = pd.read_sql(sql_request, conn)
print(data.info())
print(data)

"""
### AFFICHAGE DES TEMPS D'OPERATION PAR NOMBRE D'UNITE
plt.xlabel("Nombre d'unité par opération")
plt.ylabel("Temps de l'opération")
plt.title("Représentation du temps d'opération par unité")
plt.plot(data["unite_oeuvre"].tolist(),data["hours"].tolist(),"r+")
plt.show()
"""

### AFFICHAGE PAR REGROUPEMENT
sql_request_textile = 'SELECT id_saisie, date, nom_regroupement, unite_oeuvre, hours FROM CEN WHERE id_saisie NOT NULL AND nom_regroupement = "TEXTILE"'
data_textile = pd.read_sql(sql_request_textile, conn)

sql_request_ml = 'SELECT id_saisie, date, nom_regroupement, unite_oeuvre, hours FROM CEN WHERE id_saisie NOT NULL AND nom_regroupement = "ML"'
data_ml = pd.read_sql(sql_request_ml, conn)

sql_request_parfumerie = 'SELECT id_saisie, date, nom_regroupement, unite_oeuvre, hours FROM CEN WHERE id_saisie NOT NULL AND nom_regroupement = "PARFUMERIE"'
data_parfumerie = pd.read_sql(sql_request_parfumerie, conn)

# Tout en 1
plt.xlabel("Nombre d'unité par opération")
plt.ylabel("Temps de l'opération")
plt.title("Représentation du temps d'opération par unité")
plt.plot(data_textile["unite_oeuvre"].tolist(),data_textile["hours"].tolist(),"r+")
plt.plot(data_ml["unite_oeuvre"].tolist(),data_ml["hours"].tolist(),"b+")
plt.plot(data_parfumerie["unite_oeuvre"].tolist(),data_parfumerie["hours"].tolist(),"g+")
plt.show()

#Séparément
plt.subplot(131)
plt.xlabel("Nombre d'unité")
plt.ylabel("Temps")
plt.title("Textile")
plt.plot(data_textile["unite_oeuvre"].tolist(),data_textile["hours"].tolist(),"r+")
plt.subplot(132)
plt.xlabel("Nombre d'unité")
plt.ylabel("Temps")
plt.title("ML")
plt.plot(data_ml["unite_oeuvre"].tolist(),data_ml["hours"].tolist(),"b+")
plt.subplot(133)
plt.xlabel("Nombre d'unité")
plt.ylabel("Temps")
plt.title("Parfumerie")
plt.plot(data_parfumerie["unite_oeuvre"].tolist(),data_parfumerie["hours"].tolist(),"g+")
plt.show()

#Régression linéaire
target = 'hours'
y = data_textile[target]
features_simp = "unite_oeuvre"
X_simp = data_textile["unite_oeuvre"]
linreg_simp_model = OLS(y, add_constant(X_simp))
linreg_simp = linreg_simp_model.fit()
print(linreg_simp.summary())
beta0hs = linreg_simp.params['const']
beta1hs = linreg_simp.params[features_simp]

#Régression polynomiale
transform_poly_interac = PolynomialFeatures(degree=2, interaction_only=False, include_bias=False) # Permet de récupérer le temps au carré, utile pour la regression polynomiale
X_poly_array =  transform_poly_interac.fit_transform(data_textile[["unite_oeuvre"]])
print(len(X_poly_array[0]))

X_poly_ind = data_textile[["unite_oeuvre"]].index
X_poly_col = transform_poly_interac.get_feature_names_out(data_textile[["unite_oeuvre"]].columns)
X_poly = pd.DataFrame(X_poly_array, index=X_poly_ind, columns=X_poly_col)

linreg_poly_model = OLS(y, X_poly)
linreg_poly = linreg_poly_model.fit()
print(linreg_poly.summary())


x_seq = np.linspace(start=data_textile["unite_oeuvre"].min()-1, stop=data_textile["unite_oeuvre"].max(), num=50)


beta0h = 0 #linreg_poly.params['const']
beta1h = linreg_poly.params['unite_oeuvre']
beta2h = linreg_poly.params['unite_oeuvre^2']
print("PARAMETRES")
print(linreg_poly.params)
print(type(linreg_poly.params))

plt.figure()
plt.plot(x_seq, beta0h + beta1h * x_seq + beta2h * (x_seq*x_seq), color='black', lw=1.5)
plt.plot(x_seq, beta0hs + beta1hs * x_seq, "b--", lw=1.5)
plt.xlabel("Nombre d'unité par opération ")
plt.ylabel("Temps de l'opération")
plt.title("Représentation du temps d'opération par unité (textile)")
plt.plot(data_textile["unite_oeuvre"].tolist(),data_textile["hours"].tolist(),"r+")
plt.show()

