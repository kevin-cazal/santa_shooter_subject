# Partie 1, boîte à outils « if » : la condition est une barrière sur un
# chemin. Un thermomètre avec un trait rouge à 30 : au-dessus, la barrière
# s'ouvre et le ventilateur tourne ; en dessous, elle reste fermée. Puis la
# barrière devient la flèche du clavier : appuyée, le joueur avance.
#
#   capture.py anim anim/condition.py LaCondition -o img/outil-if.webp --fps 30
from manim import *
from commun import *


class LaCondition(Scene):
    def construct(self):
        prog = bloc_code(["temperature = 35", "", "if temperature > 30 then", "  ventilateur()", "end"], 24)
        prog.to_edge(LEFT, buff=0.6).shift(UP * 1.6)
        self.play(FadeIn(prog), run_time=0.5)

        # Le thermomètre : un tube, du mercure dont la hauteur suit la valeur, un trait rouge à 30.
        bas, haut = DOWN * 2.3, UP * 1.5
        tube = RoundedRectangle(width=0.5, height=3.8, corner_radius=0.25, stroke_color=DOUX, stroke_width=3).move_to(LEFT * 0.6 + DOWN * 0.4)
        temp = ValueTracker(0)
        y0, y1 = tube.get_bottom()[1] + 0.3, tube.get_top()[1] - 0.3

        def ytemp(t):
            return y0 + (y1 - y0) * t / 50

        mercure = always_redraw(lambda: Rectangle(width=0.26, height=max(0.01, ytemp(temp.get_value()) - y0), fill_color=ROUGE, fill_opacity=1, stroke_width=0)
                                .move_to(np.array([tube.get_center()[0], (y0 + ytemp(temp.get_value())) / 2, 0])))
        seuil = Line(tube.get_left() + LEFT * 0.25, tube.get_right() + RIGHT * 0.25, stroke_color=ALERTE, stroke_width=4).set_y(ytemp(30))
        seuil_t = code("30", 20, ALERTE).next_to(seuil, LEFT, buff=0.12)
        lecture = always_redraw(lambda: code(str(int(temp.get_value())), 24, BLANC).next_to(tube, UP, buff=0.15))
        nom = code("temperature", 20, DOUX).next_to(tube, DOWN, buff=0.15)
        self.play(FadeIn(tube), FadeIn(mercure), FadeIn(seuil), FadeIn(seuil_t), FadeIn(lecture), FadeIn(nom), run_time=0.5)

        # La barrière, sur le chemin vers le bloc ; le ventilateur derrière.
        pivot = [RIGHT * 2.2 + DOWN * 0.8]      # une liste : le pivot bouge quand la barrière glisse à gauche
        barre = Line(pivot[0], pivot[0] + RIGHT * 1.6, stroke_color=ROUGE, stroke_width=10)
        poteau = Dot(pivot[0], radius=0.12, color=DOUX)
        chemin = Line(RIGHT * 0.2 + DOWN * 0.8, RIGHT * 4.4 + DOWN * 0.8, stroke_color=GRIS, stroke_width=2)
        centre_v = RIGHT * 5.0 + DOWN * 0.8
        pales = VGroup(*[Line(centre_v, centre_v + 0.6 * np.array([np.cos(a), np.sin(a), 0]), stroke_color=CIEL, stroke_width=8)
                         for a in (0, PI / 2, PI, 3 * PI / 2)])
        moyeu = Dot(centre_v, radius=0.1, color=BLANC)
        bloc = code("ventilateur()", 20, DOUX).next_to(pales, DOWN, buff=0.45)
        self.play(FadeIn(chemin), FadeIn(poteau), FadeIn(barre), FadeIn(pales), FadeIn(moyeu), FadeIn(bloc), run_time=0.5)

        def ouvrir():
            barre.set_color(VERT)
            self.play(Rotate(barre, PI / 2, about_point=pivot[0]), run_time=0.5)

        def fermer():
            self.play(Rotate(barre, -PI / 2, about_point=pivot[0]), run_time=0.4)
            barre.set_color(ROUGE)

        # 1. Vrai.
        self.next_section("35 > 30 : la barrière s'ouvre, le bloc s'exécute")
        p = phrase("35 est au-dessus du trait 30 : la condition est vraie, la barrière s'ouvre, le ventilateur tourne")
        s = surligne(prog[2])
        self.play(FadeIn(p), temp.animate.set_value(35), Create(s), run_time=0.9)
        ouvrir()
        s.set_y(prog[3].get_y())
        self.play(Rotate(pales, 2 * TAU, about_point=centre_v), run_time=1.6, rate_func=linear)
        self.wait(0.4)
        fermer()
        self.play(FadeOut(s), run_time=0.2)

        # 2. Faux.
        self.next_section("20 > 30 : fermée, Lua saute au end")
        self.play(FadeOut(p), run_time=0.2)
        l0 = code("temperature = 20", 24).move_to(prog[0]).align_to(prog[0], LEFT)
        p = phrase("20 est sous le trait : la condition est fausse, la barrière reste fermée, Lua saute au end")
        self.play(FadeTransform(prog[0], l0), temp.animate.set_value(20), FadeIn(p), run_time=0.9)
        s = surligne(prog[2])
        self.play(Create(s), run_time=0.3)
        self.play(Indicate(barre, color=ROUGE, scale_factor=1.1), run_time=0.5)
        s.set_y(prog[4].get_y())
        self.wait(0.9)
        self.play(FadeOut(s), run_time=0.2)

        # 3. Dans le jeu.
        self.next_section("dans le jeu : la barrière est un bouton")
        self.play(FadeOut(p), FadeOut(tube), FadeOut(mercure), FadeOut(seuil), FadeOut(seuil_t), FadeOut(lecture), FadeOut(nom),
                  FadeOut(pales), FadeOut(moyeu), FadeOut(bloc), FadeOut(l0), run_time=0.4)
        self.remove(prog[0])
        prog2 = bloc_code(["if btn(3) then", "  -- avancer", "end"], 24).move_to(prog[2:]).align_to(prog, LEFT)
        self.play(FadeOut(prog[1:]), run_time=0.2)
        p = phrase("dans le jeu, la condition est un bouton : appuyé, la barrière s'ouvre et le joueur avance")
        # La barrière glisse à gauche, l'écran du jeu prend la droite.
        self.play(VGroup(chemin, poteau, barre).animate.shift(LEFT * 3.6), run_time=0.5)
        pivot[0] = pivot[0] + LEFT * 3.6
        ecran = Ecran(px=0.018, centre=RIGHT * 4.4 + DOWN * 0.8)
        x = ValueTracker(30)
        j = always_redraw(lambda: ecran.sprite("joueur", int(x.get_value()), 60, 2))
        k = manette("→").move_to(LEFT * 4.4 + DOWN * 0.8)
        self.play(FadeIn(prog2), FadeIn(p), FadeIn(ecran.cadre), FadeIn(j), FadeIn(k), run_time=0.5)
        for appui in (True, False, True):
            self.play(Transform(k, manette("→", appui).move_to(k)), run_time=0.15)
            if appui:
                ouvrir()
                self.play(x.animate.set_value(x.get_value() + 70), run_time=1.0, rate_func=linear)
                fermer()
            else:
                self.play(Indicate(barre, color=ROUGE, scale_factor=1.1), run_time=0.5)
                self.wait(0.4)
        self.wait(0.8)
