# Effets visuels

Dans cette partie, tu ajoutes ce qui donne son allure au jeu. Les étapes marquées Bonus sont
facultatives : tu peux les faire ou les sauter, la suite se débloque sans elles.

## Ciel étoilé
<!-- ws: {type: exercise, id: fx-ciel-etoile} -->

- Couleur background
- Points pour représenter les étoiles
- Vitesse de défilement fixe

## Parallaxe
<!-- ws: {type: exercise, id: fx-parallaxe} -->

- Regrouper les étoiles en fonction de leur taille
- Plus l'étoile est grosse (proche) plus elle se déplace vite

## Particules
<!-- ws: {type: exercise, id: fx-particules} -->

- Effet de particule quand collision joueur/enemy et bullet/enemy

## Bonus SFX
<!-- ws: {type: exercise, id: fx-bonus-sfx, optional: true} -->

- Onglet SFX de TIC-80: créer un son court pour le tir, un autre pour la collision
- Jouer le son du tir au moment où la balle part
- Jouer le son de collision dans les deux tests: bullet/enemy et enemy/player

## Bonus Music
<!-- ws: {type: exercise, id: fx-bonus-music, optional: true} -->

- Onglet Music de TIC-80: composer une boucle courte sur la piste 0
- Lancer la musique une seule fois, au démarrage du cart, en boucle
- Attention: un appel dans TIC() relance la musique à chaque frame

## Bonus Vitesse du vaisseau
<!-- ws: {type: exercise, id: fx-bonus-vitesse, optional: true} -->

- Le défilement des étoiles accélère quand le joueur avance
- Le défilement ralentit quand le joueur recule, mais le vaisseau n'est jamais à l'arrêt

## Bonus Sol
<!-- ws: {type: exercise, id: fx-bonus-sol, optional: true} -->

- Remplacer le rectangle par une vraie carte de tuiles
- Le sol défile automatiquement (autoscroll)

## Fin de la partie 2

Ton jeu a maintenant une allure à lui.

Dans la partie suivante, tu vas ranger ton code avant qu'il ne devienne trop long.
