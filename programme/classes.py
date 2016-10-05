import pygame
from pygame.locals import * 
from constantes import *
import xml.etree.ElementTree as ET

class LevelCollection(object):
    def __init__(self, file):
            self.structure = []
            tree = ET.parse(file)
            self.root = tree.getroot()
            self.width = 0
            self.height = 0


    def loadLevel(self,level):
        dicoAttrib = self.root[3][level].attrib
        self.width = int(dicoAttrib["Width"])
        self.height = int(dicoAttrib["Height"])
        for e in self.root[3][level]:
            line=[]
            chaine=e.text
            if len(chaine)!=self.width:
                chaine+=" "*(self.width-len(chaine))
            for char in chaine:
                line+=[char]
            self.structure+=[line]


    def deleteLevel(self):
        self.structure = []

    def afficheLevel(self,fen):
        playerStart = ()
        for xi in range(self.width):
            x = xi*taille_sprite
            for yi in range(self.height):
                y = yi*taille_sprite
                if self.structure[yi][xi] in ('+','@'):
                    playerStart = [yi,xi]
                    self.structure[yi][xi] = " "
                    fen.blit(space,(x,y))
                elif self.structure[yi][xi] == ' ':
                    fen.blit(space,(x,y))
                elif self.structure[yi][xi] == "#":
                    fen.blit(wall,(x,y))
                elif self.structure[yi][xi] == ".":
                    fen.blit(target,(x,y))
                elif self.structure[yi][xi] == "$":
                    fen.blit(element,(x,y))
                elif self.structure[yi][xi] == "*":
                    fen.blit(elementOnTarget,(x,y))
        return playerStart

    def testDir1(self,direc,perso):  # direc prend les valeurs suivantes dans lordre des direciton : -1,1,-2,2
        if direc**2 == 1:
            if self.structure[perso.playerPos[0]][perso.playerPos[1]+direc]=='$': # depart element = element simple
                return self.testDir2(direc,' ',perso)
            elif self.structure[perso.playerPos[0]][perso.playerPos[1]+direc]=='*':
                return self.testDir2(direc,'.',perso)
            else:
                return True
        else:
            direc=int(direc/2)
            if self.structure[perso.playerPos[0]+direc][perso.playerPos[1]]=='$': # depart element = element simple
                return self.testDir3(direc,' ',perso)
            elif self.structure[perso.playerPos[0]+direc][perso.playerPos[1]]=='*':
                return self.testDir3(direc,'.',perso)
            else:
                return True
            
    def testDir2(self,direc,char,perso):
        if self.structure[perso.playerPos[0]][perso.playerPos[1]+2*direc]=='.':
            self.structure[perso.playerPos[0]][perso.playerPos[1]+2*direc]='*'
            self.structure[perso.playerPos[0]][perso.playerPos[1]+direc]=char
            return True
        elif self.structure[perso.playerPos[0]][perso.playerPos[1]+2*direc]==' ':
            self.structure[perso.playerPos[0]][perso.playerPos[1]+2*direc]='$'
            self.structure[perso.playerPos[0]][perso.playerPos[1]+direc]=char
            return True
        return False

    def testDir3(self,direc,char,perso):
        if self.structure[perso.playerPos[0]+2*direc][perso.playerPos[1]]=='.':
            self.structure[perso.playerPos[0]+2*direc][perso.playerPos[1]]='*'
            self.structure[perso.playerPos[0]+direc][perso.playerPos[1]]=char
            return True
        elif self.structure[perso.playerPos[0]+2*direc][perso.playerPos[1]]==' ':
            self.structure[perso.playerPos[0]+2*direc][perso.playerPos[1]]='$'
            self.structure[perso.playerPos[0]+direc][perso.playerPos[1]]=char
            return True
        return False


class Perso:

        def __init__(self, niveau,playerStart):
                self.playerPos = playerStart # colonne,ligne
                
                self.x = playerStart[1]*taille_sprite
                self.y = playerStart[0]*taille_sprite
                
                self.direction = perso_sprite[9]
                
                #Niveau dans lequel le personnage se trouve
                self.niveau = niveau

        def deplacer(self, direction,fenetre):
                if direction == 'haut' and self.niveau.structure[self.playerPos[0]-1][self.playerPos[1]]!="#":
                        if self.niveau.testDir1(-2,self):
                            self.playerPos[0]-=1
                            return True
                    
                if direction == 'bas' and self.niveau.structure[self.playerPos[0]+1][self.playerPos[1]]!="#":
                        if self.niveau.testDir1(2,self):
                            self.playerPos[0]+=1
                            return True
                    
                if direction == 'gauche' and self.niveau.structure[self.playerPos[0]][self.playerPos[1]-1]!="#":
                        if self.niveau.testDir1(-1,self):
                            self.playerPos[1]-=1
                            return True
                    
                if direction == 'droite' and self.niveau.structure[self.playerPos[0]][self.playerPos[1]+1]!="#":
                        if self.niveau.testDir1(1,self):
                            self.playerPos[1]+=1
                            return True
                
                return False
