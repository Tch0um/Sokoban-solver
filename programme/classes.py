from constantes import * #importation de pygame et constante de pygame incluses
import xml.etree.ElementTree as ET


class Sprite(object):
    def __init__(self,surface,rep,x,y,xmax=dWidth,ymax=dHeight):
        self.x=x
        self.y=y
        self.xmax=xmax
        self.ymax=ymax
        self.surface=surface
        if rep not in ('#','$',' ','+','@','.',':'):
            raise ValueError(rep+" ne peut pas être représenté")
        else:
            self.repr=rep


    def coordPossible(self,x,y):
        return x<self.xmax and x>0 and y>0 and y<self.ymax


    def displaySprite(self,fen):
        fen.blit(self.surface,(self.y*taille_sprite,self.x*taille_sprite))

    def setCoord(self,x,y):
        if self.coordPossible(x,y):
            self.x=x
            self.y=y
        else:
            raise ValueError("coordonné impossible")

    def getCoord(self):
        return (self.x,self.y)

    def getMax(self):
        return (self.xmax,self.ymax)

    def __getitem__(self,cle):
        return self

    def deplace(*args):
        return True



class Personnage(Sprite):
    def __init__(self,surface,x,y):
        Sprite.__init__(self,surface,'@',x,y)

    def deplace(self,direction,niveau,fen):#haut,bas,gauche,droite : -1,1,-2,2
        if direction**2==1:
            if niveau.gameO[self.x+direction][self.y].repr!='#':
                if niveau.gameO[self.x+direction][self.y].deplace(direction,niveau,fen):
                    niveau.gameO[self.x+direction][self.y]=self
                    niveau.gameO[self.x][self.y]=Sprite(blank,':',self.x,self.y)
                    self.setCoord(self.x+direction,self.y)
                    
        else:
            direction=int(direction/2)
            if niveau.gameO[self.x][self.y+direction].repr!='#':
                if niveau.gameO[self.x][self.y+direction].deplace(direction*2,niveau,fen):
                    niveau.gameO[self.x][self.y+direction]=self
                    niveau.gameO[self.x][self.y]=Sprite(blank,':',self.x,self.y)
                    self.setCoord(self.x,self.y+direction)
                    



class Caisse(Sprite):
    def deplace(self,direction,niveau,fen):#haut,bas,gauche,droite : -1,1,-2,2
        if direction**2==1:#gauche,droite
            if niveau.gameO[self.x+direction][self.y].repr not in ('#','$'):
                niveau.gameO[self.x+direction][self.y]=self
                niveau.gameO[self.x][self.y]=Sprite(blank,':',self.x,self.y)
                self.displaySpriteWithAnim(direction,niveau,fen)
                #self.setCoord(self.x+direction,self.y)
                return True
                    
        else:
            direction=int(direction/2)
            if niveau.gameO[self.x][self.y+direction].repr not in ('#','$'):
                niveau.gameO[self.x][self.y+direction]=self
                niveau.gameO[self.x][self.y]=Sprite(blank,':',self.x,self.y)
                self.displaySpriteWithAnim(direction*2,niveau,fen)
                #self.setCoord(self.x,self.y+direction)
                return True
        return False

    def displaySpriteWithAnim(self,direction,niveau,fen):
        if direction**2==1:#gauche,droite
            for n in range(3):
                self.x+=direction/3
                self.displaySprite(fen)
                niveau.afficheNiveau(fen)
            self.x=int(round(self.x))
        else:
            direction=direction/2
            for n in range(3):
                self.y+=direction/3
                self.displaySprite(fen)
                niveau.afficheNiveau(fen)
            self.y=int(round(self.y))
            



