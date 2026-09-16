# Effets visuels

Dans cette partie, tu ajoutes ce qui donne son allure au jeu. Les étapes marquées Bonus sont
facultatives : tu peux les faire ou les sauter, la suite se débloque sans elles.

## Ciel étoilé
<!-- ws: {type: exercise, id: fx-ciel-etoile} -->

- Couleur background
- Points pour représenter les étoiles
- Vitesse de défilement fixe

Modifie les graphismes de ton jeu pour donner l'impression que le joueur se déplace dans un ciel étoilé.

Boite à outil:
- Couleur de background TIC-80 `cls`
- for
- {} et table.insert
- `circ` pour déssiner des étoiles de taille différentes 

Mise en application:

Fait en sorte d'avoir une couleur de fond noir.
<!-- illustration: resultat intermédiaire -->

Génère une liste de 50 d'étoiles initilisée à une position aléatoire (`math.random`) et d'une taille aléatoire (entre 1 et 5)
Fait défiler les étoiles du bord droit vers le bord gauche de l'écran.
Dessine les étoiles à l'écran
<!-- illustration: resultat final -->



## Parallaxe
<!-- ws: {type: exercise, id: fx-parallaxe} -->

- Regrouper les étoiles en fonction de leur taille
- Plus l'étoile est grosse (proche) plus elle se déplace vite

Utilise deux effets de perceptions pour rendre le ciel étoilé plus réaliste.

Boite à outil:
- Un objet proche parait plus gros, un objet éloigné parait plus petit. C'est la perspective.
- Un objet proche parait plus rapide, un objet éloigné parait plus lent. C'est la parallaxe.

Mise en application:

Tu as des étoiles plus grosses que d'autres, celles qui sont plus grosses sont donc plus proches de toi, elles doivent donc se déplacer plus rapidement que les plus petites étoiles.
A l'endroit où tu fais se déplacer les étoiles, ajoute un coéfficient qui change la vitesse de déplacement d'une étoile en fonction de sa taille.
<!-- illustration: resultat final -->


## Particules
<!-- ws: {type: exercise, id: fx-particules} -->

- Effet de particule quand collision joueur/enemy et bullet/enemy
²
Un effet de particule est un effet visuel permettant de représenter un phénomène naturel/chaotique comme de la poussière, de la neige, des flammes ou une explosion.

Pour avoir un effet de particule il nous faut:
- Une entité emettrice (d'où proviènent les particules)
- Une longevité (les particules disparaissent au bout d'un moment)
- Une physique (comment les particules vont se déplacer)


Mise en application:

Utilise une liste pour représenter tes particules `{}`. 



## Bonus SFX
<!-- ws: {type: exercise, id: fx-bonus-sfx, optional: true} -->

- Onglet SFX de TIC-80: créer un son court pour le tir, un autre pour la collision
- Jouer le son du tir au moment où la balle part
- Jouer le son de collision dans les deux tests: bullet/enemy et enemy/player


Ajoute un effet sonnore à ton jeu.



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
