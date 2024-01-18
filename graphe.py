#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Implémentation de la classe Graphe()
"""


class Graphe(object):
    def __init__(self):
        """
        Initialise un graphe sans arêtes
        """
        self.dictionnaire = dict()

        self.coords = dict()

    def ajouter_arcs(self, iterable):
        """
        Ajoute tous les arcs de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple).
        """
        for u, v, poids in iterable:
            self.ajouter_arc(u, v, poids)

    def ajouter_sommet(self, sommet, coords = (0, 0)):
        """
        Ajoute un sommet (de n'importe quel type hashable) au graphe.
        """
        self.dictionnaire[sommet] = set()
        self.coords[sommet] = coords

    def ajouter_sommets(self, iterable):
        """
        Ajoute tous les sommets de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des éléments hashables.
        """
        for sommet in iterable:
            self.ajouter_sommet(sommet)

    def boucles(self):
        """
        Renvoie les boucles du graphe, c'est-à-dire les arêtes reliant un
        sommet à lui-même.
        """
        return {
            (u, u, other_u[1]) for u in self.dictionnaire

            for other_u in self.dictionnaire[u]

            if other_u[0] == u
        }

    def contient_arc(self, u, v):
        """
        Renvoie True si l'arc {u, v} existe, False sinon.
        """
        if self.contient_sommet(u) and self.contient_sommet(v):

            for k in self.dictionnaire[u]:
                if k[0] == v:
                    return True
            return False
        return False

    def contient_sommet(self, u):
        """
        Renvoie True si le sommet u existe, False sinon.
        """
        return u in self.dictionnaire

    def degre(self, sommet):
        """
        Renvoie le nombre de voisins du sommet; s'il n'existe pas, provoque
        une erreur.
        """
        return len(self.dictionnaire[sommet])

    def nombre_arcs(self):
        """
        Renvoie le nombre d'arcs du graphe.
        """
        return len(self.arcs())

    def nombre_boucles(self):
        """
        Renvoie le nombre d'arêtes de la forme {u, u}.
        """

        return len(self.boucles())

    def nombre_sommets(self):
        """
        Renvoie le nombre de sommets du graphe.
        """
        return len(self.dictionnaire)

    def retirer_arc(self, u, v):
        """
        Retire l'arc {u, v} si elle existe; provoque une erreur sinon.
        """

        for paire in self.dictionnaire[u]:

            if paire[0] == v:
                self.dictionnaire[u].remove((v, paire[1]))  # plante si u ou v n'existe pas
                break

        for paire in self.dictionnaire[v]:

            if paire[0] == u:
                self.dictionnaire[v].remove((u, paire[1]))  # plante si u ou v n'existe pas
                break

    def retirer_arcs(self, iterable):
        """
        Retire tous les arcs de l'itérable donné du graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple).
        """
        for u, v, poids in iterable:
            self.retirer_arc(u, v)

    def retirer_sommet(self, sommet):
        """
        Efface le sommet du graphe, et retire toutes les arêtes qui lui
        sont incidentes.
        """
        del self.dictionnaire[sommet]
        # retirer le sommet des ensembles de voisins
        for u in self.dictionnaire:

            for paire in self.dictionnaire[u]:

                if paire[0] == sommet:
                    self.dictionnaire[u].discard((paire[0], paire[1]))
                    break

    def retirer_sommets(self, iterable):
        """
        Efface les sommets de l'itérable donné du graphe, et retire toutes
        les arêtes incidentes à ces sommets.
        """
        for sommet in iterable:
            self.retirer_sommet(sommet)

    def sommets(self):
        """
        Renvoie l'ensemble des sommets du graphe.
        """
        return set(self.dictionnaire.keys())

    def sous_graphe_induit(self, iterable):
        """
        Renvoie le sous-graphe induit par l'itérable de sommets donné.
        """
        G = Graphe()
        G.ajouter_sommets(iterable)
        for u, v, c in self.arcs():
            if G.contient_sommet(u) and G.contient_sommet(v):
                G.ajouter_arc(u, v, c)
        return G

    def voisins(self, sommet):
        """
        Renvoie l'ensemble des voisins du sommet donné.
        """
        return {
            u[0] for u in self.dictionnaire[sommet]
        }


    def poids_arc(self, u, v):
        """
        Renvoie la capacité de flot d'un arc {u, v}
        """
        if u in self.dictionnaire and v in self.dictionnaire:

            for i in self.dictionnaire[u]:

                if i[0] == v:
                    return i[1]

        return -1

    def arcs(self):
        """
        Renvoie l'ensemble des arcs du graphe. Une arête est représentée
        par un tuple (a, b) avec a <= b afin de permettre le renvoi de boucles.
        """
        return [
            (u, v[0], v[1]) for u in self.dictionnaire
            for v in self.dictionnaire[u]
        ]

    def transform_tuple(self, a, b, poids):
        """
        Trie les coordonnées des sommets de l'arc donnée par ordre croissant
        """
        if a > b:
            return (b, a, poids)

        return (a, b, poids)


    def sources(self):
        """
        Renvoie les sommets sources du graphe
        """
        res = set()

        not_sources = set()

        for u in self.dictionnaire:

            res.add(u)

            for i in self.dictionnaire[u]:
                not_sources.add(i[0])

        for v in not_sources:

            res.remove(v)

        return res

    def puits(self):
        """
        Renvoie les sommets puits du graphe
        """
        res = set()

        for u in self.dictionnaire:

            if self.dictionnaire[u] == set():

                res.add(u)

        return res



    def ajouter_arc(self, u, v, capacite):
        """
        Ajoute au graphe l'arc {u, v, capacite} avec capacité la capacité de flot de l'arc
        """
        # vérification de l'existence de u et v, et création(s) sinon
        if u not in self.dictionnaire:
            self.ajouter_sommet(u)
            self.dictionnaire[u] = set()
        if v not in self.dictionnaire:
            self.ajouter_sommet(v)
            self.dictionnaire[v] = set()

        # ajout de u (resp. v) parmi les voisins de v (resp. u)
        self.dictionnaire[u].add((v, capacite))



    def coord(self, sommet):
        """
        Renvoie les coordonnées du sommet donné.
        """

        if self.contient_sommet(sommet) == False:

            return None

        return self.coords[sommet]











