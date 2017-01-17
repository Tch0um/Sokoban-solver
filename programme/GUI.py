import pygame
from pygame.locals import *
import classes as cls
import sauvegarde as save
import os
import sys

def loadCollection(fenetre,file):
    global collection
    collection = file[:-4]
    print(collection)
    #fond = pygame.image.load("images/"+collection+"_bg.png")

    

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
    global collectionMenuFonctions
    fenetre.blit(pygame.image.load('images/menu_bg.png'),(0,0))
    fenetre.blit(pygame.image.load('images/menu_title.png'),(200,50))  
        
    lsFic = os.listdir('levels/')
    font = pygame.font.SysFont('Courrier', 25)
    lsFicRender = []
    for chaine1 in lsFic:
        chaine2 = ''
        for char in chaine1:
            if char=='_':
                chaine2+=' '
            else:
                chaine2+=char
        lsFicRender+=[chaine2]
        
    menuButtons = []
    for x in range(len(lsFic)):
        menuButtons+=[cls.ButtonCollectionMenu(pygame.image.load('images/buttons/template.png'),'ButtonCollectionMenu',lsFic[x],loadCollection,100,x*80+200)]
        menuButtons[x].displayButton(fenetre)
        
    menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/return.png'),'return',cls.collectionMenuFonctions[0],150,500)]
    menuButtons[-1].displayButton(fenetre)

        
    for x in range(len(lsFic)):
        fenetre.blit(font.render(lsFicRender[x][:-4],True,(20,20,20)),(140,80*x+210))
        
    whileLoop(menuButtons,fenetre)


def newGame(fenetre):
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


def saveGame(niveau,port,nbNiveau,fenetre):
    save.saveGame(niveau,port,nbNiveau)

def loadGame(fenetre):
    pass

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

def twoPlayers():
    pass

def threePlayers():
    pass

def fourPlayers():
    pass

def withAI():
    pass

def withoutAI():
    pass
