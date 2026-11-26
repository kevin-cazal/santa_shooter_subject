# Effets visuels

Ce qui donne son allure au jeu. Les étapes Bonus sont facultatives : la suite se débloque sans elles.

## Ciel étoilé
<!-- ws: {type: exercise, id: fx-ciel-etoile} -->

Un fond noir et cinquante étoiles qui défilent : le joueur vole dans la nuit.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **`cls(couleur)`** efface l'écran avec une couleur. 0 est le noir.
>
> Doc TIC-80 (en anglais) : [`cls`](https://github.com/nesbox/TIC-80/wiki/cls)

> 🧰 **La boucle `for`** répète en comptant : `i` prend chaque valeur de 1 à 3.
>
> ```lua
> for i = 1, 3 do
>   print(i)
> end
> --> 1  2  3
> ```
>
> ![for i = 1, 3 : le compteur i passe de 1 à 3, une étoile numérotée par tour, puis la boucle s'arrête. La borne devient un curseur nombre d'étoiles : 10, puis 50 : cinquante tours, cinquante étoiles, trois lignes de code.](img/outil-for.webp)
> <!-- ws:anim {src: img/outil-for.webm, chapters: img/outil-for.vtt} -->
>
> Doc Lua (en anglais) : [`for`](https://www.lua.org/manual/5.3/manual.html#3.3.5)

> 🧰 **Une liste** : `{}` la crée vide, `table.insert` ajoute à la fin, `#liste` compte, `liste[1]` est le premier.
>
> ```lua
> points = {}
> table.insert(points, {x = 10, y = 20})
> table.insert(points, {x = 50, y = 80})
> print(#points, points[2].x)   --> 2  50
> for i = 1, #points do
>   print(points[i].y)          --> 20, puis 80
> end
> ```
>
> ![points = {} : une étagère à cartes, vide, avec une étiquette #points = 0. table.insert pose une carte {x, y} à la fin, trois fois, l'étiquette compte 1, 2, 3. La case x de la carte 2 vaut 50 : un fil la relie à une position sur l'écran. for i = 1, #points : i vaut 1, 2, 3, chaque carte devient une étoile à sa position.](img/outil-liste.webp)
> <!-- ws:anim {src: img/outil-liste.webm, chapters: img/outil-liste.vtt} -->
>
> Doc Lua (en anglais) : [les tables](https://www.lua.org/manual/5.3/manual.html#3.4.9), [`table.insert`](https://www.lua.org/manual/5.3/manual.html#pdf-table.insert)

> 🧰 **`circ(x, y, rayon, couleur)`** dessine un disque. `pix(x, y, couleur)` allume un pixel.
>
> ```lua
> circ(120, 68, 3, 12)   -- un disque blanc de rayon 3, au centre
> ```
>
> Doc TIC-80 (en anglais) : [`circ`](https://github.com/nesbox/TIC-80/wiki/circ), [`pix`](https://github.com/nesbox/TIC-80/wiki/pix)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** fond noir. Une liste de 50 étoiles, position et taille (1 à 5) au hasard, qui défilent de droite à gauche et reviennent à droite.

<!-- illustration: résultat intermédiaire : le jeu sur fond noir, sans étoiles -->

<!-- illustration: GIF : les 50 étoiles défilent, toutes à la même vitesse, le bonnet au milieu -->

**C'est réussi si :** le ciel ne se vide jamais, et les étoiles n'ont pas toutes la même taille.

## Parallaxe
<!-- ws: {type: exercise, id: fx-parallaxe} -->

Une grosse étoile est proche, une petite est loin. Si les proches vont plus vite, l'œil voit de la profondeur.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **Perspective et parallaxe** : un objet proche paraît plus gros, et plus rapide. Par la fenêtre d'un train, les poteaux filent, les montagnes ne bougent pas.
>
> ![Deux ciels côte à côte, les mêmes étoiles. À gauche, toutes à la même vitesse : plat. À droite, un curseur coefficient monte de 0 à 1 : les grosses étoiles, proches, vont plus vite que les petites, on voit de la profondeur. Il redescend : la profondeur disparaît.](img/parallaxe-profondeur.webp)
> <!-- ws:anim {src: img/parallaxe-profondeur.webm, chapters: img/parallaxe-profondeur.vtt} -->
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** là où tu fais avancer les étoiles, la vitesse dépend de la taille.

<!-- illustration: GIF : le ciel en parallaxe, trois vitesses visibles -->

**C'est réussi si :** des couches d'étoiles glissent à des vitesses différentes.

## Particules
<!-- ws: {type: exercise, id: fx-particules} -->

Poussière, neige, flammes, explosion : un effet de particules. Ici, l'ennemi explose quand il est touché.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **Les trois ingrédients** : un émetteur (où elles naissent), une physique (comment elles bougent), une longévité (quand elles disparaissent).
>
> ![Le missile touche l'ennemi, qui reste en silhouette. L'émetteur : huit particules naissent à ce point, huit cartes dans la liste. La physique : chacune a sa flèche de vitesse et avance d'autant par image. La longévité : vie baisse de 1 par image, à 0 la particule est retirée et la liste se vide. Un curseur vie à 50 : les mêmes particules durent plus longtemps et vont plus loin.](img/particules-trois-ingredients.webp)
> <!-- ws:anim {src: img/particules-trois-ingredients.webm, chapters: img/particules-trois-ingredients.vtt} -->

> 🧰 **`table.remove(liste, i)`** retire l'élément `i`. Pour retirer en parcourant, parcours à l'envers : `for i = #liste, 1, -1 do`.
>
> ```lua
> noms = {"a", "b", "c"}
> table.remove(noms, 2)
> print(#noms, noms[2])   --> 2  c
> ```
>
> Doc Lua (en anglais) : [`table.remove`](https://www.lua.org/manual/5.3/manual.html#pdf-table.remove)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** une liste de particules. À chaque collision, plusieurs naissent au point de contact, chacune avec sa vitesse et sa vie.

<!-- illustration: GIF : le missile touche l'ennemi, huit particules jaillissent et s'éteignent -->

**C'est réussi si :** l'explosion part du contact, et il ne reste rien une seconde plus tard.

## Bonus SFX
<!-- ws: {type: exercise, id: fx-bonus-sfx, optional: true} -->

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **`sfx(id)`** joue le son `id`, composé dans l'onglet SFX du studio.
>
> Doc TIC-80 (en anglais) : [`sfx`](https://github.com/nesbox/TIC-80/wiki/sfx), [l'éditeur de sons](https://github.com/nesbox/TIC-80/wiki/SFX-Editor)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** un son au départ du missile, un autre dans les deux collisions.

**C'est réussi si :** chaque tir fait un bruit, chaque contact un autre.

## Bonus Music
<!-- ws: {type: exercise, id: fx-bonus-music, optional: true} -->

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **`music(piste)`** lance une piste en boucle. Dans `TIC()`, elle redémarrerait à chaque image : appelle-la une seule fois, en dehors.
>
> Doc TIC-80 (en anglais) : [`music`](https://github.com/nesbox/TIC-80/wiki/music), [l'éditeur de musique](https://github.com/nesbox/TIC-80/wiki/Music-Editor)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** une boucle courte sur la piste 0, lancée au démarrage.

**C'est réussi si :** la musique joue sans à-coups pendant la partie.

## Bonus Vitesse du vaisseau
<!-- ws: {type: exercise, id: fx-bonus-vitesse, optional: true} -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** les étoiles accélèrent quand le joueur avance, ralentissent quand il recule, sans jamais s'arrêter.

**C'est réussi si :** on sent l'accélération rien qu'en regardant le ciel.

## Bonus Sol
<!-- ws: {type: exercise, id: fx-bonus-sol, optional: true} -->

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **`map(x, y, w, h, sx, sy)`** dessine la carte de tuiles peinte dans l'onglet Map. `sx` la décale sur l'écran.
>
> Doc TIC-80 (en anglais) : [`map`](https://github.com/nesbox/TIC-80/wiki/map), [l'éditeur de carte](https://github.com/nesbox/TIC-80/wiki/Map-Editor)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** une bande de sol dans la carte, qui défile toute seule en bas de l'écran.

**C'est réussi si :** le sol défile sans trou ni saut.

## Fin de la partie 2

Ton jeu a maintenant une allure à lui.

Dans la partie suivante, tu vas ranger ton code avant qu'il ne devienne trop long.
