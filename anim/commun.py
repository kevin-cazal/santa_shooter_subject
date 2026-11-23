# Ce que les animations partagent : la palette de TIC-80 (SWEETIE-16, celle du
# cart), les sprites du jeu dessinés pixel par pixel depuis leurs tuiles, un
# écran de 240 × 136 aux coordonnées du jeu (0, 0 en haut à gauche, y vers le
# bas), du code écrit comme l'élève le tape, et une phrase sous la figure.
import math
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


def manette(touche, allumee=False, taille=0.6):
    """Une touche du clavier, comme l'overlay des GIF : allumée quand elle est appuyée."""
    k = RoundedRectangle(width=taille, height=taille, corner_radius=0.1, stroke_color=DOUX, stroke_width=2,
                         fill_color=ALERTE if allumee else PANNEAU, fill_opacity=1)
    t = texte(touche, 22, FOND if allumee else DOUX).move_to(k)
    return VGroup(k, t)


def etiquette(t, couleur=ALERTE, taille=22):
    """Une valeur affichée près d'un objet : `x = 12`."""
    return code(t, taille, couleur)
