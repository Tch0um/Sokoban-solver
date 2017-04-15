from constantes import * #importation de pygame et constante de pygame incluses
import constantes as const
import xml.etree.ElementTree as ET
import math

variables = const.variables

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
    def __init__(self,surface,rep,x,y):
        self.x=x
        self.y=y
        self.surface=surface
        if rep not in ('#','$','+','@','.',':',' '):
            raise ValueError(rep+" ne peut pas être représenté")
        else:
            self.repr=rep
    ##
    # deplace le sprite dans la fenetre fen
    def displaySprite(self):
        variables['fenetre'].blit(self.surface,(self.y*variables['spriteSize']*32+variables['niveauObj'].offset[0],self.x*variables['spriteSize']*32+variables['niveauObj'].offset[1]))


    def __getitem__(self,cle):
        return self

    ##
    # sert à autoriser le déplacement du joueur et des caisses sur les sprites vides
    def deplace(*args):
        return True

    def setSurface(self,surface):
        self.surface = surface



class Personnage(Sprite):
    ##
    # constructeur de la Classe Personnage
    def __init__(self,surface,x,y):
        Sprite.__init__(self,None,'@',x,y)
        self.setTileset()
        
    def setTileset(self):
        if variables['styleP']<=4:
            self.tilesetPerso=variables['surfaces']['perso'].subsurface(32*variables['spriteSize']*3*(variables['styleP']-1),0,32*variables['spriteSize']*3,32*variables['spriteSize']*4)
        else:
            self.tilesetPerso=variables['surfaces']['perso'].subsurface(32*variables['spriteSize']*3*(variables['styleP']-5),variables['spriteSize']*32*4,32*variables['spriteSize']*3,32*variables['spriteSize']*4)
        self.setSurface(self.tilesetPerso.subsurface(32*variables['spriteSize'],2*32*variables['spriteSize'],variables['spriteSize']*32,variables['spriteSize']*32))

    ##
    # verifie et déplace le joueur quand c'est possible
    def deplace(self,direction,rewind=True):
        if variables['niveauObj'].gameO[self.x+direction[0]][self.y+direction[1]].repr!='#':
            depl = variables['niveauObj'].gameO[self.x+direction[0]][self.y+direction[1]].deplace(direction,rewind)
            if depl in (True,"movable"): ## True si deplacement possible, movable si deplacement possible et deplacement de caisse
                if not rewind:
                    if direction==(-1,0):
                        variables['historyP']+='h'
                    elif direction==(1,0):
                        variables['historyP']+='b'
                    elif direction==(0,-1):
                        variables['historyP']+='g'
                    else:
                        variables['historyP']+='d'
                variables['niveauObj'].gameO[self.x+direction[0]][self.y+direction[1]]=self
                variables['niveauObj'].gameO[self.x][self.y]=Sprite(variables['surfaces']['blank'],':',self.x,self.y)
                variables['niveauObj'].moved.append((self.x,self.y))
                variables['niveauObj'].moved.append((self.x+direction[0],self.y+direction[1]))
                self.displaySpriteWithAnim(direction,depl)
                variables['niveauObj'].moved=[]
                #print(str(self.x),str(self.y),sep=', ')

##    def selectCaisse(self,liste):
##        distMin = 1000000
##        best = None
##        for n in range(len(liste)):
##            x1,y1=self.x,self.y
##            x2,y2=liste[n].x,liste[n].y
##            dist = math.sqrt((x2-x1)**2+(y2-y1)**2)
##            if dist<distMin:
##                distMin = dist
##                best = n
##        return best

    ##
    # deplace et rafraichit le personnage avec une animation et un changement d'image a chaques frame
    # @param direction:la direction du déplcament representé par -1,1,-2,2 pour haut, bas, gauche, droite
    # @param niveau:le niveau actuellement chargé
    # @param fen: la fenetre pygame
    def displaySpriteWithAnim(self,direction,depl):
        if depl=="movable":
            caisse = variables['niveauObj'].gameO[self.x+direction[0]*2][self.y+direction[1]*2]
            #print(caisse)
        for n in (2,1,0,1):
            self.x+=direction[0]/4
            self.y+=direction[1]/4
            if direction==(1,0):
                self.surface=self.tilesetPerso.subsurface(n*32*variables['spriteSize'],0,32*variables['spriteSize'],32*variables['spriteSize'])
            elif direction==(-1,0):
                self.surface=self.tilesetPerso.subsurface(n*32*variables['spriteSize'],3*32*variables['spriteSize'],32*variables['spriteSize'],32*variables['spriteSize'])
            elif direction==(0,1):
                self.surface=self.tilesetPerso.subsurface(n*32*variables['spriteSize'],2*variables['spriteSize']*32,32*variables['spriteSize'],32*variables['spriteSize'])
            else:
                self.surface=self.tilesetPerso.subsurface(n*32*variables['spriteSize'],32*variables['spriteSize'],32*variables['spriteSize'],32*variables['spriteSize'])
            self.displaySprite()
            if depl == "movable":
                caisse.x+=direction[0]/4
                caisse.y+=direction[1]/4
                caisse.displaySprite()
            variables['niveauObj'].afficheNiveau(inGame=True)
            pygame.time.wait(variables['speed'])
        self.x=int(round(self.x))
        self.y=int(round(self.y))
        if depl=="movable":
            caisse.x=int(round(caisse.x))
            caisse.y=int(round(caisse.y))
        
                    


