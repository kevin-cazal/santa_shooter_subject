# Partie 2, boîte à outils « La boucle for » : i compte de 1 à 3 au compteur
# à rouleaux, chaque tour tamponne une étoile numérotée. Puis la borne devient
# un curseur : 3, 10, 50 étoiles.
#
#   capture.py anim anim/boucle_for.py LaBoucleFor -o img/outil-for.webp --fps 60
import random
from manim import *
from commun import *

random.seed(5)


class LaBoucleFor(Scene):
    def construct(self):
        self.next_section("i vaut 1, puis 2, puis 3 : trois tours, trois étoiles")
        prog = bloc_code(["for i = 1, 3 do", "  -- une étoile", "end"], 28).to_edge(LEFT, buff=0.7).shift(UP * 1.6)
        self.play(FadeIn(prog), run_time=0.5)
        v = ValueTracker(0)
        c = Compteur("i", v.get_value, chiffres=2).scale(0.85)
        c.shift(RIGHT * 0.1 + UP * 1.3 - c.fenetre.get_center())
        self.add(c)
        ecran = Ecran(px=0.022, centre=RIGHT * 4.0 + DOWN * 0.2)
        self.play(FadeIn(ecran.cadre), run_time=0.3)
        p = phrase("for i = 1, 3 : i compte de 1 à 3, une étoile par tour")
        self.play(FadeIn(p), run_time=0.3)
        s = surligne(prog[0], LU)
        self.play(Create(s), run_time=0.3)
        positions = [(random.uniform(10, 230), random.uniform(10, 126)) for _ in range(50)]
        etoiles = VGroup()
        for i in (1, 2, 3):
            s.set_y(prog[0].get_y())
            self.play(v.animate.set_value(i), run_time=0.5)
            s.set_y(prog[1].get_y())
            e = VGroup(Dot(radius=0.07, color=BLANC), code(str(i), 22, CHANGE)).arrange(RIGHT, buff=0.1).move_to(ecran.pos(*positions[i - 1]))
            self.play(FadeIn(e, scale=0.4), run_time=0.3)
            etoiles.add(e)
            self.wait(0.3)
        s.set_y(prog[2].get_y()); self.wait(0.4)
        self.play(FadeOut(s), FadeOut(p), run_time=0.2)
        p = phrase("après 3, la boucle s'arrête : trois étoiles")
        self.play(FadeIn(p), run_time=0.3); self.wait(1.2)

        self.next_section("la borne est un réglage : 10, puis 50 étoiles")
        self.play(FadeOut(p), run_time=0.2)
        reg = Reglage("nombre d'étoiles", 1, 50, 3, CHANGE).placer(LEFT * 3.4 + DOWN * 1.6)
        p = phrase("la borne de la boucle est un réglage : 10 étoiles")
        n_t = always_redraw(lambda: code(f"for i = 1, {int(reg.t.get_value())} do", 28).move_to(prog[0]).align_to(prog[0], LEFT))
        self.remove(prog[0]); self.add(n_t)
        self.play(FadeIn(reg), FadeIn(p), run_time=0.4)
        self.play(reg.t.animate.set_value(10), run_time=0.8)
        for i in range(4, 11):
            e = Dot(radius=0.06, color=BLANC).move_to(ecran.pos(*positions[i - 1]))
            self.play(v.animate.set_value(i), FadeIn(e, scale=0.5), run_time=0.18, rate_func=linear)
            etoiles.add(e)
        self.wait(0.8)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("50 : cinquante tours, cinquante étoiles, trois lignes de code")
        self.play(FadeIn(p), reg.t.animate.set_value(50), run_time=0.8)
        for i in range(11, 51):
            e = Dot(radius=random.randint(1, 3) * ecran.px * 0.55, color=BLANC).move_to(ecran.pos(*positions[i - 1]))
            self.play(v.animate.set_value(i), FadeIn(e, scale=0.5), run_time=0.05, rate_func=linear)
            etoiles.add(e)
        self.wait(1.6)
