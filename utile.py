def ajouter_guillemets(chaine):
    """Ajoute des guillemets au début et à la fin de la chaîne."""
    return f'"{chaine}"'

def liste_indice_priorite(liste, k):
    """Renvoie une liste comprenant les indices i auxquels liste[i]=k"""
    L=[]
    for i in range(len(liste)):
        if liste[i] == k:
            L.append(i)
    return L