import pandas as pd
from sqlalchemy import create_engine


def name_doc(document): #take a document.extention, return it's name without the extension
    for i in range(1,len(document)):
        if document[len(document)-i] == '.':
            return document[:len(document)-i]

def refresh_database():
    path = 'data/'
    list_doc = ['CEN.xlsx','Colis moyens par UM par circuit CEN.xlsx','manif_2023.xlsx','prev_recep_melusine.xlsx','ratios.xlsx','ex_engt r120 manif 632 2024_du211223.xlsx']
    database = path + 'melusine_database.db'
    engine = create_engine('sqlite:///' + database)
    for doc in list_doc:
        if name_doc(doc) == 'CEN': # Lecture de CEN.xlsx (particulier car la colonne 13 fait crasher le programme (mais elle est inutile))
            df_cen = pd.read_excel('data/CEN.xlsx')
            df_cen.drop('time_consumed', axis=1, inplace=True)
            df_cen.to_sql('CEN', engine, index=False, if_exists='replace')
        
        elif name_doc(doc) == 'manif_2023': # Lecture de manif_2023.xlsx (particulier car les donnés commencent à la 3eme ligne + seulement les 6 colonnes sont utiles)
            df_prev = pd.read_excel('data/manif_2023.xlsx', header=2)
            df_nouveau = df_prev.iloc[0:, :6]
            df_nouveau.to_sql('manif_2023', engine, index=False, if_exists='replace')

        elif name_doc(doc) == 'Colis moyens par UM par circuit CEN': # Lecture de 'Colis moyens par UM par circuit CEN.xlsx (particulier, données commencent ligne 3)
            df_colis = pd.read_excel('data/Colis moyens par UM par circuit CEN.xlsx', header=2)
            df_colis.to_sql('Colis moyens par UM par circuit CEN', engine, index=False, if_exists='replace')
        
        else:
            df = pd.read_excel(path + doc)
            df.to_sql(name_doc(doc), engine, index=False, if_exists='replace')
            
        print(doc + " has been updated")

refresh_database()
