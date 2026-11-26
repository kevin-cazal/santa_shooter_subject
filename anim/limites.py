# Partie 1, « Rester dans les limites de l'écran » : les quatre bords, et le
# piège du bord droit et du bord bas — x est le coin gauche du sprite, pas son
# bord droit. Les conditions restent à écrire : on montre les nombres, pas le if.
#
#   capture.py anim anim/limites.py LesLimites -o img/limites-bords.webp --fps 30
from manim import *
from commun import *


class LesLimites(Scene):
    def construct(self):
        ecran = Ecran(px=0.045, centre=UP * 0.1)
        px, py = ValueTracker(116), ValueTracker(64)
        joueur = always_redraw(lambda: VGroup(
            ecran.boite(int(px.get_value()), int(py.get_value()), couleur=ALERTE, largeur=2),
            ecran.sprite("joueur", int(px.get_value()), int(py.get_value())),
            origine(ecran.pos(int(px.get_value()), int(py.get_value())), rayon=0.07)))
        tag = always_redraw(lambda: etiquette(f"x = {int(px.get_value())}   y = {int(py.get_value())}", ALERTE, 24)
                            .next_to(ecran.cadre.get_corner(UR), DL, buff=0.25))
        self.add(ecran.cadre, ecran.axes(), joueur, tag)
        self.wait(0.5)

        def bord(a, b):
            return Line(a, b, stroke_color=CIEL, stroke_width=6)

        # 1. À gauche.
        self.next_section("à gauche : x vaut 0")
        p = phrase("au bord gauche, x vaut 0 : plus petit, le joueur sortirait")
        self.play(px.animate.set_value(0), run_time=1.2)
        g = bord(ecran.cadre.get_corner(UL), ecran.cadre.get_corner(DL))
        self.play(Create(g), FadeIn(p), run_time=0.5)
        self.wait(1.3)

        # 2. En haut.
        self.next_section("en haut : y vaut 0")
        self.play(FadeOut(p), FadeOut(g), run_time=0.3)
        p = phrase("au bord haut, y vaut 0")
        self.play(py.animate.set_value(0), run_time=1.0)
        g = bord(ecran.cadre.get_corner(UL), ecran.cadre.get_corner(UR))
        self.play(Create(g), FadeIn(p), run_time=0.5)
        self.wait(1.2)

        # 3. À droite : le piège.
        self.next_section("à droite : x n'est pas le bord droit du sprite")
        self.play(FadeOut(p), FadeOut(g), py.animate.set_value(64), run_time=0.5)
        p = phrase("x = 240 : le sprite est déjà sorti de l'écran")
        self.play(px.animate.set_value(240), run_time=1.4)
        self.play(FadeIn(p), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("son bord droit, c'est x + 8 : il touche le bord quand x + 8 vaut 240")
        self.play(px.animate.set_value(232), run_time=0.8)
        acc = BraceBetweenPoints(ecran.pos(232, 73), ecran.pos(240, 73), direction=DOWN, color=ALERTE)
        huit = texte("8", 20, ALERTE).next_to(acc, DOWN, buff=0.08)
        g = bord(ecran.cadre.get_corner(UR), ecran.cadre.get_corner(DR))
        self.play(Create(g), FadeIn(acc), FadeIn(huit), FadeIn(p), run_time=0.5)
        self.wait(1.8)

        # 4. En bas : pareil.
        self.next_section("en bas : y + 8 vaut 136")
        self.play(FadeOut(p), FadeOut(g), FadeOut(acc), FadeOut(huit), run_time=0.3)
        p = phrase("en bas, pareil : le sprite touche le bord quand y + 8 vaut 136")
        self.play(py.animate.set_value(128), run_time=1.0)
        acc = BraceBetweenPoints(ecran.pos(241, 128), ecran.pos(241, 136), direction=RIGHT, color=ALERTE)
        huit = texte("8", 20, ALERTE).next_to(acc, RIGHT, buff=0.08)
        g = bord(ecran.cadre.get_corner(DL), ecran.cadre.get_corner(DR))
        self.play(Create(g), FadeIn(acc), FadeIn(huit), FadeIn(p), run_time=0.5)
        self.wait(1.6)

        self.play(FadeOut(p), FadeOut(g), FadeOut(acc), FadeOut(huit), run_time=0.3)
        p = phrase("quatre bords, quatre conditions : deux sur x, deux sur y")
        self.play(FadeIn(p), px.animate.set_value(116), py.animate.set_value(64), run_time=1.0)
        self.wait(1.5)
