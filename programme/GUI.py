import pygame
from pygame.locals import *
import classes as cls
import constantes as const
import sauvegarde as save
import os
import sys

variables = const.variables

def loadCollection(file):
    global niveaux,variables
    variables['collection'] = file[:-4]
    niveaux = cls.LevelCollection("levels/"+variables['collection']+".slc")
    print(variables['collection'])
    modeMenu()

    

def whileLoop(menuButtons,fenetre=None): #attend une action sur un bouton quelconque
    pygame.display.flip()
    menu = True
    while menu:
        pygame.time.Clock().tick(30)
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                for x in menuButtons:
                    x.isOnButton(event.pos)
            elif event.type == pygame.QUIT:
                menu = False

# menu principal
def mainMenu():
    variables['fenetre'] = pygame.display.set_mode((800,600))
    variables['fenetre'].blit(pygame.image.load('images/menu_bg.png'),(0,0))
    variables['fenetre'].blit(pygame.image.load('images/menu_title.png'),(200,50))
    variables['fenetre'].blit(pygame.image.load('images/menu_screen.png'),(450,200))
    menuButtons = []
    for x in range(len(cls.mainMenuBtList)):
        menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/'+cls.buttonCollection[cls.mainMenuBtList[x]]+'.png'),cls.buttonCollection[cls.mainMenuBtList[x]],cls.mainMenuFonctions[x],100,x*80+200)]
        menuButtons[x].displayButton()
    whileLoop(menuButtons)


def collectionMenu():
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
        variables['fenetre'].blit(pygame.image.load('images/menu_bg.png'),(0,0))
        variables['fenetre'].blit(pygame.image.load('images/menu_title.png'),(200,50)) 
        menuButtons = []
        for x in range(len(lsFic[6*(page-1):6*page])):
            z=0
            if x>=3:
                z=300
            menuButtons+=[cls.ButtonCollectionMenu(pygame.image.load('images/buttons/template.png'),'ButtonCollectionMenu',lsFic[(page-1)*6+x],loadCollection,150+z,x%3*80+200)]
            menuButtons[x].displayButton()
            variables['fenetre'].blit(font.render(lsFicRender[x+6*(page-1)][:-4],True,(20,20,20)),(190+z,x%3*80+210))

        menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/inf.png'),'inf',None,50,300),cls.ButtonMenu(pygame.image.load('images/buttons/sup.png'),'sup',None,700,300)]
        menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/return.png'),'return',cls.collectionMenuFonctions[0],150,500)]
        menuButtons[-1].displayButton()
        menuButtons[-2].displayButton()
        menuButtons[-3].displayButton()

        pygame.display.flip()
        menu = True
        while menu:
            pygame.time.Clock().tick(30)
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    for x in menuButtons:
                        if x.repr =='ButtonCollectionMenu':
                            x.isOnButton(event.pos)
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
            
        


def modeMenu():
    variables['fenetre'].blit(pygame.image.load('images/menu_bg.png'),(0,0))
    variables['fenetre'].blit(pygame.image.load('images/menu_title.png'),(200,50))
    menuButtons = []
    for x in range(len(cls.levelMenuBtList)):
        z=0
        if x>=3:
            z=300
        if cls.buttonCollection[cls.levelMenuBtList[x]] == 'return':
            menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/return.png'),'return',cls.levelMenuFonctions[x],150,500)]
        else:
            menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/'+cls.buttonCollection[cls.levelMenuBtList[x]]+'.png'),cls.buttonCollection[cls.levelMenuBtList[x]],cls.levelMenuFonctions[x],150+z,x%3*80+200)]
        menuButtons[x].displayButton()
    whileLoop(menuButtons)


def saveGame(port):
    save.saveGame(port,variables)

def loadGame():
    global collection,niveaux,variables
    tupl=save.loadGame(0,variables)
    niveaux = cls.LevelCollection("levels/"+variables['collection']+".slc")
    variables['nbNiveau'] = tupl[1]
    variables['niveauObj'] = cls.Niveau(niveaux.loadLevel(variables['nbNiveau'],variables['fenetre'])[0],tupl[0])
    variables['niveauObj'].gameConstructor()
    
    #affichage de la première frame
    variables['niveauObj'].afficheNiveau()

    whileGame()
    

def resume():
    variables['niveauObj'].afficheNiveau()
    whileGame()

def yes():
    pass

def no():
    pass

def quitt():
    pygame.quit() ## ban là ça fait une erreur pygame mais on s'en fou vu
                  ## que c'est pour fermer le jeu.

