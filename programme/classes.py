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
            print(chaine)
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
                if self.structure[xi][yi] in ('+','@'):
                    playerStart = [yi,xi]
                    self.structure[xi][yi] = " "
                    fen.blit(space,(x,y))
                elif self.structure[xi][yi] == ' ':
                    fen.blit(space,(x,y))
                elif self.structure[xi][yi] == "#":
                    fen.blit(wall,(x,y))
                elif self.structure[xi][yi] == ".":
                    fen.blit(target,(x,y))
                elif self.structure[xi][yi] == "$":
                    fen.blit(element,(x,y))
                elif self.structure[xi][yi] == "*":
                    fen.blit(elementOnTarget,(x,y))
        return playerStart

class Perso:

        def __init__(self, niveau,playerStart):
                self.playerPos = playerStart
                
                self.x = playerStart[0]*taille_sprite
                self.y = playerStart[1]*taille_sprite
                
                self.direction = perso_sprite[9]
                
                #Niveau dans lequel le personnage se trouve
                self.niveau = niveau

        def deplacer(self, direction,fenetre):
                if direction == 'haut' and self.niveau.structure[self.playerPos[1]-1][self.playerPos[0]]!="#":
                        print(self.niveau.structure[self.playerPos[1]-1][self.playerPos[0]])
                        self.playerPos[1]-=1
                        print(str(self.playerPos))
                        return True
                    
                if direction == 'bas' and self.niveau.structure[self.playerPos[1]+1][self.playerPos[0]]!="#":
                        print(self.niveau.structure[self.playerPos[1]+1][self.playerPos[0]])
                        self.playerPos[1]+=1
                        print(str(self.playerPos))
                        return True
                    
                if direction == 'gauche' and self.niveau.structure[self.playerPos[1]][self.playerPos[0]-1]!="#":
                        print(self.niveau.structure[self.playerPos[1]][self.playerPos[0]-1])
                        self.playerPos[0]-=1
                        print(str(self.playerPos))
                        return True
                    
                if direction == 'droite' and self.niveau.structure[self.playerPos[1]][self.playerPos[0]+1]!="#":
                        print(self.niveau.structure[self.playerPos[1]][self.playerPos[0]+1])
                        self.playerPos[0]+=1
                        print(str(self.playerPos))
                        return True
                
                return False
