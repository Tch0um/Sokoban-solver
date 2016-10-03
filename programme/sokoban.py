import pygame
from pygame.locals import *
from math import *

from constantes import *
from classes import *
pygame.init()

#Création de la fenêtre
fenetre= pygame.display.set_mode((640,480))
#Icone
icone = perso_sprite[0]
pygame.display.set_icon(icone)
#Titre
pygame.display.set_caption('Sokoban')

niveaux = LevelCollection("levels/"+collection+".slc")
niveaux.loadLevel(2)
fenetre= pygame.display.set_mode((niveaux.width*taille_sprite,niveaux.height*taille_sprite))

#Chargement et collage du fond
fond = pygame.image.load("images/"+collection+"_bg.png").convert()
fenetre.blit(fond, (0,0))
playerStart = niveaux.afficheLevel(fenetre)
print(str(playerStart))
#Création du personnage
perso = Perso(niveaux,playerStart)

def update():
    #recalcule toute la fenetre
    fenetre.blit(fond, (0,0))
    niveaux.afficheLevel(fenetre)
    fenetre.blit(perso.direction,(perso.x,perso.y))
    pygame.display.flip()
        
def animatePerso(direction):
    for n in range(nb_pas):
        perso.direction=perso_sprite[n%3+direction*3]
        if direction in (2,3):
            if direction%2==0:
                perso.x -= taille_sprite//nb_pas
            else:
                perso.x += taille_sprite//nb_pas
        else:
            if direction%2==0:
                perso.y-= taille_sprite//nb_pas
            else:
                perso.y+= taille_sprite//nb_pas
        update()
        pygame.time.wait(p_speed)




update()

#BOUCLE INFINI
continuer = 1
while continuer:
    pygame.time.Clock().tick(30) #limitation "fps"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0
        elif event.type == KEYDOWN:
            if event.key == K_RIGHT:
                if perso.deplacer('droite',fenetre):
                    animatePerso(3)
            if event.key == K_LEFT:
                if perso.deplacer('gauche',fenetre):
                    animatePerso(2)
            if event.key == K_UP:
                if perso.deplacer('haut',fenetre):
                    animatePerso(0)
            if event.key == K_DOWN:
                if perso.deplacer('bas',fenetre):
                    animatePerso(1)
            if event.key == K_ESCAPE:
                continuer = 0

    #niveau = Niveau(c_fichier_niveau)      #Doit-on le mettre la ou à l'exterieur de la boucle ?
    #niveau.generer()
    #niveau.afficher(fenetre)
    

pygame.quit()
