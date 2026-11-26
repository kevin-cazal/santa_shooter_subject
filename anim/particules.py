# Partie 2, « Particules » : les trois ingrédients. L'ennemi touché reste en
# silhouette à l'endroit de l'émission ; les particules naissent là, chacune
# avec sa vitesse ; un curseur « vie » règle combien d'images elles durent,
# et la liste se vide quand vie tombe à 0.
#
#   capture.py anim anim/particules.py LesParticules -o img/particules-trois-ingredients.webp --fps 30
import random
from manim import *
from commun import *

random.seed(3)
N = 8
PX = 0.06
CENTRE = LEFT * 3.0 + UP * 0.5
COULEURS = [ALERTE, ORANGE, BLANC, ALERTE, CIEL, ORANGE, BLANC, ALERTE]


class LesParticules(Scene):
    def construct(self):
        zone = Rectangle(width=7.2, height=5.0, stroke_color=DOUX, stroke_width=2).move_to(CENTRE)
        ennemi = sprite("ennemi", PX, 2, CENTRE + LEFT * 8 * PX + UP * 8 * PX)
        missile = sprite("missile", PX, 2, CENTRE + LEFT * 4.2 + UP * 4 * PX)
        titre_liste = code("particules = {}", 24, BLANC).move_to(RIGHT * 4.3 + UP * 3.2)
        self.add(zone, ennemi, missile, titre_liste)
        p = phrase("le missile touche l'ennemi : une explosion")
        self.play(FadeIn(p), missile.animate.shift(RIGHT * 3.8), run_time=0.9, rate_func=linear)
        fantome = ennemi.copy().set_opacity(0.22)
        self.add(fantome)
        self.play(FadeOut(ennemi, scale=0.3), FadeOut(missile, scale=0.3), run_time=0.25)

        vie = ValueTracker(20)        # la durée de vie, en images
        t = ValueTracker(0)           # le temps, en images
        vitesses = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(N)]
        points = VGroup()
        for i in range(N):
            d = Dot(radius=0.09, color=COULEURS[i]).move_to(CENTRE)
            d.v = vitesses[i]
            points.add(d)

        def bouger(groupe):
            tt = t.get_value()
            for d in groupe:
                d.move_to(CENTRE + RIGHT * d.v[0] * tt * PX * 2.2 + DOWN * d.v[1] * tt * PX * 2.2)
                d.set_opacity(max(0.0, min(1.0, (vie.get_value() - tt) / 6)))

        cartes = VGroup()
        for i in range(N):
            cadre = RoundedRectangle(width=3.2, height=0.46, corner_radius=0.1, stroke_color=GRIS, stroke_width=2, fill_color=PANNEAU, fill_opacity=1)
            pastille = Dot(radius=0.09, color=COULEURS[i]).move_to(cadre.get_left() + RIGHT * 0.35)
            cartes.add(VGroup(cadre, pastille))
        cartes.arrange(DOWN, buff=0.1).next_to(titre_liste, DOWN, buff=0.3)

        montre = ValueTracker(1)      # 0 quand les cartes sont rangées
        def vies():
            g = VGroup()
            for c in cartes:
                reste = max(0, int(vie.get_value() - t.get_value()))
                g.add(code(f"vie = {reste:>2}", 22, CHANGE if reste > 5 else FAUX).move_to(c[0].get_center() + RIGHT * 0.35))
            return g.set_opacity(montre.get_value())

        self.next_section("l'émetteur : elles naissent toutes au même point")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("l'émetteur : 8 particules naissent là où était l'ennemi")
        self.play(FadeIn(p), run_time=0.3)
        etiq = vies()
        for d, c, e in zip(points, cartes, etiq):
            self.play(FadeIn(d, scale=0.4), FadeIn(c), FadeIn(e), run_time=0.18)
        self.remove(*points, *etiq)
        self.add(points)
        etiq = always_redraw(vies)
        self.add(etiq)
        self.wait(1.2)

        self.next_section("la physique : chacune a sa vitesse")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("la physique : chacune a sa vitesse, et avance d'autant par image")
        fleches = VGroup(*[fleche_vitesse(CENTRE, d.v[0] * 10, d.v[1] * 10, echelle=0.011, couleur=d.get_color()) for d in points])
        self.play(FadeIn(p), FadeIn(fleches), run_time=0.5); self.wait(1.0)
        self.play(FadeOut(fleches), run_time=0.3)
        points.add_updater(bouger)
        self.play(t.animate.set_value(6), run_time=1.2, rate_func=linear)

        self.next_section("la longévité : vie baisse, à 0 on la retire")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("la longévité : vie baisse de 1 par image, à 0 la particule est retirée")
        self.play(FadeIn(p), t.animate.set_value(20), run_time=2.8, rate_func=linear)
        self.play(*[FadeOut(c) for c in cartes], montre.animate.set_value(0), run_time=0.5); self.wait(0.4)

        self.next_section("vie plus longue : les particules vont plus loin")
        self.play(FadeOut(p), run_time=0.2)
        reg = Reglage("vie", 5, 60, 20, CHANGE).placer(RIGHT * 4.3 + DOWN * 2.4)
        p = phrase("vie = 50 : les mêmes particules durent plus longtemps, et vont plus loin")
        t.set_value(0)
        self.play(FadeIn(reg), FadeIn(p), reg.t.animate.set_value(50), vie.animate.set_value(50), run_time=0.8)
        self.play(*[FadeIn(c) for c in cartes], montre.animate.set_value(1), run_time=0.3)
        self.play(t.animate.set_value(50), run_time=3.0, rate_func=linear)
        self.play(*[FadeOut(c) for c in cartes], montre.animate.set_value(0), run_time=0.4)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("la liste grandit à chaque explosion, et se vide toute seule")
        self.play(FadeIn(p), run_time=0.3); self.wait(1.4)
