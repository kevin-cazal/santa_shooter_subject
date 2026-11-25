# Alternative manim au GIF img/input-deplacement.gif (étape Input du joueur) :
# le bonnet suit les flèches, la manette sous l'écran allume la touche appuyée.
#
#   capture.py anim anim/alt_deplacement.py LeDeplacement -o img/alt-input-deplacement.webp --fps 30 --no-video
from manim import *
from commun import *


class Manette:
    """Les quatre flèches, comme l'overlay des GIF : la touche appuyée s'allume."""

    def __init__(self, scene, centre):
        self.scene = scene
        self.pos = {"haut": centre + UP * 0.7, "bas": centre, "gauche": centre + LEFT * 0.7, "droite": centre + RIGHT * 0.7}
        self.fl = {"haut": "↑", "bas": "↓", "gauche": "←", "droite": "→"}
        self.touches = {k: manette(self.fl[k]).move_to(p) for k, p in self.pos.items()}
        scene.add(*self.touches.values())

    def appuyer(self, k, allumee):
        self.scene.play(Transform(self.touches[k], manette(self.fl[k], allumee).move_to(self.pos[k])), run_time=0.12)


class LeDeplacement(Scene):
    def construct(self):
        ecran = Ecran(px=0.03, centre=UP * 0.9)
        x, y = ValueTracker(112), ValueTracker(60)
        j = always_redraw(lambda: ecran.sprite("joueur", int(x.get_value()), int(y.get_value()), 2))
        self.add(ecran.cadre, j)
        m = Manette(self, DOWN * 2.3)
        p = phrase("le bonnet se déplace avec les flèches du clavier, tant que la touche est enfoncée")
        self.play(FadeIn(p), run_time=0.4)
        for k, dx, dy in (("droite", 60, 0), ("bas", 0, 36), ("gauche", -90, 0), ("haut", 0, -50), ("droite", 40, 0)):
            m.appuyer(k, True)
            self.play(x.animate.set_value(x.get_value() + dx), y.animate.set_value(y.get_value() + dy), run_time=1.0, rate_func=linear)
            m.appuyer(k, False)
            self.wait(0.35)
        self.wait(0.8)
