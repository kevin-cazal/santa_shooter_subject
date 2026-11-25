# Partie 1, boîte à outils « Incrémenter » : compteur = compteur + 1 est une
# marche d'escalier. Un jeton +1 tombe dans le compteur à rouleaux, et le
# bonnet monte d'une marche. Puis l'escalier se couche : x = x + 1, le joueur
# avance d'un pixel par image.
#
#   capture.py anim anim/incrementer.py Incrementer -o img/outil-incrementer.webp --fps 30
from manim import *
from commun import *

PX = 0.05


class Incrementer(Scene):
    def construct(self):
        ligne = code("compteur = compteur + 1", 34).move_to(UP * 2.8)
        gauche, droite = ligne[0:8], ligne[9:19]
        self.play(Write(ligne), run_time=0.8)
        v = ValueTracker(0)
        c = Compteur("compteur", v.get_value, chiffres=1).scale(0.9)
        c.shift(LEFT * 4.2 + DOWN * 0.4 - c.fenetre.get_center())
        self.add(c)
        # L'escalier : cinq marches qui montent vers la droite.
        marches = VGroup()
        for i in range(5):
            m = Rectangle(width=1.0, height=0.45 * (i + 1), stroke_color=GRIS, stroke_width=2, fill_color=PANNEAU, fill_opacity=1)
            m.move_to(RIGHT * (-1.0 + i * 1.0) + DOWN * (2.5 - 0.45 * (i + 1) / 2))
            marches.add(m)
        numeros = VGroup(*[code(str(i), 20, DOUX).next_to(m, DOWN, buff=0.1) for i, m in enumerate(marches)])
        self.play(FadeIn(marches), FadeIn(numeros), run_time=0.5)

        def dessus(i):
            return marches[i].get_top() + LEFT * 4 * PX + UP * 8 * PX

        bonnet = sprite("joueur", PX, 1, dessus(0))
        self.play(FadeIn(bonnet), run_time=0.3)

        def jeton():
            j = VGroup(Circle(radius=0.3, fill_color=ALERTE, fill_opacity=1, stroke_width=0), code("+1", 22, FOND)).move_to(droite[8:10].get_center())
            return j

        def tour(n, lent):
            r = 1.0 if lent else 0.5
            s = surligne(droite, CIEL)
            self.play(Create(s), run_time=0.25 * r)
            j = jeton()
            self.play(FadeIn(j, scale=0.5), run_time=0.3 * r)
            self.play(Transform(s, surligne(gauche, ALERTE)), j.animate.move_to(c.fenetre.get_center()), run_time=0.5 * r)
            self.play(FadeOut(j, scale=0.3), v.animate.set_value(n + 1), bonnet.animate.move_to(dessus(n + 1) + DOWN * 4 * PX), run_time=0.45 * r)
            self.play(FadeOut(s), run_time=0.15 * r)

        self.next_section("à droite : la valeur actuelle, plus 1")
        p = phrase("à droite du =, Lua prend la valeur actuelle et ajoute 1 : un jeton +1")
        self.play(FadeIn(p), run_time=0.3)
        s = surligne(droite, CIEL)
        self.play(Create(s), run_time=0.3)
        j = jeton()
        self.play(FadeIn(j, scale=0.5), run_time=0.4)
        self.wait(0.5)

        self.next_section("à gauche : le résultat est stocké")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("à gauche du =, le jeton entre dans la boîte : compteur vaut 1, et le bonnet monte d'une marche")
        self.play(FadeIn(p), Transform(s, surligne(gauche, ALERTE)), j.animate.move_to(c.fenetre.get_center()), run_time=0.6)
        self.play(FadeOut(j, scale=0.3), v.animate.set_value(1), bonnet.animate.move_to(dessus(1) + DOWN * 4 * PX), run_time=0.5)
        self.play(FadeOut(s), run_time=0.2)
        self.wait(0.7)

        self.next_section("encore : la boîte compte, le bonnet monte")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("la même ligne, encore : à chaque fois, un jeton de plus et une marche de plus")
        self.play(FadeIn(p), run_time=0.3)
        tour(1, True)
        tour(2, False)
        tour(3, False)
        self.wait(0.5)

        self.next_section("dans le jeu : x = x + 1, un pixel par image")
        self.play(FadeOut(p), FadeOut(marches), FadeOut(numeros), FadeOut(bonnet), run_time=0.3)
        p = phrase("dans le jeu, x = x + 1 à chaque image : l'escalier est couché, le joueur avance d'un pixel")
        l2 = code("x = x + 1", 34).move_to(ligne)
        ecran = Ecran(px=0.024, centre=RIGHT * 1.2 + DOWN * 1.0)
        x = ValueTracker(20)
        jj = always_redraw(lambda: ecran.sprite("joueur", int(x.get_value()), 60, 2))
        cx = Compteur("x", x.get_value, chiffres=3).scale(0.9)
        cx.shift(c.fenetre.get_center() - cx.fenetre.get_center())
        self.remove(c)
        self.add(cx)
        self.play(FadeTransform(ligne, l2), FadeIn(p), FadeIn(ecran.cadre), FadeIn(jj), run_time=0.6)
        self.play(x.animate.set_value(180), run_time=2.4, rate_func=linear)
        self.wait(0.8)
