# -*- coding: utf-8 -*-
import sys
import os
import math
import time
import numpy as np
from math import sqrt

import Background

sens_fleche = ""

#le module animat gere le type abstrait de donnee animat
#un animat est un objet qui se deplace dans le terminal 

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Création personnage ou monstre aux coordonnées x,y
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def create(x, y, type_objet, arme="", last_move_x='d'):
    
    #creation animat
    animat               	= dict()
    animat["x"]          	= x
    animat["y"]          	= y

    # derniere direction de deplacement enregistree 
    # 'd' pour droite
    # 'q' pour gauche
    animat["last_move_x"]   = last_move_x

    # type_objet = "personnage" , "monstre" ou "fleche"
    animat["type_objet"] = type_objet

    # point de vie de l'animat
    animat["vie"]        = 2 #valeur par default

    # "weapon    = " " , "epee"    ou "arc"
    animat["weapon"]     = arme

    # deplacement naturel
    # Au debut du jeu, les objets ont tous un déplacement naturel identique : ils tombent
    # Pour faire tomber un objet, on incremente de 1, la coordonnée y
    animat["deplacement_naturel_x"] = 0
    animat["deplacement_naturel_y"] = 1

    animat["direction"]  = '' 
    # Propriétés non spécifique aux personnages mais à la taille de l'écran
    # pour definir la zone de déplacement autorisée
    [max_y, max_x]      = Background.get_terminal_size()
    animat["xMax"]      = max_x 
    animat["yMax"]      = max_y 
    animat["xMin"]      = 1
    animat["yMin"]      = 1

    return animat

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Pour afficher le personnage ou le montre
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def show(a): 
    global sens_fleche
    check_coordinates(a)

    xD       = int(a["x"]+1)
    # Position la plus a gauche
    xG       = int(a["x"]-1)
    # Position la plus a droite
    x        = int(a["x"]) 


    y        = int(a["y"]) 
    y2       = int(a["y"]-1)

    # Valeurs par default
    forme    = ""
    abscisse = x
    x1       = xG
    x2       = x
    oeil1    = oeil2 = "°"
    yeux1    = yeux2 = "<"

    # Actualisation de la forme du personnage
    if a["direction"] == "d":
        forme    = "}"
        abscisse = xD
        x1       = xG
        x2       = x
    elif a["direction"] == "q":
        forme    = "{" 
        abscisse = xG 
        x1       = x
        x2       = xD


    # Couleur différente si personnage , fleche ou monstre
    if a["type_objet"] == "personnage":
        couleurB = "yellow"
        couleurF = "black"
        oeil1 = oeil2 = "^"
    elif a["type_objet"] == "monstre":
        couleurB = "dark_cyan"
        couleurF = "black"  
        oeil1    = "°"
        oeil2    = "°"
    elif a["type_objet"] == "fleche":
        couleurB = "red"
        couleurF = "white"
#    elif a["type_objet"] == "boss":
#        couleurB = "black"
#        couleurF = "white"
#        yeux1    = ">" 
#        yeux2    = "<"   
#        oeil1 = oeil2 = " "


    code1 = Background.return_code_for_console(oeil1, 		str(x1),  str(y),  			foreground=couleurF, background=couleurB)
    code2 = Background.return_code_for_console(oeil2, 		str(x2),  str(y),  			foreground=couleurF, background=couleurB)
    code3 = Background.return_code_for_console(forme, 		str(abscisse),     str(y),  foreground=couleurF, background=couleurB)
    code4 = Background.return_code_for_console(sens_fleche, str(xD),   	str(y),  		foreground=couleurF, background=couleurB)
    code5 = Background.return_code_for_console(yeux1, 		str(xG),  	str(y2),  		foreground=couleurF, background=couleurB)
    code6 = Background.return_code_for_console(yeux2, 		str(x),   	str(y2),  		foreground=couleurF, background=couleurB)

    # Au premier niveau,   les monstres n'ont pas d'arme
    # Au second niveau,    les monstres ont des épées
    # Au troisième niveau, les monstres ont des arcs
    if a["type_objet"] == "personnage" or a["type_objet"] == "monstre" :
        if a["weapon"] == "arc":
            print(code1)
            print(code2)
            print(code3)
        else :
            print(code1)
            print(code2)

    elif a["type_objet"] == "fleche":
        print(code4)

