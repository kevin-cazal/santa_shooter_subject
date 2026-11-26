# Partie 1, « Rester dans les limites de l'écran » : les quatre bords, les
# nombres collés au bonnet avec son point d'origine et ses guides, et une loupe
# sur le bord droit pour voir x + 8 = 240 pixel par pixel. Les conditions
# restent à écrire : on montre les nombres, pas le if.
#
#   capture.py anim anim/limites.py LesLimites -o img/limites-bords.webp --fps 30
from manim import *
from commun import *


class LesLimites(Scene):
    def construct(self):
        ecran = Ecran(px=0.032, centre=LEFT * 1.6 + UP * 0.3)
        px, py = ValueTracker(116), ValueTracker(64)
        joueur = always_redraw(lambda: VGroup(
            ecran.boite(int(px.get_value()), int(py.get_value()), couleur=CHANGE, largeur=2),
            ecran.sprite("joueur", int(px.get_value()), int(py.get_value())),
            origine(ecran.pos(int(px.get_value()), int(py.get_value())), rayon=0.07)))
        def etiq_f():
            x, y = int(px.get_value()), int(py.get_value())
            e = etiquette(f"x = {x}  y = {y}", CHANGE, 22)
            # Collée au bonnet : au-dessus, ou en dessous près du bord haut ; jamais hors du cadre.
            e.next_to(ecran.pos(x + 4, y + 8), DOWN, buff=0.3) if y < 20 else e.next_to(ecran.pos(x + 4, y), UP, buff=0.3)
            g, d = ecran.cadre.get_left()[0] + 0.1, ecran.cadre.get_right()[0] + 0.8
            if e.get_left()[0] < g:
                e.shift(RIGHT * (g - e.get_left()[0]))
            if e.get_right()[0] > d:
                e.shift(LEFT * (e.get_right()[0] - d))
            return e
        etiq = always_redraw(etiq_f)
        gd = always_redraw(lambda: guides(ecran, int(px.get_value()), int(py.get_value())))
        self.add(ecran.cadre, ecran.axes(), gd, joueur, etiq)
        self.wait(0.5)

        def bord(a, b):
            return Line(a, b, stroke_color=LU, stroke_width=6)

        self.next_section("à gauche : x vaut 0")
        p = phrase("bord gauche : x = 0")
        self.play(px.animate.set_value(0), run_time=1.2)
        g = bord(ecran.cadre.get_corner(UL), ecran.cadre.get_corner(DL))
        self.play(Create(g), FadeIn(p), run_time=0.5); self.wait(1.2)

        self.next_section("en haut : y vaut 0")
        self.play(FadeOut(p), FadeOut(g), run_time=0.3)
        p = phrase("bord haut : y = 0")
        self.play(py.animate.set_value(0), run_time=1.0)
        g = bord(ecran.cadre.get_corner(UL), ecran.cadre.get_corner(UR))
        self.play(Create(g), FadeIn(p), run_time=0.5); self.wait(1.2)

        self.next_section("à droite : x n'est pas le bord droit du sprite")
        self.play(FadeOut(p), FadeOut(g), py.animate.set_value(64), run_time=0.5)
        p = phrase("x = 240 : le sprite est déjà sorti de l'écran")
        self.play(px.animate.set_value(240), run_time=1.4)
        self.play(FadeIn(p), run_time=0.4); self.wait(1.2)
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("son bord droit est x + 8 : il touche le bord quand x + 8 = 240")
        self.play(px.animate.set_value(232), run_time=0.8)
        # La loupe sur le bord droit : les 8 pixels du sprite, puis le bord.
        PXL = 0.16
        coin = RIGHT * 3.6 + UP * 1.3
        pos = lambda x, y: coin + RIGHT * (x - 228) * PXL + DOWN * (y - 64) * PXL
        loupe = VGroup(*[Line(pos(x, 62), pos(x, 74), stroke_color=DOUX, stroke_width=1, stroke_opacity=0.25) for x in range(228, 243)],
                       *[Line(pos(228, y), pos(242, y), stroke_color=DOUX, stroke_width=1, stroke_opacity=0.25) for y in range(62, 75)],
                       sprite("joueur", PXL, 1, pos(232, 64)), origine(pos(232, 64), rayon=0.09),
                       Line(pos(240, 62), pos(240, 74), stroke_color=LU, stroke_width=6),
                       BraceBetweenPoints(pos(232, 73), pos(240, 73), direction=DOWN, color=CHANGE),
                       code("8", 22, CHANGE).move_to(pos(236, 76)), code("240", 20, LU).next_to(pos(240, 62), UP, buff=0.1))
        cadre_loupe = Rectangle(width=14 * PXL, height=12 * PXL, stroke_color=CHANGE, stroke_width=2).move_to(pos(235, 68))
        zone = Rectangle(width=14 * ecran.px, height=12 * ecran.px, stroke_color=CHANGE, stroke_width=1.5).move_to(ecran.pos(235, 68))
        g = bord(ecran.cadre.get_corner(UR), ecran.cadre.get_corner(DR))
        self.play(Create(g), FadeIn(p), run_time=0.4)
        lien = Line(zone.get_corner(UR), cadre_loupe.get_corner(UL), stroke_color=CHANGE, stroke_width=1.5)
        self.play(FadeIn(zone), FadeIn(loupe), FadeIn(cadre_loupe), Create(lien), run_time=0.7)
        self.wait(2.0)
        self.play(FadeOut(loupe), FadeOut(cadre_loupe), FadeOut(zone), FadeOut(lien), FadeOut(p), FadeOut(g), run_time=0.4)

        self.next_section("en bas : y + 8 vaut 136")
        p = phrase("bord bas : pareil, le sprite touche quand y + 8 = 136")
        self.play(py.animate.set_value(128), run_time=1.0)
        acc = BraceBetweenPoints(ecran.pos(241, 128), ecran.pos(241, 136), direction=RIGHT, color=CHANGE)
        huit = code("8", 22, CHANGE).next_to(acc, RIGHT, buff=0.08)
        g = bord(ecran.cadre.get_corner(DL), ecran.cadre.get_corner(DR))
        self.play(Create(g), FadeIn(acc), FadeIn(huit), FadeIn(p), run_time=0.5); self.wait(1.6)

        self.play(FadeOut(p), FadeOut(g), FadeOut(acc), FadeOut(huit), run_time=0.3)
        p = phrase("quatre bords, quatre conditions : deux sur x, deux sur y")
        self.play(FadeIn(p), px.animate.set_value(116), py.animate.set_value(64), run_time=1.0); self.wait(1.4)
