# Ce que les animations partagent : la palette de TIC-80 (SWEETIE-16, celle du
# cart), les sprites du jeu dessinés pixel par pixel depuis leurs tuiles, un
# écran de 240 × 136 aux coordonnées du jeu (0, 0 en haut à gauche, y vers le
# bas), du code écrit comme l'élève le tape, et une phrase sous la figure.
import math
import re
from manim import *

# La palette du cart, index 0 à 15.
PALETTE = ["#1a1c2c", "#5d275d", "#b13e53", "#ef7d57", "#ffcd75", "#a7f070", "#38b764", "#257179",
           "#29366f", "#3b5dc9", "#41a6f6", "#73eff7", "#f4f4f4", "#94b0c2", "#566c86", "#333c57"]
FOND = PALETTE[0]          # le noir de TIC-80 : le ciel du jeu
PANNEAU = "#22243a"
BLANC = PALETTE[12]
DOUX = PALETTE[13]
GRIS = PALETTE[14]
CIEL = PALETTE[11]
ALERTE = PALETTE[4]
ORANGE = PALETTE[3]
ROUGE = PALETTE[2]
VERT = PALETTE[5]
BLEU = PALETTE[10]

# Les tuiles du cart : 64 chiffres hexadécimaux, un par pixel, ligne par ligne.
TUILES = {
    "joueur": "c0000000c2000000c2220000c22222ccc22222ccc2220000c2000000c0000000",   # le bonnet, tuile 0
    "missile": "00000000000000000000000ccccccccccccccccc0000000c0000000000000000",  # tuile 1
    "ennemi": "0055550005555550555555555525525555555555550000550505505000555500",   # tuile 16
}
W, H = 240, 136

config.background_color = FOND


def code(texte, taille=30, couleur=BLANC):
    """Une ligne de code, en monospace, telle que l'élève la tape."""
    return Text(texte, font="DejaVu Sans Mono", font_size=taille, color=couleur)


def texte(t, taille=24, couleur=BLANC):
    """Des mots, pas du code : la police des phrases."""
    return Text(t, font="DejaVu Sans", font_size=taille, color=couleur)


def bloc_code(lignes, taille=24, couleur=BLANC):
    """Plusieurs lignes de code, alignées à gauche, l'indentation gardée. Un Text
    par ligne, pour pouvoir en entourer ou en changer une."""
    largeur = code("x", taille).width
    groupe = VGroup(*[code(l.strip() if l.strip() else "·", taille, couleur) for l in lignes])
    groupe.arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    gauche = groupe.get_left()[0]
    for ligne, t in zip(groupe, lignes):
        retrait = len(t) - len(t.lstrip(" "))
        ligne.shift(RIGHT * (gauche + retrait * largeur - ligne.get_left()[0]))
        if not t.strip():
            ligne.set_opacity(0)
    return groupe


def phrase(t, couleur=CIEL, taille=26):
    """La phrase sous la figure : ce que l'état montré veut dire."""
    m = texte(t, taille, couleur)
    if m.width > config.frame_width - 1:
        m.scale_to_fit_width(config.frame_width - 1)
    return m.to_edge(DOWN, buff=0.4)


def titre(t, couleur=ALERTE, taille=28):
    m = texte(t, taille, couleur)
    if m.width > config.frame_width - 1:
        m.scale_to_fit_width(config.frame_width - 1)
    return m.to_edge(UP, buff=0.4)


def surligne(m, couleur=ALERTE):
    return SurroundingRectangle(m, color=couleur, buff=0.08, stroke_width=3)


def sprite(nom, px, echelle=1, coin=ORIGIN):
    """Le sprite `nom`, pixel par pixel : un carré de `px` unités manim par pixel
    du jeu (× `echelle`, comme le paramètre scale de spr). La couleur 0 est
    transparente, comme dans le jeu. Le coin haut-gauche du sprite est en `coin`."""
    g = VGroup()
    cote = px * echelle
    for i, ch in enumerate(TUILES[nom]):
        if ch == "0":
            continue
        r, c = divmod(i, 8)
        g.add(Square(side_length=cote, fill_color=PALETTE[int(ch, 16)], fill_opacity=1, stroke_width=0)
              .move_to(coin + RIGHT * (c + 0.5) * cote + DOWN * (r + 0.5) * cote))
    return g


