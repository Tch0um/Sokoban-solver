import pygame
from pygame.locals import *

from constantes import *
pygame.init()

#Création de la fenêtre
fenetre = pygame.display.set_mode(taille_fenetre)
#Icone
icone = pygame.image.load(image_icone).convert_alpha()
pygame.display.set_icon(icone)
#Titre
pygame.display.set_caption('Sokoban')










#BOUCLE INFINI
continuer = 1
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0

    pygame.display.flip()

pygame.quit()


