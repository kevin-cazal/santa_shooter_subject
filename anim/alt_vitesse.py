# Alternative manim aux trois GIF du vecteur vitesse (img/vitesse-ralenti.gif,
# vitesse-comparaison.gif, vitesse-diagonale.gif), en une scène à trois états :
# au ralenti, la position augmente de la vitesse à chaque image ; quatre
# missiles à quatre vitesses ; une vitesse en x et une en y font une diagonale.
#
#   capture.py anim anim/alt_vitesse.py LeVecteurVitesse -o img/alt-vitesse.webp --fps 30
from manim import *
from commun import *


class LeVecteurVitesse(Scene):
    def construct(self):
        ecran = Ecran(px=0.03, centre=UP * 0.9)
        self.add(ecran.cadre)

        # 1. Au ralenti.
        self.next_section("au ralenti : à chaque image, la position augmente de la vitesse")
        img = ValueTracker(0)
        mx = ValueTracker(8)
        m = always_redraw(lambda: ecran.sprite("missile", int(mx.get_value()), 60, 2))
        tag = always_redraw(lambda: etiquette(f"mx = {int(mx.get_value())}", ALERTE, 24).next_to(ecran.cadre, DOWN, buff=0.25).shift(LEFT * 2.5))
        c = Compteur("image", img.get_value, chiffres=1, couleur=CIEL).scale(0.6)
        c.shift(RIGHT * 2.5 + DOWN * 2.5 - c.fenetre.get_center())
        self.add(c, m, tag)
        p = phrase("au ralenti, vitesse +24 : à chaque image, mx augmente de 24. 8, puis 32, puis 56…")
        self.play(FadeIn(p), run_time=0.3)
        for i in range(1, 9):
            self.play(img.animate.set_value(i), run_time=0.25)
            self.play(mx.animate.set_value(8 + 24 * i), run_time=0.2)
        self.wait(0.8)
        self.play(FadeOut(p), FadeOut(m), FadeOut(tag), FadeOut(c), run_time=0.3)

        # 2. Quatre vitesses.
        self.next_section("quatre missiles, quatre vitesses")
        p = phrase("avec 0, le missile ne bouge pas. Avec -2, il recule. Plus la vitesse est grande, plus il va vite")
        t = ValueTracker(0)
        vitesses = (0, 1, -2, 3)
        missiles = VGroup()
        for n, v in enumerate(vitesses):
            yy = 20 + n * 28
            missiles.add(always_redraw(lambda v=v, yy=yy: ecran.sprite("missile", int(110 + v * t.get_value()), yy, 2)))
        labels = VGroup(*[etiquette(f"{v:+d}" if v else "0", ALERTE, 22).move_to(ecran.pos(14, 20 + n * 28 + 6)) for n, v in enumerate(vitesses)])
        fleches = VGroup(*[Arrow(ecran.pos(26, 20 + n * 28 + 6), ecran.pos(26 + v * 12, 20 + n * 28 + 6), buff=0, color=CIEL, stroke_width=4,
                                 max_tip_length_to_length_ratio=0.3) for n, v in enumerate(vitesses) if v])
        self.play(FadeIn(p), FadeIn(missiles), FadeIn(labels), FadeIn(fleches), run_time=0.4)
        self.play(t.animate.set_value(40), run_time=2.4, rate_func=linear)
        self.wait(0.6)
        self.play(FadeOut(p), FadeOut(missiles), FadeOut(labels), FadeOut(fleches), run_time=0.3)

        # 3. La diagonale.
        self.next_section("+2 sur x et +1 sur y : une diagonale")
        p = phrase("une vitesse de +2 sur x et de +1 sur y : l'objet avance en diagonale")
        t2 = ValueTracker(0)
        e = always_redraw(lambda: ecran.sprite("ennemi", int(30 + 2 * t2.get_value()), int(20 + t2.get_value()), 2))
        fx = always_redraw(lambda: Arrow(ecran.pos(30 + 2 * t2.get_value() + 8, 20 + t2.get_value() + 8), ecran.pos(30 + 2 * t2.get_value() + 8 + 24, 20 + t2.get_value() + 8), buff=0, color=ORANGE, stroke_width=4, max_tip_length_to_length_ratio=0.3))
        fy = always_redraw(lambda: Arrow(ecran.pos(30 + 2 * t2.get_value() + 8, 20 + t2.get_value() + 8), ecran.pos(30 + 2 * t2.get_value() + 8, 20 + t2.get_value() + 8 + 12), buff=0, color=BLEU, stroke_width=4, max_tip_length_to_length_ratio=0.3))
        fd = always_redraw(lambda: Arrow(ecran.pos(30 + 2 * t2.get_value() + 8, 20 + t2.get_value() + 8), ecran.pos(30 + 2 * t2.get_value() + 8 + 24, 20 + t2.get_value() + 8 + 12), buff=0, color=ALERTE, stroke_width=4, max_tip_length_to_length_ratio=0.3))
        leg = VGroup(etiquette("+2 sur x", ORANGE, 22), etiquette("+1 sur y", BLEU, 22), etiquette("la diagonale", ALERTE, 22)).arrange(RIGHT, buff=0.8).next_to(ecran.cadre, DOWN, buff=0.3)
        self.play(FadeIn(p), FadeIn(e), FadeIn(fx), FadeIn(fy), FadeIn(fd), FadeIn(leg), run_time=0.4)
        self.play(t2.animate.set_value(80), run_time=3.0, rate_func=linear)
        self.wait(0.8)
