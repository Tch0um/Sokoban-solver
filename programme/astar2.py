import time

### logging ###
import logging as log
fic = open('astar2.log','w')
fic.close()

log.basicConfig(filename='astar2.log',level=log.DEBUG,format='%(levelname)s: %(message)s         --- line %(lineno)d in %(filename)s')
### ####### ###


def printG():
    time.sleep(0.2)
    for x in grille:
        for y in x:
            if y.visited:
                print(F.RED+ str(y),end=' ')
            else:
                if y.x==start[0] and y.y==start[1]:
                    print(F.GREEN + str(y),end=' ')
                    
                elif y.x==end[0] and y.y==end[1]:
                    print(F.BLUE + str(y),end=' ')
                    
                else:
                    print(F.WHITE+ str(y),end=' ')
        print()
    print()
            
class Noeud(object):
    def __init__(self,x,y,etat,dist=0,visited=False):
        self.x = x
        self.y = y
        self.etat = etat
        self.dist = dist
        self.visited = visited

    def __repr__(self):
        return str(self.etat)

    def __getitem__(self):
        return self

def f(start,end):
    g = start.dist+1
    h = abs(end.x-start.x)+abs(end.y-start.y)
    return g+h

def astar(grille,start,end):
    log.info(str(start)+'  '+str(end))
    start = grille[start[0]][start[1]]
    end = grille[end[0]][end[1]]
    openList = []
    closedList = []

    openList.append(start)
    start.dist=f(start,end)

    while openList !=[]: #O is empty ?
        dist = 10000
        nSelected = None
        for n in openList: #Pick nBest from O such that f(nBest)<=f(n)
            log.debug('nCoord '+str(n.x)+', '+str(n.y))
            if f(n,end)<=dist:
                dist = f(n,end)
                nSelected = n
            log.debug('nDist '+str(dist))
            

        closedList.append(nSelected) #Remove nBest from O
        openList.remove(nSelected) #..and add it to C
        nSelected.visited = True
        printG()
        log.info('nSelected:'+str(nSelected.x)+', '+str(nSelected.y))
        if nSelected==end:
            log.info('chemin trouvé')
            return [(n.x,n.y) for n in closedList]
        else:
            successeur(openList,closedList,grille,nSelected,end)

    log.info('aucun chemin trouvé')
    return

def successeur(openList,closedList,grille,nSelected,end):
    neighbors = []
    for n in ((-1,0),(1,0),(0,-1),(0,1)):
        if nSelected.x+n[0]>=0 and nSelected.y+n[1]>=0 and nSelected.x+n[0]<len(grille) and nSelected.y+n[1]<len(grille[0]):
            log.debug('dans la grille')
            if grille[nSelected.x+n[0]][nSelected.y+n[1]] not in closedList and grille[nSelected.x+n[0]][nSelected.y+n[1]].etat==1:
                log.debug('noeud absent dans la closedList')
                neighbors.append(grille[nSelected.x+n[0]][nSelected.y+n[1]]) #Expand all nodes x that neighbors of nBest and not in C

    log.debug('neighbors '+str(len(neighbors)))
    for n in neighbors:
        if n in openList: #x is not in O ?
            n.dist = f(n,end) #update f(n)
        else:
            openList.append(n) #add x to O
    
    log.debug('openList '+str(len(openList)))



if __name__=="__main__":
    from random import *
    from colorama import Fore as F

    print(F.GREEN + 'depart ' + F.BLUE + 'arrivée')
    
    grille=[]
    for x in range(10):
        line=[]
        for y in range(10):
            line+=[Noeud(x,y,randint(0,1))]
        grille+=[line]

    #test de f(random,random)
    start = (randint(0,9),randint(0,9))
    end = (randint(0,9),randint(0,9))

    printG()
    
    res = f(grille[start[0]][start[1]],grille[end[0]][end[1]])
    print('\n'+str(start),str(end),str(res),sep=', ')
    grille[end[0]][end[1]].etat=1


    
    print(astar(grille,start,end))
