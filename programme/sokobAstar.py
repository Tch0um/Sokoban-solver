
from copy import deepcopy
    
class Sommet(object):

    def __init__(self, x, y, F, direction = (0,0), predecesseur = None):

        self.x = x
        self.y = y
        self.F = F
        self.direction = direction  #Direction par lequel nous sommes arrivés à ce sommet/noeud
        self.predecesseur = predecesseur

    def __repr__(self):
        if self.predecesseur == None:
            precedent = "None"
        else:
            precedent = "("+str(self.predecesseur.x)+","+str(self.predecesseur.y)+")"
        return "("+str(self.x)+","+str(self.y)+")  F = "+str(self.F)+"  prédécesseur = "+precedent
    
        



def Astar(grille, depart, arrivee, coordPerso=None, barique = 1, direction = [(1,0), (-1,0), (0,1), (0,-1)]):
    """
    :param grille: Grille contenant nécessairement le point de départ et le point d'arrivé. Au mieux, cette grille est seulement d'une largeur/hauteur correspondant au déplacement maximal de l'unité de départ. Cette grille ne doit contenir que des 1 (chemin possible) et des 0 (obstacles).
    :type grille: list                                             !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    :param depart: Coordonnées x,y de départ du chemin à réaliser. !-!-!-!-!DOIT CORRESPONDRE AUX COORDONNEES DE LA BARIQUE A DEPLACER!-!-!-!-!
    :type depart: tuple                                            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    :param arrivee: Coordonnées x,y d'arrivée du chemin à réaliser.
    :type arrivee: tuple
    :param coordPerso: Coordonnée du personnage au lancement d'Astar.
    :type coordPerso: tuple
    :param barique: Vrai si le Astar lancé est pour la barique, sinon Faux, ce qui correspond au déplacement du joueur (En cas de changement d'orientation)
    :type barique: boolean
    :param direction: Directions possible à partir d'une case. Exemple: [(1,0),(-1,0),(0,1),(0,-1)]
    :type direction: list of tuple
    """

    #Variables présente
    #depart : Sommet source
    #arrivee : Sommet destination
    #E : Liste des sommets à explorer, par défaut contient depart
    #V : Liste des sommets visités, par défaut vide
    #X : Sommet, ou liste des sommets, le(s) plus court(s)
    #x et y les coordonnées d'un sommet
    #F le coût de déplacement entre le point de départ et l'arrivée
    #predecesseur le pointeur vers le sommet précédent du chemin en cours
    #newCoord : Variable temporaire permettant d'analyser les cases adjacentes à celle (la case) en cours d'analyse
    #FIN : Si None, aucun chemin n'est possible, sinon lance le retraçage du chemin
    #precedent: Variable temporaire permettant de "remonter" le chemin arrivé à la cible voulue
    #Chemin : Liste des coordonnées des sommets par lequel le chemin passe
    

    arrivee = Sommet(arrivee[0], arrivee[1], 0)
    depart = Sommet(depart[0], depart[1], 0, None)
    E = [depart]
    V = []
    #sens = (0,0)    #Sens dans lequel se dirige la barique/personnage. Permet de détecter la modification de direction et donc le relancement d'Astar si besoin.
    
    while E != [] and (arrivee.x,arrivee.y) not in [(A.x,A.y) for A in E]:
        # print("E : ",E)
        #Récupération du sommet X de coût F minimum
        X = None
        for i in E:
            if X==None or i.F < X.F:
                X = i

        #Ajout de X à la liste V, donc on l'enlève de E
        E.remove(X)
        V.append(X)
        
        V_coords = [(i.x,i.y) for i in V]   #Permet des comparaisons de sommet plus facilement à l'aide de leurs coordonnées

        #Ajout des successeurs de X (non visités) à la liste E
        for i in direction:
            #Si les coordonnées appartiennent bien à la grille donnée
            if i[0]+X.x >= 0 and i[0]+X.x < len(grille[0]) and i[1]+X.y >= 0 and i[1]+X.y < len(grille):
                #Si ces coordonnées ne correspondent pas à un obstacle
                if grille[i[1]+X.y][i[0]+X.x]:
                    if barique and i != X.direction:    #Si changement de direction il y a
                        grilleTmp = deepcopy(grille)    #Copie d'une grille temporaire
                        grilleTmp[X.y][X.x] = 0         #La barique devient un obstacle pour le déplacement du personnage
                        if X.predecesseur != None : coordPerso = (X.predecesseur.x,X.predecesseur.y)    #Condition pour traiter aussi l'état initial
                        if Astar(grilleTmp,coordPerso,(X.x-i[0],X.y-i[1]),None,0):  #Si Astar trouve un chemin pour que le Perso se mette dans les conditions nécessaire au changement de direction de la barique
                            newCoord = Sommet(i[0]+X.x, i[1]+X.y, ((V[-1].F+1)+abs(i[0]+X.x-arrivee.x)+abs(i[1]+X.y-arrivee.y)-(abs(V[-1].x-arrivee.x)+abs(V[-1].y-arrivee.y))), i, V[-1])
                            #Si ces coordonnées n'ont pas déjà été visité
                            if (newCoord.x,newCoord.y) not in V_coords:
                                #Si successeurs déjà dans E, et coût F inférieur au successeur déjà présent, alors remplacer coût et successeur
                                if (newCoord.x,newCoord.y) in [(k.x,k.y) for k in E]:
                                    for j in E:
                                        if (newCoord.x,newCoord.y) == (j.x,j.y):
                                            if newCoord.F < j.F:
                                                j.F = newCoord.F
                                                j.predecesseur = newCoord.predecesseur
                                else:
                                    E.append(newCoord)
                    else:
                        newCoord = Sommet(i[0]+X.x, i[1]+X.y, ((V[-1].F+1)+abs(i[0]+X.x-arrivee.x)+abs(i[1]+X.y-arrivee.y)-(abs(V[-1].x-arrivee.x)+abs(V[-1].y-arrivee.y))), i, V[-1])
                        #Si ces coordonnées n'ont pas déjà été visité
                        if (newCoord.x,newCoord.y) not in V_coords:
                            #Si successeurs déjà dans E, et coût F inférieur au successeur déjà présent, alors remplacer coût et successeur
                            if (newCoord.x,newCoord.y) in [(k.x,k.y) for k in E]:
                                for j in E:
                                    if (newCoord.x,newCoord.y) == (j.x,j.y):
                                        if newCoord.F < j.F:
                                            j.F = newCoord.F
                                            j.predecesseur = newCoord.predecesseur
                            else:
                                E.append(newCoord)

    #Récupération du chemin
    FIN = None
    for i in E:
        if (i.x,i.y) == (arrivee.x,arrivee.y):
            FIN = i

    #Si FIN n'est pas None, donc qu'un chemi existe bien
    if FIN:
        precedent = FIN.predecesseur
        Chemin = [(FIN.x,FIN.y,"Heuristique:"+str(FIN.F))]
        while precedent != None:
            Chemin.append((precedent.x,precedent.y,"Heuristique:"+str(precedent.F)))
            precedent = precedent.predecesseur
        Chemin.reverse()
        Chemin = Chemin[1:] #On supprime les coordonnées de départ
        #Test
        return Chemin
    else:
        return False


def essai():
    g = [[1,1,1,0,0,0,1,1,1],[1,1,0,1,1,1,0,1,1],[1,0,1,1,1,1,1,0,1],[0,1,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,1,0],[0,1,1,1,1,1,1,1,0],[1,0,1,1,1,1,1,0,1],[1,1,0,1,1,1,0,1,1],[1,1,1,0,0,0,1,1,1]]
    for x in g:
        for y in x:
            print(y,end='')
        print()
    print(Astar(g,(3,5),(4,2),(1,4)))


