import time
import astar2 as ast

### logging ###
import logging as log
fic = open('astar3.log','w')
fic.close()

log.basicConfig(filename='astar3.log',level=log.INFO,format='%(levelname)s: %(message)s         --- line %(lineno)d in %(filename)s')
log.info('log ok')
### ####### ###


def printG():
    #time.sleep(0.2)
    for x in grille:
        for y in x:
            if y.visited:
                print(F.RED+ str(y),end=' ')
            else:
                if y.etat =='+':
                    print(F.BLUE+'+',end=' ')
                elif y.etat=='$':
                    print(F.GREEN+'$',end=' ')
                else:
                    print(F.WHITE+y.etat,end=' ')
        print()
    print()
            
class Noeud(object):
    def __init__(self,x,y,etat,dist=0,visited=False,target=None):
        self.x = x
        self.y = y
        self.etat = etat
        self.dist = dist
        self.visited = visited
        self.target = target

    def __repr__(self):
        return str(self.etat)

    def __getitem__(self):
        return self

def f(start,end):
    g=ast.astar(grille,(start.x,start.y),(end.x,end.y))
    if g!=None:
        return g
    return 0

def searchItem(item):
    liste = []
    for x in grille:
        for y in x:
            if y.etat==item:
                liste+=[y]
    return liste


def astar(grille):
    start = searchItem('$')
    end = searchItem('+')
    log.info('start '+str(['('+str(n.x)+','+str(n.y)+')' for n in start]))
    log.info('end '+str(['('+str(n.x)+','+str(n.y)+')' for n in end]))
    openLists = []
    closedLists = []
    startWithoutEnd = False #depart sans arrivée

    for s in start: ### assigne une arrivée à tout les departs quand c'est possible
        ends = []
        for e in range(len(start)):
            trajet = f(s,end[e])
            log.warning('trajet '+str(trajet))
            if trajet!=None:
                    ends+=[(end[e],trajet)]
            else:
                log.info('trajet impossible')
                startWithoutEnd = True
                
        for x in grille:##suppression de couleur rouge
            for y in x:
                y.visited=False
                
        openLists+=[ends]
        print('\n'*3+str(closedLists)+'\n'*3)
        #closedLists+=[[]]
    log.warning('openLists '+str(openLists))
    log.warning('closedLists '+str(closedLists))
    print(closedLists)

                

    while not startWithoutEnd: 
        endsSelected = []
        for n in range(len(openLists)): #Pick nBest from O such that f(nBest)<=f(n)
            dist = 100000
            for end in openLists[n]:
                if len(ends[1])<=dist:
                    dist = len(ends[1])
                    endsSelected += [end]
            log.warning('endsSelected '+str(endsSelected))

            closedLists.append(endsSelected) #Remove nBest from 0

        openLists = []
        printG()
        
        if len(closedLists)==len(start):
            log.info('chemin trouvé')
            log.info('closedLists '+str(closedLists))
            return [(n.x,n.y) for n in closedLists]
        else:
            successeur(openList,closedLists,grille,nSelected,end)

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

    print(F.GREEN + 'departs ' + F.BLUE + 'arrivées')
    
    grille=[]
    for x in range(10):
        line=[]
        for y in range(10):
            line+=[Noeud(x,y,'-')]
        grille+=[line]
    for x in range(2):
        x1,y1=randint(0,len(grille)-1),randint(0,len(grille)-1)
        grille[x1][y1] = Noeud(x1,y1,'X')
    for n in range(4):
        x1,y1=randint(0,len(grille)-1),randint(0,len(grille)-1)
        x2,y2=randint(0,len(grille)-1),randint(0,len(grille)-1)
        while x2==x1 and y2==y1:
            x2,y2=randint(0,len(grille)-1),randint(0,len(grille)-1)
        grille[x1][y1] = Noeud(x1,y1,'$')
        grille[x2][y2] = Noeud(x2,y2,'+')
    printG()
    print(astar(grille))
