'''Ce module contient les différente constantes du jeu'''
import pygame
from pygame.locals import *

pygame.init()

#Image de l'icone
c_image_icone = "images/caisse.png"

#Taille de la fénêtre
c_taille_fenetre = 720,480

#fichier du niveau
c_fichier_niveau="levels/niveau.txt"

#test temporaire
image_accueil = "imgs/accueil.png"
image_fond = "imgs/fond.jpg"
image_mur = "images/caisse30.png"
image_depart = "imgs/depart.png"
image_arrivee = "imgs/arrivee.png"

nombre_sprite_cote = 15
taille_sprite = 30
cote_fenetre = nombre_sprite_cote * taille_sprite

