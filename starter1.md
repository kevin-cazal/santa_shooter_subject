# Le jeu de base

Un joueur qui bouge, qui tire, des ennemis, un score. Les étapes se font dans l'ordre : ses outils, un objectif, l'image à obtenir.

# Intro

1. Clique sur **Ouvrir TIC-80** : la console s'ouvre à côté des instructions.
   <!-- ws:cue runtime -->
2. À gauche le jeu, à droite l'éditeur de code, dessous un terminal Lua pour essayer les exemples.
3. Dans la console : `run` lance le jeu, `studio` ouvre les éditeurs, <kbd>Échap</kbd> revient à la console.

<!-- illustration: la fenêtre TIC-80 à côté du sujet : le jeu, l'éditeur, le terminal Lua ; le bouton Ouvrir TIC-80 et la console encadrés -->

**Un jeu, c'est une boucle.** TIC-80 appelle ta fonction `TIC` 60 fois par seconde.

![La boucle de jeu. La ligne x = 0 s'exécute une fois. Puis TIC tourne : x augmente, cls efface l'écran, spr dessine le joueur à la position x. De plus en plus vite : le joueur avance d'un pixel par image.](img/intro-boucle.webp)
<!-- ws:anim {src: img/intro-boucle.webm, chapters: img/intro-boucle.vtt} -->

# Mouvement joueur

## Sprite
<!-- ws: {type: exercise, id: mouvement-joueur-sprite} -->

Un sprite, c'est un dessin de 8 pixels sur 8. Le tien : le bonnet du Père Noël.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **Le studio** : dans la console, tape `studio`. Choisis la case 0, dessine pixel par pixel.
>
> ![Dans la console de TIC-80, on tape studio puis Entrée : l'éditeur de sprites s'ouvre.](img/sprite-studio.gif)
>
> ![On choisit la case #0, puis on dessine le sprite pixel par pixel : d'abord le blanc, ensuite le rouge.](img/sprite-dessin.gif)

> 🧰 **`spr(id, x, y)`** dessine le sprite `id` à la position `x`, `y`. Toujours après `cls`, qui efface l'écran.
>
> ```lua
> spr(17, 20, 100)   -- le sprite 17, en x = 20 et y = 100
> spr(17, 60, 100)   -- le même, 40 pixels plus à droite
> ```
>
> Doc TIC-80 (en anglais) : [`spr`](https://github.com/nesbox/TIC-80/wiki/spr#parameters), [`cls`](https://github.com/nesbox/TIC-80/wiki/cls#description)

> 🧰 **La transparence** : un 4ᵉ paramètre à `spr`, le numéro de la couleur à rendre invisible. La palette va de 0 (en haut à gauche) à 15.
>
> ```lua
> spr(17, 20, 100, 1)   -- la couleur 1 disparaît
> ```
>
> ![Dans la palette, la couleur encadrée est le noir, la couleur numéro 0. C'est elle qui doit devenir transparente.](img/sprite-palette-transparence.png)
>
> Doc TIC-80 (en anglais) : [`colorkey`](https://github.com/nesbox/TIC-80/wiki/spr#parameters)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** ton bonnet dans le jeu, sans le carré noir autour.

![Le sprite du joueur dans le jeu (agrandi à droite). Les pixels noirs autour du bonnet sont encore visibles.](img/sprite-ecran-sans-transparence.png)

![Le même sprite avec la transparence : il ne reste que le bonnet.](img/sprite-ecran-avec-transparence.png)

**C'est réussi si :** le bonnet est seul sur le fond, comme sur la deuxième image.

## Input
<!-- ws: {type: exercise, id: mouvement-joueur-input} -->

Le bonnet s'affiche. Maintenant, il bouge avec les flèches.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **Une variable** stocke une valeur. Crée-la en haut du code, hors de `function TIC()` : sinon elle repart de zéro 60 fois par seconde.
>
> ```lua
> vies = 3
> print(vies)   --> 3
> ```
>
> ![x = 20 : la boîte x contient 20, et le jeu dessine le bonnet à 20. x = 120 : le bonnet est à 120. La ligne x = 20 écrite dans TIC() remplit la boîte à chaque tour, et le bonnet revient à 20 malgré la flèche. Hors de TIC(), la boîte est remplie une seule fois et le bonnet avance.](img/outil-variable.webp)
> <!-- ws:anim {src: img/outil-variable.webm, chapters: img/outil-variable.vtt} -->
>
> Doc Lua (en anglais) : [les variables](https://www.lua.org/manual/5.3/manual.html#3.2)

> 🧰 **Incrémenter** : Lua calcule la droite du `=`, puis stocke le résultat à gauche.
>
> ```lua
> compteur = 0
> compteur = compteur + 1   --> 1
> compteur = compteur - 1   --> 0
> ```
>
> ![Le bonnet porte son nombre x, sa position : 20. x = x + 1 : x prend 1 de plus, et le bonnet avance d'un pixel sur une règle où chaque pixel se voit. Encore : 22, 23, 24. Puis dans TIC(), 60 fois par seconde : le bonnet file vers la droite.](img/outil-incrementer.webp)
> <!-- ws:anim {src: img/outil-incrementer.webm, chapters: img/outil-incrementer.vtt} -->
>
> Doc Lua (en anglais) : [l'affectation](https://www.lua.org/manual/5.3/manual.html#3.3.3), [`+` et `-`](https://www.lua.org/manual/5.3/manual.html#3.4.1)

> 🧰 **`btn(numéro)`** est vrai tant que la touche est enfoncée.
>
> | Numéro | Touche |
> |---|---|
> | 0 | flèche haut |
> | 1 | flèche bas |
> | 2 | flèche gauche |
> | 3 | flèche droite |
> | 4 | Z |
> | 5 | X |
>
> Doc TIC-80 (en anglais) : [`btn`](https://github.com/nesbox/TIC-80/wiki/btn#parameters)

> 🧰 **`if`** : le bloc s'exécute seulement si la condition est vraie. Chaque `if` se ferme par `end`.
>
> ```lua
> temperature = 35
> if temperature > 30 then
>   print("il fait chaud")
> end
> ```
>
> ![temperature = 35 : 35 > 30 est vrai, Lua entre dans le bloc et print affiche il fait chaud. Avec 20 : faux, Lua saute au end, rien ne s'affiche. Dans le jeu, la condition est un bouton : appuyé, le joueur avance ; relâché, rien.](img/outil-if.webp)
> <!-- ws:anim {src: img/outil-if.webm, chapters: img/outil-if.vtt} -->
>
> Doc Lua (en anglais) : [`if`](https://www.lua.org/manual/5.3/manual.html#3.3.4), [les comparaisons](https://www.lua.org/manual/5.3/manual.html#3.4.4)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** deux variables `x` et `y`, changées par les flèches, utilisées par `spr`.

![Le joueur se déplace avec les flèches du clavier. La manette sous le jeu allume les touches au moment où elles sont appuyées.](img/input-deplacement.gif)

**C'est réussi si :** le bonnet avance tant que la flèche est enfoncée, dans les quatre directions.

## Rester dans les limites de l'écran
<!-- ws: {type: exercise, id: mouvement-joueur-limites} -->

Trop loin, le bonnet sort de l'écran. Il doit s'arrêter contre les bords.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **L'écran** fait 240 pixels sur 136. Le point (0, 0) est en haut à gauche.
>
> ![L'écran de TIC-80. Le point 0 est en haut à gauche. X augmente vers la droite, Y augmente vers le bas. Les pointillés montrent la position X et la position Y du joueur.](img/ecran-axes.png)

> 🧰 **Les quatre bords** : `x` et `y` sont le coin en haut à gauche d'un sprite de 8 pixels.
>
> ![Les quatre bords. À gauche, x vaut 0. En haut, y vaut 0. À droite, avec x = 240 le sprite est déjà sorti : son bord droit est x + 8, il touche le bord quand x + 8 vaut 240. En bas, pareil avec y + 8 et 136.](img/limites-bords.webp)
> <!-- ws:anim {src: img/limites-bords.webm, chapters: img/limites-bords.vtt} -->
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** quatre conditions, une par bord.

![Avant : sans conditions, le joueur sort de l'écran et disparaît.](img/limites-avant.gif)

![Après : avec les conditions, le joueur s'arrête contre les bords de l'écran.](img/limites-apres.gif)

**C'est réussi si :** le bonnet reste entièrement visible, flèche enfoncée ou pas.

# Bullet

## Sprite
<!-- ws: {type: exercise, id: bullet-sprite} -->

Un joueur qui tire, c'est mieux. D'abord, le missile existe.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 Les outils de cette étape : le studio, `spr`, une variable. Tu les as déjà.
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** un missile dessiné dans une autre case, affiché en (10, 10) par deux variables `mx` et `my`.

<!-- illustration: le bonnet et le missile affichés en même temps, le missile en haut à gauche en (10, 10) -->

**C'est réussi si :** missile et bonnet sont visibles en même temps.

## Input
<!-- ws: {type: exercise, id: bullet-input} -->

Un appui sur le bouton de tir lance le missile tout droit, depuis le joueur.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **Le vecteur vitesse** : de combien la position change à chaque image. Une variable, ajoutée à la position à chaque tour de `TIC`.
>
> ```lua
> position = 0
> vitesse = 3
> position = position + vitesse   --> 3
> position = position + vitesse   --> 6
> ```
>
> | `vitesse` | La position... |
> |---|---|
> | `1` | augmente doucement |
> | `5` | augmente vite |
> | `-2` | diminue |
> | `0` | ne change pas |
>
> ![Au ralenti, avec un vecteur vitesse de +24 pour bien voir : à chaque image, la position du missile augmente de 24. Elle vaut 8, puis 32, puis 56, et ainsi de suite.](img/vitesse-ralenti.gif)
>
> ![Quatre missiles, avec leur vitesse écrite à gauche. Avec 0, le missile ne bouge pas. Avec -2, il va vers la gauche. Plus la flèche est longue, plus le missile va vite.](img/vitesse-comparaison.gif)
>
> ![Une vitesse de +2 sur X (flèche orange) et de +1 sur Y (flèche bleue) : l'objet avance en diagonale (flèche jaune).](img/vitesse-diagonale.gif)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** une vitesse `vmx`. Au tir, le missile prend la position du joueur et une vitesse ; à chaque image, il avance.

<!-- illustration: GIF avec manette : appui sur Z, le missile part de la position du joueur et traverse l'écran vers la droite -->

**C'est réussi si :** le missile part du bonnet et traverse l'écran sans dévier.

## Logique additionnelle
<!-- ws: {type: exercise, id: bullet-logique} -->

Si tu martèles le bouton, le missile se téléporte en plein vol. Et une fois sorti, il ne revient jamais.

![Le problème : à chaque appui sur le bouton de tir, le missile revient devant le joueur, même s'il est déjà parti.](img/tir-spam-avant.gif)

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **`==`** compare deux valeurs. `=` stocke : `if vies = 0 then` est une erreur.
>
> ```lua
> vies = 0
> print(vies == 0)   --> true
> print(vies == 3)   --> false
> ```
>
> Doc Lua (en anglais) : [les comparaisons](https://www.lua.org/manual/5.3/manual.html#3.4.4)

> 🧰 **`and`** : vrai seulement si les deux conditions sont vraies.
>
> ```lua
> age = 15
> billet = true
> print(age >= 12 and billet)   --> true
> billet = false
> print(age >= 12 and billet)   --> false
> ```
>
> Doc Lua (en anglais) : [`and`, `or`, `not`](https://www.lua.org/manual/5.3/manual.html#3.4.5)

> 🧰 **Un seul missile, qui fait des tours.** Sa vitesse dit dans quel état il est.
>
> ![La vie d'un missile. Au repos, hors de l'écran, vitesse 0. Appui sur Z : il prend la position du joueur et une vitesse de 3. Il avance à chaque image. Sorti par la droite, il revient au repos. Un seul missile, qui fait des tours.](img/tir-cycle.webp)
> <!-- ws:anim {src: img/tir-cycle.webm, chapters: img/tir-cycle.vtt} -->
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** le tir part seulement si le missile est au repos. Sorti à droite, il revient se cacher en (-10, -10), vitesse 0.

![Avec la nouvelle condition : le missile part une seule fois, les appuis suivants ne font plus rien.](img/tir-spam-apres.gif)

![Zoom sur le coin en haut à gauche de l'écran. Le missile est en (-10, -10), dans la zone sombre : il est en dehors de l'écran et le joueur ne le voit pas.](img/missile-hors-ecran.png)

**C'est réussi si :** jamais deux missiles en même temps, et toujours un tir possible après la sortie.

# Enemy

## Sprite
<!-- ws: {type: exercise, id: enemy-sprite} -->

Un ennemi, immobile pour l'instant.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **Le studio pendant que le jeu tourne** : <kbd>Échap</kbd>, puis OPEN STUDIO.
>
> ![Depuis le jeu qui tourne : la touche Échap (à gauche de la manette) ouvre le menu de TIC-80, la flèche du bas descend jusqu'à OPEN STUDIO, le bouton A l'ouvre. On choisit ensuite une case libre et on dessine l'ennemi pixel par pixel : d'abord le vert, ensuite les deux yeux rouges.](img/ennemi-dessin.gif)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** ton ennemi, dans une case libre, affiché quelque part sur l'écran.

![Le joueur et l'ennemi affichés en même temps à l'écran.](img/ennemi-ecran.png)

**C'est réussi si :** bonnet, missile et ennemi sont tous les trois à l'écran.

## Mouvement
<!-- ws: {type: exercise, id: enemy-mouvement} -->

L'ennemi avance tout seul vers la gauche. Sorti, il repart de la droite, à une hauteur au hasard.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **`math.random(min, max)`** : un nombre entier au hasard, entre `min` et `max`. Nouveau à chaque appel.
>
> ```lua
> de = math.random(1, 6)
> print(de)   --> 4 (ou 1, 2, 3, 5, 6 : comme un dé)
> ```
>
> ![de = math.random(1, 6), six fois : un dé tombe sur 4, 1, 6, 3, 6, 2. Puis ey = math.random(0, 136) : l'ennemi apparaît à droite de l'écran à une hauteur différente à chaque appel.](img/outil-random.webp)
> <!-- ws:anim {src: img/outil-random.webm, chapters: img/outil-random.vtt} -->
>
> Doc Lua (en anglais) : [`math.random`](https://www.lua.org/manual/5.3/manual.html#pdf-math.random)

> 🧰 **Une vitesse négative** va vers la gauche : le missile à `-2` de l'étape Bullet recule.
>
> ```lua
> x = 100
> vitesse = -2
> x = x + vitesse   --> 98
> ```
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** `ex`, `ey`, `vex`, `vey`. Il part un peu à droite de l'écran, à un `ey` aléatoire, et y repart quand il sort à gauche.

![L'ennemi traverse l'écran de droite à gauche. À chaque nouveau passage, sa hauteur est choisie au hasard.](img/ennemi-mouvement.gif)

**C'est réussi si :** l'ennemi réapparaît à droite après chaque sortie, jamais à la même hauteur.

# Collision

## Enemy VS Player
<!-- ws: {type: exercise, id: collision-enemy-player} -->

L'ennemi traverse le bonnet comme un fantôme. Quand ils se touchent, les deux repartent de leur départ.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **La boîte de collision** d'un sprite va de `x` à `x + 8` et de `y` à `y + 8`.
>
> ![Un sprite agrandi : il fait 8 pixels de large et 8 pixels de haut. Le cadre blanc est sa boîte de collision.](img/collision-dimensions.png)
>
> ![La boîte du sprite va de X à X + largeur sur l'axe horizontal, et de Y à Y + hauteur sur l'axe vertical.](img/collision-boite-position.png)

> 🧰 **Deux boîtes se touchent** quand elles se chevauchent sur X et sur Y. Quelles comparaisons sont vraies de 10–18 contre 15–23, et fausses contre 20–28 ?
>
> ![Sur l'axe X, le segment du joueur va de 10 à 18. L'ennemi de 15 à 23 : oui, ils se chevauchent entre 15 et 18. De 20 à 28 : non. Sur l'axe Y, la même question. Oui sur X mais non sur Y : pas de collision. Oui sur les deux axes : collision.](img/collision-deux-axes.webp)
> <!-- ws:anim {src: img/collision-deux-axes.webm, chapters: img/collision-deux-axes.vtt} -->
>
> ![Pas de collision : les deux boîtes ne se touchent pas.](img/collision-non.png)
>
> ![Collision : les deux boîtes se chevauchent (zone rayée).](img/collision-oui.png)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** une condition qui détecte le contact, et réinitialise les deux positions.

<!-- illustration: GIF : l'ennemi arrive sur le bonnet, les deux disparaissent et réapparaissent à leur position de départ -->

**C'est réussi si :** le contact renvoie les deux sprites au départ, un passage à côté ne fait rien.

## Enemy VS Bullet
<!-- ws: {type: exercise, id: collision-enemy-bullet} -->

Même méthode entre le missile et l'ennemi. Cette fois, toucher rapporte des points.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **`print(texte, x, y, couleur)`** écrit sur l'écran. Après `cls`, sinon le texte est effacé.
>
> ```lua
> print("BONJOUR", 10, 20)
> ```
>
> Doc TIC-80 (en anglais) : [`print`](https://github.com/nesbox/TIC-80/wiki/print#parameters)

> 🧰 **`..`** colle un texte et un nombre.
>
> ```lua
> vies = 3
> print("VIES: " .. vies)   --> VIES: 3
> ```
>
> Doc Lua (en anglais) : [la concaténation](https://www.lua.org/manual/5.3/manual.html#3.4.6)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** une variable `score`, +100 par ennemi touché, affichée à l'écran. Missile et ennemi repartent au départ.

![Le missile touche l'ennemi : le missile et l'ennemi disparaissent et le score passe de 0 à 100.](img/collision-tir-score.gif)

**C'est réussi si :** le score monte à chaque ennemi touché, pas quand le missile le rate.

## Bonus : fonction check_collision
<!-- ws: {type: exercise, id: collision-check-collision, optional: true} -->

Tes deux tests font le même calcul avec des variables différentes. Un code écrit deux fois, c'est une fonction qui attend.

<!-- ws:toolbox -->
### Boîte à outils

> 🧰 **Une fonction** reçoit des valeurs entre parenthèses et renvoie un résultat avec `return`.
>
> ```lua
> function double(n)
>   return n * 2
> end
> print(double(4))   --> 8
> ```
>
> ![function double(n) : une machine nommée double. print(double(4)) : 4 entre et devient n, return renvoie n * 2, 8 s'affiche. double(10) : le même calcul, 20. Dans le jeu, deux boîtes entrent dans check_collision et true ou false ressort.](img/outil-fonction.webp)
> <!-- ws:anim {src: img/outil-fonction.webm, chapters: img/outil-fonction.vtt} -->
>
> Doc Lua (en anglais) : [les fonctions](https://www.lua.org/manual/5.3/manual.html#3.4.11)
<!-- /ws:toolbox -->

### Mise en application
<!-- ws:doit -->

**Ton objectif :** `check_collision` reçoit deux boîtes (position, largeur, hauteur) et répond `true` ou `false`. Tes deux tests l'appellent.

**C'est réussi si :** le jeu joue comme avant, avec un seul calcul de collision.

## Fin de la partie 1

Ton jeu est jouable : le joueur bouge, il tire, les ennemis arrivent et le score monte.

Dans la partie suivante, tu vas t'occuper de ce que le joueur voit.
