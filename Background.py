# -*- coding: utf-8 -*-
import time
import os
import sys
import select
import tty 
import termios
import numpy as np
import random

list_of_background_codes    = []
plateformes                 = []

max_X                       = 0
max_Y                       = 0

cursor_off                  = '\033[?25l'
cursor_on                   = '\033[?25h'

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Couleurs utilisées pour le backgound
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
back = {
    'black':        '40',
    'dark_red':        '41',
    'dark_green':    '42',
    'dark_yellow':    '43',
    'dark_blue':    '44',
    'dark_pink':    '45',
    'dark_cyan':    '46',
    'dark_gray':    '100',
    'gray':            '47',
    'red':            '101',
    'green':        '102',
    'yellow':        '103',
    'blue':            '104',
    'pink':            '105',
    'cyan':            '106',
    'white':        '107',
    'default':        '49',
    'dark_white':    '47', # also gray , allow "dark" prefix to all colors
    'dark_black':    '40', # identical to black, allow "dark" prefix to all colors
}

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Couleurs utilisées pour le foreground
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
fore = {
    'black':        '30',
    'dark_red':        '31',
    'dark_green':    '32',
    'dark_yellow':    '33',
    'dark_blue':    '34',
    'dark_pink':    '35',
    'dark_cyan':    '36',
    'dark_gray':    '90',
    'gray':            '37',
    'red':            '91',
    'green':        '92',
    'yellow':        '93',
    'blue':            '94',
    'pink':            '95',
    'cyan':            '96',
    'white':        '97',
    'dark_white':    '37', # also gray , allow "dark" prefix to all colors
    'dark_black':    '30', # identical to black, allow "dark" prefix to all colors
}


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Options d'affichage pour un caractère
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
opt = {
    'bold' :             '\033[1m',
    'italic' :           '\033[3m',
    'underlined' :       '\033[4m',
    'blink' :            '\033[5m',
    'none' :             '',
    '' :                 '',
    }




# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Efface 
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def clearC():
    os.system('cls' if os.name=='nt' else 'clear')

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Retourne le nombre de colonnes et de ligne du terminal
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_terminal_size():

    global max_Y, max_X

    ligne, colonne   = os.popen('stty size', 'r').read().split()
    max_Y   = max_y   = int(ligne)
    max_X   = max_x   = int(colonne)

    return( [max_y, max_x] )

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# retourne le code sous la forme d'une chaine pour controler l'affichage d'un caractère
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def return_code_for_console( text, x, y,  foreground='white', background='default', option='none'): 

    if x<0 or y<0 :
        code = ''
    else:
        code = cursor_off + opt[option] + '\033[' + str(y) + ';' + str(x) + 'H\033[' + fore[foreground] + ';' +back[background] + 'm' + text + '\033[0m'

    return( code )

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Retourne les couleurs à utiliser pour ce caractère
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_colors_for_this_car(car):

    is_plateforme = False

    if car == 's' :
        background_color    = font_color    = 'dark_pink'   
    elif car == 'o':
        background_color    = font_color    = 'pink'        
    elif car == '/':
        background_color    = font_color    = 'dark_yellow' 
    elif car == 'h':
        background_color    = font_color    = 'dark_black'  
    elif car == ':':
        background_color    = font_color    = 'yellow'      
    elif car == '+':
        background_color    = font_color    = 'dark_pink'   
    elif car == '`':
        background_color    = font_color    = 'white'       
    elif car == 'y':
        background_color    = font_color    = 'dark_gray'  
    elif car == '-':
        background_color    = font_color    = 'dark_gray'   
    elif car == '.':
        background_color    = font_color    = 'dark_white'  
    elif car == 'A':
        background_color    = font_color    = 'dark_red'   
    elif car == 'B':
        background_color    = font_color    = 'dark_white'   
    elif car == 'M':
        background_color    = font_color    = 'dark_black'  
    elif car == 'b':
        background_color    = font_color    = 'white'       
    elif car == 'g':
        background_color    = font_color    = 'dark_white'  
    elif car == 'r':
        background_color    = font_color    = 'dark_red'    
    elif car == 'q':
        background_color    = font_color    = 'red'         
    elif car == 'a':
        background_color    = font_color    = 'black'       
    elif car == 'X':
        background_color    = 'dark_red'    
        font_color          = 'red'
        is_plateforme       = True
    else:
        background_color    = font_color    = 'blue'        

    return( [background_color, font_color, is_plateforme] )

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Prepare l'affichage du fond d'écran
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def init_background(filename='galerie.txt', debug = False):
    
    global list_of_background_codes
    
    # Reset list of background code
    list_of_background_codes =  []

    # Récupération de la dimension du terminal
    max_y, max_x = get_terminal_size()
    if debug == True:
        print('> Terminal size max_y=%d max_x=%d' % (max_y, max_x) )

    # Ouverture du fichier contenant le background
    f   = open(filename, 'r')
    y   = 1
    x   = 1

    while True:

        line = f.readline()
        x = 1

        if line == '':
            # either end of file or just a blank line.....
            # we'll assume EOF, because we don't have a choice with the while loop!
            break
        else:

            # For all char in the line
            for car in line:

                background, color, is_plateforme = get_colors_for_this_car(car)

                # Add theses coordinates to the plateforme
                if is_plateforme:
                    plateformes.append([x,y])

                code = return_code_for_console( car, x, y, foreground=color, background=background)
                list_of_background_codes.append(code)

                # Next row    
                x += 1 

                if x > max_x:
                    if debug == True:
                        print('> Stop to read the line')
                    break   

        # Next line        
        y += 1

        # ca fout la grouille si on met > strict
        if y >= max_y:
            if debug == True:
                print('> Stop to read the file')    
            break
        
    # Mode debug
    if debug == True:
        print('> Last coordinates                  : y, x = %d %d' % (y, x) )
        print('> Number of elements in plateformes : %d' % len(plateformes) )

    # Close the file containing the background
    f.close()


# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Restore background
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def display_background():

    fast_display = False
    if fast_display == True:

        for code in list_of_background_codes:
            print(code)

    else:
        time_to_display    = 5
        nb_codes           = len(list_of_background_codes)
        sleep_duration     = time_to_display / nb_codes
        remaining_indices  = np.arange(0,nb_codes)

        for i in range(nb_codes):

            indice_to_display = random.randint(0, len(remaining_indices)-1 )

            print( list_of_background_codes[remaining_indices[indice_to_display]] )

            remaining_indices = np.delete(remaining_indices, indice_to_display)
            time.sleep(sleep_duration)

# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Restore background
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def partial_restore_background(list_pos_to_restore):

    
    list_pos    = np.array(list_pos_to_restore)
    len_tab     = len(list_pos)

    if len_tab >=2:

        list_pos = list_pos.reshape(len_tab/2,2)

        for pos in list_pos:
            
            x       = pos[0]  # x est compris entre 1 et max_X
            y       = pos[1]  # y est compris entre 1 et max_Y

            # Troouver indice dans un tableau à une dimension de taille (max_Y*max_X)
            # Les indices dans ce tableau vont de 0 à (max_Y*max_X-1)
            # pour x=1, y=1, on doit trouver 0
            # pour x=1, y=2, on doit trouver max_X
            indice  = int(x-1 + (y-1)*max_X)

            if indice < len(list_of_background_codes):
                code    = list_of_background_codes[indice]
                print(code)

        #print('Indice %d  %s' % (indice, code)) 
       
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Retourne les coordonnées des plateformes
# Les plateformes sont définies par des X dans l'image
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_plateforme():
    return plateformes

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Change de background
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def change_background(level):
    
    global plateformes

    #print('Change background')
    plateformes                 = []
    if level == 0:
        filename_fond = "galerie.txt"
    elif level == 1 :
        filename_fond = "montagne.txt"
    elif level == 2:
        filename_fond = "arbre.txt"
    elif level == 3 :
        filename_fond = "volcan.txt"
    if level != 4:
        init_background( filename_fond )
        display_background()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Pour afficher du texte aux coordonnes x_start_text, y_start_text
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def display_text(text, x_start_text, y_start_text):

    list_pos       = []
    y_start_letter = int(y_start_text)
    x_start_letter = int(x_start_text)

    for c in text:
        filename = 'lettres/%s.txt' % c
    
        # Ouverture du fichier contenant le background
        try:
            with open(filename, 'r') as f:
                y   = y_start_letter
                x   = x_start_letter

                while True:

                    line = f.readline()
                    x    = x_start_letter

                    if line == '':
                        break
                    else:
                        # For all char in the line
                        for car in line:
                            if car != ' ':
                                background, color, r = get_colors_for_this_car(car)
                                code = return_code_for_console( car, x, y, foreground=color, background=background)
                                print(code) 
                                list_pos = np.append(list_pos, [int(x),int(y)] )
                            x += 1  # Next row  
                    y += 1 # Next line 

                # Close the file containing the background
                f.close()
        except:
            print('Erreur : Pas de fichier pour représenter le caractère %s' % filename)
        x_start_letter += 8

    return list_pos
        
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Test affichage background
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':  

    debug = True
    if debug:
        init_background(debug = debug)  
        display_background()


    list_pos = display_text('levelI', 10, 10)
    time.sleep(2)
    partial_restore_background(list_pos)