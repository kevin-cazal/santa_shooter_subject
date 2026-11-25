# Partie 1, boîte à outils « math.random » : une roue à six secteurs qui
# tourne et s'arrête, six fois. Puis la roue devient un rouleau vertical le
# long de l'écran, gradué de 0 à 136 : il s'arrête à une hauteur, et l'ennemi
# apparaît là.
#
#   capture.py anim anim/hasard.py LeHasard -o img/outil-random.webp --fps 30
from manim import *
from commun import *

COULEURS_SECTEURS = [ROUGE, ORANGE, ALERTE, VERT, CIEL, BLEU]


class LeHasard(Scene):
    def construct(self):
        # 1. La roue.
        self.next_section("math.random(1, 6) : la roue s'arrête sur un nombre")
        ligne = code("de = math.random(1, 6)", 32).move_to(UP * 2.9)
        self.play(Write(ligne), run_time=0.7)
        centre = LEFT * 2.6 + UP * 0.2
        roue = VGroup()
        for k in range(6):
            a0 = k * TAU / 6
            roue.add(AnnularSector(inner_radius=0.0, outer_radius=1.5, angle=TAU / 6, start_angle=a0, fill_color=COULEURS_SECTEURS[k],
                                   fill_opacity=0.85, stroke_color=FOND, stroke_width=3).move_arc_center_to(centre))
            roue.add(code(str(k + 1), 28, FOND).move_to(centre + 1.0 * np.array([np.cos(a0 + TAU / 12), np.sin(a0 + TAU / 12), 0])))
        aiguille = Triangle(fill_color=BLANC, fill_opacity=1, stroke_width=0).scale(0.22).rotate(PI).move_to(centre + UP * 1.75)
        p = phrase("math.random(1, 6) : la roue tourne et s'arrête sur un nombre entre 1 et 6, nouveau à chaque appel")
        self.play(FadeIn(roue), FadeIn(aiguille), FadeIn(p), run_time=0.5)
        # La bande des résultats, à droite.
        bande = VGroup()
        angle = 0
        for n, tirage in enumerate((4, 1, 6, 3, 6, 2)):
            # L'aiguille est en haut : le secteur `tirage` doit finir sous elle.
            cible = PI / 2 - ((tirage - 1) * TAU / 6 + TAU / 12)
            delta = (cible - angle) % TAU + TAU * (2 if n == 0 else 1)
            s = surligne(ligne[3:], CIEL)
            self.play(Create(s), run_time=0.15)
            self.play(Rotate(roue, delta, about_point=centre), run_time=1.0 if n == 0 else 0.6, rate_func=rate_functions.ease_out_cubic)
            angle = (angle + delta) % TAU
            jet = VGroup(Square(side_length=0.6, fill_color=COULEURS_SECTEURS[tirage - 1], fill_opacity=0.85, stroke_width=0), code(str(tirage), 26, FOND))
            jet.move_to(RIGHT * (1.2 + n * 0.8) + UP * 0.2)
            self.play(FadeIn(jet, scale=0.5), FadeOut(s), run_time=0.25)
            bande.add(jet)
        self.wait(0.8)

        # 2. Le rouleau le long de l'écran.
        self.next_section("math.random(0, 136) : une hauteur sur l'écran")
        self.play(FadeOut(p), FadeOut(roue), FadeOut(aiguille), FadeOut(bande), run_time=0.4)
        l2 = code("ey = math.random(0, 136)", 32).move_to(UP * 2.9)
        self.play(FadeTransform(ligne, l2), run_time=0.5)
        ecran = Ecran(px=0.03, centre=RIGHT * 0.6 + DOWN * 0.5)
        rouleau = RoundedRectangle(width=0.7, height=ecran.cadre.height, corner_radius=0.12, stroke_color=DOUX, stroke_width=3,
                                   fill_color=PANNEAU, fill_opacity=1).next_to(ecran.cadre, LEFT, buff=0.35)
        grad = VGroup(*[VGroup(Line(rouleau.get_left() + RIGHT * 0.05, rouleau.get_left() + RIGHT * 0.25, stroke_color=DOUX, stroke_width=2),
                               code(str(v), 14, DOUX)).arrange(RIGHT, buff=0.06).move_to(rouleau.get_left() + RIGHT * 0.3).set_y(ecran.pos(0, v)[1])
                       for v in (0, 34, 68, 102, 136)])
        p = phrase("math.random(0, 136) : le rouleau s'arrête à une hauteur de l'écran, et l'ennemi apparaît là")
        self.play(FadeIn(ecran.cadre), FadeIn(rouleau), FadeIn(grad), FadeIn(p), run_time=0.5)
        ey = ValueTracker(0)
        curseur = always_redraw(lambda: Line(rouleau.get_left(), rouleau.get_right(), stroke_color=ALERTE, stroke_width=6).set_y(ecran.pos(0, ey.get_value())[1]))
        self.add(curseur)
        ennemi = None
        for h in (12, 101, 55, 128, 30):
            s = surligne(l2[3:], CIEL)
            self.play(Create(s), run_time=0.15)
            self.play(ey.animate.set_value(h), run_time=0.8, rate_func=rate_functions.ease_out_bounce)
            e = ecran.sprite("ennemi", 224, h, 1)
            if ennemi is None:
                self.play(FadeIn(e, scale=0.5), FadeOut(s), run_time=0.3)
            else:
                self.play(FadeTransform(ennemi, e), FadeOut(s), run_time=0.3)
            ennemi = e
            self.wait(0.4)
        self.wait(1.0)
