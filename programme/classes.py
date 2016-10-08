from constantes import * #importation de pygame et constante de pygame incluses
import xml.etree.ElementTree as ET


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

        #change la taille de la fenetre et des sprites en fonction de la taille du niveau
        if self.width>11 or self.height>11:
            global taille_sprite,space,wall,target,element,elementOnTarget,pOnTarget,perso_sprite
            taille_sprite,space,wall,target,element,elementOnTarget,pOnTarget,perso_sprite  =  taille_sprite_mini,space_mini,wall_mini,target_mini,element_mini,elementOnTarget_mini,pOnTarget_mini,perso_sprite_mini

        fenetre= pygame.display.set_mode((self.width*taille_sprite,self.height*taille_sprite))


    ##
    # supprime le niveau chargé
    def deleteLevel(self):
        self.structure = []

    ##
    # affiche le niveau dans la fenetre avec les sprites
    # @param fen:la fenetre dans laquelle le niveau sera affiché
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

    ##
    # verifie si dans la case de destination du joueur se trouve une caisse ou une target avec une caisse dessus
    # @param direc:donne la direction du joueur (-1,1,-2,2) pour (gauche,droite,haut,bas)
    # @param perso:l'instance du personnage
    # @return vrai/faux
    def caisseAdjacente(self,direc,perso):
        if direc**2 == 1:
            if self.structure[perso.playerPos[0]][perso.playerPos[1]+direc]=='$': # depart element = element simple
                return self.caisseMovableLigne(direc,' ',perso)
            elif self.structure[perso.playerPos[0]][perso.playerPos[1]+direc]=='*':
                return self.caisseMovableLigne(direc,'.',perso)
            else:
                return True
        else:
            direc=int(direc/2)
            if self.structure[perso.playerPos[0]+direc][perso.playerPos[1]]=='$': # depart element = element simple
                return self.caisseMovableColonne(direc,' ',perso)
            elif self.structure[perso.playerPos[0]+direc][perso.playerPos[1]]=='*':
                return self.caisseMovableColonne(direc,'.',perso)
            else:
                return True

    ##
    # verifie la case direction du personnage +2 pour gauche/droite si celle ci est disponible pour une caisse
    # @param direc:donne la direction du joueur
    # @param char:donnée de la case adjacente au joueur
    # @param perso:l'instance du personnage
    # @return vrai/faux
    def caisseMovableLigne(self,direc,char,perso):
        if self.structure[perso.playerPos[0]][perso.playerPos[1]+2*direc]=='.':
            self.structure[perso.playerPos[0]][perso.playerPos[1]+2*direc]='*'
            self.structure[perso.playerPos[0]][perso.playerPos[1]+direc]=char
            return True
        elif self.structure[perso.playerPos[0]][perso.playerPos[1]+2*direc]==' ':
            self.structure[perso.playerPos[0]][perso.playerPos[1]+2*direc]='$'
            self.structure[perso.playerPos[0]][perso.playerPos[1]+direc]=char
            return True
        return False

    ##
    # verifie la case direction du personnage +2 pour haut/bas si celle ci est disponible pour une caisse
    # @param direc:donne la direction du joueur
    # @param char:donnée de la case adjacente au joueur
    # @param perso:l'instance du personnage
    # @return vrai/faux
    def caisseMovableColonne(self,direc,char,perso):
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
        ##
        # constructeur du personnage
        # @param niveau:instance du niveau du jeu
        # @param playerStart:point de départ du personnage lu dans le niveau
        def __init__(self,niveau,playerStart):
                self.playerPos = playerStart # colonne,ligne
                self.x = playerStart[1]*taille_sprite
                self.y = playerStart[0]*taille_sprite
                self.direction = perso_sprite[9]
                self.niveau = niveau

        ##
        # execute le déplacement du personnage puis appele les fonctions qui se charge du déplacement des caisses
        # @param direction: direction du personnage
        # @param fenetre:fenetre dans laquelle le personnage et les caisse se déplacent
        # @return vrai/faux
        def deplacer(self, direction,fenetre):
                if direction == 'haut' and self.niveau.structure[self.playerPos[0]-1][self.playerPos[1]]!="#": #test si un mur est présent
                        if self.niveau.caisseAdjacente(-2,self):
                            self.playerPos[0]-=1
                            return True
                    
                if direction == 'bas' and self.niveau.structure[self.playerPos[0]+1][self.playerPos[1]]!="#":
                        if self.niveau.caisseAdjacente(2,self):
                            self.playerPos[0]+=1
                            return True
                    
                if direction == 'gauche' and self.niveau.structure[self.playerPos[0]][self.playerPos[1]-1]!="#":
                        if self.niveau.caisseAdjacente(-1,self):
                            self.playerPos[1]-=1
                            return True
                    
                if direction == 'droite' and self.niveau.structure[self.playerPos[0]][self.playerPos[1]+1]!="#":
                        if self.niveau.caisseAdjacente(1,self):
                            self.playerPos[1]+=1
                            return True
                
                return False

        ##
        # créé une animation du déplacement du personnage
        # @param direction:direction du personnage
        # @param fen:fenetre dans laquelle le personnage est déplacé
        def animatePerso(self,direction,fen):
                animation = (1,0,2,0)
                for n in animation:
                    self.direction=perso_sprite[n+direction*3]
                    if direction in (2,3):
                        if direction%2==0:
                            self.x -= taille_sprite//len(animation)
                        else:
                            self.x += taille_sprite//len(animation)
                    else:
                        if direction%2==0:
                            self.y-= taille_sprite//len(animation)
                        else:
                            self.y+= taille_sprite//len(animation)
                    pygame.time.wait(p_speed)
                    update(self.niveau,self,fen)
