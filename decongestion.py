from subprocess import *
from math import sqrt

"""
Im
"""


def reconstruireChemin(graphe, begin, end, parents):
    """
    Renvoie le chemin reconstruit de begin à end dans graphe et None si n'existe pas (Fonction du cours)
    """
    chemin = type(graphe)()

    v = end

    while v != begin:

        if parents[v] == None:
            return None

        chemin.ajouter_arc(parents[v], v, graphe.poids_arc(parents[v], v))

        v = parents[v]

    return chemin




def cheminAugmentant(graphe, source, puits):
    """
    Renvoie un chemon de source à puits  de graphe ou None si n'existe pas (Fonction du cours)
    """
    already_visited = {}
    parents = {}

    for i in graphe.sommets():
        parents[i] = None
        already_visited[i] = False

    to_treat = list()
    to_treat.append(source)

    while to_treat != []:

        sommet = to_treat.pop()

        if sommet == puits:
            break

        if not already_visited[sommet]:

            already_visited[sommet] = True

            for successor in graphe.voisins(sommet):
                to_treat.append(successor)

                if parents[successor] == None:

                    parents[successor] = sommet


    return reconstruireChemin(graphe, source, puits, parents)





def augmenterFlot(flot, chemin):
    """
    Augmente le flot donné au maximul sur le chemin donné
    """
    min_cap = min([c for (one, two, c) in chemin.arcs()])

    for (u, v, c) in chemin.arcs():

        if (u, v) in flot:

            flot[(u, v)] = flot[(u, v)] + min_cap

        else:
            flot[(u, v)] = flot[(u, v)] - min_cap



def mettreAJourResiduel(graphe, graphe_f, arcs, flot):
    """
    Modifie les arcs du graphe résiduel 'graphe_f' suivant l'augmentation de flot subie.
    """
    cap_f = dict()

    for (u, v, c) in arcs:

        if graphe.contient_arc(v, u):

            tmp = u
            u = v
            v = tmp

        cap_f[(u, v)] = graphe.poids_arc(u, v) - flot[(u, v)]
        cap_f[(v, u)] = flot[(u, v)]

    for (u, v, c) in arcs:

        if cap_f[(u, v)] > 0:

            graphe.ajouter_arc(u, v, cap_f[(u, v)])
        else:

            graphe_f.retirer_arc(u, v)






def fordFulkerson(graphe):
    """
    Renvoie un flot maximum pour le graphe donné.
    """
    flot = dict()

    sauv_graphe = type(graphe)()

    for (u, v, c) in graphe.arcs():
        sauv_graphe.ajouter_arc(u, v, c)


    for (u, v, c) in graphe.arcs():

        flot[(u, v)] = 0


    for i in graphe.sources():
        source = i


    for i in graphe.puits():
        puits = i


    graphe_f = type(graphe)()

    for (u, v, c) in sauv_graphe.arcs():
        graphe_f.ajouter_arc(u, v, c)

    chemin = cheminAugmentant(graphe_f, source, puits)


    while chemin != None:
        augmenterFlot(flot, chemin)
        mettreAJourResiduel(sauv_graphe, graphe_f, chemin.arcs(), flot)
        chemin = cheminAugmentant(graphe_f, source, puits)


    return flot





def flot_maximum(graphe):
    """
    Renvoie le couple (valeur de flot, flot maximum) calculé sur le graphe donné.
    """

    #Calcul du flot maximum
    flot = fordFulkerson(graphe)


    val_flot = 0
    sources = graphe.sources()

    #on parcourt le flot et pour chaque source rencontrée
    #on regarde le flot sortant de cette source et on l'ajoute au résultar
    for (u, v) in flot:

        if u in sources:
            val_flot = val_flot + flot[(u, v)]



    return (val_flot, flot)





def reseau_residuel(reseau, flot):
    """
    Renvoie le réseau résiduel crée à l'aide du réseau et du flot circulant dans ce réseau.
    """

    #On reneverra un graphe
    result = type(reseau)()

    arcs = [(u, v) for u, v, c in reseau.arcs()]
    sommets = reseau.sommets()

    #arcs du résiduel
    arcs_f = set()


    for u in sommets:

        for v in sommets:

            #Si {u, v} est un arc du réseau
            if (u, v) in arcs:

                c_f = reseau.poids_arc(u, v) - flot[(u, v)]

                # On exclut les arc ayant 0 comme valeur de flot
                if c_f != 0:
                    arcs_f.add((u, v, c_f))

            # Si {v, u} est un arc du réseau
            if (v, u) in arcs:

                c_f = flot[(v, u)]

                # On exclut les arc ayant 0 comme valeur de flot
                if c_f != 0:
                    arcs_f.add((u, v, c_f))

    #On ajoute les arcs du graphe résiduel
    result.ajouter_arcs(arcs_f)

    return result





