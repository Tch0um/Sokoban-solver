"""Classes du jeu de Labyrinthe Donkey Kong"""

import pygame
from pygame.locals import * 
from constantes import *

class Niveau:
	"""Classe permettant de créer un niveau"""
	def __init__(self, fichier):
		self.fichier = fichier
		self.structure = 0
	
	
	def generer(self):
		"""Méthode permettant de générer le niveau en fonction du fichier.
		On crée une liste générale, contenant une liste par ligne à afficher"""	
		#On ouvre le fichier
		with open(self.fichier, "r") as fichier:
			structure_niveau = []
			#On parcourt les lignes du fichier
			for ligne in fichier:
				ligne_niveau = []
				#On parcourt les sprites (lettres) contenus dans le fichier
				for sprite in ligne:
					#On ignore les "\n" de fin de ligne
					if sprite != '\n':
						#On ajoute le sprite à la liste de la ligne
						ligne_niveau.append(sprite)
				#On ajoute la ligne à la liste du niveau
				structure_niveau.append(ligne_niveau)
			#On sauvegarde cette structure
			self.structure = structure_niveau
	
	
	def afficher(self, fenetre):
                """Méthode permettant d'afficher le niveau en fonction 
		de la liste de structure renvoyée par generer()"""
				
		#On parcourt la liste du niveau
                num_ligne = 0
                for ligne in self.structure:
                    #On parcourt les listes de lignes
                    num_case = 0
                    for sprite in ligne:
                        #On calcul la position réelle en pixels
                        x = num_case * taille_sprite
                        y = num_ligne * taille_sprite
                        if sprite == 'a':
                            fenetre.blit(arbre, (x,y))
                        if sprite == 'p':
                            fenetre.blit(puit, (x,y))
                        if sprite == 'h':
                            fenetre.blit(herbe, (x,y))
                        if sprite == 'c':
                            fenetre.blit(caisse, (x,y))
                        if sprite == 'r':
                            fenetre.blit(route, (x,y))
                        num_case += 1
                    num_ligne +=1
class Perso:

        def __init__(self, bas, gauche, droite, haut, niveau):
        #Sprites du personnage
                self.droite = perso_droite1
                self.gauche = perso_gauche1
                self.haut = perso_haut1
                self.bas = perso_bas1
                #Position du personnage en cases et en pixels
                self.case_x = 1
                self.case_y = 6
                self.x = 68
                self.y = 204        #Direction par défaut
                self.direction = self.droite
                #Niveau dans lequel le personnage se trouve
                self.niveau = niveau

        def deplacer(self, direction):
                '''Méthode permettant de déplacer le personnage'''
                #Déplacement vers la droite
                if direction == 'droite':
                    #Pour ne pas dépasser l'écran
                    if self.case_x < (nombre_sprite_cote - 1):
                        #On vérifie que la case de déstination n'est pas un mur
                        if self.niveau.structure[self.case_y][self.case_x+1] != 'a':
                            #Déplacement d'une case
                            self.case_x += 1
                            #Calcul de la position "réelle" en pixel
                            self.x = self.case_x * taille_sprite
                        #Image dans la bonne direction
                        self.direction = self.droite

                #Déplacement vers la gauche
                if direction == 'gauche':
                    if self.case_x < (nombre_sprite_cote +1):
                        if self.niveau.structure[self.case_y][self.case_x-1] != 'a':
                            self.case_x -= 1
                            self.x = self.case_x * taille_sprite
                        self.direction = self.gauche

                #Déplacement vers le haut
                if direction == 'haut':
                    if self.case_y > 0:
                        if self.niveau.structure[self.case_y-1][self.case_x] != 'a':
                            self.case_y -= 1
                            self.y = self.case_y * taille_sprite
                    self.direction = self.haut
        
                #Déplacement vers le bas
                if direction == 'bas':
                    if self.case_y < (nombre_sprite_cote - 1):
                        if self.niveau.structure[self.case_y+1][self.case_x] != 'a':
                            self.case_y += 1
                            self.y = self.case_y * taille_sprite
                    self.direction = self.bas