class Ecran:
    """L'écran de TIC-80 : 240 × 136 pixels du jeu, `px` unités manim par pixel,
    le coin (0, 0) en haut à gauche, y vers le bas — les coordonnées du jeu."""

    def __init__(self, px=0.03, centre=ORIGIN, fond=FOND):
        self.px = px
        self.cadre = Rectangle(width=W * px, height=H * px, fill_color=fond, fill_opacity=1,
                               stroke_color=DOUX, stroke_width=2).move_to(centre)
        self.coin = self.cadre.get_corner(UL)

    def pos(self, x, y):
        """Le point manim du pixel (x, y) du jeu."""
        return self.coin + RIGHT * x * self.px + DOWN * y * self.px

    def sprite(self, nom, x, y, echelle=1):
        return sprite(nom, self.px, echelle, self.pos(x, y))

    def sprite_clippe(self, nom, x, y, echelle=1):
        """Comme `sprite`, mais les pixels hors de l'écran sont invisibles : le jeu
        ne dessine rien au-delà des bords, et un missile au repos en (-10, -10)
        ne se voit pas."""
        g = self.sprite(nom, x, y, echelle)
        g_, d_ = self.cadre.get_left()[0], self.cadre.get_right()[0]
        h_, b_ = self.cadre.get_top()[1], self.cadre.get_bottom()[1]
        for px in g:
            cx, cy = px.get_center()[0], px.get_center()[1]
            if cx < g_ or cx > d_ or cy > h_ or cy < b_:
                px.set_opacity(0)
        return g

    def boite(self, x, y, l=8, h=8, couleur=ALERTE, largeur=2):
        """Le rectangle de x à x + l et de y à y + h."""
        r = Rectangle(width=l * self.px, height=h * self.px, stroke_color=couleur, stroke_width=largeur, fill_opacity=0)
        return r.move_to(self.pos(x + l / 2, y + h / 2))

    def axes(self, couleur=DOUX):
        """Les repères de l'écran : 0 en haut à gauche, 240 à droite, 136 en bas."""
        g = VGroup(
            texte("0", 18, couleur).next_to(self.cadre.get_corner(UL), UL, buff=0.1),
            texte("240", 18, couleur).next_to(self.cadre.get_corner(UR), UP, buff=0.12),
            texte("136", 18, couleur).next_to(self.cadre.get_corner(DL), LEFT, buff=0.12),
            Arrow(self.cadre.get_corner(UL) + UP * 0.35, self.cadre.get_corner(UL) + UP * 0.35 + RIGHT * 1.6,
                  buff=0, color=couleur, stroke_width=3, max_tip_length_to_length_ratio=0.12),
            Arrow(self.cadre.get_corner(UL) + LEFT * 0.35, self.cadre.get_corner(UL) + LEFT * 0.35 + DOWN * 1.2,
                  buff=0, color=couleur, stroke_width=3, max_tip_length_to_length_ratio=0.15),
        )
        g.add(texte("x", 20, couleur).next_to(g[3], UP, buff=0.05),
              texte("y", 20, couleur).next_to(g[4], LEFT, buff=0.05))
        return g


def origine(point, couleur=ALERTE, rayon=0.055):
    """Le petit point à l'origine d'un sprite, son pixel en haut à gauche : c'est
    là que pointent x et y. Toujours présent quand on nomme les coordonnées d'un sprite."""
    return Dot(point, radius=rayon, color=couleur)


def manette(touche, allumee=False, taille=0.6):
    """Une touche du clavier, comme l'overlay des GIF : allumée quand elle est appuyée."""
    k = RoundedRectangle(width=taille, height=taille, corner_radius=0.1, stroke_color=DOUX, stroke_width=2,
                         fill_color=ALERTE if allumee else PANNEAU, fill_opacity=1)
    t = texte(touche, 22, FOND if allumee else DOUX).move_to(k)
    return VGroup(k, t)


