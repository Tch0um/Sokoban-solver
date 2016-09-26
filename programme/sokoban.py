import pygame
from pygame.locals import *

from constantes import *
from classes import *
pygame.init()

#Création de la fenêtre
fenetre = pygame.display.set_mode(c_taille_fenetre)
#Icone
icone = pygame.image.load(c_image_icone).convert_alpha()
pygame.display.set_icon(icone)
#Titre
pygame.display.set_caption('Sokoban')










#BOUCLE INFINI
continuer = 1
while continuer:
    pygame.time.Clock().tick(30) #limitation "fps" pour pas avoir le cpu à fond
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0

    niveau = Niveau(c_fichier_niveau)
    niveau.generer()
    niveau.afficher(fenetre)
    
    pygame.display.flip()

pygame.quit()


