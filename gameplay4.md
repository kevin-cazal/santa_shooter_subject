# Gameplay
<!-- ws: {type: chapter, topology: free} -->

Une liste de défis. Choisis-en un ou plusieurs, dans l'ordre que tu veux : chacun est indépendant des autres.

## Patterns d'ennemi

### Sinusoïde
<!-- ws: {type: exercise, id: gameplay-sinusoide} -->

**Ton objectif :** l'ennemi avance vers la gauche en ondulant de haut en bas. `math.sin` et un compteur d'images sont tes outils.

**C'est réussi si :** des vagues régulières, sans jamais sortir par le haut ou le bas.

### Vagues
<!-- ws: {type: exercise, id: gameplay-vagues} -->

**Ton objectif :** plusieurs ennemis apparaissent en groupe, dans une liste, comme tes étoiles. La vague suivante arrive quand la première est passée ou détruite.

**C'est réussi si :** les collisions marchent avec chaque ennemi de la vague.

### Boss
<!-- ws: {type: exercise, id: gameplay-boss} -->

**Ton objectif :** un ennemi plus gros, qui encaisse plusieurs missiles, et qui apparaît de temps en temps.

**C'est réussi si :** on voit le boss encaisser, et sa destruction rapporte plus.

## Armes

### Double tir
<!-- ws: {type: exercise, id: gameplay-double-tir} -->

**Ton objectif :** deux missiles au même appui, un au-dessus et un en dessous.

**C'est réussi si :** chaque missile touche séparément.

### Triple tir
<!-- ws: {type: exercise, id: gameplay-triple-tir} -->

**Ton objectif :** trois missiles tirés en même temps : un tout droit, un vers le haut, un vers le bas.

**C'est réussi si :** les trois missiles s'écartent en avançant.

### Tir plus rapide
<!-- ws: {type: exercise, id: gameplay-tir-rapide} -->

**Ton objectif :** moins d'attente entre deux tirs, réglée par un compteur d'images.

**C'est réussi si :** un seul nombre change la cadence.

### Laser
<!-- ws: {type: exercise, id: gameplay-laser} -->

**Ton objectif :** bouton enfoncé, une ligne part du joueur vers la droite et touche tout ennemi qu'elle croise. Rien ne se déplace.

**C'est réussi si :** le laser se voit, et touche sans délai.

### Homing missile
<!-- ws: {type: exercise, id: gameplay-homing-missile} -->

**Ton objectif :** à chaque image, la vitesse du missile se corrige vers l'ennemi le plus proche.

**C'est réussi si :** le missile tourne pour suivre un ennemi qui change de hauteur.

## Équilibrage

### Munitions
<!-- ws: {type: exercise, id: gameplay-munitions} -->

**Ton objectif :** un nombre de tirs affiché, qui baisse à chaque tir et remonte avec le temps.

**C'est réussi si :** à zéro, le bouton ne fait rien, puis refonctionne.

### Difficulté
<!-- ws: {type: exercise, id: gameplay-difficulte} -->

**Ton objectif :** un réglage qui grandit avec le temps de jeu : la vitesse ou le nombre des ennemis.

**C'est réussi si :** la partie est visiblement plus dure après une minute.

## Fin de l'atelier

Tu décides quand cette partie est finie : valide cette étape quand tu as fait les défis qui t'intéressaient.

Merci d'avoir suivi l'atelier. Ton avis nous aide à l'améliorer pour les prochains.
