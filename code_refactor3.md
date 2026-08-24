# Refactor du code

- Le code actuel utilise beaucoup de variables globales (x, y, bullet_x, enemy_x, etc)
- Plus on ajoute de fonctionnalites (armes, vagues d'ennemis, boss), plus c'est difficile a suivre
- Objectif: regrouper les variables et le comportement de chaque objet du jeu dans une seule table

## Notion d'objet en Lua
<!-- ws: {type: prose} -->

- Une table peut contenir des valeurs ET des fonctions
- Une fonction stockee dans une table peut utiliser self pour acceder aux autres valeurs de la table
- Le sucre syntaxique : (deux points) permet d'appeler une fonction sans repeter self a chaque fois
- Reference: https://www.lua.org/pil/16.html (juste le principe de base, pas besoin d'aller plus loin, on ne fait pas de vraies classes ni d'heritage)

## Joueur
<!-- ws: {type: exercise, id: refactor-joueur} -->

- Remplacer x, y, player_speed par une table player = {x=.., y=.., speed=..}
- Deplacer le code de mouvement dans une fonction player:update()
- Deplacer le code d'affichage dans une fonction player:draw()
- Appeler player:update() et player:draw() dans TIC()

## Bullet
<!-- ws: {type: exercise, id: refactor-bullet} -->

- Meme principe: une table bullet = {x=.., y=.., speed=..}
- Fonction bullet:update() pour le deplacement et le reset hors ecran
- Fonction bullet:draw()

## Enemy
<!-- ws: {type: exercise, id: refactor-enemy} -->

- Meme principe: une table enemy = {x=.., y=.., speed=..}
- Fonction enemy:update()
- Fonction enemy:draw()

## Collision
<!-- ws: {type: exercise, id: refactor-collision} -->

- Garder une fonction a part pour les collisions, par exemple check_collisions()
- Cette fonction regarde player, bullet et enemy et applique les consequences (score, reset position, particules)

## Etoiles, particules, sol
<!-- ws: {type: exercise, id: refactor-etoiles} -->

- Ces elements sont deja des tables dans une liste, pas besoin de gros changement
- Optionnel: ajouter des fonctions update/draw sur chaque etoile ou particule

## Fin de la partie 3

Ton code est rangé. Chaque objet du jeu a sa table, avec ses valeurs et ses fonctions.

Dans la partie suivante, tu choisis toi-même les défis que tu veux ajouter au jeu.

## Pourquoi ce refactor avant la partie Gameplay

- La partie Gameplay ajoute plusieurs ennemis et plusieurs balles (double tir, triple tir, vagues, boss)
- Avec des tables, ce sera plus facile de faire une liste de plusieurs ennemis ou balles
- Sans ce refactor, le code deviendrait vite tres long avec des variables comme enemy2_x, enemy3_x, etc