def options(alphaBg=False,fromPauseMenu=False):
    if alphaBg:
        variables['niveauObj'].afficheNiveau()
        bg = pygame.Surface((variables['fenetre'].get_size()))
        bg.fill((0,0,0))
        bg.convert_alpha()
        bg.set_alpha(180)
        variables['fenetre'].blit(bg,(0,0))
    else:
        variables['fenetre'].blit(pygame.image.load('images/menu_bg.png'),(0,0))
    variables['fenetre'].blit(pygame.image.load('images/menu_title.png'),(200,50))
    
    menuButtons = []
    for x in range(len(cls.optionMenuBtList)):
        if cls.buttonCollection[cls.optionMenuBtList[x]] == 'return' and fromPauseMenu:
            menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/return.png'),'return',lambda: pause(),150,500)]
        else:
            menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/'+cls.buttonCollection[cls.optionMenuBtList[x]]+'.png'),cls.buttonCollection[cls.optionMenuBtList[x]],cls.optionMenuFonctions[x],150,500)]
        menuButtons[x].displayButton()
    whileLoop(menuButtons)


def twoPlayers():
    print('2 joueurs')

def threePlayers():
    print('3 joueurs')

def fourPlayers():
    print('4 joueurs')

def withAI():
    pass

def pause():
    variables['niveauObj'].afficheNiveau()
    bg = pygame.Surface((variables['fenetre'].get_size()))
    bg.fill((0,0,0))
    bg.convert_alpha()
    bg.set_alpha(180)
    variables['fenetre'].blit(bg,(0,0))
    variables['fenetre'].blit(pygame.image.load('images/menu_title.png'),(200,50))
    menuButtons = []
    for x in range(len(cls.pauseMenuBtList)):
        z=0
        if x>=3:
            z=300
        menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/'+cls.buttonCollection[cls.pauseMenuBtList[x]]+'.png'),cls.buttonCollection[cls.pauseMenuBtList[x]],cls.pauseMenuFonctions[x],150+z,x%3*80+200)]
        menuButtons[x].displayButton()
    whileLoop(menuButtons)
    

def withoutAI():
    global variables
    
    variables['nbNiveau'] = 1
    tupleG = niveaux.loadLevel(variables['nbNiveau'],variables['fenetre'])
    variables['niveauObj'] = cls.Niveau(tupleG[0],tupleG[1])
    variables['niveauObj'].gameConstructor()
    #affichage de la première frame
    variables['niveauObj'].afficheNiveau()
    whileGame()
    

def whileGame(AI=False):
    global variables
    #boucle pygame
    continuer = 1
    #print(niveau)
    while continuer:
        pygame.time.Clock().tick(30) #limitation "fps"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = 0
            elif event.type == KEYDOWN:
                coordPerso = variables['niveauObj'].findPersonnage()
                if event.key == K_RIGHT:
                    variables['niveauObj'].gameO[coordPerso[0]][coordPerso[1]].deplace((0,1),False)
                    variables['niveauObj'].afficheNiveau()
                    
                if event.key == K_LEFT:
                    variables['niveauObj'].gameO[coordPerso[0]][coordPerso[1]].deplace((0,-1),False)
                    variables['niveauObj'].afficheNiveau()
                    
                if event.key == K_UP:
                    variables['niveauObj'].gameO[coordPerso[0]][coordPerso[1]].deplace((-1,0),False)
                    variables['niveauObj'].afficheNiveau()
                    
                if event.key == K_DOWN:
                    variables['niveauObj'].gameO[coordPerso[0]][coordPerso[1]].deplace((1,0),False)
                    variables['niveauObj'].afficheNiveau()
                    
                if event.key == K_BACKSPACE:
                    ##print('return')
                    if variables['historyP']!=[]:
                        save.rewind(variables)
                    
                if event.key == K_HOME:
                    for n in range (len(variables['historyP'])):
                        save.rewind(variables)

                if event.key == K_ESCAPE:
                    pause()
                    
                if event.key == K_KP0:
                    if variables['styleP']!=8:
                        variables['styleP']+=1
                    else:
                        variables['styleP']=1
                    variables['niveauObj'].gameO[coordPerso[0]][coordPerso[1]].setTileset()
                    variables['niveauObj'].afficheNiveau()
                    
                if event.key == K_KP_PLUS:
                    variables['speed']+=5
                    print(variables['speed'])
                    
                if event.key == K_KP_MINUS:
                    if variables['speed']>5:
                        variables['speed']-=5
                    print(variables['speed'])
                    
                #print(variables)
        if variables['niveauObj'].checkTarget(): #test de victoire
            print('vous avez gagné !!!')
