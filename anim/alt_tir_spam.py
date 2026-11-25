# Alternative manim aux GIF img/tir-spam-avant.gif et img/tir-spam-apres.gif :
# avant, chaque appui ramène le missile devant le joueur ; après, le missile
# part une seule fois et les appuis suivants ne font rien.
#
#   capture.py anim anim/alt_tir_spam.py LeTirSpam -o img/alt-tir-spam.webp --fps 30
from manim import *
from commun import *

JX, JY = 24, 60


class LeTirSpam(Scene):
    def construct(self):
        ecran = Ecran(px=0.03, centre=UP * 0.9)
        mx = ValueTracker(-24)
        j = ecran.sprite("joueur", JX, JY, 2)
        m = always_redraw(lambda: ecran.sprite_clippe("missile", int(mx.get_value()), JY + 6, 2))
        k = manette("Z").move_to(DOWN * 2.3)
        self.add(ecran.cadre, j, m, k)

        def appui():
            self.play(Transform(k, manette("Z", True).move_to(k)), run_time=0.08)
            self.play(Transform(k, manette("Z").move_to(k)), run_time=0.08)

        self.next_section("avant : chaque appui ramène le missile devant le joueur")
        p = phrase("avant : à chaque appui, le missile revient devant le joueur, même s'il est déjà parti")
        self.play(FadeIn(p), run_time=0.3)
        for _ in range(4):
            mx.set_value(JX + 16)
            appui()
            self.play(mx.animate.set_value(JX + 16 + 70), run_time=0.55, rate_func=linear)
        self.play(mx.animate.set_value(250), run_time=1.0, rate_func=linear)
        self.wait(0.5)

        self.next_section("après : le missile part une seule fois")
        self.play(FadeOut(p), run_time=0.2)
        mx.set_value(-24)
        p = phrase("après : le missile part une seule fois, les appuis suivants ne font plus rien")
        self.play(FadeIn(p), run_time=0.3)
        mx.set_value(JX + 16)
        appui()
        # Le missile vole ; les appuis suivants ne le ramènent pas.
        for _ in range(4):
            self.play(mx.animate.set_value(mx.get_value() + 52), run_time=0.5, rate_func=linear)
            appui()
        self.play(mx.animate.set_value(250), run_time=0.3, rate_func=linear)
        self.wait(0.8)
