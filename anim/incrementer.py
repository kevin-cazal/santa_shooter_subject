# Partie 1, boîte à outils « Incrémenter » : compteur = compteur + 1. Lua lit
# la valeur à droite, calcule, puis stocke le résultat à gauche. Trois tours,
# la boîte est un compteur à rouleaux.
#
#   capture.py anim anim/incrementer.py Incrementer -o img/outil-incrementer.webp --fps 30
from manim import *
from commun import *


class Incrementer(Scene):
    def construct(self):
        v = ValueTracker(0)
        c = Compteur("compteur", v.get_value, chiffres=1).scale(0.9)
        c.shift(LEFT * 3.2 + UP * 0.6 - c.fenetre.get_center())
        self.add(c)
        ligne = code("compteur = compteur + 1", 34).move_to(UP * 2.7)
        gauche, droite = ligne[0:8], ligne[9:19]      # un Text ne compte pas les espaces
        self.play(Write(ligne), run_time=0.9)
        calc = VGroup()

        def tour(n, lent):
            nonlocal calc
            # 1. À droite : lire.
            s = surligne(droite, CIEL)
            self.play(Create(s), run_time=0.3 if lent else 0.15)
            lu = code(str(n), 34, CIEL).move_to(RIGHT * 2.6 + UP * 0.6)
            plus = code(f"{n} + 1", 34, CIEL).move_to(RIGHT * 2.6 + UP * 0.6)
            self.play(FadeTransform(c.rouleaux.copy(), lu), run_time=0.5 if lent else 0.25)
            # 2. Calculer.
            self.play(FadeTransform(lu, plus), run_time=0.4 if lent else 0.2)
            res = code(str(n + 1), 34, ALERTE).move_to(plus)
            self.play(FadeTransform(plus, res), run_time=0.4 if lent else 0.2)
            # 3. À gauche : stocker.
            self.play(Transform(s, surligne(gauche, ALERTE)), run_time=0.3 if lent else 0.15)
            self.play(res.animate.move_to(c.fenetre.get_center()), v.animate.set_value(n + 1), run_time=0.6 if lent else 0.3)
            self.remove(res)
            self.play(FadeOut(s), run_time=0.2 if lent else 0.1)

        self.next_section("à droite : on lit la valeur")
        p = phrase("à droite du =, Lua lit la valeur de la boîte : 0")
        self.play(FadeIn(p), run_time=0.3)
        s = surligne(droite, CIEL)
        self.play(Create(s), run_time=0.3)
        lu = code("0", 34, CIEL).move_to(RIGHT * 2.6 + UP * 0.6)
        self.play(FadeTransform(c.rouleaux.copy(), lu), run_time=0.5)
        self.wait(0.6)

        self.next_section("on calcule : 0 + 1")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("puis il calcule : 0 + 1, ça fait 1")
        plus = code("0 + 1", 34, CIEL).move_to(lu)
        self.play(FadeIn(p), FadeTransform(lu, plus), run_time=0.5)
        res = code("1", 34, ALERTE).move_to(plus)
        self.play(FadeTransform(plus, res), run_time=0.4)
        self.wait(0.6)

        self.next_section("à gauche : on stocke le résultat")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("à gauche du =, le résultat est stocké dans la boîte : compteur vaut 1")
        self.play(FadeIn(p), Transform(s, surligne(gauche, ALERTE)), run_time=0.4)
        self.play(res.animate.move_to(c.fenetre.get_center()), v.animate.set_value(1), run_time=0.6)
        self.remove(res)
        self.play(FadeOut(s), run_time=0.2)
        self.wait(0.8)

        self.next_section("encore, et encore : la boîte compte")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("la même ligne, encore : lire, calculer, stocker. La boîte compte")
        self.play(FadeIn(p), run_time=0.3)
        tour(1, True)
        tour(2, False)
        tour(3, False)
        self.wait(0.4)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("dans le jeu, x = x + 1 à chaque image : le joueur avance")
        ecran = Ecran(px=0.02, centre=RIGHT * 3.2 + DOWN * 1.6)
        x = ValueTracker(20)
        j = always_redraw(lambda: ecran.sprite("joueur", int(x.get_value()), 60, 2))
        self.play(FadeIn(p), FadeIn(ecran.cadre), FadeIn(j), run_time=0.5)
        self.play(x.animate.set_value(160), run_time=1.6, rate_func=linear)
        self.wait(0.8)
