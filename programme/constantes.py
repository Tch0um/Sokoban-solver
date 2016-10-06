'''Ce module contient les différente constantes du jeu'''
import pygame
from pygame.locals import *

pygame.init()

nombre_sprite_cote = 20
taille_sprite = 64
cote_fenetre = nombre_sprite_cote * taille_sprite
collection = "AC_Diamonds"


#Chargement des images
tileset = pygame.image.load("images/palette.png")
tileset_route = pygame.image.load('images/route.png')
tileset_perso = pygame.image.load('images/perso64.png')
tileset_perso_mini = pygame.image.load('images/perso32.png')
tileset_col = pygame.image.load('images/'+collection+'_style64.png')
tileset_col_mini = pygame.image.load('images/'+collection+'_style32.png')
fond = pygame.image.load("images/"+collection+"_bg.png")

#tileset de la carte
arbre = tileset.subsurface(4,287,59,65)
puit = tileset.subsurface(63,327,67,90)
caisse = tileset.subsurface(256,0,129,129)
herbe = tileset.subsurface(160,449,33,33)
route = tileset_route.subsurface(16,136,35,35)

space = tileset_col.subsurface(64,64,0,0)
wall = tileset_col.subsurface(0,0,64,64)
target = tileset_col.subsurface(0,64,64,64)
element = tileset_col.subsurface(64,64,64,64)
elementOnTarget = tileset_col.subsurface(64,0,64,64)
pOnTarget = target


#variables du personnage
nb_pas = 3            #nb de boucle de 3 pas par changement de cases
p_speed = 40         #miliseconds par pas

#tileset personnage
# haut,bas,gauche,droite
perso_sprite = [tileset_perso.subsurface(448,192,64,64),tileset_perso.subsurface(384,192,64,64),tileset_perso.subsurface(512,192,64,64),tileset_perso.subsurface(448,0,64,64),tileset_perso.subsurface(384,0,64,64),tileset_perso.subsurface(512,0,64,64),tileset_perso.subsurface(448,64,64,64),tileset_perso.subsurface(384,64,64,64),tileset_perso.subsurface(512,64,64,64),tileset_perso.subsurface(448,128,64,64),tileset_perso.subsurface(384,128,64,64),tileset_perso.subsurface(512,128,64,64)]
