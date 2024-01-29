def somme_proba_temps(X, Y):
    """La fonction permet de calculer les probas de la somme de deux variables aléatoires discretes (stocke sous forme de liste)
    ATTENTION : Cette fonction n'est adapte que pour les listes en temps.
    Elle revoie sous forme de liste la loi de la somme X+Y 
    
    Les categories de temps sont des multiples du timeleap (15 min), on remarque donc que pour Z = X + Y, 
    Z[i] = P(Z = 15 * (i+1)) = SOMME(P(X = 15*j) * P(Y = 15*k) avec j+k = i+1) = SOMME(X[j-1] * Y[k-1] avec j+k = i+1) = SOMME(X[j] * Y[k] avec j+k = i-1)
    On remarque que Z est bornée par les bornes de X et Y (la valeur max de Z est la valeur max de X + la valeur max de Y), ce qui justifie la taille de la liste Z
    """
    #print(X, Y)
    Z=[0 for i in range(len(X)*len(Y) - 1)] 
    for i in range(1,len(X)*len(Y) - 1):
        #print(i)
        for j in range(i):
            k=i-j-1
            if j<(len(X)) and k < len(Y): #On balaye les combinaisons valable pour faire le calcul
                Z[i]+=X[j]*Y[k]
    return Z

def adapt_size_va(X, max_size = 7*4):
    if len(X) > max_size:
        end_val = sum(X[max_size:])
        X = X[:max_size]
        X[-1] += end_val
    return X

def temps_sc_alpha(X, alpha=0.01):
    """ Objectif de la fonction : Donner le temps qu'on doit accorder à une tâche afin d'etre sur de pouvoir réaliser la tache sauf dans alpha% des cas

    Entree : X = liste donnant la loi discrète des variables aleatoires en temps (représentant la tâche à accomplir), alpha = seuil

    Sortie : L'index de la liste, correspondant au temps qu'il faut s'accorder"""
    for i in range(1,len(X)):
        if sum(X[:len(X)-i+1])<1-alpha:
            return len(X)-i+1
    return 0

#print(temps_sc_alpha(somme_proba_temps([0,1,0,0], [0.5, 0.5,0,0])))