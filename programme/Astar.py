from classes import *

def triggerIA(cPerso,niveau,fen):
    liste = niveau.selectTarget()
    for z in range(len(liste[0])):
        ls = deplCaisse((liste[0][z].x,liste[0][z].y),(liste[1][z].x,liste[1][z].y))
        print(str(ls)+' '*5+'ligne 7')
        commandePerso(ls,niveau.gameO[cPerso[0]][cPerso[1]],liste[0][z],niveau,fen)
        

def deplCaisse(dep,ar):
    ls=[]
    if ar[0]>dep[0]:
        ls.append([1,ar[0]-dep[0]])
    elif ar[0]<dep[0]:
        ls.append([-1,dep[0]-ar[0]])
    if ar[1]>dep[1]:
        ls.append([2,ar[1]-dep[1]])
    elif ar[1]<dep[1]:
        ls.append([-2,dep[1]-ar[1]])
    return ls

def commandePerso(ls,perso,caisse,niveau,fen):
    for x in ls:
        if perso.y<=caisse.y and x[0]==-2:
            if perso.x==caisse.x:
                deplacement(True,perso,(perso.x-1,perso.y),niveau,fen)
                deplacement(False,perso,(caisse.x,caisse.y+1),niveau,fen)
            else:
                deplacement(False,perso,(caisse.x,caisse.y+1),niveau,fen)
        elif x[0]==2:
            deplacement(True,perso,(caisse.x,caisse.y-1),niveau,fen)
        elif x[0]==1:
            deplacement(True,perso,(caisse.x-1,caisse.y),niveau,fen)
        else:
            deplacement(True,perso,(caisse.x+1,caisse.y),niveau,fen)
        for n in range(x[1]):
            deplacement(True,perso,(caisse.x,caisse.y),niveau,fen)

def deplacement(xpr,perso,ar,niveau,fen):
    print(ar)
    while (perso.x,perso.y)!=ar:
        if (perso.y==ar[1] or xpr) and perso.x!=ar[0]:
            if ar[0]>perso.x:
                perso.deplace(1,niveau,fen)
            else:
                perso.deplace(-1,niveau,fen)
        else:
            if ar[1]>perso.y:
                perso.deplace(2,niveau,fen)
            else:
                perso.deplace(-2,niveau,fen)
    print('destination!')
