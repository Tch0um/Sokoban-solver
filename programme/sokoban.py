##from sokobAstar import *
from Astar import *# importation de constante.py , pygame, constante pygame, classes.py, math, Astar.py
from sauvegarde import *

pygame.init()

#Création de la fenêtre avec ses attributs
fenetre= pygame.display.set_mode((800,600))
icone = perso_sprite[0]
pygame.display.set_icon(icone)
pygame.display.set_caption('Sokoban')


#menu principal
def mainMenu():
    fenetre.blit(pygame.image.load('images/menu_bg.png'),(0,0))
    fenetre.blit(pygame.image.load('images/menu_title.png'),(200,50))
    fenetre.blit(pygame.image.load('images/menu_screen.png'),(450,200))
    menuButtons = []
    for x in range(4):
        print(buttonCollection[mainMenu[x]])
        menuButtons+=[ButtonMenu(pygame.image.load('images/buttons/'+buttonCollection[mainMenuBtList[x]]+'.png'),buttonCollection[mainMenuBtList[x]],buttonFunctions[mainMenuBtList[x]],100,x*80+200)]
        menuButtons[x].displayButton(fenetre)
        
    pygame.display.flip()
    menu = True
        
    while menu:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for x in menuButtons:
                    x.isOnButton(event.pos)


#chargement du niveau
niveaux = LevelCollection("levels/"+collection+".slc")
grilleNiveau = niveaux.loadLevel(1,fenetre)
niveau = Niveau(grilleNiveau[0],grilleNiveau[1])
niveau.gameConstructor()

#affichage de la première frame
niveau.afficheNiveau(fenetre)


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
            if event.key == K_F2:
                saveGame(niveau,0,0)
            if event.key == K_F3:
                print(loadGame(0))
            if event.key == K_SPACE:# appuyer sur * pour avoir le chemin
##                triggerAstar(coordPerso)
                triggerIA(niveau,fenetre)
            #print(niveau) #debugger dans la console
    if niveau.checkTarget(): #test de victoire
        print('vous avez gagné !!!')
        continuer = 0
        
pygame.quit()