class Niveau(object):
    def __init__(self,grillePlan,grilleObstacle):
        self.grilleP=grillePlan #contient vides, platformes --- ' ', '+', False
        self.grilleO=grilleObstacle # contient murs, caisses --- '#', '$','@', False
        self.gameP=[]
        self.gameO=[]

        
    def gameConstructor(self): # construit les grilles gameP et gameO avec des objets
        for x in range(len(self.grilleP)):
            line=[]
            for y in range(len(self.grilleP[0])):
                if self.grilleP[x][y]:
                    if self.grilleP[x][y]==' ':
                        line+=[Sprite(space,' ',x,y)]
                    elif self.grilleP[x][y]=='+':
                        line+=[Sprite(target,'+',x,y)]
                    else:
                        line+=[Sprite(blank,':',x,y)]
                else:
                    line+=[Sprite(blank,':',x,y)]
            self.gameP+=[line]
            
        for x in range(len(self.grilleO)):
            line=[]
            for y in range(len(self.grilleO[0])):
                if self.grilleO[x][y]:
                    if self.grilleO[x][y]=='$':
                        line+=[Caisse(element,'$',x,y)]
                    elif self.grilleO[x][y]=='#':
                        line+=[Sprite(wall,'#',x,y)]
                    elif self.grilleO[x][y]=='@':
                        line+=[Personnage(perso_sprite[6],x,y)]
                    else:
                        line+=[Sprite(blank,':',x,y)]
                else:
                    line+=[Sprite(blank,':',x,y)]
            self.gameO+=[line]

            
    def afficheNiveau(self,fen):
        fen.blit(fond,(0,0))
        for x in range(len(self.gameP)):
            for y in range(len(self.gameP[0])):
                self.gameP[x][y].displaySprite(fen)
        for x in range(len(self.gameO)):
            for y in range(len(self.gameO[0])):
                self.gameO[x][y].displaySprite(fen)
        pygame.display.flip()
        

    def findPersonnage(self):
        for x in range (len(self.grilleO)):
            for y in range(len(self.grilleO[0])):
                if self.gameO[x][y].repr=='@':
                    return (x,y)

    def checkTarget(self):
        for x in range (len(self.gameO)):
            for y in range(len(self.gameO[0])):
                if self.gameP[x][y].repr=='+' and self.gameO[x][y].repr!='$':
                    return False
        return True

                
    def __repr__(self):
        ch=''
        for x in self.gameP:
            ch+='|'
            for y in x:
                if y.repr==' ':
                    ch+='  '
                else:
                    ch+=y.repr+' '
            ch+='|\n'
        ch+='\n'*5
        for x in self.gameO:
            ch+='|'
            for y in x:
                ch+=y.repr+' '
            ch+='|\n'
        return ch


##
# rafraichit la fenetre pygame en fonction de perso et de niveaux
# @param niveaux:la grille correspondant au niveau actuel
# @param perso:l'instance du personnage
# @param fenetre:l'instance de la fenetre à rafraichir
def update(niveaux,perso,fenetre):
    fenetre.blit(fond, (0,0))
    niveaux.afficheLevel(fenetre)
    fenetre.blit(perso.direction,(perso.x,perso.y))
    pygame.display.flip()





class LevelCollection(object):
    ##
    # constructeur de la collection de niveaux
    # @param file:fichier contenant la collection de niveaux
    def __init__(self, file):
            self.structure = []
            tree = ET.parse(file)
            self.root = tree.getroot()
            self.width = 0
            self.height = 0

    ##
    # charge un niveau parmit la collection de niveaux. change la taille de la fenetre en fonction de la taille du niveau
    # @param level:numero du niveau dans la collection
    # @param fenetre:la fenetre à redimensionner
    def loadLevel(self,level,fenetre):
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

            
        grilleP,grilleO=[],[]
        for x in range(len(self.structure)):
            lineP,lineO=[],[]
            for y in range(len(self.structure[0])):
                if self.structure[x][y] in ('@','#','$'):
                    lineO+=[self.structure[x][y]]
                    lineP+=[False]
                elif self.structure[x][y]=='*':
                    lineO+=['$']
                    lineP+=['+']
                elif self.structure[x][y]=='.':
                    lineO+=[False]
                    lineP+=['+']
                elif self.structure[x][y]=='+':
                    lineO+=['@']
                    lineP+=['+']
                else:
                    lineO+=[False]
                    lineP+=[self.structure[x][y]]
            grilleP+=[lineP]
            grilleO+=[lineO]

        #change la taille de la fenetre et des sprites en fonction de la taille du niveau
        if self.width>11 or self.height>11:
            global taille_sprite,space,wall,target,element,elementOnTarget,pOnTarget,perso_sprite,dWidth,dHeight
            taille_sprite,space,wall,target,element,elementOnTarget,pOnTarget,perso_sprite  =  taille_sprite_mini,space_mini,wall_mini,target_mini,element_mini,elementOnTarget_mini,pOnTarget_mini,perso_sprite_mini
            
        fenetre= pygame.display.set_mode((self.width*taille_sprite,self.height*taille_sprite))
        dWidth,dHeight=self.width,self.height
        
        return (grilleP,grilleO)
        

    ##
    # supprime le niveau chargé
    def deleteLevel(self):
        self.structure = []
