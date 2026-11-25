# Partie 2, « Particules » : les trois ingrédients. Un émetteur (elles naissent
# toutes au même point), une physique (chacune a sa vitesse), une longévité
# (vie baisse, à 0 on la retire de la liste). La liste grandit et se vide.
#
#   capture.py anim anim/particules.py LesParticules -o img/particules-trois-ingredients.webp --fps 30
import random
from manim import *
from commun import *

random.seed(3)
N, VIE = 8, 20
PX = 0.06                       # un pixel du jeu : zoom sur l'explosion
CENTRE = LEFT * 3.0 + UP * 0.5  # l'ennemi, là où tout se passe
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
        self.play(FadeOut(ennemi, scale=0.3), FadeOut(missile, scale=0.3), run_time=0.25)

        # Les particules : une vitesse chacune, en pixels par image, et une vie en images.
        vitesses = [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(N)]
        t = ValueTracker(0)           # le temps, en images du jeu
        points = VGroup()
        for i in range(N):
            d = Dot(radius=0.09, color=COULEURS[i]).move_to(CENTRE)
            d.v = vitesses[i]
            points.add(d)

        def bouger(groupe):
            for d in groupe:
                tt = t.get_value()
                d.move_to(CENTRE + RIGHT * d.v[0] * tt * PX * 2.2 + DOWN * d.v[1] * tt * PX * 2.2)
                d.set_opacity(max(0.0, min(1.0, (VIE - tt) / 6)))

        # La liste, à droite : une carte par particule, avec sa vie.
        cartes = VGroup()
        for i in range(N):
            cadre = RoundedRectangle(width=3.2, height=0.46, corner_radius=0.1, stroke_color=GRIS, stroke_width=2,
                                     fill_color=PANNEAU, fill_opacity=1)
            pastille = Dot(radius=0.09, color=COULEURS[i]).move_to(cadre.get_left() + RIGHT * 0.35)
            cartes.add(VGroup(cadre, pastille))
        cartes.arrange(DOWN, buff=0.1).next_to(titre_liste, DOWN, buff=0.3)
        titre_liste.generate_target()

        def vies():
            g = VGroup()
            for c in cartes:
                reste = max(0, VIE - int(t.get_value()))
                g.add(code(f"vie = {reste:>2}", 20, ALERTE if reste > 5 else ROUGE).move_to(c[0].get_center() + RIGHT * 0.35))
            return g

        # 1. L'émetteur.
        self.next_section("l'émetteur : elles naissent toutes au même point")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("l'émetteur : 8 particules naissent au même point, 8 entrées dans la liste")
        self.play(FadeIn(p), run_time=0.3)
        etiq = vies()
        for d, c, e in zip(points, cartes, etiq):
            self.play(FadeIn(d, scale=0.4), FadeIn(c), FadeIn(e), run_time=0.18)
        # Les éléments sont entrés un par un ; on les remplace par leurs groupes,
        # sinon l'updater du groupe ne tourne pas et les étiquettes figées restent.
        self.remove(*points, *etiq)
        self.add(points)
        etiq = always_redraw(vies)
        self.add(etiq)
        self.wait(1.2)

        # 2. La physique.
        self.next_section("la physique : chacune a sa vitesse")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("la physique : chacune a sa propre vitesse, et avance d'autant à chaque image")
        fleches = VGroup(*[Arrow(CENTRE, CENTRE + (RIGHT * d.v[0] + DOWN * d.v[1]) * 1.1, buff=0, color=d.get_color(),
                                 stroke_width=3, max_tip_length_to_length_ratio=0.2) for d in points])
        self.play(FadeIn(p), FadeIn(fleches), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(fleches), run_time=0.3)
        points.add_updater(bouger)
        self.play(t.animate.set_value(6), run_time=1.2, rate_func=linear)

        # 3. La longévité.
        self.next_section("la longévité : vie baisse, à 0 on la retire")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("la longévité : vie baisse de 1 à chaque image. À 0, la particule est retirée de la liste")
        self.play(FadeIn(p), t.animate.set_value(VIE), run_time=2.8, rate_func=linear)
        points.remove_updater(bouger)
        self.remove(etiq)
        self.play(*[FadeOut(c) for c in cartes], *[FadeOut(d) for d in points], run_time=0.5)
        self.wait(0.4)
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("la liste grandit à chaque explosion, et se vide toute seule")
        self.play(FadeIn(p), run_time=0.4)
        self.wait(1.6)