def sommets_accessibles(graphe, source):
    """
    Renvoie l'ensemble des sommets acessibles depuis un sommet source dans le graphe donné
    """
    sommets = [source]

    result = [source]

    #Tant qu'il existe des voisins
    while sommets != []:

        successors = []

        # Pour chaque sommet....
        for sommet in sommets:

            #....on regarde ses voisins dans le graphe
            for som in graphe.voisins(sommet):

                if som not in result:
                    successors.append(som)

        result = result + successors

        sommets = successors


    return set(result)



def coupe_minimum(residuel, sources):
    """
    Renvoie la coupe minimum du graphe résiduel donné selon les sommets sources donnés
    """
    s = []
    result = []

    # Pour chaque sommet source....
    for source in sources:

        #..... on ajoute à la liste les sommets accessibles depuis celle ci
        s = s + list(sommets_accessibles(residuel, source))

        #Pour chaque sommet du residuel...
        for u in residuel.sommets():

            if u not in s:

                result.append(u)


    return (s, result)









def augmentations_uniques_utiles(graphe, flot_max):
    """
    Renvoie l'ensemble des arcs dont l'augmentation de capacité permettrait à elle seule
    """

    result = set()
    graphe_f = reseau_residuel(graphe, flot_max)

    coupe_min = coupe_minimum(graphe_f, graphe.sources())

    # On parcourt tous les sommets du premier ensemble
    for u in coupe_min[0]:

        # On parcourt tous les sommets du second ensemble
        for v in coupe_min[1]:

            # Si le graphe contient un arc dont le premier sommet est dans un ensemble et le second dans l'autre
            # alors on ajoute au resultat
            if graphe.contient_arc(u, v) == True:

                result.add((u, v))

    return result








def arcs_entrants(graphe, sommet):
    """
    Renvoie l'ensemble arcs entrant en un sommet donné.
    """
    result = []

    for u in graphe.sommets():

        if graphe.contient_arc(u, sommet):
            result.append((u, sommet))


    return result



def arcs_sortants(graphe, sommet):
    """
    Renvoie l'ensemble des arcs sortants d'un sommet donné.
    """
    result = []

    for u in graphe.sommets():

        if graphe.contient_arc(sommet, u):
            result.append((sommet, u))

    return result





def augmentations_uniques_utiles_calibrees(graphe, flot_max):
    """
    Renvoie l'ensemble des arcs dont l'augmentation donnée dans le résultat permettrait d'augmenter le flot au maximum
    possible
    """
    graphe_f = reseau_residuel(graphe, flot_max)

    arcs = augmentations_uniques_utiles(graphe, flot_max)

    result = []

    # Pour chaque arc permettant une augmentation utile unique
    for u, v in arcs:

        poids_gauche = 0
        poids_droit = 0

        # On regarde les arcs à gauche (k, u)
        voisins_g = arcs_entrants(graphe, u)

        for u_bis, v_bis in voisins_g:

            poids = graphe_f.poids_arc(u_bis, v_bis)

            poids_gauche = poids_gauche + poids

        # On regarde les arcs à droite (v, k)
        voisins_d = arcs_sortants(graphe, v)
        for u_bis, v_bis in voisins_d:

            poids = graphe_f.poids_arc(u_bis, v_bis)

            poids_droit = poids_droit + poids


        # Si il y avait bien au moins un arc à gauche et un arc a droite
        if voisins_d != [] and voisins_g != []:

            result_to_append = min(poids_gauche, poids_droit)

            # On ajoute l'arc
            if result_to_append > 0:
                result.append(((u, v,), result_to_append))

        else:

            # S'il n'y a pas d'arc à droite
            if voisins_d == []:

                result_to_append = poids_gauche

                if result_to_append > 0:
                    result.append(((u, v), result_to_append))
            else:

                result_to_append = poids_droit

                if result_to_append > 0:
                    result.append(((u, v), result_to_append))


    return result



def augmentation_graphe(graphe, arc, augmentation):
    """
    Renvoie le graphe dans lequel on remplace l'arc donné par l'ancien arc ayant subit une augmentation donnée.
    """
    new_graphe = type(graphe)()

    for old_arc in graphe.arcs():

        if old_arc[0] == arc[0] and old_arc[1] == arc[1]:

            new_graphe.ajouter_arc(arc[0], arc[1], old_arc[2] + augmentation)

        else:

            new_graphe.ajouter_arc(old_arc[0], old_arc[1], old_arc[2])



    return new_graphe





