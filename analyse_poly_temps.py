import pandas as pd
import sqlite3 
conn = sqlite3.connect('data/melusine_database.db') #Outil permettant d'exploiter la base de donnée
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures # For (polynomial) feature engineering
from statsmodels.api import OLS # For the linear regression
from statsmodels.tools import add_constant # To add the constant in a model
import numpy as np

#Dataframe des valeurs exploitable
sql_request = "SELECT hours, unite_oeuvre, strftime('%m',date) as mois, nom_regroupement, COUNT(*) AS occurence FROM CEN WHERE id_saisie NOT NULL GROUP BY hours, unite_oeuvre, strftime('%m',date) ORDER BY COUNT(*) DESC"
data = pd.read_sql(sql_request, conn)
data.to_sql('CEN_usable', conn, index=False, if_exists='replace')

ql_request = "SELECT hours, unite_oeuvre, strftime('%m',date) as mois, nom_regroupement FROM CEN WHERE id_saisie NOT NULL"
data = pd.read_sql(ql_request, conn)
data.to_sql('CEN_usable_sans_occ', conn, index=False, if_exists='replace')

from discretisation import *
from utile import ajouter_guillemets


def regpoly_selon_param(mois='mois', cat='nom_regroupement', deg=2, constante=False, database='CEN_usable_sans_occ', timeleap=15):
    """Réalise une régression polynomiale du temps d'opération en fonction du nombre d'objet de l'opération. 
    Cette régression se fait (ou non) sur un certain regroupement de produit (cat) et sur un mois d'execution (mois). 
    La regression polynomiale est par défaut de degré 2 (le degré a été déterminé par analyse des p-valeurs), et la constante a été retiré pour plus de logique.
    "timeleap" correspond à la discretisation du temps qui est choisi pour le programme (en minutes)."""


    if mois != 'mois':
        mois = ajouter_guillemets(mois) #Permet la compatibilité avec l'absence de paramètre demandé 
        print(mois)
                            #(si aucun mois renseigné, la condition mois = mois est toujours respecté dans la requête, si renseigné la condition sur le mois en SQL doit être de la forme mois='val_mois')
    if cat != 'nom_regroupement':
        cat = ajouter_guillemets(cat) #Similaire 
        print(cat)
    request = "SELECT hours, unite_oeuvre FROM " + database + " WHERE nom_regroupement=" + cat + " AND mois=" + mois
    print(request) 
    df = pd.read_sql(request, conn)
    discret_hours(df, timeleap=timeleap)

    target = 'hours'
    y = df[target]
    transform_poly_interac = PolynomialFeatures(degree=deg, interaction_only=False, include_bias=False) # Permet de récupérer le temps au carré, utile pour la regression polynomiale
    X_poly_array =  transform_poly_interac.fit_transform(df[["unite_oeuvre"]])

    X_poly_ind = df[["unite_oeuvre"]].index
    X_poly_col = transform_poly_interac.get_feature_names_out(df[["unite_oeuvre"]].columns)
    X_poly = pd.DataFrame(X_poly_array, index=X_poly_ind, columns=X_poly_col)

    if constante:
        X_poly=add_constant(X_poly)
    
    linreg_poly_model = OLS(y, X_poly)
    linreg_poly = linreg_poly_model.fit()
    print(linreg_poly.summary())
    return linreg_poly #linreg_poly renvoit 


def print_regpoly_selon_param(mois='mois', cat='nom_regroupement', database='CEN_usable_sans_occ', timeleap=15):


    linreg_poly_params = regpoly_selon_param(mois, cat)
    beta1h = linreg_poly_params['unite_oeuvre']
    beta2h = linreg_poly_params['unite_oeuvre^2']

    if mois != 'mois':
        mois = ajouter_guillemets(mois) #Permet la compatibilité avec l'absence de paramètre demandé 
        print(mois)
                            #(si aucun mois renseigné, la condition mois = mois est toujours respecté dans la requête, si renseigné la condition sur le mois en SQL doit être de la forme mois='val_mois')
    if cat != 'nom_regroupement':
        cat = ajouter_guillemets(cat) #Similaire 
        print(cat)
    request = "SELECT hours, unite_oeuvre FROM " + database + " WHERE nom_regroupement=" + cat + " AND mois=" + mois
    print(request) 
    df = pd.read_sql(request, conn)
    discret_hours(df, timeleap=timeleap)

    def P(x_seq):
        return beta1h * x_seq + beta2h * (x_seq*x_seq)
    def floor_P(x_seq, timeleap=15):
        mult = 60/timeleap
        return np.ceil(P(x_seq)*mult)/mult

    x_seq = np.linspace(start=df["unite_oeuvre"].min()-1, stop=df["unite_oeuvre"].max(), num=400)
    plt.figure()
    plt.plot(x_seq, P(x_seq), color='black', lw=1.5)
    plt.plot(x_seq, floor_P(x_seq), "b--", lw=1.5)
    plt.xlabel("Nombre d'unité par opération ")
    plt.ylabel("Temps de l'opération")
    plt.title("Représentation du temps d'opération par unité (cat :" + cat +", mois :" + mois + ")")
    plt.plot(df["unite_oeuvre"].tolist(),df["hours"].tolist(),"r+")
    plt.show()



def occurence_array(database = 'CEN_usable', timeleap = 15): #table des occurences (en temps), en fonction du type de produit, du mois et de la quantité
    conn = sqlite3.connect('data/melusine_database.db') #Outil permettant d'exploiter la base de donnée
    mois=['01','02','03','04','05','06','07','08','09','10','11','12']
    cat=['TEXTILE','ML','PARFUMERIE']
    inv_mois={'01':0,'02':1,'03':2,'04':3,'05':4,'06':5,'07':6,'08':7,'09':8,'10':9,'11':10,'12':11}
    inv_cat={'TEXTILE':0,'ML':1,'PARFUMERIE':2}
    table_occ=[[[0 for i in range(int(7*(60/timeleap)))] for j in range(len(mois))] for j in range(len(cat))]
    for m in mois:
        for c in cat:
            request = "SELECT hours, unite_oeuvre, occurence FROM " + database + " WHERE nom_regroupement='" + c + "' AND mois='" + m + "'"
            df = pd.read_sql(sql_request, conn)
            discret_hours(df, timeleap=timeleap)
            for i in range(df.shape[0]):
                table_occ[inv_cat[c]][inv_mois[m]][int(df.loc[i,'hours']*60/timeleap - 1)] += df.loc[i,'occurence']
    return table_occ

