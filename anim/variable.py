# Partie 1, boîte à outils « Une variable » : une boîte avec un nom, qui stocke
# une valeur ; print la lit. Puis le piège : créée dans TIC(), la boîte est
# refaite à chaque tour, et sa valeur ne bouge jamais.
#
#   capture.py anim anim/variable.py LaVariable -o img/outil-variable.webp --fps 30
from manim import *
from commun import *


class LaVariable(Scene):
    def construct(self):
        # 1. Une boîte.
        self.next_section("vies = 3 : une boîte, un nom, une valeur")
        ligne = code("vies = 3", 32).move_to(UP * 2.6)
        self.play(Write(ligne), run_time=0.8)
        p = phrase("une variable stocke une valeur : une boîte, un nom dessus, une valeur dedans")
        b = Boite("vies", 3, centre=LEFT * 3 + UP * 0.4)
        self.play(FadeIn(p), run_time=0.3)
        self.play(FadeTransform(ligne[0:4].copy(), b.nom), FadeIn(b.cadre), run_time=0.7)
        self.play(FadeTransform(ligne[5:6].copy(), b.val), run_time=0.6)
        self.wait(1.0)

        # 2. print lit la boîte.
        self.next_section("print(vies) lit la boîte")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("print(vies) lit ce qu'il y a dans la boîte, et l'affiche")
        l2 = code("print(vies)", 32).next_to(ligne, DOWN, buff=0.3)
        con = Console(self, RIGHT * 3 + UP * 0.2)
        self.play(FadeIn(p), Write(l2), run_time=0.8)
        s = surligne(b.cadre, CIEL)
        self.play(Create(s), run_time=0.3)
        v = b.val.copy()
        self.play(v.animate.move_to(con.cadre.get_center()), run_time=0.6)
        self.remove(v)
        con.ecrire("3")
        self.play(FadeOut(s), run_time=0.2)
        self.wait(1.0)

        # 3. Le piège.
        self.next_section("dans TIC() : refaite à chaque tour")
        self.play(FadeOut(p), FadeOut(ligne), FadeOut(l2), FadeOut(con.cadre), FadeOut(con.titre), *[FadeOut(l) for l in con.lignes], run_time=0.3)
        prog = bloc_code(["function TIC()", "  vies = 3", "  vies = vies - 1", "end"], 26).move_to(UP * 2.3)
        p = phrase("dans TIC(), la ligne vies = 3 est refaite à chaque tour, et la valeur ne bouge jamais")
        tours = ValueTracker(0)
        # Le compteur avant la phrase : ses caches, couleur du fond, passeraient dessus.
        c = Compteur("tour", tours.get_value, chiffres=2, couleur=CIEL).scale(0.7)
        c.shift(RIGHT * 3 + DOWN * 1.9 - c.fenetre.get_center())
        self.add(c)
        self.play(FadeIn(prog), FadeIn(p), run_time=0.5)
        s = surligne(prog[1])
        self.play(Create(s), run_time=0.3)
        for t in range(1, 5):
            s.set_y(prog[1].get_y())
            b.changer(self, 3, run_time=0.25)
            s.set_y(prog[2].get_y())
            b.changer(self, 2, run_time=0.25)
            self.play(tours.animate.set_value(t), run_time=0.3)
        self.wait(0.4)
        self.play(FadeOut(p), FadeOut(s), run_time=0.2)
        p = phrase("crée tes variables en haut du code, hors de TIC() : une seule fois")
        prog2 = bloc_code(["vies = 3", "", "function TIC()", "  vies = vies - 1", "end"], 26).move_to(prog)
        self.play(FadeTransform(prog, prog2), FadeIn(p), run_time=0.7)
        for t in range(5, 9):
            b.changer(self, 2 - (t - 5) - 1 + 1, run_time=0.25)
            self.play(tours.animate.set_value(t), run_time=0.3)
        self.wait(1.2)
