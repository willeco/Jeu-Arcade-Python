#______________________________________________________________________________________________________________________________________________________________________________________________________________
#
#                                                                PROJET INFORMATIQUE S2-A_02
#                                                                   
#                                                                 ####### BLOB JUMP #######
#
#                                                              WILLIAM LE CORRE   DAMIEN CRENN
#
#                                                                 vendredi 22 decembre 2017
#______________________________________________________________________________________________________________________________________________________________________________________________________________
#
#modules externes
import sys
import os
import time
import select
import tty 
import termios
import random
import numpy as np
#mes modules
import Background 
import Animat

#interaction clavier
old_settings = termios.tcgetattr(sys.stdin)

#donnee du jeu
personnage           = None
boss                 = None
monstres             = list()
fleches              = list()

background           = None 
timeStep             = None
level                = 0
ending               = False
max_x                = 0
max_y                = 0

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Creation des monstres
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def creation_monstres(nb_monstres = 15):
    global monstres, max_x, max_y

    for m in range (nb_monstres):
        monstres.append(Animat.create(x=random.randint(1,max_x), y=random.randint(3,max_y), type_objet="monstre"))

def supprimer_monstres():
    global monstres
    monstres = []

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Initialisation du jeu
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def init(debug = False):
    global personnage, background, timeStep, level, monstres, boss, max_x, max_y

    max_y, max_x = Background.get_terminal_size()
    #print max_y
    #print max_x
    #initialisation de la partie

    # Creation des elements du jeu (personnage et monstres)

    personnage   = Animat.create(x=2,  y=5, type_objet="personnage")

#    boss         = Animat.create(x=random.randint(5,max_x),  y=5, type_objet="boss")


    creation_monstres(nb_monstres = 20)

    # Creation du fond 
    Background.init_background('galerie.txt')
    Background.display_background()

    # interaction clavier
    tty.setcbreak(sys.stdin.fileno())


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Interaction avec le clavier
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def interact():
    global personnage, background, level, fleches, monstres 
    #gestion des evenement clavier
    c                   = ""
    has_moved           = False
    level_has_changed   = False

    # si une touche est appuyee
    if isData():

        # recuperation touche appuye
        c = sys.stdin.read(1)
#        print ord(c)
        
        if c == '\x1b':         
            # x1b is ESC
            quitGame()
        
        elif c == 'k' :
            # Touche k appuye : creation fleche avec pour coordonnees celle
            # du personnage et une direction de deplacement en x egale a celle
            # du personnage
            personnage["weapon"]    = "arc"
            fleches.append(Animat.create(x           = personnage["x"], 
                                         y           = personnage["y"], 
                                         type_objet  = "fleche", 
                                         last_move_x = personnage["last_move_x"]))

        elif c == 'q' or 'd' or ' ':
            # deplacement a droite ou a gauche, ou saut
            personnage["weapon"]    = "arc"
            personnage["direction"] = c  
            # Permet de changer de direction du personnage
            [has_moved, level, level_has_changed] = Animat.changeDirection(personnage, level, c, monstres)

    return has_moved, level_has_changed

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Recuperation evenement clavier
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Boucle sans fin
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def run(debug = False):    
    global personnage, level, monstres

    list_pos_to_restore      = []

    # Boucle de simulation 
    while 1:

        #effacer la console
        if False:
            sys.stdout.write("\033[1;1H")
            sys.stdout.write("\033[2J")

        # Interaction avec l'objet
        [has_movedA,        level_has_changed1]          = interact()
        [has_movedB, level, level_has_changed2]          = Animat.move_personnage(personnage, level, monstres, debug)

        if level_has_changed1 == True or level_has_changed2 == True:
            supprimer_monstres()
            creation_monstres(nb_monstres = (level+1)*10)        
#        has_moved                                      = Animat.move_monstre(boss,level)   

        # affichage des differents elements
        # On garde en memoire les positions pour une restauration
        # ulterieure du fond d'ecran

        # Mieux vaut rafraichir la position du personnage tout le temps
        # Il etait souvent efface par la collision avec les montres
        Background.partial_restore_background(list_pos_to_restore)

        list_pos_to_restore                              = Animat.show(personnage)

#        if has_moved:
#            list_pos_to_restore.extend( Animat.show(boss) )

        for monstre in monstres:
            has_moved = Animat.move_monstre(monstre)
            if has_moved:
                list_pos_to_restore.extend( Animat.show(monstre) )    
                
        # Deplacement des fleches
        ind_fleche              = 0
        list_arrow_to_remove    = []
        for fleche in fleches:
            [has_moved, delete_fleche] = Animat.move_fleche(fleche) 

            if has_moved:
                list_pos_to_restore.extend ( Animat.show(fleche) )

            if delete_fleche == False:
                # actualisation des points de vie
                delete_fleche = Animat.monster_life(fleche, monstres) 


            if delete_fleche == True:
                list_arrow_to_remove.append(ind_fleche)

            ind_fleche += 1


        # On supprime les fleches qui doivent l'etre    
        for ind_arrow in list_arrow_to_remove:
            #print('Suppression fleche %d' % ind_arrow)
            fleches.pop(ind_arrow)

        # On test la collision entre le personnage et les monstres
        game_over = Animat.player_life(personnage, monstres)

        # Arret du jeu
        if game_over == True  or level == 4:
            quitGame()

        # restoration couleur 
        sys.stdout.write("\033[37m")
        sys.stdout.write("\033[40m")

        #deplacement curseur
        sys.stdout.write("\033[0;0H\n")

        time.sleep(0.0365)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# fin
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def quitGame():    
    
    #restoration parametres terminal
    global old_settings
    sys.stdout.write("\033[1;1H")
    sys.stdout.write("\033[2J")
    #couleur white
    sys.stdout.write("\033[37m")
    sys.stdout.write("\033[40m")
    
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
    sys.exit()

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
debug = False
init(debug)
#try:
run(debug)

#finally:
quitGame()
