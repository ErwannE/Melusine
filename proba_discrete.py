""" DISCRETISATION DE LA LOI DE PROBA DE LA DUREE D'ECLATEMENT

HYPOTHESE : Le temps d'éclatement est une variable aléatoire dont la loi de probabilité est modifié 
            par certains paramètres (nombre de colis lors de l'opération, regroupement du produits, mois)

OBJECTIF : Déterminer la loi de cette variable aléatoire "Temps d'éclatement"

METHODE : 
- On transforme les variables continues "Temps d'éclatement" et "Nombre de colis" en variable discrète en regroupant les valeurs dans certaines catégories 
    (ex : un temps d'élatement de 12min sera mi dans la catégorie "15 minutes", un colis homogène de 1152 objets sera mi dans la catégorie "1 000" objets)
- On considère que, pour chaque combinaison de catégories (nombre de colis, mois, regroupement) le temps suit une variables aléatoire (discrète, 
    raison pour laquelle on a discrétisé la variable "Temps d'éclatement")
- On calcule empiriquement les lois à l'aide de nos historiques. On a alors un outil prédictif donnant une probabilité d'éclatement pour un colis précis.

UTILISATION : 
Les jours de travail durant 7h, on sera amener à sommer les variables aléatoires précédentes afin de créer un emploi du temps. On peut gérer la probabilité de finir
dans les temps un planning (puisqu'on somme des variables aléatoires de lois connues) à l'aide d'un seuil à fixer alpha (par exemple, alpha=1% veut dire qu'il faut 
qu'une journée de travail doit réalisable dans au plus 99% des cas (compte tenu que le temps d'éclatement est considéré aléatoire, suivant les lois exprimées avant)).
Une fois un planning fait avec une certaine probabilité de réussite, on pourra alors avoir la date d'affrêtement.
"""

from discretisation import *
from analyse_poly_temps import ajouter_guillemets
import sqlite3 
conn = sqlite3.connect('data/melusine_database.db') #Outil permettant d'exploiter la base de donnée

def proba_condi(cat, mois, database='CEN_usable_sans_occ', timeleap = 15, seuils = [0, 250, 600, 1000, 1500]): 
    print("cat : "+cat+", mois : "+mois)
    if mois != 'mois':
        mois = ajouter_guillemets(mois) #Permet la compatibilité avec l'absence de paramètre demandé 
                            #(si aucun mois renseigné, la condition mois = mois est toujours respecté dans la requête, si renseigné la condition sur le mois en SQL doit être de la forme mois='val_mois')
    if cat != 'nom_regroupement':
        cat = ajouter_guillemets(cat) #Similaire 

    request = "SELECT hours, unite_oeuvre FROM " + database + " WHERE nom_regroupement=" + cat + " AND mois=" + mois
    df = pd.read_sql(request, conn)
    discret_hours(df, timeleap=timeleap)
    discret_unite(df, seuils=seuils)

    law = [[0 for i in range(int(7*(60/timeleap)))] for j in range(len(seuils))] # Les lois selon les différentes catégories d'unite (range(len(seuils))) et de temps
    occ = [0 for i in range(len(seuils))] # Compte les occurences dans chaque catégorie en vu de la normalisation

    for i in range(df.shape[0]):
        law[df.loc[i,"cat_unite_oeuvre"]][int(df.loc[i,'hours']*60/timeleap - 1)] += 1
        occ[df.loc[i,"cat_unite_oeuvre"]] += 1
    
    for i in range(int(7*(60/timeleap))): # Normalisation pour que la somme fasse 1
        for j in range(len(seuils)):
            law[j][i] /= occ[j]
    
    return law


def table_proba_condi(list_cat=['ML','TEXTILE','PARFUMERIE'], list_mois=['01','02','03','04','05','06','07','08','09','10'], database='CEN_usable_sans_occ', timeleap = 15, seuils = [0, 250, 600, 1000, 1500]):
    return {cat:{mois:proba_condi(cat, mois, database=database, timeleap=timeleap, seuils=seuils) for mois in list_mois} for cat in list_cat}