# Une couleur par objet du jeu, dans les animations comme dans le sujet : celle de son
# sprite. Le missile est blanc, la couleur du texte : il prend le bleu clair de la palette.
C_JOUEUR, C_ENNEMI, C_MISSILE = ROUGE, VERT, BLEU


def var(t, famille, taille=22, couleur=BLANC):
    """`ex = 232` : chaque nom devant un `=` prend la couleur de son objet, le reste
    garde `couleur`. Un nom peut avoir des espaces (« enemy x = 232 »)."""
    m = code(t, taille, couleur)
    sans = t.replace(" ", "")
    for nom in re.findall(r"([A-Za-z_][A-Za-z0-9_ .]*?)\s*=", t):
        cle = nom.replace(" ", "")
        i = sans.find(cle + "=")
        if i >= 0:
            m[i:i + len(cle)].set_color(famille)
    return m


def bapteme(scene, longs, courts, famille, taille, position, buff=0.15, attente=0.9, run_time=0.8):
    """À la première apparition d'une variable : son nom long (« enemy y = 101 ») se
    transforme en son nom court (« ey = 101 »), dans la couleur de son objet. Rend le
    groupe des noms courts, à retirer de la scène si un `always_redraw` prend la suite."""
    if isinstance(longs, str):
        longs, courts = [longs], [courts]
    l = VGroup(*[var(t, famille, taille) for t in longs]).arrange(DOWN, aligned_edge=LEFT, buff=buff).move_to(position)
    c = VGroup(*[var(t, famille, taille) for t in courts]).arrange(DOWN, aligned_edge=LEFT, buff=buff).move_to(position)
    scene.play(FadeIn(l), run_time=0.4)
    scene.wait(attente)
    scene.play(FadeTransform(l, c), run_time=run_time)
    return c


def etiquette(t, couleur=ALERTE, taille=22):
    """Une valeur affichée près d'un objet : `x = 12`."""
    return code(t, taille, couleur)


def roule(cran):
    """Une valeur de compteur qui reste sur son chiffre au début de chaque cran,
    puis roule vers le suivant. `cran` est un nombre à virgule : 2.5, c'est le
    milieu du troisième cran."""
    k = int(cran + 1e-9)
    u = min(1, max(0, (cran - k - 0.6) / 0.4))
    return k + u * u * (3 - 2 * u)


