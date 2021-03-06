import pygame
from pygame.locals import *
import GUI as bt
import sys
from L10n import fr_FR
variables = {}

### logging ###
import logging as log
fic = open('sokoban.log','w')
fic.close()

log.basicConfig(filename='sokoban.log',level=log.DEBUG,format='%(levelname)s: %(message)s --- line %(lineno)d in %(filename)s')
### ####### ###


pygame.init()
pygame.mixer.init()
pygame.mixer.music.fadeout(4000) #Fondu à 4000ms de la fin des musiques
#Création de la fenêtre avec ses attributs
variables['fenetre'] = pygame.display.set_mode((800,600))
variables['font'] = pygame.font.SysFont('Courrier', 25)
variables['quit'] = False

#variables du personnage
variables['speed'] = 30 #milliseconds par pas
variables['styleP'] = 1 #selection perso
variables['historyP']=[] #historique des déplacements du perso
variables['historyC']=[] #historique des déplacements de chaque caisse


variables['collection'] = "AC_Diamonds"
variables['lang']=fr_FR # ligne pour changer la langue du programme
buttonCollection = ['newGame',
                    'save',
                    'loadGame',
                    'resume',
                    'yes',
                    'no',
                    'quit',
                    'options',
                    '2Players',
                    '3Players',
                    '4Players',
                    'withAI',
                    'withoutAI',
                    'ok',
                    'cancel',
                    'previous',
                    'next',
                    'return',
                    'mainMenu',
                    'template',
                    'inf',
                    'sup']

### menu
mainMenuBtList = [0,2,7,6]
mainMenuFonctions = [lambda: bt.collectionMenu(),lambda: bt.loadGame(),lambda: bt.options(),lambda:bt.onLeave()]
levelMenuBtList = [11,12,8,9,10,17]
levelMenuFonctions = [lambda: bt.withAI(),lambda: bt.withoutAI(),lambda: bt.twoPlayers(),lambda: bt.threePlayers(),lambda: bt.fourPlayers(), lambda: bt.collectionMenu()]
pauseMenuBtList = [3,1,2,7,18]
pauseMenuFonctions = [lambda: bt.resume(),lambda: bt.saveGame(0),lambda: bt.loadGame(),lambda: bt.options(),lambda: bt.mainMenu()]
collectionMenuBtList = [19,17]
collectionMenuFonctions = [lambda: bt.mainMenu()]
optionMenuBtList = [20,21,20,21,17]
optionMenuFonctions = [lambda: bt.previousStyle(),lambda: bt.nextStyle(),lambda: bt.previousSpeed(),lambda: bt.nextSpeed()]

### sons
variables['sounds'] = {}
variables['sounds']['moving']=pygame.mixer.Sound("sounds/pas_cutted.wav")
variables['sounds']['push']=pygame.mixer.Sound("sounds/swoosh.wav")


### sprites taille normale
variables['spriteSize'] = 1
variables['surfaces'] = {}
def setSurfaces():
    global variables
    variables['surfaces']['perso'] = pygame.image.load('images/perso'+str(variables['spriteSize']*32)+'.png')
    variables['surfaces']['world'] = pygame.image.load('images/style1_'+str(variables['spriteSize']*32)+'.png')
    variables['surfaces']['blank'] = pygame.Surface((0,0))
    variables['surfaces']['wall'] = variables['surfaces']['world'].subsurface(0,0,variables['spriteSize']*32,variables['spriteSize']*32)
    variables['surfaces']['space'] = variables['surfaces']['world'].subsurface(variables['spriteSize']*32,0,variables['spriteSize']*32,variables['spriteSize']*32)
    variables['surfaces']['target'] = variables['surfaces']['world'].subsurface(0,variables['spriteSize']*32,variables['spriteSize']*32,variables['spriteSize']*32)
    variables['surfaces']['element'] = variables['surfaces']['world'].subsurface(variables['spriteSize']*32,variables['spriteSize']*32,variables['spriteSize']*32,variables['spriteSize']*32)
setSurfaces()

log.debug(variables)


pygame.display.set_icon(variables['surfaces']['element'])#icone de la fenetre
pygame.display.set_caption('Sokoban')#nom de la fenetre