#    elif a["type_objet"] == "boss":
#        print(code1)
#        print(code2)
#        print(code5)
#        print(code6)

    # On definit ici la liste des positions du background à restorer prochainement
    # Il s'agit des coordonnées occupées par le personnage ou le monstre
    # Le tableau contient les couples de positions de la manière suivante
    # [x1,y1, x2,y2, x3,y3, ...]
    list_pos_to_restore = [x,y, xG,y, xD,y]

    return list_pos_to_restore


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Pour tester une éventuelle collision de l'objet avec les plateformes
# l'objet peut être un personnage ou un monstre
# test_collision est appelée par les fonctions 
#    - move 
#    - ou par la fonction change_direction
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def test_collision(a, debug=False):
    plateformes           = Background.get_plateforme()
    collision             = False
    collision_Verticale   = False

    for p in plateformes:

        if a["x"] == p[0] and ((a["y"]+1) == p[1]):
            collision = True

            if debug == True:
                print('> collision %d %d  %d %d' % ( a["x"] , a["y"], p[0], p[1] ) )

            break
        else:
            collision = False

#        if a["x"] == p[0] and a["y"] == p[1]:
#            collision_Verticale = True
#        else:
#            collision_Verticale = False

    return collision



# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Check x coordinates 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def check_x_coordinate(a):

    limits_reached = False

    if a["x"] >= a["xMax"]:
        a["x"]         = a["xMax"]
        limits_reached = True

    if a["x"] < a["xMin"]:
        a["x"]         = a["xMin"]
        limits_reached = True

    return(limits_reached)
        
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Check y coordinates 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def check_y_coordinate(a):

    limits_reached = False

    if a["y"] >= a["yMax"]-1:
        a["y"]         = a["yMax"]-1
        limits_reached = True

    if a["y"] <= a["yMin"]:
        a["y"]         = a["yMin"]
        limits_reached = True

    return(limits_reached)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Check coordinates (Ne pas dépasser les limites  de l'écran)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def check_coordinates(a):
    limits_reached_x = check_x_coordinate(a)
    limits_reached_y = check_y_coordinate(a)


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Changement de niveau lorsque l'on atteint l'extrémité de l'écran
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def change_level(a, level, monstres):

    level_has_changed   = False

    dx                  = a["x"] - a["xMax"]
    dx                  = dx*dx
    dy                  = a["y"] - a["yMax"] +2
#    dy                  = a["y"] - 1
    dy                  = dy*dy
    dist                = math.sqrt(dx+dy)

    # L'utilisateur doit tuer tous les monstres avant de pouvoir passer au niveau supérieur.
    if monstres == []:

        if dist <= 1:
            a["x"] = 2
            a["y"] = 5

            level += 1
            level_has_changed = True

            if level != 4:
                print level

                Background.change_background(level)        
            
                # Display level and erase after 2 secondes
                text_level          = 'level%d' % level
                list_pos_to_restore = Background.display_text(text_level,a["xMax"]/2-8*3, a["yMax"]/2-8)
                time.sleep(2)
                Background.partial_restore_background(list_pos_to_restore)


    return [level, level_has_changed]


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Mouvement naturel du personnage
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def move_personnage(a, level, monstres, debug=False):

    has_moved                        = False
    level_has_changed                = False

    # Test collision avec les plateformes
    collision   = test_collision(a, debug)

    # Si pas de collision, l'objet tombe
    if collision == False:
        a["y"]         = a["y"] + a["deplacement_naturel_y"]
        limits_reached = check_y_coordinate(a)
        has_moved      = True 

    # Si l'objet est un personnage, on vérifie ses coordonnées pour vérifier
    # si il ne doit pas y avoir un changement de niveau
    check_coordinates(a)
    [level, level_has_changed] = change_level(a, level, monstres)
    

    return [has_moved, level, level_has_changed]



# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Inverse le Mouvement naturel des monstres
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def inverser_direction_x(a):
    a["deplacement_naturel_x"] = -a["deplacement_naturel_x"]  

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Mouvement naturel des monstres
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def move_monstre(a, debug=False):


    has_moved      = False

    # Test collision avec les plateformes
    collision      = test_collision(a, debug)

    limits_y       = check_y_coordinate(a)

    if (collision == False) and (limits_y == False):

        # Si pas de collision, et que deplacement_naturel_y == 0
        # On est en extrémité de plateforme, on
        # change de direction
        inverser_direction_x(a)         

    else:
        # collision == True:
        # Désormais le monstre ne tombera plus et restera sur la plateforme
        if a["deplacement_naturel_y"] != 0:
           a["deplacement_naturel_y"] = 0
           a["deplacement_naturel_x"] = 1


    # Deplacement suivant x si necessaire
    if a["deplacement_naturel_x"] != 0:
        a["x"]      += a["deplacement_naturel_x"]

        # Test limit x
        limits_x = check_x_coordinate(a)
        if limits_x == True:
            inverser_direction_x(a)

        has_moved    = True 

    # Deplacement suivant y si necessaire
    if a["deplacement_naturel_y"] != 0:
        a["y"]      += a["deplacement_naturel_y"]

        # Test limit y
        limits_y = check_y_coordinate(a)
        if limits_y == True:
            a["deplacement_naturel_x"] = 1

        has_moved    = True 


    return has_moved

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gestion du Mouvement des fleches
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def move_fleche(a):
    global sens_fleche

    delete_fleche = False
    max_y , max_x = Background.get_terminal_size()
    has_moved     = False


    if a["last_move_x"] == 'd':
    	# Deplacement de la Fleche vers la Droite
        a["x"]     += 2
        has_moved   = True
        sens_fleche = ">"
    elif a["last_move_x"] == 'q':
    	# Deplacement de la fleche vers Gauche
        a["x"]     -= 2
        has_moved   = True        
        sens_fleche = "<"

    if a["x"] >= max_x or a["x"] <= 1:
        delete_fleche = True

    return [has_moved, delete_fleche]

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Test de collision entre les fleches et les monstres
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def collision_fleche_monstre(f, m):
    # f: animat fleche
    # m: animat monstre
    touche = False
    if abs(f["x"]-m["x"])<=2 and f["y"] == m["y"]:
        touche = True

    return touche 

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Test de collision entre le personnage et les monstres
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def collision_personnage_monstre(p, m):
    # p: animat personnage
    # m: animat monstre
    choque = False
    if abs(p["x"]-m["x"])<=2 and p["y"] == m["y"]:
        choque = True

    return choque 

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gestion du Mouvement du personnage en fonction des touches appuyees
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def changeDirection(a, level, key, monstres):

    max_y, max_x        = Background.get_terminal_size()
    has_moved           = False
    level_has_changed   = False
    list_pos_to_restore = []
    collision           = test_collision(a)


    if key == 'd':
        # Touche 'd' pour aller à droite
        a["last_move_x"]  	= 'd'
        a["x"]      		= a["x"] + 1
        has_moved   		= True

    elif key == 'q':
        # Touche 'q' pour aller a gauche
        a["last_move_x"]  	= 'q'
        a["x"]      		= a["x"] - 1
        has_moved   		= True

    elif key == ' ':
        # Barre d'espace pour sauter
        saut = 0

        if collision == True or a["y"] == (max_y-1):
#        if True:
            while saut < 4:

            	# Saut en hauteur
                a["y"] = a["y"] - 1

                if a["last_move_x"] == 'd':
                	# Deplacement simultane vers la droite si 
                	# precedent deplacement demande vers la droite 
                    a["x"] = a["x"] + 1
                elif a["last_move_x"] == 'q':
                	# Deplacement simultanee vers la gauche
                	# si precedent deplacement demande vers la gauche
                    a["x"] = a["x"] - 1     
                has_moved  = True
                saut += 1


    if has_moved:    
        check_coordinates(a)
        [level, level_has_changed] = change_level(a, level, monstres)

    return [has_moved, level, level_has_changed]

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gestion des points de vie
# p: personnage
# f: fleche
# m: monstre
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gestion des points de vie du personnage
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def player_life(p,monstres):

    game_over       = False
    delete_fleche   = False
    ind_monstre     = 0

    # On regarde d'abord si il n'y a pas une collision personnage / monstre
    for m in monstres:
        if collision_personnage_monstre(p,m):
            p["vie"]        = 0
            game_over       = True

            list_pos_to_restore = Background.display_text("G",p["xMax"]/2-8*3, p["yMax"]/2-8)
            time.sleep(2)
            Background.partial_restore_background(list_pos_to_restore)

            #print("GAME OVER")            
            break
    return game_over

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Gestion des points de vie des monstres
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
def monster_life(f,monstres):

    game_over       = False
    delete_fleche   = False

    if game_over == False:        

        delete_fleche = False
        
        for m in monstres:

            if collision_fleche_monstre(f,m) == True :

                #print('monstre tue')            
                delete_fleche   = True

                # vie des monstres
                m["vie"] -= 1


                if m["vie"] == 0:
                    monstres.remove(m)

                break
    

    return delete_fleche          

