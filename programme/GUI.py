import pygame
from pygame.locals import *
import classes as cls
import constantes as const
import sauvegarde as save
import os
import sys

variables = const.variables

def loadCollection(fenetre,file):
    global niveaux,variables
    variables['collection'] = file[:-4]
    niveaux = cls.LevelCollection("levels/"+variables['collection']+".slc")
    print(variables['collection'])
    modeMenu(fenetre)

    

def whileLoop(menuButtons,fenetre=None): #attend une action sur un bouton quelconque
    pygame.display.flip()
    menu = True
    while menu:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for x in menuButtons:
                    if x.repr =='ButtonCollectionMenu':
                        x.isOnButton(event.pos,fenetre)
                    else:
                        x.isOnButton(event.pos)
            elif event.type == pygame.QUIT:
                menu = False
    pygame.quit()

# menu principal
def mainMenu(fenetre):
    fenetre.blit(pygame.image.load('images/menu_bg.png'),(0,0))
    fenetre.blit(pygame.image.load('images/menu_title.png'),(200,50))
    fenetre.blit(pygame.image.load('images/menu_screen.png'),(450,200))
    menuButtons = []
    for x in range(len(cls.mainMenuBtList)):
        menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/'+cls.buttonCollection[cls.mainMenuBtList[x]]+'.png'),cls.buttonCollection[cls.mainMenuBtList[x]],cls.mainMenuFonctions[x],100,x*80+200)]
        menuButtons[x].displayButton(fenetre)
    whileLoop(menuButtons)