def ensemble_minimum_augmentations_utiles_calibrees(graphe, flot_max, cible):
        """
        Renvoie l'ensemble des arrêtes à augmenter et de combien en capacité pour atteindre la valeur
        de flot cible donnée.
        """
        flot_restant = cible

        flot = flot_maximum(graphe)[0]
        flot_vise = flot + cible

        result = []

        # Tant que la valeur de flot après changement et la veleur de flot souhaitée
        # ne sont pas égales on continue l'algorithme
        while flot < flot_vise:

            choosen = None
            min_arc = None

            # On regarde les arcs d'augmentation
            arcs = augmentation_uniques_utiles_calibrees(graphe, flot_max)

            # Il n'existe plus aucun arc d'augmentation utile on renvoie None (aucun résultat
            # ne statistait la demande cible)
            if arcs == []:

                return None

            # Pour chacun des arcs d'augmentation
            for arc in arcs:

                # Si l'arc possède une augmentation egale au flot restant à pourovir pour atteindre la cible
                if arc[1] == flot_restant:
                    choosen = arc

                else:

                    # Sinon on prend l'arc d'augmentation minimum
                    if min_arc == None:
                        min_arc = arc

                    else:

                        if min_arc[1] > arc[1]:

                            min_arc = arc

            # On a eu un arc d'augmentation egale au flot restant
            if choosen != None:

                result.append(choosen)
                graphe = augmentation_graphe(graphe, (choosen[0][0], choosen[0][1]), choosen[1])
                flot_restant = flot_restant - choosen[1]

            # On a trouvé aucun arc correspondant
            elif min_arc != None:

                result.append(min_arc)
                graphe = augmentation_graphe(graphe, (min_arc[0][0], min_arc[0][1]), min_arc[1])
                flot_restant = flot_restant - min_arc[1]



            # Recalcul des valeur de flot
            (flot, flot_max) = flot_maximum(graphe)


        return result






def dist_euclidienne(a, b):
    """
    Renvoi le résultat de la distance euclidienne entre les points de coordonnées en 2D des
    sommets a et b
    """
    (xa, ya) = a
    (xb, yb) = b


    result = sqrt(((xb - xa) ** 2) + ((yb - ya) ** 2))

    return result



def val_flot(graphe, flot_max):
    """
    Renvoie la valeur d'une flot donné
    """
    somme = 0

    for src in graphe.sources():

        for dest in graphe.voisins(src):

            somme = somme + flot_max[(src, dest)]


    return somme





def augmentation(graphe, u, v, flot_max):
    """
    Renvoie la valeur de l'augmentation unique maximum de l'arc {u, v} dans le graphe (Le procèdé est le même que dans
    la fonction précédente calculant les capacité des arcs maximum menant à une augmentation de flot)
    """

    entrants = arcs_entrants(graphe, u)
    sortants = arcs_sortants(graphe, v)

    graphe_f = reseau_residuel(graphe, flot_max)

    poids_gauche = 0
    poids_droit = 0

    for u, v in entrants:

        poids = graphe_f.poids_arc(u, v)

        poids_gauche = poids_gauche + poids


    for u, v in sortants:

        poids = graphe_f.poids_arc(u, v)

        poids_droit = poids_droit + poids



    if entrants != [] and sortants != []:

        result_to_append = min(poids_gauche, poids_droit)

        if result_to_append > 0:
            return result_to_append

    else:

        if sortants == []:

            result_to_append = poids_gauche

            if result_to_append > 0:
                return result_to_append
        else:

            result_to_append = poids_droit

            if result_to_append > 0:
                return result_to_append

    return -1


def rajouts_uniques_utiles(graphe, flot_max):
    """
    Renvoie l'ensemble des arcs avec leur budget et la capacité maximum pour laquelle cela ajouterait une augmentationnde
    de valeur de flot dans le graphe donné.
    """
    sommets = graphe.sommets()

    flot_circulant = flot_max
    flot_max = val_flot(graphe, flot_max)

    result = []


    for u in sommets:

        for v in sommets:

            graphe_tmp = type(graphe)()

            for a, b, c in graphe.arcs():
                graphe_tmp.ajouter_arc(a, b, c)


            # Si l'arrête respecte ces conditions, on l'ajoute au graphe residuel
            if u != v and not graphe.contient_arc(v, u) and not graphe.contient_arc(u, v) and v not in graphe_tmp.sources() and u not in graphe_tmp.puits():

                # On donne un capacité de 1 car on veut voir si il y a bien une augmentation de flot
                # pour une valeur minimale
                graphe_tmp.ajouter_arc(u, v, 1)

                # si on voit que le flot augmente en rajoutant cet arc avec une capacité minimale de 1
                if flot_maximum(graphe_tmp)[0] > flot_max and not (u in graphe_tmp.sources() and v in graphe_tmp.puits()):

                    p = graphe.coord(u)
                    q = graphe.coord(v)

                    increase = augmentation(graphe, u, v, flot_circulant)

                    if increase != -1:

                        result.append((u, v, dist_euclidienne(p, q), increase))


    return result












