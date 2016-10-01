'''Ce module contient les différente constantes du jeu'''
import pygame
from pygame.locals import *

pygame.init()

nombre_sprite_cote = 20
taille_sprite = 34
cote_fenetre = nombre_sprite_cote * taille_sprite

#Chargement des images
tileset = pygame.image.load("images/palette.png")
tileset_route = pygame.image.load('images/route.png')
tileset_perso = pygame.image.load('images/perso.png')

#tileset de la carte
arbre = tileset.subsurface(4,287,59,65)
puit = tileset.subsurface(63,327,67,90)
caisse = tileset.subsurface(256,0,129,129)
herbe = tileset.subsurface(160,449,33,33)
route = tileset_route.subsurface(16,136,35,35)


#variables du personnage
nb_pas = 2            #nb de boucle de 3 pas par changement de cases
p_speed = 40         #miliseconds par pas

#tileset personnage
# haut,bas,gauche,droite
perso_sprite = [tileset_perso.subsurface(223,96,33,33),tileset_perso.subsurface(193,96,33,33),tileset_perso.subsurface(253,96,33,33),tileset_perso.subsurface(223,0,33,33),tileset_perso.subsurface(193,0,33,33),tileset_perso.subsurface(253,0,33,33),tileset_perso.subsurface(223,32,33,33),tileset_perso.subsurface(193,32,33,33),tileset_perso.subsurface(253,32,33,33),tileset_perso.subsurface(223,64,33,33),tileset_perso.subsurface(193,64,33,33),tileset_perso.subsurface(253,64,33,33)]
