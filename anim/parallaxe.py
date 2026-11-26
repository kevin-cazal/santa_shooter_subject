# Partie 2, « Parallaxe » : deux ciels côte à côte, les mêmes étoiles. À
# gauche, toutes à la même vitesse : plat. À droite, un curseur « coefficient »
# règle de combien les grosses étoiles vont plus vite : 0, c'est plat aussi ;
# plus il monte, plus on voit de la profondeur. Le coefficient reste à écrire.
#
#   capture.py anim anim/parallaxe.py LaParallaxe -o img/parallaxe-profondeur.webp --fps 30
import random
from manim import *
from commun import *

random.seed(7)
ETOILES = [(random.uniform(0, W), random.uniform(2, H - 2), random.randint(1, 3)) for _ in range(50)]


class Ciel:
    def __init__(self, scene, centre, coef):
        self.ecran = Ecran(px=0.025, centre=centre)
        self.coef = coef      # un ValueTracker : 0 = même vitesse, 1 = vitesse selon la taille
        self.etoiles = VGroup()
        for gx, gy, taille in ETOILES:
            e = Dot(radius=taille * self.ecran.px * 0.6, color=BLANC if taille > 1 else DOUX)
            e.gx, e.gy, e.taille = gx, gy, taille
            self.etoiles.add(e)
        self.etoiles.add_updater(self.avancer)
        self.avancer(self.etoiles, 0)
        scene.add(self.ecran.cadre, self.etoiles, self.ecran.sprite("joueur", 16, 60, 2))

    def avancer(self, groupe, dt):
        c = self.coef.get_value()
        for e in groupe:
            vitesse = 1.0 * (1 - c) + e.taille * 0.6 * c
            e.gx -= dt * 60 * vitesse
            if e.gx < 0:
                e.gx += W
            e.move_to(self.ecran.pos(e.gx, e.gy))


class LaParallaxe(Scene):
    def construct(self):
        plat = Ciel(self, LEFT * 3.3 + UP * 0.6, ValueTracker(0))
        coef = ValueTracker(0)
        profond = Ciel(self, RIGHT * 3.3 + UP * 0.6, coef)
        t1 = texte("même vitesse pour toutes", 22, DOUX).next_to(plat.ecran.cadre, UP, buff=0.2)
        t2 = texte("vitesse selon la taille", 22, CHANGE).next_to(profond.ecran.cadre, UP, buff=0.2)
        reg = Reglage("coefficient", 0, 1, 0, CHANGE, decimales=1).placer(RIGHT * 3.3 + DOWN * 2.4)
        self.add(t1, t2, reg)

        self.next_section("coefficient 0 : les deux ciels sont plats")
        p = phrase("coefficient 0 : les deux ciels sont plats, comme un dessin")
        self.play(FadeIn(p), run_time=0.4); self.wait(3.0)

        self.next_section("coefficient 1 : les grosses étoiles vont plus vite")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("à droite, le coefficient monte : les grosses étoiles, proches, vont plus vite")
        self.play(FadeIn(p), coef.animate.set_value(1), reg.t.animate.set_value(1), run_time=2.0); self.wait(2.6)

        self.next_section("retour vers 0 : la profondeur disparaît")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("le coefficient redescend : la profondeur disparaît")
        self.play(FadeIn(p), coef.animate.set_value(0.2), reg.t.animate.set_value(0.2), run_time=2.0); self.wait(1.6)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("c'est la parallaxe : de la profondeur sans 3D, avec un seul coefficient")
        self.play(FadeIn(p), coef.animate.set_value(1), reg.t.animate.set_value(1), run_time=1.5); self.wait(2.6)