class Compteur(VGroup):
    """Un compteur à rouleaux, comme un compteur kilométrique : un rouleau de
    chiffres de 0 à 9 par chiffre, dans une fenêtre. Quand les unités passent
    de 9 à 0, les dizaines roulent en même temps. Un zéro à gauche reste vide.
    C'est la façon convenue de montrer une boucle : jamais une flèche qui tourne.

    `valeur()` est lue à chaque image ; entre deux entiers, les rouleaux sont
    entre deux chiffres. `nom` au-dessus, `legende` (des lignes) en dessous."""

    HAUT = 1.25
    PAS = 0.78

    def __init__(self, nom, valeur, chiffres=1, couleur=ALERTE, legende=()):
        super().__init__()
        self.valeur, self.n = valeur, chiffres
        large = 0.37 + self.PAS * chiffres
        self.fenetre = RoundedRectangle(width=large, height=self.HAUT, corner_radius=0.12, stroke_color=couleur,
                                        stroke_width=3, fill_color=PANNEAU, fill_opacity=1)
        c = self.fenetre.get_center()
        self.rouleaux = VGroup(*[VGroup(*[Text(str(d), font="DejaVu Sans Mono", font_size=56, color=couleur) for d in range(10)])
                                 for _ in range(chiffres)])
        # Deux caches de la couleur du fond : on ne voit les rouleaux que dans la fenêtre.
        caches = VGroup(*[Rectangle(width=large + 0.4, height=self.HAUT, fill_color=FOND, fill_opacity=1, stroke_width=0)
                          .next_to(self.fenetre, sens, buff=0) for sens in (UP, DOWN)])
        bord = self.fenetre.copy().set_fill(opacity=0)
        traits = VGroup(*[Line(c + RIGHT * x + UP * self.HAUT / 2, c + RIGHT * x + DOWN * self.HAUT / 2, stroke_color=couleur,
                               stroke_width=1.5, stroke_opacity=0.35)
                          for x in [self.PAS * ((chiffres - 1) / 2 - i - 0.5) for i in range(chiffres - 1)]])
        self.nom = code(nom, 30, couleur).next_to(self.fenetre, UP, buff=0.25)
        self.legende = VGroup(*[texte(l, 20, DOUX) for l in legende]).arrange(DOWN, buff=0.1).next_to(self.fenetre, DOWN, buff=0.25)
        self.add(self.fenetre, self.rouleaux, caches, bord, traits, self.nom, self.legende)
        self.rouleaux.add_updater(self.rouler)
        self.rouler(self.rouleaux)

    def rouler(self, m):
        v = max(0.0, self.valeur())
        echelle = self.fenetre.height / self.HAUT      # le compteur a pu être agrandi
        for i, rouleau in enumerate(m):
            p = 10 ** i
            # Le rouleau i avance d'un chiffre quand tous ceux de droite passent de 9 à 0.
            r = math.floor(v / p) + max(0.0, (v % p) - (p - 1)) if i else v
            place = self.fenetre.get_center() + RIGHT * self.PAS * echelle * ((self.n - 1) / 2 - i)
            vide = i > 0 and v < p          # le zéro à gauche : rien
            for d, chiffre in enumerate(rouleau):
                ecart = (d - r + 5) % 10 - 5            # entre -5 et 5 : 0 au milieu de la fenêtre
                chiffre.move_to(place + DOWN * max(-1, min(1, ecart)) * self.fenetre.height)
                visible = abs(ecart) < 0.999 and not (vide and d == 0)
                chiffre.set_opacity(1 if visible else 0)


class Boite:
    """Une variable dessinée : une boîte avec son nom au-dessus et sa valeur dedans.
    Ses trois morceaux s'ajoutent à la scène un par un (`poser`), pour que
    `changer` puisse remplacer la valeur par un fondu sans toucher au reste."""

    def __init__(self, nom, valeur, couleur=ALERTE, largeur=1.7, centre=ORIGIN):
        self.couleur = couleur
        self.cadre = RoundedRectangle(width=largeur, height=0.9, corner_radius=0.12, stroke_color=couleur,
                                      stroke_width=3, fill_color=PANNEAU, fill_opacity=1).move_to(centre)
        self.nom = code(nom, 24, couleur).next_to(self.cadre, UP, buff=0.12)
        self.val = code(str(valeur), 30, BLANC).move_to(self.cadre)

    def mobjects(self):
        return [self.cadre, self.nom, self.val]

    def poser(self, scene, anime=True, run_time=0.5):
        if anime:
            scene.play(FadeIn(self.cadre), FadeIn(self.nom), FadeIn(self.val), run_time=run_time)
        else:
            scene.add(self.cadre, self.nom, self.val)

    def changer(self, scene, valeur, run_time=0.5):
        nv = code(str(valeur), 30, BLANC).move_to(self.cadre)
        scene.play(FadeTransform(self.val, nv), run_time=run_time)
        self.val = nv

    def effacer(self, scene, run_time=0.4):
        scene.play(FadeOut(self.cadre), FadeOut(self.nom), FadeOut(self.val), run_time=run_time)


class Console:
    """Le terminal Lua du runtime : ce que `print` affiche, ligne après ligne."""

    def __init__(self, scene, centre, largeur=4.6, hauteur=2.2, lignes=4):
        self.scene, self.max = scene, lignes
        self.cadre = Rectangle(width=largeur, height=hauteur, stroke_color=GRIS, stroke_width=2,
                               fill_color="#101120", fill_opacity=1).move_to(centre)
        self.titre = texte("terminal Lua", 16, DOUX).next_to(self.cadre.get_corner(UL), DR, buff=0.12)
        self.lignes = []
        scene.add(self.cadre, self.titre)

    def ecrire(self, t, couleur=VERT, run_time=0.4):
        l = code(t, 22, couleur)
        if self.lignes:
            l.next_to(self.lignes[-1], DOWN, aligned_edge=LEFT, buff=0.12)
        else:
            l.next_to(self.titre, DOWN, aligned_edge=LEFT, buff=0.18)
        if len(self.lignes) >= self.max:
            vieux = self.lignes.pop(0)
            self.scene.play(FadeOut(vieux), *[m.animate.shift(UP * 0.42) for m in self.lignes], run_time=0.3)
            l.shift(UP * 0.42)
        self.lignes.append(l)
        self.scene.play(FadeIn(l, shift=RIGHT * 0.2), run_time=run_time)
        return l


