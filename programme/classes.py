from constantes import * #importation de pygame et constante de pygame incluses
import xml.etree.ElementTree as ET
import math


class Noeud(object):

    def __init__(self, x, y, C, direction = (0,0), predecesseur = None):

        self.x = x
        self.y = y
        self.C = C
        self.direction = direction  #Direction par lequel nous sommes arrivés à ce noeud
        self.predecesseur = predecesseur

    def __repr__(self):
        if self.predecesseur == None:
            precedent = "None"
        else:
            precedent = "("+str(self.predecesseur.x)+","+str(self.predecesseur.y)+")"
        return "("+str(self.x)+","+str(self.y)+")  C = "+str(self.C)+"  prédécesseur = "+precedent


class Sprite(object):
    ##
    # constructeur des sprites
    # @param surface:la surface qui represente le sprite
    # @param rep:la representation du sprite
    # @param x:coordonnée x du sprite
    # @param y:coordonnée y du sprite
    # @param xmax:maximum que la valeur x peut prendre
    # @param ymax:maximum que la valeur y peut prendre
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

    ##
    # test si les coordonnées se trouvent dans la fenetre actuelle
    def coordPossible(self,x,y):
        return x<self.xmax and x>0 and y>0 and y<self.ymax

    ##
    # deplace le sprite dans la fenetre fen
    def displaySprite(self,fen):
        fen.blit(self.surface,(self.y*taille_sprite,self.x*taille_sprite))


    def __getitem__(self,cle):
        return self

    ##
    # sert à autoriser le déplacement du joueur et des caisses sur les sprites vides
    def deplace(*args):
        return True



class Personnage(Sprite):
    ##
    # constructeur de la Classe Personnage
    def __init__(self,surface,x,y):
        if taille_sprite==64:
            self.size=2
        else:
            self.size=1
        if style_perso<=4:
            self.tilesetPerso=tileset_perso.subsurface(32*self.size*3*(style_perso-1),0,32*self.size*3,32*self.size*4)
        else:
            self.tilesetPerso=tileset_perso.subsurface(32*self.size*3*(style_perso-5),self.size*32*4,32*self.size*3,32*self.size*4)
        Sprite.__init__(self,self.tilesetPerso.subsurface(32*self.size,2*32*self.size,self.size*32,self.size*32),'@',x,y)

    ##
    # verifie et déplace le joueur quand c'est possible
    def deplace(self,direction,niveau,fen,variables):#haut,bas,gauche,droite : -1,1,-2,2
        if direction**2==1:
            if direction<0:
                variables['historyP']+='h'
            else:
                variables['historyP']+='b'
            if niveau.gameO[self.x+direction][self.y].repr!='#':
                if niveau.gameO[self.x+direction][self.y].deplace(direction,niveau,fen,variables):
                    niveau.gameO[self.x+direction][self.y]=self
                    niveau.gameO[self.x][self.y]=Sprite(blank,':',self.x,self.y)
                    self.displaySpriteWithAnim(direction,niveau,fen)
                    print(str(self.x),str(self.y),sep=', ')
                    
                    
        else:
            direction=int(direction/2)
            if direction<0:
                variables['historyP']+='g'
            else:
                variables['historyP']+='d'
            if niveau.gameO[self.x][self.y+direction].repr!='#':
                if niveau.gameO[self.x][self.y+direction].deplace(direction*2,niveau,fen,variables):
                    niveau.gameO[self.x][self.y+direction]=self
                    niveau.gameO[self.x][self.y]=Sprite(blank,':',self.x,self.y)
                    self.displaySpriteWithAnim(direction*2,niveau,fen)
                    print(str(self.x),str(self.y),sep=', ')

    def selectCaisse(self,liste):
        distMin = 1000000
        best = None
        for n in range(len(liste)):
            x1,y1=self.x,self.y
            x2,y2=liste[n].x,liste[n].y
            dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
            if dist<distMin:
                distMin = dist
                best = n
        return best

    ##
    # deplace et rafraichit le personnage avec une animation et un changement d'image a chaques frame
    # @param direction:la direction du déplcament representé par -1,1,-2,2 pour haut, bas, gauche, droite
    # @param niveau:le niveau actuellement chargé
    # @param fen: la fenetre pygame
    def displaySpriteWithAnim(self,direction,niveau,fen):
        if direction**2==1:#haut, bas
            for n in (2,1,0,1):
                self.x+=direction/4
                if direction==1:
                    self.surface=self.tilesetPerso.subsurface(n*32*self.size,0,32*self.size,32*self.size)
                else:
                    self.surface=self.tilesetPerso.subsurface(n*32*self.size,3*32*self.size,32*self.size,32*self.size)
                self.displaySprite(fen)
                niveau.afficheNiveau(fen)
                pygame.time.wait(speed)
            self.x=int(round(self.x))
        else:
            direction=direction/2
            for n in (2,1,0,1):
                self.y+=direction/4
                if direction==1:
                    self.surface=self.tilesetPerso.subsurface(n*32*self.size,2*self.size*32,32*self.size,32*self.size)
                else:
                    self.surface=self.tilesetPerso.subsurface(n*32*self.size,32*self.size,32*self.size,32*self.size)
                self.displaySprite(fen)
                niveau.afficheNiveau(fen)
                pygame.time.wait(speed)
            self.y=int(round(self.y))
                    



