# -*- coding: utf-8 -*-

# format d'un etat = [[(xCaisse,yCaisse),..],(posX,posY),(Hamming,parent)]
import constantes as constAstar
variables = constAstar.variables

class Node(object):
    
    def __init__(self,caisses,pos,h,parent=None):
        self.box = caisses #liste de tuple
        self.pos = pos #tuple
        self.h = h #entier
        self.parent = parent #pointeur sur Node

    def __repr__(self):
        return str(self.pos)+', '+str(self.parent)+'\n'

class ABRNode(object):
    def __init__(self,node,ga=None,dr=None):
        self.node = node
        self.ga = ga
        self.dr = dr

    def add(self,element):
        if element.h<self.node.h:
            self.ga.add(element)
        elif element.h>self.node.h:
            self.dr.add(element)

    def remove(self,element):
        if element.node.h<self.node.h:
            self.ga.remove(element)
        elif element.node.h>self.node.h:
            self.dr.remove(element)


def niveauToState():
    S = []
    M = []
    caisses = []
    perso = (variables['persoObj'].x,variables['persoObj'].y)
    for x in range (len(variables['niveauObj'].gameO)):
        for y in range(len(variables['niveauObj'].gameO[0])):
            if variables['niveauObj'].gameO[x][y].repr == '$':
                caisses.append((x,y))
            elif variables['niveauObj'].gameO[x][y].repr == '#':
                M.append((x,y))
            if variables['niveauObj'].gameP[x][y].repr == '+':
                S.append((x,y))
    return S,Node(caisses,perso,boxSelector(caisses,perso,S),None),M


def endTest(etat,S):
    for box in etat.box:
        if box not in S:
            return False
    return True


def Hamming(start,end):
    return abs(end[0]-start[0])+abs(end[1]-start[1])


def boxSelector(caisses,pos,S):
    lsBoxHamming = []
    for c in caisses:
        lsTarHamming = []
        for st in S:
            lsTarHamming.append(Hamming(c,st))
        lsBoxHamming.append(min(lsTarHamming)+Hamming(pos,c))
    return min(lsBoxHamming)
    

def successeur(etat,S,M,openList,closedList):
    lsState = []
    cutClosed = [(node.box,node.pos) for node in closedList]
    cutOpen = [(node.box,node.pos) for node in openList]
    for dire in [(0,1),(0,-1),(1,0),(-1,0)]:
        posX,posY = etat.pos[0]+dire[0],etat.pos[1]+dire[1]
        if (posX,posY) in etat.box and ((posX+dire[0],posY+dire[1]) not in etat.box) and ((posX+dire[0],posY+dire[1]) not in M):
            caisses = []
            for c in etat.box: # change la coodonnée de la caisse qui sera déplacé par le mouvement
                if c==(posX,posY):
                    caisses.append((posX+dire[0],posY+dire[1]))
                else:
                    caisses.append(c)
                                
            newState = Node(caisses,(posX,posY),boxSelector(caisses,(posX,posY),S),etat)
            if (newState.box,newState.pos) not in cutClosed:
                lsState.append(newState)
                        
        elif ((posX,posY) not in etat.box) and ((posX,posY) not in M):
            newState = Node(etat.box,(posX,posY),boxSelector(etat.box,(posX,posY),S),etat)
            if (newState.box,newState.pos) not in cutClosed:
                lsState.append(newState)

    #print('lsState '+str(lsState))
    for state in lsState:
        if (state.box,state.pos) not in cutOpen:
            openList.append(state)
        else:
            if state.h<openList[cutOpen.index((state.box,state.pos))].h:
                openList[cutOpen.index((state.box,state.pos))] = state

def astar():
    init = niveauToState()
    S = init[0]
    M = init[2]
    #print('M '+str(M))
    start = init[1]

    openList = []
    closedList = []

    openList.append(start)
    cpt = 0
    while openList!=[]:
        cpt+=1
        sSelected = Node([],(),1000000000)
        for state in openList:
            if state.h<sSelected.h:
                sSelected = state

        closedList.append(sSelected)
        openList.remove(sSelected)

        if endTest(sSelected,S):
            print("chemin trouvé en %s iterations" %(cpt))
            #print(sSelected)
            return reconstructPath(sSelected)
        else:
            successeur(sSelected,S,M,openList,closedList)
    return

def reconstructPath(node):
    dire = []
    currentNode = node
    while currentNode.parent!=None:
        dire.append((currentNode.pos[0]-currentNode.parent.pos[0],currentNode.pos[1]-currentNode.parent.pos[1]))
        currentNode = currentNode.parent
    return dire
