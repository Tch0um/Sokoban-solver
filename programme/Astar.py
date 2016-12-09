from classes import *

def triggerIA(niveau,fen):
    liste = niveau.selectTarget()
    number = len(liste[0])
    for z in range(number):
        cPerso = niveau.findPersonnage()
        caisseN = niveau.gameO[cPerso[0]][cPerso[1]].selectCaisse(liste[0])
        grille = niveau.grilleObstacle()
        grille[liste[0][caisseN].x][liste[0][caisseN].y]=1
        ls = Astar(grille,(liste[0][caisseN].x,liste[0][caisseN].y),(liste[1][caisseN].x,liste[1][caisseN].y))
        print(str(ls)+' '*5+'ligne 12')
        commandePerso(ls,niveau.gameO[cPerso[0]][cPerso[1]],liste[0][caisseN],niveau,fen)
        del liste[0][caisseN]
        del liste[1][caisseN]

def commandePerso(ls,perso,caisse,niveau,fen):
    for n in ls:
        if (perso.x,perso.y)!=(caisse.x-n[0],caisse.y-n[1]):
            grille = niveau.grilleObstacle()
            grille[perso.x][perso.y]=1
            print(str(((caisse.x-n[0],caisse.y-n[1]),(perso.x,perso.y)))+' '*5+'ligne 25')
            lsPerso = Astar(grille,(perso.x,perso.y),(caisse.x-n[0],caisse.y-n[1]))
            print(str(lsPerso)+' '*5+'ligne 27')
            for dep in lsPerso:
                deplacement(perso,(perso.x+dep[0],perso.y+dep[1]),niveau,fen,dep)
        deplacement(perso,(caisse.x,caisse.y),niveau,fen,n)



def deplacement(perso,ar,niveau,fen,di):
    print(ar)
    if di ==(1,0):
        perso.deplace(1,niveau,fen)
    elif di ==(-1,0):
        perso.deplace(-1,niveau,fen)
    elif di ==(0,1):
        perso.deplace(2,niveau,fen)
    else:
        perso.deplace(-2,niveau,fen)
    print('destination : '+str((perso.x,perso.y)))


def Astar(grille,depart,ar):#liste de liste -- tuple -- tuple
    openSet,closeSet = [],[]
    start = Noeud(depart[0],depart[1],0)
    end = Noeud(ar[0],ar[1],0,0)

    openSet.append(start)

    while openSet!=[] and (end.x,end.y) not in [(n.x,n.y) for n in openSet]:
        noeud = None
        for n in openSet:
            if noeud==None or n.C < noeud.C:
                noeud = n

        openSet.remove(noeud)
        closeSet.append(noeud)
        for i in ((1,0), (-1,0), (0,1), (0,-1)):
            if i[0]+noeud.x >= 0 and i[0]+noeud.x < len(grille[0]) and i[1]+noeud.y >= 0 and i[1]+noeud.y < len(grille) and grille[i[0]+noeud.x][i[1]+noeud.y]:
                newCoord = Noeud(i[0]+noeud.x, i[1]+noeud.y, ((closeSet[-1].C+1)+abs(i[0]+noeud.x-end.x)+abs(i[1]+noeud.y-end.y)-(abs(closeSet[-1].x-end.x)+abs(closeSet[-1].y-end.y))), i, closeSet[-1])
                #Si ces coordonnées n'ont pas déjà été visité
                if (newCoord.x,newCoord.y) not in [(n.x,n.y) for n in closeSet]:
                    #Si successeurs déjà dans E, et coût F inférieur au successeur déjà présent, alors remplacer coût et successeur
                    if (newCoord.x,newCoord.y) in [(k.x,k.y) for k in openSet]:
                        for l in openSet:
                            if (newCoord.x,newCoord.y) == (l.x,l.y):
                                if newCoord.C < l.C:
                                    l.C = newCoord.C
                                    l.predecesseur = newCoord.predecesseur
                    else:
                        openSet.append(newCoord)

    FIN = None
    for n in openSet:
        if (n.x,n.y) == (end.x,end.y):
            FIN = n

    if FIN:
        precedent = FIN.predecesseur
        Chemin = [(FIN.x,FIN.y,"Heuristique:"+str(FIN.C))]
        while precedent != None:
            Chemin.append((precedent.x,precedent.y,"Heuristique:"+str(precedent.C)))
            precedent = precedent.predecesseur
        Chemin.reverse()
        lsDir = []
        for x in range(len(Chemin)):
            if not (x+1)==len(Chemin):
                       if Chemin[x+1][0]>Chemin[x][0]:
                           lsDir.append((1,0))
                       elif Chemin[x+1][0]<Chemin[x][0]:
                           lsDir.append((-1,0))
                       elif Chemin[x+1][1]>Chemin[x][1]:
                           lsDir.append((0,1))
                       elif Chemin[x+1][1]<Chemin[x][1]:
                           lsDir.append((0,-1))
        return lsDir
    else:
        return False
