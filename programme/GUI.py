import pygame
from pygame.locals import *
import classes as cls
import constantes as const
import sauvegarde as save
import os
import astar42
import time
from pygame import mixer
import imagery as i

pygame.mixer.init()
deplacement=pygame.mixer.Sound("sons/pas_cutted.wav")
pousser=pygame.mixer.Sound("sons/swoosh.wav")

variables = const.variables
def placeCenter(surf1,surf2):
    x = (surf1.get_size()[0]//2)-(surf2.get_size()[0]//2)
    y = (surf1.get_size()[1]//2)-(surf2.get_size()[1]//2)
    return (x,y)

def loadCollection(file):
    global niveaux,variables
    variables['collection'] = file[:-4]
    niveaux = cls.LevelCollection("levels/"+variables['collection']+".slc")
    variables['levelNo'] = 1
    print(variables['collection'])
    levelMenu()

    

def whileLoop(menuButtons,fenetre=None): #attend une action sur un bouton quelconque
    pygame.display.flip()
    while  not variables['quit']:
        pygame.time.Clock().tick(30)
        eventIncr,event = 0,pygame.event.get()
        while not variables['quit'] and eventIncr<len(event):
            if event[eventIncr].type == MOUSEBUTTONDOWN and event[eventIncr].button == 1:
                for x in menuButtons:
                    x.isOnButton(event[eventIncr].pos)
            eventIncr+=1
    quitt()

# menu principal
def mainMenu():
    variables['persoObj']=cls.Personnage(None,0,0)
    variables['ingame']=False
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

    ### liste des nom de fichiers ###
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
    ### ########################## ###

    page=1
    pagination = True
    print((len(lsFic)//6)+1)
    while not variables['quit'] and pagination:
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
            variables['fenetre'].blit(variables['font'].render(lsFicRender[x+6*(page-1)][:-4],True,(20,20,20)),(190+z,x%3*80+210))

        menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/inf.png'),'inf',None,50,300),cls.ButtonMenu(pygame.image.load('images/buttons/sup.png'),'sup',None,700,300)]
        menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/return.png'),'return',cls.collectionMenuFonctions[0],150,500)]
        menuButtons[-1].displayButton()
        menuButtons[-2].displayButton()
        menuButtons[-3].displayButton()

        pygame.display.flip()
        menu = True
        while not variables['quit'] and menu:
            pygame.time.Clock().tick(30)
            eventIncr,event = 0,pygame.event.get()
            while not variables['quit'] and eventIncr<len(event):
                if event[eventIncr].type == MOUSEBUTTONDOWN and event[eventIncr].button == 1:
                    for x in menuButtons:
                        if x.repr =='ButtonCollectionMenu':
                            x.isOnButton(event[eventIncr].pos)
                        else:
                            if x.repr=='inf' and page>1 and x.isOnButton(event[eventIncr].pos):
                                menu=False
                                page=page-1
                                print('dans while inf, page = '+str(page))
                            elif x.repr=='sup' and page<((len(lsFic)//6)+1)and x.isOnButton(event[eventIncr].pos):
                                menu=False
                                page=page+1
                                print('dans while sup, page = '+str(page))
                            else:
                                x.isOnButton(event[eventIncr].pos)
                eventIncr+=1





### menu niveau ###
def nextLevel():
    variables['levelNo']+=1
    levelMenu()

def previousLevel():
    variables['levelNo']-=1


def levelMenu():
    fontTextLevel = pygame.font.SysFont('Courrier', 40)
    variables['fenetre'].blit(pygame.image.load('images/menu_bg.png'),(0,0))
    variables['fenetre'].blit(fontTextLevel.render('#'+str(variables['levelNo']),True,(220,220,220)),(380,70))
    preview = niveaux.loadPreview()
    variables['fenetre'].blit(preview,placeCenter(variables['fenetre'],preview))
    menuButtons=[cls.ButtonMenu(pygame.image.load('images/buttons/inf.png'),'inf',lambda: previousLevel(),50,300),cls.ButtonMenu(pygame.image.load('images/buttons/sup.png'),'sup',lambda: nextLevel(),700,300)]
    menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/return.png'),'return',lambda: collectionMenu(),150,500)]
    for bt in menuButtons:
        bt.displayButton()
    whileLoop(menuButtons)





### menu mode ###
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





### menu sauvegarde ###
def saveGame(port):
    save.saveGame(port,variables)
    fontTextSaving = pygame.font.SysFont('Courrier', 40)
    variables['fenetre'].blit(fontTextSaving.render('Sauvegarde effectuée',True,(220,220,220)),(variables['fenetre'].get_size()[0]-350,variables['fenetre'].get_size()[1]-50))
    pygame.display.flip()

def loadGame():
    global collection,niveaux,variables
    tupl=save.loadGame(0,variables)
    niveaux = cls.LevelCollection("levels/"+variables['collection']+".slc")
    variables['levelNo'] = tupl[1]
    variables['niveauObj'] = cls.Niveau(niveaux.loadLevel(variables['nbNiveau'],variables['fenetre'])[0],tupl[0])
    variables['niveauObj'].gameConstructor()
    if variables['spriteSize']==2:
        print('essaie')
        variables['niveauObj'].offset=[(800-2*32*len(variables['niveauObj'].gameO[0]))//2,(600-2*32*len(variables['niveauObj'].gameO))//2]
    
    #affichage de la première frame
    variables['niveauObj'].afficheNiveau()

    whileGame()
    




### menu pause ###
def resume():
    variables['niveauObj'].afficheNiveau()
    whileGame()

def yes():
    pass

def no():
    pass

def onLeave():
    variables['quit']=True

def quitt():
    print('pygame.quit()')
    pygame.quit()


def pause():
    variables['niveauObj'].afficheNiveau(display=False)
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
    




### menu options ###
def previousStyle():
    print('previousStyle')
    if variables['styleP']!=1:
        variables['styleP']-=1
        options()
    

def nextStyle():
    print('nextStyle')
    if variables['styleP']!=8:
        variables['styleP']+=1
        options()

def previousSpeed():
    if variables['speed']>5:
        variables['speed']-=5
    print(variables['speed'])
    options()

def nextSpeed():
    variables['speed']+=5
    print(variables['speed'])
    options()

def options():
    variables['persoObj'].setTileset()
    if variables['ingame']:
        variables['niveauObj'].afficheNiveau(display=False)
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
        if cls.buttonCollection[cls.optionMenuBtList[x]] == 'return':
            if variables['ingame']:
                menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/return.png'),'return',lambda: pause(),150,500)]
            else:
                menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/return.png'),'return',lambda: mainMenu(),150,500)]
        else:
            if cls.buttonCollection[cls.optionMenuBtList[x]] == 'sup':
                menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/'+cls.buttonCollection[cls.optionMenuBtList[x]]+'.png'),cls.buttonCollection[cls.optionMenuBtList[x]],cls.optionMenuFonctions[x],600,(x-1)*100+200)]
            else:
                
                menuButtons+=[cls.ButtonMenu(pygame.image.load('images/buttons/'+cls.buttonCollection[cls.optionMenuBtList[x]]+'.png'),cls.buttonCollection[cls.optionMenuBtList[x]],cls.optionMenuFonctions[x],100,x*100+200)]
        menuButtons[x].displayButton()
    #resize personnage
    if variables['spriteSize']==1:
        
        variables['fenetre'].blit(i.scaleUpSurface(i.scaleUpSurface(variables['persoObj'].surface)),(320,150))
    else:
        variables['fenetre'].blit(i.scaleUpSurface(variables['persoObj'].surface),(320,150))
    fontTextSaving = pygame.font.SysFont('Courrier', 40)
    variables['fenetre'].blit(fontTextSaving.render(str(variables['speed'])+' ms',True,(220,220,220)),(320,400))
    whileLoop(menuButtons)





### lancement de parties ###
def twoPlayers():
    print('2 joueurs')

def threePlayers():
    print('3 joueurs')

def fourPlayers():
    print('4 joueurs')

def withAI():
    pass


def withoutAI():
    global variables
    
    tupleG = niveaux.loadLevel()
    variables['niveauObj'] = cls.Niveau(tupleG[0],tupleG[1])
    variables['niveauObj'].gameConstructor()
    #affichage de la première frame
    variables['niveauObj'].afficheNiveau()
    whileGame()
    

def whileGame(AI=False):
    while not variables['quit']:
        variables['ingame']=True
        pygame.time.Clock().tick(30) #limitation "fps"
        gameIncr,game = 0,pygame.event.get()
        while not variables['quit'] and gameIncr<len(game):
            if game[gameIncr].type == pygame.QUIT:
                continuer = 0
            elif game[gameIncr].type == KEYDOWN:
                if game[gameIncr].key == K_RIGHT:
                    deplacement.play()
                    variables['persoObj'].deplace((0,1),False)                    
                if game[gameIncr].key == K_LEFT:
                    deplacement.play()
                    variables['persoObj'].deplace((0,-1),False)                    
                if game[gameIncr].key == K_UP:
                    deplacement.play()
                    variables['persoObj'].deplace((-1,0),False)
                if game[gameIncr].key == K_DOWN:
                    deplacement.play()
                    variables['persoObj'].deplace((1,0),False)
                    
                if game[gameIncr].key == K_BACKSPACE:
                    ##print('return')
                    if variables['historyP']!=[]:
                        save.rewind(variables)
                    
                if game[gameIncr].key == K_HOME:
                    for n in range (len(variables['historyP'])):
                        save.rewind(variables)

                if game[gameIncr].key == K_a:
                    lsDep = astar42.astar()
                    print('lsDep '+str(lsDep))
                    if lsDep!=None:
                        lsDep.reverse()
                        for x in lsDep:
                            variables['persoObj'].deplace(x,False)
                            
                if game[gameIncr].key == K_ESCAPE:
                    pause()
            gameIncr+=1
                    
                #print(variables)
        if variables['niveauObj'].checkTarget(): #test de victoire
            pass
