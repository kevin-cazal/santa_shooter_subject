# Partie 1, boîte à outils « Une variable », sous l'étape Input : la boîte x
# contient 20, et le jeu dessine le bonnet là où dit la boîte. Changer la boîte
# déplace le bonnet. Le piège : x = 20 écrit dans TIC() remplit la boîte à
# chaque tour, et le bonnet revient à 20 malgré la flèche. Hors de TIC(), la
# boîte est remplie une seule fois, et le bonnet avance.
#
#   capture.py anim anim/variable.py LaVariable -o img/outil-variable.webp --fps 30
from manim import *
from commun import *


class LaVariable(Scene):
    def construct(self):
        x = ValueTracker(20)
        ecran = Ecran(px=0.026, centre=RIGHT * 3.2 + UP * 0.9)
        bonnet = always_redraw(lambda: ecran.sprite("joueur", int(x.get_value()), 60, 2))
        etiq = always_redraw(lambda: VGroup(origine(ecran.pos(int(x.get_value()), 60)),
                                            etiquette(f"x = {int(x.get_value())}", ALERTE, 22).next_to(ecran.pos(int(x.get_value()) + 8, 60), UP, buff=0.15)))
        boite = Boite("x", 20, centre=LEFT * 3.4 + DOWN * 0.9)
        tours = ValueTracker(0)
        cpt = Compteur("tour", tours.get_value, chiffres=2, couleur=CIEL).scale(0.65)
        cpt.shift(RIGHT * 3.2 + DOWN * 2.5 - cpt.fenetre.get_center())
        touche = manette("→").move_to(LEFT * 3.4 + DOWN * 2.6)

        # 1. Une boîte, et le bonnet est là où elle dit.
        self.next_section("x = 20 : une boîte, et le bonnet est à 20")
        ligne = code("x = 20", 32).to_edge(LEFT, buff=0.8).shift(UP * 2.4)
        self.play(Write(ligne), run_time=0.6)
        p = phrase("la boîte x contient 20 : le bonnet est dessiné à x = 20")
        self.play(FadeIn(p), run_time=0.3)
        boite.poser(self)
        self.play(FadeIn(ecran.cadre), run_time=0.3)
        self.play(FadeTransform(boite.val.copy(), etiq), FadeIn(bonnet), run_time=0.6)
        g = guides(ecran, 20, 60)
        self.play(Create(g), run_time=0.5); self.wait(1.0)
        self.play(FadeOut(g), run_time=0.3)

        # 2. Changer la boîte déplace le bonnet.
        self.next_section("changer la boîte, c'est déplacer le bonnet")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("x = 120 : la boîte change, le bonnet est dessiné à 120")
        l2 = code("x = 120", 32).move_to(ligne).align_to(ligne, LEFT)
        self.play(FadeIn(p), FadeTransform(ligne, l2), run_time=0.5)
        ligne = l2
        boite.changer(self, 120)
        self.play(x.animate.set_value(120), run_time=0.8)
        self.wait(0.8)

        # 3. Le piège : dans TIC(), la boîte est remplie à chaque tour.
        self.next_section("dans TIC() : la boîte est remplie à chaque tour")
        self.play(FadeOut(p), FadeOut(ligne), run_time=0.2)
        prog = bloc_code(["function TIC()", "  x = 20", "  -- la flèche fait", "  -- avancer x", "end"], 24).to_edge(LEFT, buff=0.8).shift(UP * 1.9)
        self.add(cpt, touche)
        boite.changer(self, 20, run_time=0.2)
        x.set_value(20)
        p = phrase("x = 20 dans TIC() : à chaque tour la boîte est remise à 20")
        # Le tuyau part à droite de la ligne, contourne le bloc de code par la droite, et descend dans la boîte.
        xd = prog.get_right()[0] + 0.4
        yl = prog[1].get_right()[1]
        yc = boite.cadre.get_top()[1] + 0.3
        tuyau = VGroup(Line(prog[1].get_right() + RIGHT * 0.15, np.array([xd, yl, 0]), stroke_color=ALERTE, stroke_width=5),
                       Line(np.array([xd, yl, 0]), np.array([xd, yc, 0]), stroke_color=ALERTE, stroke_width=5),
                       Line(np.array([xd, yc, 0]), np.array([boite.cadre.get_center()[0], yc, 0]), stroke_color=ALERTE, stroke_width=5),
                       Line(np.array([boite.cadre.get_center()[0], yc, 0]), boite.cadre.get_top(), stroke_color=ALERTE, stroke_width=5))
        self.play(FadeIn(prog), FadeIn(p), Create(tuyau), run_time=0.6)
        self.play(Transform(touche, manette("→", True).move_to(touche)), run_time=0.15)
        for t in range(1, 5):
            # La flèche fait avancer x… et la ligne le remet à 20.
            self.play(tours.animate.set_value(t), x.animate.set_value(26), run_time=0.35, rate_func=linear)
            self.remove(boite.val); boite.val = code("26", 30, BLANC).move_to(boite.cadre); self.add(boite.val)
            s = surligne(prog[1])
            self.play(Create(s), run_time=0.15)
            self.play(FadeOut(s), x.animate.set_value(20), run_time=0.2)
            self.remove(boite.val); boite.val = code("20", 30, BLANC).move_to(boite.cadre); self.add(boite.val)
        self.play(Transform(touche, manette("→").move_to(touche)), run_time=0.15)
        self.wait(0.6)

        # 4. Hors de TIC() : une seule fois.
        self.next_section("hors de TIC() : remplie une seule fois, le bonnet avance")
        self.play(FadeOut(p), FadeOut(tuyau), run_time=0.3)
        prog2 = bloc_code(["x = 20", "", "function TIC()", "  -- la flèche fait", "  -- avancer x", "end"], 24).move_to(prog).align_to(prog, LEFT)
        p = phrase("x = 20 hors de TIC() : remplie une seule fois, le bonnet avance")
        self.play(FadeTransform(prog, prog2), FadeIn(p), run_time=0.6)
        self.play(Transform(touche, manette("→", True).move_to(touche)), run_time=0.15)
        for t in range(5, 9):
            self.play(tours.animate.set_value(t), x.animate.set_value(x.get_value() + 24), run_time=0.4, rate_func=linear)
            self.remove(boite.val); boite.val = code(str(int(x.get_value())), 30, BLANC).move_to(boite.cadre); self.add(boite.val)
        self.play(Transform(touche, manette("→").move_to(touche)), run_time=0.15)
        self.wait(1.2)