# ---------------------------------------------------------------------------
# Le code couleur, fixé le 26/11 : une couleur par rôle, reprise partout.
CHANGE = ALERTE      # ce qui change : une valeur, un jeton, une étiquette qui bouge
LU = CIEL            # ce qu'on lit : une condition, une ligne surlignée, un curseur
VRAI = VERT
FAUX = ROUGE


def fleche_vitesse(depart, vx, vy=0, echelle=0.06, couleur=LU):
    """La flèche de vitesse : part de l'origine du sprite, sa longueur dit la vitesse,
    son sens le signe. `echelle` : unités manim par unité de vitesse."""
    if vx == 0 and vy == 0:
        return Dot(depart, radius=0.06, color=couleur)
    return Arrow(depart, depart + RIGHT * vx * echelle * 10 + DOWN * vy * echelle * 10, buff=0, color=couleur,
                 stroke_width=5, max_tip_length_to_length_ratio=0.3)


def guides(ecran, x, y, couleur=CHANGE):
    """Les guides pointillés : de l'origine du sprite jusqu'au bord du bas et jusqu'au
    bord de gauche, pour dire quel nombre est x et lequel est y."""
    return VGroup(DashedLine(ecran.pos(x, y), ecran.pos(x, H), stroke_color=couleur, stroke_width=2),
                  DashedLine(ecran.pos(x, y), ecran.pos(0, y), stroke_color=couleur, stroke_width=2))


def fil(depart, arrivee, couleur=CHANGE):
    """Le fil : un trait fin entre l'origine d'un sprite et ses nombres rangés sur le côté."""
    return Line(depart, arrivee, stroke_color=couleur, stroke_width=1.5, stroke_opacity=0.75)


def badge(t, couleur=LU, taille=20):
    """L'étiquette d'état : « tiré », « prêt à être tiré », sur l'objet."""
    fond = RoundedRectangle(width=0.36 + 0.115 * len(t), height=0.42, corner_radius=0.2, fill_color=couleur, fill_opacity=1, stroke_width=0)
    return VGroup(fond, texte(t, taille, FOND).move_to(fond))


class Reglage(VGroup):
    """Un curseur : un nom, un rail, un bouton, et sa valeur à droite. Le nom est le mot de
    l'élève, jamais la ligne de la solution. Porté de World Generator."""

    def __init__(self, nom, mini, maxi, valeur, couleur=LU, largeur=2.6, decimales=0):
        super().__init__()
        self.t = ValueTracker(valeur)
        self.mini, self.maxi = mini, maxi
        self.rail = Line(LEFT * largeur / 2, RIGHT * largeur / 2, stroke_color=DOUX, stroke_width=4)
        self.nom = texte(nom, 22, couleur).next_to(self.rail, UP, buff=0.22)
        self.bouton = Dot(radius=0.13, color=couleur)
        self.bouton.add_updater(lambda m: m.move_to(self.rail.point_from_proportion(min(1, max(0, (self.t.get_value() - mini) / (maxi - mini))))))
        self.bouton.update()
        fmt = (lambda v: str(round(v))) if decimales == 0 else (lambda v: f"{v:.{decimales}f}")
        self.nombre = always_redraw(lambda: code(fmt(self.t.get_value()), 22, couleur).next_to(self.rail, RIGHT, buff=0.2))
        self.add(self.rail, self.nom, self.bouton, self.nombre)

    def placer(self, pos):
        self.shift(pos - self.rail.get_center())
        return self