class Caisse(Sprite):
    ##
    # verifie et deplace la caisse quand c'est possible, autorise le déplacement du personnage en renvoyant True/false
    def deplace(self,direction,rewind=True):#haut,bas,gauche,droite : -1,1,-2,2
        if variables['niveauObj'].gameO[self.x+direction[0]][self.y+direction[1]].repr not in ('#','$'):
            variables['niveauObj'].gameO[self.x+direction[0]][self.y+direction[1]]=self
            variables['niveauObj'].gameO[self.x][self.y]=Sprite(variables['surfaces']['blank'],':',self.x,self.y)
            variables['niveauObj'].moved.append((self.x+direction[0],self.y+direction[1]))
            #print(str(self.x+direction[0]),str(self.y+direction[1]),'truc',sep=' ')
            if not rewind:
                variables['historyC'] += [[str(self.x+direction[0]),str(self.y+direction[1]),str(len(variables['historyP']))]]
            else:
                variables['niveauObj'].moved.append((self.x,self.y))
                for n in range(4):
                    self.x+=direction[0]/4
                    self.y+=direction[1]/4
                    self.displaySprite()
                    variables['niveauObj'].afficheNiveau(inGame=True)
                variables['niveauObj'].moved=[]
                self.x=int(round(self.x))
                self.y=int(round(self.y))
            return "movable"
        return False


class Niveau(object):
    ##
    # constructeur du niveau
    # @param grillePlan:la grille du plan
    # @param grilleObstacle:la grille des obstacles
    def __init__(self,grillePlan,grilleObstacle,screenOffset=[0,0]):
        self.grilleP=grillePlan #contient vides, platformes --- ' ', '+', False
        self.grilleO=grilleObstacle # contient murs, caisses --- '#', '$','@', False
        self.gameP=[]
        self.gameO=[]
        self.moved=[]
        self.perso=None
        self.caisses=[]
        self.stelles=[]
        self.offset=screenOffset


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
                                
    ##
    # construit les grilles gameP et gameO avec les grille de plan et d'obstacle. gameP et gameO sont des grilles contenant que des Sprites, spécialisés ou non.
    def gameConstructor(self): # construit les grilles gameP et gameO avec des objets
        for x in range(len(self.grilleP)):
            line=[]
            for y in range(len(self.grilleP[0])):
                if self.grilleP[x][y]:
                    if self.grilleP[x][y]=='+': ## stelle ##
                        obj = Sprite(variables['surfaces']['target'],'+',x,y)
                        line+=[obj]
                        self.stelles.append(obj)
                        
                    else:
                        line+=[Sprite(variables['surfaces']['space'],' ',x,y)]
                else:
                    line+=[Sprite(variables['surfaces']['space'],' ',x,y)]
            self.gameP+=[line]
            
        for x in range(len(self.grilleO)):
            line=[]
            for y in range(len(self.grilleO[0])):
                if self.grilleO[x][y]:
                    if self.grilleO[x][y]=='$': ## caisse ##
                        obj = Caisse(variables['surfaces']['element'],'$',x,y)
                        line+=[obj]
                        self.caisses.append(obj)
                    elif self.grilleO[x][y]=='#': ## mur ##
                        line+=[Sprite(variables['surfaces']['wall'],'#',x,y)]
                    elif self.grilleO[x][y]=='@': ## personnage ##
                        variables['persoObj'].x = x
                        variables['persoObj'].y = y
                        variables['persoObj'].setTileset()
                        line+=[variables['persoObj']]
                        self.perso=variables['persoObj']
                    else:
                        line+=[Sprite(variables['surfaces']['blank'],':',x,y)]
                else:
                    line+=[Sprite(variables['surfaces']['blank'],':',x,y)]
            self.gameO+=[line]

    ##
    # met en place graphiquement le niveau et rafraichit la fenetre
    def afficheNiveau(self,display=True,inGame=False):
        if inGame:
            for n in self.moved:
                #print(n)
                self.gameP[n[0]][n[1]].displaySprite()
            #print()
            for n in self.moved:
                self.gameO[n[0]][n[1]].displaySprite()
        else:
            variables['fenetre'].blit(pygame.Surface(variables['fenetre'].get_size()),(0,0))
            for x in range(len(self.gameP)):
                for y in range(len(self.gameP[0])):
                    self.gameP[x][y].displaySprite()
            for x in range(len(self.gameO)):
                for y in range(len(self.gameO[0])):
                    self.gameO[x][y].displaySprite()
        if display:
            pygame.display.flip()
        #print(self)
            
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
            global variables
            variables['spriteSize']=1
            fenetre= pygame.display.set_mode((self.width*variables['spriteSize']*32,self.height*variables['spriteSize']*32))
        else:
            variables['spriteSize']=2
            fenetre= pygame.display.set_mode((800,600))
            
        const.setSurfaces()
        
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

    def displayButton(self):
        variables['fenetre'].blit(self.surface,self.coord)

class ButtonCollectionMenu(ButtonMenu):
    def __init__(self,surface,rep,file,function,x=0,y=0):
        ButtonMenu.__init__(self,surface,rep,function,x,y)
        self.file = file

    def isOnButton(self,pos):
        if pos[0]<self.coord[0]+self.dim[0] and pos[0]>self.coord[0] and pos[1]<self.coord[1]+self.dim[1] and pos[1]>self.coord[1]:
            self.function(self.file)
