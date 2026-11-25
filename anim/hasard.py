# Partie 1, boîte à outils « math.random » : un nombre entier au hasard entre
# min et max, nouveau à chaque appel. D'abord un dé, puis une hauteur sur
# l'écran pour l'ennemi.
#
#   capture.py anim anim/hasard.py LeHasard -o img/outil-random.webp --fps 30
import random
from manim import *
from commun import *

random.seed(11)
FACES = {1: [(0, 0)], 2: [(-1, 1), (1, -1)], 3: [(-1, 1), (0, 0), (1, -1)], 4: [(-1, 1), (1, 1), (-1, -1), (1, -1)],
         5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)], 6: [(-1, 1), (1, 1), (-1, 0), (1, 0), (-1, -1), (1, -1)]}


def de(n, centre, cote=1.1):
    g = VGroup(RoundedRectangle(width=cote, height=cote, corner_radius=0.18, fill_color=BLANC, fill_opacity=1, stroke_width=0))
    for dx, dy in FACES[n]:
        g.add(Dot(radius=0.09, color=FOND).move_to(centre + RIGHT * dx * cote * 0.27 + UP * dy * cote * 0.27))
    g[0].move_to(centre)
    return g


class LeHasard(Scene):
    def construct(self):
        self.next_section("math.random(1, 6) : comme un dé")
        ligne = code("de = math.random(1, 6)", 32).move_to(UP * 2.9)
        self.play(Write(ligne), run_time=0.8)
        p = phrase("math.random(1, 6) : un nombre entier entre 1 et 6, nouveau à chaque appel")
        self.play(FadeIn(p), run_time=0.3)
        con = Console(self, RIGHT * 3.6 + UP * 0.4, largeur=3.6, hauteur=2.6, lignes=5)
        tirages = [4, 1, 6, 3, 6, 2]
        dessus = None
        for n in tirages:
            d = de(n, LEFT * 2.6 + UP * 0.4)
            s = surligne(ligne[3:], CIEL)
            self.play(Create(s), run_time=0.15)
            if dessus is None:
                self.play(FadeIn(d, scale=0.6), run_time=0.3)
            else:
                self.play(FadeTransform(dessus, d), run_time=0.3)
            dessus = d
            self.play(FadeOut(s), run_time=0.1)
            con.ecrire(f"print(de)  --> {n}", couleur=BLANC, run_time=0.25)
        self.wait(1.0)

        self.next_section("math.random(0, 136) : une hauteur sur l'écran")
        self.play(FadeOut(p), FadeOut(dessus), FadeOut(con.cadre), FadeOut(con.titre), *[FadeOut(l) for l in con.lignes], run_time=0.4)
        l2 = code("ey = math.random(0, 136)", 32).move_to(UP * 2.9)
        self.play(FadeTransform(ligne, l2), run_time=0.6)
        p = phrase("de 0 à 136 : toute la hauteur de l'écran. L'ennemi repart d'une hauteur différente à chaque fois")
        ecran = Ecran(px=0.03, centre=DOWN * 0.5)
        self.play(FadeIn(p), FadeIn(ecran.cadre), FadeIn(ecran.axes()), run_time=0.5)
        ennemi = None
        for ey in (12, 101, 55, 128, 30):
            e = ecran.sprite("ennemi", 224, ey, 1)
            tag = etiquette(f"ey = {ey}", ALERTE, 22).next_to(ecran.cadre, RIGHT, buff=0.3).set_y(ecran.pos(0, ey + 4)[1])
            s = surligne(l2[3:], CIEL)
            self.play(Create(s), run_time=0.15)
            if ennemi is None:
                self.play(FadeIn(e, scale=0.6), FadeIn(tag), run_time=0.4)
            else:
                self.play(FadeTransform(ennemi, e), FadeTransform(ancien, tag), run_time=0.4)
            ennemi, ancien = e, tag
            self.play(FadeOut(s), run_time=0.1)
            self.wait(0.5)
        self.wait(1.0)
