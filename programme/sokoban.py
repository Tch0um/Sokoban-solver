#from Astar import *# importation de constante.py , pygame, constante pygame, classes.py, math, Astar.py
# -*- coding:utf-8 -*-
from GUI import *
import L10n as l10n
#chargement menu principal
pygame.mixer.music.load("sounds/LeafShapedFeelings_7thGearRemix.mp3")
pygame.mixer.music.play()

#chargement des langues
lang = os.environ['GDM_LANG']
if lang in l10n.langageAvailable:
    variables['lang']=l10n.langageAvailable[lang]
else:    
    variables['lang']=l10n.fr_FR
mainMenu()
