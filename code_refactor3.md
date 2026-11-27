# Refactor du code

Beaucoup de variables globales : `x`, `y`, `mx`, `ex`... Plus tu ajoutes d'armes et d'ennemis, plus c'est dur à suivre. Ici, chaque objet du jeu rassemble ses valeurs et ses fonctions dans une table. Le jeu ne change pas : il se range.

## Notion d'objet en Lua
<!-- ws: {type: prose} -->

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **Une table avec des cases nommées** : `player.x` se lit « la case `x` de la boîte `player` ».
>
> ![Six variables éparpillées : x, y, player_speed, ex, ey, vex. Les trois du joueur se rangent dans une boîte player, avec des cases x, y, speed. player.x se lit : la case x de la boîte player. Puis les trois de l'ennemi forment une boîte enemy, avec les mêmes noms de cases.](img/refactor-tables.webp)
> <!-- ws:anim {src: img/refactor-tables.webm, chapters: img/refactor-tables.vtt} -->

> 🧰 **Une fonction dans une table, et `self`** : écrite avec `:`, la fonction reçoit la table sous le nom `self`.
>
> ```lua
> chat = {nom = "Félix", faim = 3}
> function chat:manger()
>   self.faim = self.faim - 1
> end
> chat:manger()
> print(chat.faim)   --> 2
> ```
>
> ![chat est une table avec une case nom et une jauge faim à 3. function chat:manger() est une fonction de cette table. chat:manger() : la carte entre dans la fonction sous le nom self, sa jauge baisse d'un cran, et elle ressort à 2. Puis la carte player entre dans player:update(), dont le corps est le commentaire bouger, et ressort déplacée.](img/outil-self.webp)
> <!-- ws:anim {src: img/outil-self.webm, chapters: img/outil-self.vtt} -->
>
> Référence (en anglais) : [Programming in Lua, chapitre 16](https://www.lua.org/pil/16.html). Juste le principe : pas de classes ni d'héritage ici.
<!-- /ws:toolbox -->

## Joueur
<!-- ws: {type: exercise, id: refactor-joueur} -->
<!-- étape de modelage : la forme de la table et des fonctions est donnée volontairement -->

Le premier objet à ranger. Sa forme t'est donnée ; à toi d'y déplacer le code.

```lua
player = {x = 0, y = 68, speed = 1.5}

function player:update()
  -- le mouvement et les limites
end

function player:draw()
  -- l'affichage
end
```

### Mise en application
<!-- ws:doit -->

**Ton objectif :** `TIC()` appelle `player:update()` puis `player:draw()`, et plus rien d'autre pour le joueur.

**C'est réussi si :** le bonnet bouge et s'arrête aux bords exactement comme avant.

## Bullet
<!-- ws: {type: exercise, id: refactor-bullet} -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** une table `bullet` avec `x`, `y`, `speed`, `bullet:update()` pour le vol et le retour au repos, `bullet:draw()`.

**C'est réussi si :** plus de `mx`, `my`, `vmx`, et le tir marche comme avant.

## Enemy
<!-- ws: {type: exercise, id: refactor-enemy} -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** une table `enemy`, `enemy:update()` pour le mouvement et le replacement à droite, `enemy:draw()`.

**C'est réussi si :** plus de `ex`, `ey`, `vex`, `vey`, et l'ennemi traverse comme avant.

## Collision
<!-- ws: {type: exercise, id: refactor-collision} -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** une fonction `check_collisions()` qui regarde `player`, `bullet` et `enemy`, et applique les conséquences : score, retour au départ, particules.

**C'est réussi si :** `TIC()` tient en une dizaine de lignes et se lit comme une liste.

## Étoiles, particules, sol
<!-- ws: {type: exercise, id: refactor-etoiles} -->

Déjà des tables dans une liste : pas de gros changement.

### Mise en application
<!-- ws:doit -->

**Ton objectif :** le code des étoiles et des particules regroupé au même endroit. En option, `update` et `draw` sur chacune.

**C'est réussi si :** tu retrouves chaque élément du jeu en lisant les noms des tables.

## Fin de la partie 3

Ton code est rangé. Chaque objet du jeu a sa table, avec ses valeurs et ses fonctions.

La partie Gameplay ajoute plusieurs ennemis et plusieurs missiles. Avec des tables, une liste d'ennemis s'écrit comme ta liste d'étoiles.
