# Alternative manim aux GIF img/limites-avant.gif et img/limites-apres.gif :
# sans conditions, le bonnet sort de l'écran et disparaît ; avec, il s'arrête
# contre le bord. La manette montre la flèche maintenue.
#
#   capture.py anim anim/alt_limites.py LesLimitesAvantApres -o img/alt-limites.webp --fps 30
from manim import *
from commun import *


class LesLimitesAvantApres(Scene):
    def construct(self):
        ecran = Ecran(px=0.03, centre=UP * 0.9)
        x = ValueTracker(150)

        # Hors de l'écran, le jeu ne dessine rien : le sprite s'efface au-delà du bord.
        j = always_redraw(lambda: ecran.sprite_clippe("joueur", int(x.get_value()), 60, 2))
        k = manette("→").move_to(DOWN * 2.3)
        self.add(ecran.cadre, j, k)

        self.next_section("avant : sans conditions, le joueur sort de l'écran")
        p = phrase("avant : sans conditions, le joueur sort de l'écran et disparaît")
        self.play(FadeIn(p), Transform(k, manette("→", True).move_to(k)), run_time=0.3)
        self.play(x.animate.set_value(260), run_time=2.2, rate_func=linear)
        self.play(Transform(k, manette("→").move_to(k)), run_time=0.15)
        self.wait(0.8)

        self.next_section("après : avec les conditions, il s'arrête contre le bord")
        self.play(FadeOut(p), run_time=0.2)
        x.set_value(150)
        p = phrase("après : avec les conditions, le joueur s'arrête contre le bord de l'écran")
        self.play(FadeIn(p), Transform(k, manette("→", True).move_to(k)), run_time=0.3)
        self.play(x.animate.set_value(224), run_time=1.5, rate_func=linear)
        self.wait(1.2)
        self.play(Transform(k, manette("→").move_to(k)), run_time=0.15)
        self.wait(0.6)
