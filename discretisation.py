import pandas as pd #Bibliothèque des dataframes
import numpy as np  #Fonctions mathématiques

def discret_unite(df, colonne = "unite_oeuvre", seuils = [0, 250, 600, 1000, 1500]): #Modifie le champ de façon à discretiser les valeurs d'unités grace aux seuils

    def cat_discretisation(val, seuil): #Renvoie la valeur de catégorie de la valeur val
        assert val >= seuil[0], "la valeur doit être supérieur au premier seuil"
        for i in range(len(seuil)-1):
            if val < seuil[i+1]:
                return i
        return len(seuil)-1

    try:
        n_colonne=[cat_discretisation(df.loc[i,colonne], seuils) for i in range(df.shape[0])]
        nouvelle_serie = pd.Series(n_colonne, name="cat_"+colonne)
        df["cat_" + colonne] = nouvelle_serie

    except KeyError:
        print("La colonne " + colonne + " n'existe pas dans le dataframe")

def discret_hours(df, column='hours', timeleap = 15): #Formate le champ 'column" du dataframe de facon à arrondir les temps d'opérations dans des "espaces de temps" timeleap (multiples de timeleap, en minutes)
    try:
        mult = 60/timeleap
        df[column] = np.ceil(np.array(df[column].tolist())*mult)/mult #Conversion en array numpy pour utiliser ceil

    except KeyError:
        print("La colonne " + column + " n'existe pas dans le dataframe")