from math import *
from classes import * #importation de constante.py , pygame et constante pygame incluses

pygame.init()

#Création de la fenêtre avec ses attributs
fenetre= pygame.display.set_mode((640,480))
icone = perso_sprite[0]
pygame.display.set_icon(icone)
pygame.display.set_caption('Sokoban')




niveaux = LevelCollection("levels/"+collection+".slc")
niveaux.loadLevel(2,fenetre)



#Création du personnage et premier affichage
playerStart = niveaux.afficheLevel(fenetre)
perso = Perso(niveaux,playerStart)
update(niveaux,perso,fenetre)


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
                    perso.animatePerso(3,fenetre)
            if event.key == K_LEFT:
                if perso.deplacer('gauche',fenetre):
                    perso.animatePerso(2,fenetre)
            if event.key == K_UP:
                if perso.deplacer('haut',fenetre):
                    perso.animatePerso(0,fenetre)
            if event.key == K_DOWN:
                if perso.deplacer('bas',fenetre):
                    perso.animatePerso(1,fenetre)
            if event.key == K_ESCAPE:
                continuer = 0
                
pygame.quit()
