import pygame
from pygame.locals import *

from constantes import *
from classes import *
pygame.init()

#Création de la fenêtre
fenetre= pygame.display.set_mode((640,480), RESIZABLE)
#Icone
icone = perso_bas1
pygame.display.set_icon(icone)
#Titre
pygame.display.set_caption('Sokoban')

#Chargement et collage du fond
fond = pygame.image.load("images/grass2.png").convert()
fenetre.blit(fond, (0,0))
#Création du niveau
carte = Niveau('levels/carte')
carte.generer()
carte.afficher(fenetre)
#Création du personnage
perso = Perso(perso_bas1, perso_gauche1, perso_droite1, perso_haut1, carte)






#BOUCLE INFINI
continuer = 1
while continuer:
    pygame.time.Clock().tick(30) #limitation "fps" pour pas avoir le cpu à fond
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                perso.deplacer('droite')
            if event.key == K_LEFT:
                perso.deplacer('gauche')
            if event.key == K_UP:
                perso.deplacer('haut')
            if event.key == K_DOWN:
                perso.deplacer('bas')
    #Affichage aux nouvelles positions
    fenetre.blit(fond, (0,0))
    carte.afficher(fenetre)
    #Ajout ici
    fenetre.blit(perso.direction, (perso.x, perso.y))

    #niveau = Niveau(c_fichier_niveau)      #Doit-on le mettre la ou à l'exterieur de la boucle ?
    #niveau.generer()
    #niveau.afficher(fenetre)
    
    pygame.display.flip()

pygame.quit()


