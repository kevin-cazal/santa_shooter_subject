# Partie 2, boîte à outils « La boucle for » : i compte de 1 à 3, le bloc
# s'exécute à chaque tour. Puis for i = 1, 50 : cinquante tours, cinquante
# étoiles dans le ciel. La boucle est un compteur à rouleaux.
#
#   capture.py anim anim/boucle_for.py LaBoucleFor -o img/outil-for.webp --fps 60
import random
from manim import *
from commun import *

random.seed(5)


class LaBoucleFor(Scene):
    def construct(self):
        self.next_section("i vaut 1, puis 2, puis 3 : trois tours")
        prog = bloc_code(["for i = 1, 3 do", "  print(i)", "end"], 28).to_edge(LEFT, buff=0.7).shift(UP * 1.6)
        self.play(FadeIn(prog), run_time=0.5)
        v = ValueTracker(0)
        c = Compteur("i", v.get_value, chiffres=2).scale(0.85)
        c.shift(RIGHT * 0.1 + UP * 1.3 - c.fenetre.get_center())
        self.add(c)
        con = Console(self, RIGHT * 4.0 + UP * 1.2, largeur=3.6, hauteur=2.0, lignes=3)
        p = phrase("for i = 1, 3 : i prend chaque valeur de 1 à 3, et le bloc s'exécute à chaque tour")
        self.play(FadeIn(p), run_time=0.3)
        s = surligne(prog[0])
        self.play(Create(s), run_time=0.3)
        for i in (1, 2, 3):
            s.set_y(prog[0].get_y())
            self.play(v.animate.set_value(i), run_time=0.5)
            s.set_y(prog[1].get_y())
            con.ecrire(str(i), run_time=0.3)
            self.wait(0.2)
        s.set_y(prog[2].get_y())
        self.wait(0.3)
        self.play(FadeOut(s), run_time=0.2)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("trois tours, trois lignes. Après 3, la boucle s'arrête")
        self.play(FadeIn(p), run_time=0.3)
        self.wait(1.0)

        self.next_section("for i = 1, 50 : cinquante étoiles")
        self.play(FadeOut(p), FadeOut(con.cadre), FadeOut(con.titre), *[FadeOut(l) for l in con.lignes], run_time=0.3)
        prog2 = bloc_code(["for i = 1, 50 do", "  -- une étoile", "end"], 28).move_to(prog).align_to(prog, LEFT)
        self.play(FadeTransform(prog, prog2), v.animate.set_value(0), run_time=0.6)
        p = phrase("for i = 1, 50 : cinquante tours, et à chaque tour une étoile de plus dans le ciel")
        ecran = Ecran(px=0.022, centre=RIGHT * 4.0 + DOWN * 0.2)
        self.play(FadeIn(p), FadeIn(ecran.cadre), run_time=0.4)
        etoiles = [Dot(radius=random.randint(1, 3) * ecran.px * 0.55, color=BLANC).move_to(ecran.pos(random.uniform(2, 238), random.uniform(2, 134)))
                   for _ in range(50)]
        s = surligne(prog2[1])
        self.add(s)
        for i, e in enumerate(etoiles, start=1):
            d = 0.22 if i <= 5 else (0.1 if i <= 15 else 0.045)
            self.play(v.animate.set_value(i), FadeIn(e, scale=0.5), run_time=d, rate_func=linear)
        self.play(FadeOut(s), run_time=0.2)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("une boucle, c'est ce qui fait 50 étoiles avec trois lignes")
        self.play(FadeIn(p), run_time=0.3)
        self.wait(1.4)