"""
def ensemble_optimal_rajouts(graphe, flot_max, budget):

    budget_restant = budget

    flot = flot_maximum(graphe)[0]

    flot_vise = flot + cible

    result = []

    while True:

        choosen = None
        min_arc = None

        arcs = rajouts_uniques_utiles(graphe, flot_max)

        if arcs == []:
            return None

        for arc in arcs:

            if arc[1] == flot_restant:
                choosen = arc

            else:

                if min_arc == None:
                    min_arc = arc

                else:

                    if min_arc[1] > arc[1]:
                        min_arc = arc

        if choosen != None:

            result.append(choosen)
            graphe = augmentation_graphe(graphe, (choosen[0][0], choosen[0][1]), choosen[1])
            flot_restant = flot_restant - choosen[1]

        elif min_arc != None:

            result.append(min_arc)
            graphe = augmentation_graphe(graphe, (min_arc[0][0], min_arc[0][1]), min_arc[1])
            flot_restant = flot_restant - min_arc[1]

        (flot, flot_max) = flot_maximum(graphe)

        # print("Result : ", result)
        # print("Flot restant : ", flot, flot_vise, flot_max)

    return result


"""












def export_dot(graphe):
    """
    Renvoie une chaîne encodant le graphe au format dot.
    (Version Graphes pondérés)

    """

    encodage = "digraph G {\n"


    for sommet in graphe.sommets():

        encodage = encodage + str(sommet) + ";\n"


    liaisons = graphe.arcs()

    for arc in liaisons:

        encodage = encodage + str(arc[0]) + " -> " + str(arc[1]) + " [label=\"" + str(arc[2]) + "\"]" + ";\n"

    encodage = encodage + "}"
    return encodage


def create_dot(graphe, file_name):
    """
    Crée un fichier .dot avec les informations du graphe donné

    :param graphe: Graphe dont les données seront formattées pour concevoir une fichier d'extension .dot
    :param file_name: String représentant le nom du fichier sans l'extension

    """

    file_name = file_name + ".dot"

    run(["touch", file_name])

    file = open(file_name, 'w')

    file.write(export_dot(graphe))

    file.close()


def execute_dot(file_name):
    """
    Permet d'executer un fichier .dot et ouvrir l'image produite par la configuration/données du fichier

    :param file_name: String représentant le nom du fichier sans l'extension

    """
    picture_name = file_name + ".png"
    file_name = file_name + ".dot"

    run(["circo", "-Tpng", file_name, "-o", picture_name])
    run(["open", picture_name])


def launch_graphe(graphe, file_name):
    """
    Fonction qui crée puis lance la commande terminale permettant d'ouvrir l'image du graphe
    """
    create_dot(graphe, file_name)
    execute_dot(file_name)






"""
if __name__ == '__main__':


    G = Graphe()

    #G.ajouter_arc('s', 'v', 4)
    #G.ajouter_arc('v', 't', 2)

    for sommet, coordonnees in [('s', (0, 0)), ('a', (1.5, 1)), ('b', (1.5, -1)), ('c', (3, 0)), ('d', (4.5, 1)), ('e', (4.5, -1)), ('t', (6, 0))]:
        G.ajouter_sommet(sommet, coords=coordonnees)


    for u, v, c in [('s', 'a', 4), ('s', 'b', 4), ('a', 'd', 1), ('a', 'c', 3), ('b', 'c', 3), ('b', 'e', 1),
                    ('c', 't', 2), ('d', 't', 2), ('e', 't', 4)]: G.ajouter_arc(u, v, c)

    #launch_graphe(G, "Graphe_capacité")


    flot = flot_maximum(G)

    print("\nFlot : ", flot, "\n")




    g_flot = Graphe()

    for (u, v) in flot[1]:

        g_flot.ajouter_arc(u, v, flot[1][(u, v)])


    launch_graphe(g_flot, "Graphe_flot")

    flot_2 = {('s', 'a'): 0, ('s', 'b'): 0, ('a', 'd'): 0, ('a', 'c'): 0, ('b', 'e'): 0, ('b', 'c'): 0, ('d', 't'): 0, ('c', 't'): 0, ('e', 't'): 0}

    g_f = reseau_residuel(G, flot[1])
    print("Residuel : ", g_f.arcs())

    #launch_graphe(g_f, "Graphe_residuel")


    print("Coupe minimum : ", coupe_minimum(g_f, G.sources()))



    print("Augmentation unique utile : ", sorted(augmentations_uniques_utiles(G, flot[1])))


    print("Augmentations utiles calibrées : ", augmentation_uniques_utiles_calibrees(G, flot[1]))


    print("Ensemble augmentations utiles calibrées : ", ensemble_minimum_augmentations_utiles_calibrees(G, flot[1], 5))





    print("Rajouts uniques utiles", rajouts_uniques_utiles(G, flot[1]))
"""