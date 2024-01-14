from fonction_proba import *
from utile import liste_indice_priorite

def planning_jour(liste_va_tache, liste_priorite, nombre_ouvrier, heure=7, alpha=0.01):
    """ Objectif de la fonction : Determiner les emplois du temps des choses des taches à faire en fonction d'une liste de tache, 
    d'une liste de priorite (associe à la liste de tache), du nombre d'ouvrier et du nombre d'heure de travail (fixe à 7h et non à 
    6h30 pour etre en accord avec les donnees).

    Entree : liste_va_tache = liste de loi de variable aléatoire associé aux taches, liste_priorite = liste associe aux taches (dans 
    le meme ordre !) donnant les ordres de priorite de realisation des taches (nombre de jour jusqu'a date limite), 
    nombre_ouvrier = nombre d'ouvrier travaillant ce jour la, heure = nombre d'heure de travail de chaque ouvrier, 
    alpha = seuil de surete (quel pourcentage d'erreur de plannification (planning trop long pour la journee) est admissible)

    Sortie : liste comprenant l'indice de la liste des taches qu'ils doivent faire ce jour, avec en dernière liste les indices des
    taches non realisees ce jour la

    """
    L=[[] for i in range(nombre_ouvrier+1)]
    liste_va_ouvrier = [0 for i in range(nombre_ouvrier+1)] # le planning d'un ouvrier est modelise comme une variable aleatoire, c'est la somme des variables aleatoires associees aux taches qu'il doit faire
    priorite_max = max(liste_priorite)
    priorite_min = min(liste_priorite)

    for p in range(priorite_min, priorite_max+1):
        indice_prio = liste_indice_priorite(liste_priorite, p)
        for k in indice_prio:
            tache=liste_va_tache[k]
            in_planning=False
            for i in range(nombre_ouvrier): #On parcourt les ouvriers pour voir si cette tache peut s'ajouter à son planning
                if liste_va_ouvrier[i]==0:
                    liste_va_ouvrier[i]=tache
                    L[i].append(k)
                    in_planning=True
                    break
                if (temps_sc_alpha(somme_proba_temps(liste_va_ouvrier[i],tache),alpha) + 1)/4 <= heure:
                    liste_va_ouvrier[i] = somme_proba_temps(liste_va_ouvrier[i], tache)
                    L[i].append(k)
                    in_planning=True
                    break

            if not in_planning:
                L[nombre_ouvrier].append(k) 

    return L

def test_plannif():
    liste_va = [[0,1,0,0], [0.5, 0.5,0,0], [1], [0,2/3, 1/3], [0.5, 0, 0.5],[0,2/3, 1/3],[0,2/3, 1/3]]
    liste_prio = [0, 3, 2, 2, 1, 2, 7]
    print(planning_jour(liste_va, liste_prio, nombre_ouvrier=2, heure=2))
            
test_plannif()

    