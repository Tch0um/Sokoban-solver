from math import *
from classes import * #importation de constante.py , pygame et constante pygame incluses

pygame.init()

#Création de la fenêtre avec ses attributs
fenetre= pygame.display.set_mode((640,480))
icone = perso_sprite[0]
pygame.display.set_icon(icone)
pygame.display.set_caption('Sokoban')




niveaux = LevelCollection("levels/"+collection+".slc")
grilleNiveau = niveaux.loadLevel(0,fenetre)
niveau = Niveau(grilleNiveau[0],grilleNiveau[1])


niveau.gameConstructor()
niveau.afficheNiveau(fenetre)

continuer = 1
while continuer:
    pygame.time.Clock().tick(30) #limitation "fps"
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = 0
        elif event.type == KEYDOWN:
            coordPerso = niveau.findPersonnage()
            if event.key == K_RIGHT:
                niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(2,niveau)
                niveau.afficheNiveau(fenetre)
            if event.key == K_LEFT:
                niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(-2,niveau)
                niveau.afficheNiveau(fenetre)
            if event.key == K_UP:
                niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(-1,niveau)
                niveau.afficheNiveau(fenetre)
            if event.key == K_DOWN:
                niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(1,niveau)
                niveau.afficheNiveau(fenetre)
            if event.key == K_ESCAPE:
                continuer = 0
pygame.quit()
