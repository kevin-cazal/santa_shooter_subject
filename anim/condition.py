# Partie 1, boîte à outils « if » : la condition est vraie, le bloc s'exécute ;
# fausse, Lua saute au end. Puis le lien avec le jeu : si la flèche est
# appuyée, le joueur avance.
#
#   capture.py anim anim/condition.py LaCondition -o img/outil-if.webp --fps 30
from manim import *
from commun import *


class LaCondition(Scene):
    def construct(self):
        prog = bloc_code(["temperature = 35", "", "if temperature > 30 then", '  print("il fait chaud")', "end"], 26)
        prog.to_edge(LEFT, buff=0.7).shift(UP * 1.0)
        b = Boite("temperature", 35, centre=RIGHT * 1.6 + UP * 2.4)
        con = Console(self, RIGHT * 3.4 + DOWN * 0.4, largeur=4.2, hauteur=1.8, lignes=3)
        self.play(FadeIn(prog), run_time=0.6)
        b.poser(self)

        def passage(val, vrai):
            s = surligne(prog[2])
            self.play(Create(s), run_time=0.3)
            test = code(f"{val} > 30", 30, CIEL).next_to(b.cadre, DOWN, buff=0.35)
            self.play(FadeTransform(b.val.copy(), test), run_time=0.5)
            verdict = code("vrai" if vrai else "faux", 30, VERT if vrai else ROUGE).move_to(test)
            self.play(FadeTransform(test, verdict), run_time=0.5)
            if vrai:
                s.set_y(prog[3].get_y())
                self.wait(0.3)
                con.ecrire("il fait chaud")
            else:
                s.set_y(prog[4].get_y())
                self.wait(0.6)
            self.play(FadeOut(s), FadeOut(verdict), run_time=0.3)

        self.next_section("35 > 30 est vrai : le bloc s'exécute")
        p = phrase("la condition est vraie : Lua entre dans le bloc, et print s'exécute")
        self.play(FadeIn(p), run_time=0.3)
        passage(35, True)
        self.wait(0.8)

        self.next_section("20 > 30 est faux : Lua saute au end")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("avec 20, la condition est fausse : Lua saute directement au end, rien ne s'affiche")
        self.play(FadeIn(p), run_time=0.3)
        self.play(*[FadeOut(l) for l in con.lignes], run_time=0.3)
        con.lignes.clear()
        b.changer(self, 20)
        passage(20, False)
        self.wait(0.8)

        self.next_section("dans le jeu : si la flèche est appuyée")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("dans le jeu, la condition est un bouton : appuyé, le joueur avance ; relâché, rien")
        prog2 = bloc_code(["if btn(3) then", "  -- avancer", "end"], 26).move_to(prog).align_to(prog, LEFT)
        self.play(FadeTransform(prog, prog2), FadeIn(p), run_time=0.7)
        ecran = Ecran(px=0.016, centre=RIGHT * 3.6 + DOWN * 2.0)
        x = ValueTracker(40)
        j = always_redraw(lambda: ecran.sprite("joueur", int(x.get_value()), 60, 2))
        k = manette("→").next_to(ecran.cadre, LEFT, buff=0.3)
        self.play(FadeIn(ecran.cadre), FadeIn(j), FadeIn(k), run_time=0.4)
        for appui in (True, False, True):
            self.play(Transform(k, manette("→", appui).move_to(k)), run_time=0.15)
            if appui:
                self.play(x.animate.set_value(x.get_value() + 60), run_time=1.0, rate_func=linear)
            else:
                self.wait(0.8)
        self.wait(0.8)
