# Partie 3, « Notion d'objet en Lua » : des variables éparpillées deviennent
# une table par objet du jeu, une boîte avec des cases nommées. player.x se lit
# « la case x de la boîte player ». Les fonctions viennent après, dans le sujet.
#
#   capture.py anim anim/tables.py LesTables -o img/refactor-tables.webp --fps 30
from manim import *
from commun import *

JOUEUR = [("x = 0", "x = 0"), ("y = 68", "y = 68"), ("player_speed = 1.5", "speed = 1.5")]
ENNEMI = [("ex = 250", "x = 250"), ("ey = 40", "y = 40"), ("vex = -1.2", "speed = -1.2")]


def boite(nom, lignes, couleur, centre):
    """Une table dessinée : son nom au-dessus, une case par ligne."""
    rangs = VGroup(*[var(l, couleur, 24) for l in lignes]).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    cadre = RoundedRectangle(width=rangs.width + 0.9, height=rangs.height + 0.6, corner_radius=0.15,
                             stroke_color=couleur, stroke_width=3, fill_color=PANNEAU, fill_opacity=1)
    rangs.move_to(cadre)
    titre_ = code(nom, 26, couleur).next_to(cadre, UP, buff=0.15)
    return VGroup(cadre, rangs, titre_).move_to(centre)


class LesTables(Scene):
    def construct(self):
        # 1. Éparpillées.
        self.next_section("aujourd'hui : des variables éparpillées")
        places = [LEFT * 4.8 + UP * 2.6, LEFT * 0.8 + UP * 1.6, LEFT * 3.4 + DOWN * 0.6,
                  RIGHT * 4.6 + UP * 2.6, RIGHT * 1.2 + DOWN * 0.5, RIGHT * 5.4 + DOWN * 0.6]
        libres = VGroup(*[var(l, C_JOUEUR if i < 3 else C_ENNEMI, 26) for i, (l, _) in enumerate(JOUEUR + ENNEMI)])
        for m, pl in zip(libres, places):
            m.move_to(pl)
        p = phrase("six variables mélangées : trois du joueur, trois de l'ennemi")
        self.play(LaggedStart(*[FadeIn(m, scale=0.8) for m in libres], lag_ratio=0.15), run_time=1.2)
        self.play(FadeIn(p), run_time=0.4)
        self.wait(1.4)

        # 2. Une table.
        self.next_section("une table : une boîte avec des cases nommées")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("une table : une boîte nommée, avec des cases nommées")
        joueur = boite("player", [l for _, l in JOUEUR], C_JOUEUR, LEFT * 3.2 + UP * 0.9)
        self.play(FadeIn(p), FadeIn(joueur[0]), FadeIn(joueur[2]), run_time=0.6)
        for m, rang in zip(libres[:3], joueur[1]):
            self.play(FadeTransform(m, rang), run_time=0.7)
        self.wait(0.6)
        ligne = code("player = { x = 0, y = 68, speed = 1.5 }", 26).move_to(DOWN * 1.6)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("dans le code, la boîte s'écrit entre accolades")
        self.play(FadeIn(p), Write(ligne), run_time=1.2)
        self.wait(1.4)

        # 3. player.x
        self.next_section("player.x : la case x de la boîte")
        self.play(FadeOut(p), FadeOut(ligne), run_time=0.3)
        p = phrase("player.x : la case x de la boîte player, ici 0")
        acces = code("player.x", 30, C_JOUEUR).next_to(joueur, DOWN, buff=0.6)
        s = surligne(joueur[1][0])
        self.play(FadeIn(p), FadeIn(acces), Create(s), run_time=0.6)
        self.wait(1.6)

        # 4. Une boîte par objet.
        self.next_section("une boîte par objet du jeu")
        self.play(FadeOut(p), FadeOut(acces), FadeOut(s), run_time=0.3)
        p = phrase("une boîte par objet, mêmes cases : x, y, speed")
        ennemi = boite("enemy", [l for _, l in ENNEMI], C_ENNEMI, RIGHT * 3.2 + UP * 0.9)
        self.play(FadeIn(p), FadeIn(ennemi[0]), FadeIn(ennemi[2]), run_time=0.6)
        for m, rang in zip(libres[3:], ennemi[1]):
            self.play(FadeTransform(m, rang), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("player.x, enemy.x : le code dit de qui il parle")
        self.play(FadeIn(p), run_time=0.4)
        self.wait(1.6)
