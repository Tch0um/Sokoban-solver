from math import *
from classes import * #importation de constante.py , pygame et constante pygame incluses
from sokobAstar import *

pygame.init()

#Création de la fenêtre avec ses attributs
fenetre= pygame.display.set_mode((640,480))
icone = perso_sprite[0]
pygame.display.set_icon(icone)
pygame.display.set_caption('Sokoban')



#chargement du niveau
niveaux = LevelCollection("levels/"+collection+".slc")
grilleNiveau = niveaux.loadLevel(0,fenetre)
niveau = Niveau(grilleNiveau[0],grilleNiveau[1])
niveau.gameConstructor()

#affichage de la première frame
niveau.afficheNiveau(fenetre)


def triggerAstar():
    liste = niveau.benzebute()
    lsAstar = []
    for z in range(len(liste[0])):
        grille = niveau.grilleObstacle()
        lsAstar.append(Astar(grille,(liste[0][z].x,liste[0][z].y),(liste[1][z].x,liste[1][z].y),coordPerso))
        print(lsAstar[-1])


#boucle pygame
deplastar=None # deplastar = variable pour effectuer le déplacement du personnage avec A*
continuer = 1
print(niveau)
while continuer:
    pygame.time.Clock().tick(30) #limitation "fps"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0
        elif event.type == KEYDOWN:
            coordPerso = niveau.findPersonnage()
            if event.key == K_RIGHT or deplastar==0: # deplastar = variable pour effectuer le déplacement du personnage
                niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(2,niveau,fenetre)
                niveau.afficheNiveau(fenetre)
            if event.key == K_LEFT or deplastar==1:
                niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(-2,niveau,fenetre)
                niveau.afficheNiveau(fenetre)
            if event.key == K_UP or deplastar==2:
                niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(-1,niveau,fenetre)
                niveau.afficheNiveau(fenetre)
            if event.key == K_DOWN or deplastar==3:
                niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(1,niveau,fenetre)
                niveau.afficheNiveau(fenetre)
            if event.key == K_ESCAPE:
                continuer = 0
            if event.key == K_KP_MULTIPLY:# appuyer sur * pour avoir le chemin
                triggerAstar()
            #print(niveau) #debugger dans la console
    if niveau.checkTarget(): #test de victoire
        print('vous avez gagné !!!')
        continuer = 0
        
pygame.quit()
