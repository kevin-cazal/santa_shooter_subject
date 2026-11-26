# Alternative manim au GIF img/ennemi-mouvement.gif : l'ennemi traverse l'écran
# de droite à gauche, et repart de la droite à une hauteur au hasard.
#
#   capture.py anim anim/alt_ennemi.py LEnnemiTraverse -o img/alt-ennemi-mouvement.webp --fps 30 --no-video
from manim import *
from commun import *


class LEnnemiTraverse(Scene):
    def construct(self):
        ecran = Ecran(px=0.03, centre=UP * 0.6)
        ex, ey = ValueTracker(250), ValueTracker(40)

        e = always_redraw(lambda: VGroup(ecran.sprite_clippe("ennemi", int(ex.get_value()), int(ey.get_value()), 2),
                                         origine(ecran.pos(min(max(int(ex.get_value()), 0), 239), int(ey.get_value())))))
        j = ecran.sprite("joueur", 20, 60, 2)
        tag = always_redraw(lambda: etiquette(f"ey = {int(ey.get_value())}", ALERTE, 24).next_to(ecran.cadre, DOWN, buff=0.3))
        self.add(ecran.cadre, j, e, tag)
        p = phrase("l'ennemi traverse de droite à gauche. À chaque passage, sa hauteur est choisie au hasard")
        self.play(FadeIn(p), run_time=0.3)
        for h in (40, 104, 12, 76):
            ey.set_value(h)
            ex.set_value(250)
            self.play(ex.animate.set_value(-20), run_time=2.0, rate_func=linear)
        self.wait(0.5)
