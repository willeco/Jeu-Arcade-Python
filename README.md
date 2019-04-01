# Jeu-Arcade-Python
Jeu d'Arcade en Python dans une console

## Règles du jeu
Le but du jeu est de tuer tous les monstres présents dans chaque niveau pour
pouvoir passer au suivant, puis de se rendre au point de "téléportation"
(point qui se trouve en bas à droite du terminal).
Une fois ces deux conditions respectées, l'utilisateur passe au niveau suivant.
Le jeu prend fin si le personnage meurt ou s'il arrive à la fin du niveau 3.

## Commandes manuelles
Effets | Touches
------------ | -------------
Déplacement latéral droit | d
Déplacement latéral gauche | q
Saut | touche espace
Tir de fleches | k
Quitter le jeu | 'echap' ou flêches directionnelles

## Principe de gestion des vies
* Vie personnage : Si le personnage entre en collision avec un monstre le jeu
prend fin.
* Vie monstre : Un monstre meurt au bout de 2 coups.
* Vie flèche : Si une flèche heurte un monstre ou les cotés du terminal, elle
disparait.

