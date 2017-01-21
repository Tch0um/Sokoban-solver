import pygame
from pygame.locals import *
import GUI as bt

dWidth=21
dHeight=21
blank = pygame.Surface((0,0))

pygame.init()

#Création de la fenêtre avec ses attributs
fenetre= pygame.display.set_mode((800,600))
#icone = perso_sprite[0]
#pygame.display.set_icon(icone)
pygame.display.set_caption('Sokoban')


#variables du personnage
speed = 0        #milliseconds par pas
style_perso = 7  #selection perso

variables = {'historyP':[],'historyC':[]}


collection = "AC_Diamonds"
fond = pygame.image.load("images/"+'AC_Diamonds'+"_bg.png")
history = []



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
tileset_perso = pygame.image.load('images/perso64.png')
tileset_col = pygame.image.load('images/'+collection+'_style64.png')

taille_sprite = 64
space = tileset_col.subsurface(64,64,0,0)
wall = tileset_col.subsurface(0,0,64,64)
target = tileset_col.subsurface(0,64,64,64)
element = tileset_col.subsurface(64,64,64,64)
elementOnTarget = tileset_col.subsurface(64,0,64,64)
pOnTarget = target

perso_sprite = [tileset_perso.subsurface(448,192,64,64),tileset_perso.subsurface(384,192,64,64),tileset_perso.subsurface(512,192,64,64),tileset_perso.subsurface(448,0,64,64),tileset_perso.subsurface(384,0,64,64),tileset_perso.subsurface(512,0,64,64),tileset_perso.subsurface(448,64,64,64),tileset_perso.subsurface(384,64,64,64),tileset_perso.subsurface(512,64,64,64),tileset_perso.subsurface(448,128,64,64),tileset_perso.subsurface(384,128,64,64),tileset_perso.subsurface(512,128,64,64)]


### sprites taille reduite
tileset_perso_mini = pygame.image.load('images/perso32.png')
tileset_col_mini = pygame.image.load('images/'+collection+'_style32.png')

taille_sprite_mini=32
space_mini = tileset_col_mini.subsurface(32,32,0,0)
wall_mini = tileset_col_mini.subsurface(0,0,32,32)
target_mini = tileset_col_mini.subsurface(0,32,32,32)
element_mini = tileset_col_mini.subsurface(32,32,32,32)
elementOnTarget_mini = tileset_col_mini.subsurface(32,0,32,32)
pOnTarget_mini = target

perso_sprite_mini = [tileset_perso_mini.subsurface(224,96,32,32),tileset_perso_mini.subsurface(192,96,32,32),tileset_perso_mini.subsurface(256,96,32,32),tileset_perso_mini.subsurface(224,0,32,32),tileset_perso_mini.subsurface(192,0,32,32),tileset_perso_mini.subsurface(256,0,32,32),tileset_perso_mini.subsurface(224,32,32,32),tileset_perso_mini.subsurface(192,32,32,32),tileset_perso_mini.subsurface(256,32,32,32),tileset_perso_mini.subsurface(224,64,32,32),tileset_perso_mini.subsurface(192,64,32,32),tileset_perso_mini.subsurface(256,64,32,32)]

