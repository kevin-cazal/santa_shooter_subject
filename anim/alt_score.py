# Alternative manim au GIF img/collision-tir-score.gif : le missile touche
# l'ennemi, les deux disparaissent, le score passe de 0 à 100, puis à 200.
#
#   capture.py anim anim/alt_score.py LeScore -o img/alt-collision-tir-score.webp --fps 30 --no-video
from manim import *
from commun import *

JX, JY = 24, 60


class LeScore(Scene):
    def construct(self):
        ecran = Ecran(px=0.03, centre=UP * 0.6)
        mx = ValueTracker(-24)
        ex, ey = ValueTracker(250), ValueTracker(60)
        score = ValueTracker(0)
        j = ecran.sprite("joueur", JX, JY, 2)
        m = always_redraw(lambda: ecran.sprite_clippe("missile", int(mx.get_value()), JY, 2))

        e = always_redraw(lambda: ecran.sprite_clippe("ennemi", int(ex.get_value()), int(ey.get_value()), 2))
        texte_score = always_redraw(lambda: code(f"SCORE: {int(score.get_value())}", 22, BLANC).move_to(ecran.pos(40, 8)))
        k = manette("Z").move_to(DOWN * 2.5)
        self.add(ecran.cadre, j, m, e, texte_score, k)
        p = phrase("le missile touche l'ennemi : les deux disparaissent, et le score gagne 100")
        self.play(FadeIn(p), run_time=0.3)
        for n, h in enumerate((60, 90)):
            ey.set_value(h)
            ex.set_value(250)
            # L'ennemi avance ; le joueur tire quand il est à mi-chemin.
            self.play(ex.animate.set_value(150), run_time=1.2, rate_func=linear)
            mx.set_value(JX + 16)
            self.play(Transform(k, manette("Z", True).move_to(k)), run_time=0.08)
            self.play(Transform(k, manette("Z").move_to(k)), run_time=0.08)
            # Le missile file, l'ennemi continue, ils se croisent.
            cible = 130 if h == 60 else 150
            self.play(mx.animate.set_value(cible - 16), ex.animate.set_value(cible), run_time=0.9, rate_func=linear)
            if h == 60:
                flash = Rectangle(width=16 * ecran.px, height=16 * ecran.px, stroke_color=ORANGE, stroke_width=6).move_to(ecran.pos(cible + 8, h + 8))
                self.play(FadeIn(flash), run_time=0.1)
                self.play(flash.animate.scale(1.8).set_stroke(opacity=0), score.animate.set_value(100), run_time=0.5)
                mx.set_value(-24); ex.set_value(250)
            else:
                # Avec ey = 90, le missile passe en dessous : il rate, le score ne bouge pas.
                self.play(mx.animate.set_value(250), ex.animate.set_value(-20), run_time=1.2, rate_func=linear)
                self.play(FadeOut(p), run_time=0.2)
                p = phrase("quand le missile rate, le score ne bouge pas")
                self.play(FadeIn(p), run_time=0.3)
        self.wait(1.0)
