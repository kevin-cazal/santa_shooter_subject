# Partie 2, « Parallaxe » : des étoiles de tailles différentes. Toutes à la
# même vitesse, le ciel est plat. Les grosses (proches) plus vite que les
# petites (loin) : de la profondeur, sans 3D. Le coefficient reste à écrire.
#
#   capture.py anim anim/parallaxe.py LaParallaxe -o img/parallaxe-profondeur.webp
import random
from manim import *
from commun import *

random.seed(7)


class LaParallaxe(Scene):
    def construct(self):
        ecran = Ecran(px=0.03, centre=LEFT * 2.4 + UP * 0.3)
        k = ValueTracker(0)        # 0 : même vitesse pour toutes ; 1 : vitesse selon la taille
        etoiles = VGroup()
        for _ in range(50):
            taille = random.randint(1, 3)
            e = Dot(radius=taille * ecran.px * 0.55, color=BLANC if taille > 1 else DOUX)
            e.gx, e.gy, e.taille = random.uniform(0, W), random.uniform(2, H - 2), taille
            etoiles.add(e)

        def avancer(groupe, dt):
            for e in groupe:
                vitesse = 1.0 * (1 - k.get_value()) + e.taille * 0.6 * k.get_value()   # pixels par image
                e.gx -= dt * 60 * vitesse
                if e.gx < 0:
                    e.gx, e.gy = W, random.uniform(2, H - 2)
                e.move_to(ecran.pos(e.gx, e.gy))

        avancer(etoiles, 0)
        etoiles.add_updater(avancer)
        joueur = ecran.sprite("joueur", 16, 60, 2)
        self.add(ecran.cadre, etoiles, joueur)

        # 1. Même vitesse.
        self.next_section("toutes à la même vitesse : un ciel plat")
        p = phrase("toutes les étoiles à la même vitesse : le ciel est plat, comme un dessin")
        self.play(FadeIn(p), run_time=0.5)
        self.wait(3.0)

        # 2. Vitesse selon la taille.
        self.next_section("les grosses étoiles sont proches : plus vite")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("une grosse étoile est proche : elle va plus vite. Une petite est loin : plus lente")
        legende = VGroup()
        for taille, mots in ((1, "petite · loin · lente"), (2, "moyenne"), (3, "grosse · proche · rapide")):
            d = Dot(radius=taille * 0.05 + 0.03, color=BLANC)
            fl = Arrow(ORIGIN, LEFT * (0.35 + 0.45 * taille), buff=0, color=ALERTE, stroke_width=4,
                       max_tip_length_to_length_ratio=0.25).next_to(d, LEFT, buff=0.15)
            t = texte(mots, 18, DOUX).next_to(d, RIGHT, buff=0.2)
            legende.add(VGroup(fl, d, t))
        legende.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(RIGHT * 4.0 + UP * 0.6)
        self.play(FadeIn(p), FadeIn(legende), k.animate.set_value(1), run_time=1.2)
        self.wait(3.2)

        # 3. La parallaxe.
        self.next_section("la parallaxe : de la profondeur, sans 3D")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("c'est la parallaxe : l'œil voit de la profondeur, sans aucune 3D")
        self.play(FadeIn(p), run_time=0.4)
        self.wait(3.0)
