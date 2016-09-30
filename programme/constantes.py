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
arbre = tileset.subsurface(4,287,59,65)
puit = tileset.subsurface(63,327,67,90)
caisse = tileset.subsurface(256,0,129,129)
herbe = tileset.subsurface(160,449,33,33)
route = tileset_route.subsurface(16,136,35,35)
#Frames du personnages
#Bas
perso_bas1 = tileset_perso.subsurface(223,0,33,33)
perso_bas2 = tileset_perso.subsurface(193,0,33,33)
perso_bas3 = tileset_perso.subsurface(253,0,33,33)
#Gauche
perso_gauche1 = tileset_perso.subsurface(223,32,33,33)
perso_gauche2 = tileset_perso.subsurface(193,32,33,33)
perso_gauche3 = tileset_perso.subsurface(253,32,33,33)
#Droite
perso_droite1 = tileset_perso.subsurface(223,64,33,33)
perso_droite2 = tileset_perso.subsurface(193,64,33,33)
perso_droite3 = tileset_perso.subsurface(253,64,33,33)
#Haut
perso_haut1 = tileset_perso.subsurface(223,96,33,33)
perso_haut2 = tileset_perso.subsurface(193,96,33,33)
perso_haut3 = tileset_perso.subsurface(253,96,33,33)

#Tuples des Images
position_perso=(perso_bas1,perso_bas2,perso_bas3,perso_gauche1,
                perso_gauche2,perso_gauche3,perso_droite1,perso_droite2,
                perso_droite3,perso_haut1,perso_haut2,perso_haut3)

