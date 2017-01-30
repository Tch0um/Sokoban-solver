import pygame
from pygame.locals import *
import GUI as bt
variables = {}

### logging ###
import logging as log
fic = open('sokoban.log','w')
fic.close()

log.basicConfig(filename='sokoban.log',level=log.DEBUG,format='%(levelname)s: %(message)s --- line %(lineno)d in %(filename)s')
### ####### ###

pygame.init()

#Création de la fenêtre avec ses attributs
fenetre= pygame.display.set_mode((800,600))
#icone = perso_sprite[0]
#pygame.display.set_icon(icone)
pygame.display.set_caption('Sokoban')


#variables du personnage
variables['speed'] = 10        #milliseconds par pas
variables['styleP'] = 8  #selection perso

variables['historyP']=[]
variables['historyC']=[]


variables['collection'] = "AC_Diamonds"
fond = pygame.image.load("images/bg1.png")



buttonCollection = ['newGame','saveGame','loadGame','resume','yes','no','quit','options','2players','3players','4players','withAI','withoutAI','ok','cancel','previous','next','return','mainMenu','template','inf','sup']

### menu
mainMenuBtList = [0,2,7,6]
mainMenuFonctions = [lambda: bt.collectionMenu(fenetre),lambda: bt.loadGame(fenetre),lambda: bt.options(fenetre),lambda:bt.quitt()]
levelMenuBtList = [11,12,8,9,10,17]
levelMenuFonctions = [lambda: bt.withAI(fenetre),lambda: bt.withoutAI(fenetre),lambda: bt.twoPlayers(fenetre),lambda: bt.threePlayers(fenetre),lambda: bt.fourPlayers(fenetre), lambda: bt.collectionMenu(fenetre)]
pauseMenuBtList = [3,1,2,6]
collectionMenuBtList = [19,17]
collectionMenuFonctions = [lambda: bt.mainMenu(fenetre)]



### sprites taille normale
variables['spriteSize'] = 1
variables['surfaces'] = {}
def setSurfaces():
    global variables
    variables['surfaces']['perso'] = pygame.image.load('images/perso'+str(variables['spriteSize']*32)+'.png')
    variables['surfaces']['world'] = pygame.image.load('images/style1_'+str(variables['spriteSize']*32)+'.png')
    variables['surfaces']['blank'] = pygame.Surface((0,0))
    variables['surfaces']['wall'] = variables['surfaces']['world'].subsurface(0,0,variables['spriteSize']*32,variables['spriteSize']*32)
    variables['surfaces']['target'] = variables['surfaces']['world'].subsurface(0,variables['spriteSize']*32,variables['spriteSize']*32,variables['spriteSize']*32)
    variables['surfaces']['element'] = variables['surfaces']['world'].subsurface(variables['spriteSize']*32,variables['spriteSize']*32,variables['spriteSize']*32,variables['spriteSize']*32)
setSurfaces()

log.debug(variables)