def collectionMenu(fenetre):
    lsFic = os.listdir('levels/')
    font = pygame.font.SysFont('Courrier', 25)

    
    lsFicRender = []
    for chaine1 in lsFic:
        chaine2 = ''
        if len(chaine1)>13:
            for char in chaine1[:13]: 
                if char=='_':
                    chaine2+=' '
                else:
                    chaine2+=char
        else:
            for char in chaine1:
                if char=='_':
                    chaine2+=' '
                else:
                    chaine2+=char
        lsFicRender+=[chaine2]

    page=1
    pagination = True
    print((len(lsFic)//6)+1)
    while pagination:
        print('page = '+str(page))
        fenetre.blit(pygame.image.load('images/menu_bg.png'),(0,0))
        fenetre.blit(pygame.image.load('images/menu_title.png'),(200,50)) 
        menuButtons = []
        for x in range(len(lsFic[6*(page-1):6*page])):
            z=0
            if x>=3:
                z=300
            menuButtons+=[cls.ButtonCollectionMenu(pygame.image.load('images/buttons/template.png'),'ButtonCollectionMenu',lsFic[(page-1)*6+x],loadCollection,150+z,x%3*80+200)]
            menuButtons[x].displayButton(fenetre)
            fenetre.blit(font.render(lsFicRender[x+6*(page-1)][:-4],True,(20,20,20)),(190+z,x%3*80+210))

        menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/inf.png'),'inf',None,50,300),cls.ButtonMenu(pygame.image.load('images/buttons/sup.png'),'sup',None,700,300)]
        menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/return.png'),'return',cls.collectionMenuFonctions[0],150,500)]
        menuButtons[-1].displayButton(fenetre)
        menuButtons[-2].displayButton(fenetre)
        menuButtons[-3].displayButton(fenetre)

        pygame.display.flip()
        menu = True
        while menu:
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for x in menuButtons:
                        if x.repr =='ButtonCollectionMenu':
                            x.isOnButton(event.pos,fenetre)
                        else:
                            if x.repr=='inf' and page>1 and x.isOnButton(event.pos):
                                menu=False
                                page=page-1
                                print('dans while inf, page = '+str(page))
                            elif x.repr=='sup' and page<((len(lsFic)//6)+1)and x.isOnButton(event.pos):
                                menu=False
                                page=page+1
                                print('dans while sup, page = '+str(page))
                            else:
                                x.isOnButton(event.pos)
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    menu=False
                    pagination = False
            
        


def modeMenu(fenetre):
    fenetre.blit(pygame.image.load('images/menu_bg.png'),(0,0))
    fenetre.blit(pygame.image.load('images/menu_title.png'),(200,50))
    menuButtons = []
    for x in range(len(cls.levelMenuBtList)):
        z=0
        if x>=3:
            z=300
        if cls.buttonCollection[cls.levelMenuBtList[x]] == 'return':
            menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/return.png'),'return',cls.levelMenuFonctions[x],150,500)]
        else:
            menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/'+cls.buttonCollection[cls.levelMenuBtList[x]]+'.png'),cls.buttonCollection[cls.levelMenuBtList[x]],cls.levelMenuFonctions[x],150+z,x%3*80+200)]
        menuButtons[x].displayButton(fenetre)
    whileLoop(menuButtons)


def saveGame(niveau,port,nbNiveau,fenetre,variables):
    save.saveGame(niveau,port,nbNiveau,variables)

def loadGame(fenetre):
    global collection,niveaux,variables
    tupl=save.loadGame(0,variables)
    niveaux = cls.LevelCollection("levels/"+variables['collection']+".slc")
    nbNiveau = tupl[1]
    niveau = cls.Niveau(niveaux.loadLevel(nbNiveau,fenetre)[0],tupl[0])
    niveau.gameConstructor()
    
    #affichage de la première frame
    niveau.afficheNiveau(fenetre)
    
    whileGame(fenetre,nbNiveau,niveau)
    

def resume():
    pass

def yes():
    pass

def no():
    pass

def quitt():
    pygame.quit() ## ban là ça fait une erreur pygame mais on s'en fou vu
                  ## que c'est pour fermer le jeu.

def options(fenetre):
    pass

def twoPlayers(fenetre):
    print('2 joueurs')

def threePlayers(fenetre):
    print('3 joueurs')

def fourPlayers(fenetre):
    print('4 joueurs')

def withAI(fenetre):
    pass

def withoutAI(fenetre):
    global variables
    
    nbNiveau = 1
    tupleG = niveaux.loadLevel(nbNiveau,fenetre)
    niveau = cls.Niveau(tupleG[0],tupleG[1])
    niveau.gameConstructor()
    #affichage de la première frame
    niveau.afficheNiveau(fenetre)
    whileGame(fenetre,nbNiveau,niveau)
    

def whileGame(fenetre,nbNiveau,niveau,AI=False):
    #boucle pygame
    continuer = 1
    #print(niveau)
    while continuer:
        pygame.time.Clock().tick(30) #limitation "fps"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = 0
            elif event.type == KEYDOWN:
                coordPerso = niveau.findPersonnage()
                if event.key == K_RIGHT:
                    niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(2,niveau,fenetre,False)
                    niveau.afficheNiveau(fenetre)
                if event.key == K_LEFT:
                    niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(-2,niveau,fenetre,False)
                    niveau.afficheNiveau(fenetre)
                if event.key == K_UP:
                    niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(-1,niveau,fenetre,False)
                    niveau.afficheNiveau(fenetre)
                if event.key == K_DOWN:
                    niveau.gameO[coordPerso[0]][coordPerso[1]].deplace(1,niveau,fenetre,False)
                    niveau.afficheNiveau(fenetre)
                if event.key == K_SPACE:
                    ##print('return')
                    if variables['historyP']!=[]:
                        save.rewind(fenetre,variables,niveau,coordPerso)
                if event.key == K_F2:
                    saveGame(niveau,0,nbNiveau,fenetre,variables)
                if event.key == K_ESCAPE:
                    continuer = 0
                if event.key == K_KP0:
                    if variables['styleP']!=8:
                        variables['styleP']+=1
                    else:
                        variables['styleP']=1
                    niveau.gameO[coordPerso[0]][coordPerso[1]].setTileset()
                    niveau.afficheNiveau(fenetre)
                if event.key == K_KP_PLUS:
                    variables['speed']+=5
                    print(variables['speed'])
                if event.key == K_KP_MINUS:
                    if variables['speed']>5:
                        variables['speed']-=5
                    print(variables['speed'])
                #print(variables)
        if niveau.checkTarget(): #test de victoire
            print('vous avez gagné !!!')
            continuer = 0
            
    pygame.quit()