class Caisse(Sprite):
    ##
    # verifie et deplace la caisse quand c'est possible, autorise le déplacement du personnage en renvoyant True/false
    def deplace(self,direction,niveau,fen,variables=False):#haut,bas,gauche,droite : -1,1,-2,2
        if direction**2==1:#gauche,droite
            if niveau.gameO[self.x+direction][self.y].repr not in ('#','$'):
                niveau.gameO[self.x+direction][self.y]=self
                niveau.gameO[self.x][self.y]=Sprite(blank,':',self.x,self.y)
                self.displaySpriteWithAnim(direction,niveau,fen)
                if variables:
                    variables['historyC'] += [[str(self.x),str(self.y),str(len(variables['historyP'])-1)]]
                return True
                    
        else:
            direction=int(direction/2)
            if niveau.gameO[self.x][self.y+direction].repr not in ('#','$'):
                niveau.gameO[self.x][self.y+direction]=self
                niveau.gameO[self.x][self.y]=Sprite(blank,':',self.x,self.y)
                self.displaySpriteWithAnim(direction*2,niveau,fen)
                if variables:
                    variables['historyC'] += [[str(self.x),str(self.y),str(len(variables['historyP'])-1)]]
                return True
        return False


    ##
    # deplace et rafraichit la caisse avec une animation
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
    ##
    # constructeur du niveau
    # @param grillePlan:la grille du plan
    # @param grilleObstacle:la grille des obstacles
    def __init__(self,grillePlan,grilleObstacle):
        self.grilleP=grillePlan #contient vides, platformes --- ' ', '+', False
        self.grilleO=grilleObstacle # contient murs, caisses --- '#', '$','@', False
        self.gameP=[]
        self.gameO=[]

    def grilleObstacle(self):
        grille = []
        for i in range(len(self.gameO)):          #Pour chaque ligne
            LigneTmp = []
            for j in range(len(self.gameO[0])):   #Pour chaque colonne
                if self.gameO[i][j].repr==':':
                    LigneTmp.append(1)
                    print('1',end='')
                else:
                    LigneTmp.append(0)
                    print('0',end='')
            grille.append(LigneTmp)
            print()

        return grille


    ##
    # verifie toute les caisses qui ne sont pas sur les caisses
    # @return: la liste des references de toute les caisses qui verifie la condition
    def caisseNotOnTarget(self):
        ls=[]
        for x in range(len(self.gameO)):
            for y in range(len(self.gameO[0])):
                if self.gameO[x][y].repr == "$" and self.gameP[x][y].repr != "+":
                    ls.append(self.gameO[x][y])
        return ls


    def allTarget(self):
        ls=[]
        for x in range(len(self.gameP)):
            for y in range(len(self.gameP[0])):
                if self.gameP[x][y].repr == "+" and self.gameO[x][y].repr!="$":
                    ls.append(self.gameP[x][y])
        return ls


    def selectTarget(self):
        lsCaisse,lsTarget = self.caisseNotOnTarget(),self.allTarget()
        
        lsTmp = []
        for caisse in lsCaisse:
            x1,y1 = caisse.x,caisse.y
            x = 100000
            for n in range (len(lsTarget)):
                x2,y2 = lsTarget[n].x,lsTarget[n].y
                dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
                if dist<x:
                    x = dist
                    target = lsTarget[n]
                    rang = n
            lsTmp.append(target)
            del lsTarget[rang]
        return [lsCaisse,lsTmp]


                                
    ##
    # construit les grilles gameP et gameO avec les grille de plan et d'obstacle. gameP et gameO sont des grilles contenant que des Sprites, spécialisés ou non.
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

    ##
    # met en place graphiquement le niveau et rafraichit la fenetre
    def afficheNiveau(self,fen):
        fen.blit(fond,(0,0))
        for x in range(len(self.gameP)):
            for y in range(len(self.gameP[0])):
                self.gameP[x][y].displaySprite(fen)
        for x in range(len(self.gameO)):
            for y in range(len(self.gameO[0])):
                self.gameO[x][y].displaySprite(fen)
        pygame.display.flip()
        
    ##
    # cherche le personnage dans la grille gameO
    # @return: le tuple x,y de la position du personnage
    def findPersonnage(self):
        for x in range (len(self.grilleO)):
            for y in range(len(self.grilleO[0])):
                if self.gameO[x][y].repr=='@':
                    return (x,y)

    ##
    # verifie si une caisse est presente sur chaque cibles.
    # @return: vrai/faux
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
    # charge un niveau de la collection de niveaux
    # @param level:numero du niveau dans la collection
    # @param fenetre:la fenetre à redimensionner
    # @return: un tuple de grilles : la grille du plan et la grile des obstacles
    def loadLevel(self,level,fenetre):
        dicoAttrib = self.root[3][level].attrib
        self.width = int(dicoAttrib["Width"])
        self.height = int(dicoAttrib["Height"])
        
        #lecture du fichier slc
        for e in self.root[3][level]:
            line=[]
            chaine=e.text
            if len(chaine)!=self.width:
                chaine+=" "*(self.width-len(chaine))
            for char in chaine:
                line+=[char]
            self.structure+=[line]

            
        grilleP,grilleO=[],[]
        #creation de la grille du plan et de la grille d'obstacles
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

class ButtonMenu:
    def __init__(self,surface,rep,function,x=0,y=0):
        self.surface = surface
        self.repr=rep
        self.function = function
        self.coord = (x,y)
        self.dim = surface.get_size() #tuple (width,height)

    def isOnButton(self,pos):
        if pos[0]<self.coord[0]+self.dim[0] and pos[0]>self.coord[0] and pos[1]<self.coord[1]+self.dim[1] and pos[1]>self.coord[1]:
            if self.function !=None:
                self.function()
            else:
                return True

    def displayButton(self,fen):
        fen.blit(self.surface,self.coord)

class ButtonCollectionMenu(ButtonMenu):
    def __init__(self,surface,rep,file,function,x=0,y=0):
        ButtonMenu.__init__(self,surface,rep,function,x,y)
        self.file = file

    def isOnButton(self,pos,fenetre):
        if pos[0]<self.coord[0]+self.dim[0] and pos[0]>self.coord[0] and pos[1]<self.coord[1]+self.dim[1] and pos[1]>self.coord[1]:
            self.function(fenetre,self.file)
