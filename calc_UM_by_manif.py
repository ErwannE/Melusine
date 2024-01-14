'''
Pour obtenir les dates prédictives de fin de production des palettes, il est nécessaire de savoir combien de palettes
nous allons constituer pour chaque manifestation. Cela nous permettra de connaître le temps total de travail à 
effectuer et ainsi de mieux répartir dans le temps les opérations à effectuer par les opérateurs.
'''
import pandas as pd
import sqlite3 
conn = sqlite3.connect('data/melusine_database.db') #Outil permettant d'exploiter la base de données

# ETAPE 1 : Récupérer les données du nombre de colis par produit par manifestation

def get_nb_colis_by_manif(data_table = 'PRépa CEN'): # Crée ou met à jour la table dans la database
    # Si la table n'existe pas, on la crée
    request = 'CREATE TABLE IF NOT EXISTS nb_colis_par_manif AS SELECT ITEMID, ITEMLL, RAYID, MNFID,\
          SUM("SUM(NBPRISEPREP)") AS TotalNBPRISEPREP FROM "' + data_table + '" GROUP BY ITEMID'
    conn.execute(request)

    # Sinon, on update la table déjà existante
    insert_request = f'''
        INSERT INTO nb_colis_par_manif
        SELECT ITEMID, ITEMLL, RAYID, MNFID, SUM("SUM(NBPRISEPREP)") as TotalNBPRISEPREP
        FROM "{data_table}"
        GROUP BY ITEMID, ITEMLL, RAYID, MNFID
    '''
    conn.execute(insert_request)
    

# get_nb_colis_by_manif()

# ETAPE 2 : Calculer le volume de chaque colis de chaque produit pour établir le volume total des manif DEJA CONNUES
    # (étude des données pour prévoir le volume futur)
    
def create_useful_table_vol_col(data_table = 'prev_recep_melusine'): 
    # Prend uniquement les données qui nous intéressent
    # Si la table n'existe pas, on la crée
    request = f'''
        CREATE TABLE IF NOT EXISTS "{data_table}_useful" AS SELECT RAYON, IMPORT, manifestation, "nb colis",\
            "volume prévisionnel"/"nb colis" AS volume_prev_par_colis, "volume prévisionnel" AS "volume_prev_total", \
                "volume réel cde import"/"nb colis" AS volume_reel_par_colis, "volume réel cde import" FROM "{data_table}"\
                      WHERE "volume prévisionnel" IS NOT NULL
    '''
    conn.execute(request)

    # Sinon, on update la table déjà existante
    insert_request = f'''
        INSERT INTO "{data_table}_useful"
        SELECT RAYON, IMPORT, manifestation, "nb colis", "volume prévisionnel"/"nb colis" AS volume_prev_par_colis, \
            "volume prévisionnel" AS "volume_prev_total", "volume réel cde import"/"nb colis" \
                AS volume_reel_par_colis, "volume réel cde import" FROM "{data_table}" \
                    WHERE "volume prévisionnel" IS NOT NULL
    '''
    conn.execute(insert_request)

# create_useful_table_vol_col
    
# ETAPE 3 : prévoir le volume de chaque colis de chaque manif pour les manif à venir
    
# ETAPE 4 : établir le volume total de la manif et diviser par le volume d'une palette pour obtenir le nb de palettes

