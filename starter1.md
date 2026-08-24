# Le jeu de base

Dans cette partie, tu construis le jeu : un joueur qui bouge, qui tire, des ennemis qui arrivent
et un score qui monte.

# Intro

- TIC-80
- Environment
- init -> loop: update, draw

# Mouvement joueur

## Sprite
<!-- ws: {type: exercise, id: mouvement-joueur-sprite} -->

- TIC-80 Sprite Editor: Santa Hat
- Position initiale
- Nommer les variables player_x, player_y (comme player_speed)
- Code: Draw Sprite

## Input
<!-- ws: {type: exercise, id: mouvement-joueur-input} -->

- if btn(x): update position
- limites bordures écran

# Bullet

## Sprite
<!-- ws: {type: exercise, id: bullet-sprite} -->

- TIC-80 Sprite Editor: Bullet
- Position initiale: out of bound

## Input
<!-- ws: {type: exercise, id: bullet-input} -->

- if btn(x): shoot at player coordinate
- déplacement du bullet
- out of bound reset

# Enemy

## Sprite
<!-- ws: {type: exercise, id: enemy-sprite} -->

- TIC-80 Sprite Editor: Enemy
- Position initiale: X = out of bound (droite), Y = random

## Mouvement
<!-- ws: {type: exercise, id: enemy-mouvement} -->

- Vers la gauche
- Out of bound (gauche) retour à droite, Y = random

# Collision

- AABB

## Enemy VS Player
<!-- ws: {type: exercise, id: collision-enemy-player} -->

- Reset position player
- Reset position enemy

## Enemy VS Bullet
<!-- ws: {type: exercise, id: collision-enemy-bullet} -->

- Reset position bullet
- Reset position enemy
- Increment score
- Display score

## Fonction check_collision
<!-- ws: {type: exercise, id: collision-check-collision} -->

- Une fois les deux tests de collision ecrits, remarquer qu'ils font le meme calcul avec des variables differentes
- Deplacer ce calcul dans une fonction check_collision, c'est beaucoup plus propre et fortement recommande des qu'un meme code est ecrit deux fois

## Fin de la partie 1

Ton jeu est jouable : le joueur bouge, il tire, les ennemis arrivent et le score monte.

Dans la partie suivante, tu vas t'occuper de ce que le joueur voit.
