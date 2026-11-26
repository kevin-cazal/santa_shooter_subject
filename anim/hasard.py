# Partie 1, boîte à outils « math.random » : une roue de loterie, chiffres
# droits. math.random(1, 6) : trois tours, trois nombres. Puis la roue graduée
# de 0 à 136, avec un repère net entre 136 et 0 : elle tombe sur 101, le 101
# devient le y de l'ennemi (son x est affiché aussi), et l'ennemi avance vers
# la gauche : x baisse, y reste 101.
#
#   capture.py anim anim/hasard.py LeHasard -o img/outil-random.webp --fps 30
import random
from manim import *
from commun import *

random.seed(11)
SECTEURS = [ROUGE, ORANGE, VERT, "#7b5ea7", ALERTE, BLEU]


class Roue:
    """Une roue de loterie : `n` secteurs, les étiquettes droites, le pointeur à droite ;
    le secteur gagnant est celui qui passe sous le pointeur (angle 0)."""

    def __init__(self, centre, rayon, etiquettes, couleurs, taille_texte=30):
        self.centre, self.rayon, self.n = centre, rayon, len(etiquettes)
        self.disque = VGroup()
        self.textes = VGroup()
        pas = TAU / self.n
        for k, (et, coul) in enumerate(zip(etiquettes, couleurs)):
            a0 = k * pas
            self.disque.add(AnnularSector(inner_radius=0, outer_radius=rayon, angle=pas, start_angle=a0, fill_color=coul,
                                          fill_opacity=1, stroke_color=BLANC, stroke_width=2).move_arc_center_to(centre))
            if et != "":
                a = a0 + pas / 2
                t = code(str(et), taille_texte, FOND if coul in (ALERTE, VERT, ORANGE) else BLANC)
                t.angle_rel = a
                self.textes.add(t)
        self.angle = 0.0
        self._placer_textes()
        self.moyeu = Circle(radius=rayon * 0.16, fill_color=BLANC, fill_opacity=1, stroke_color=DOUX, stroke_width=2).move_to(centre)
        self.pointeur = Triangle(fill_color=BLEU, fill_opacity=1, stroke_color=BLANC, stroke_width=2).scale(0.32).rotate(PI / 2)
        self.pointeur.move_to(centre + RIGHT * (rayon + 0.12))

    def _placer_textes(self):
        # Les chiffres restent droits : ils tournent avec la roue, pas sur eux-mêmes.
        for t in self.textes:
            a = t.angle_rel + self.angle
            t.move_to(self.centre + self.rayon * 0.64 * np.array([np.cos(a), np.sin(a), 0]))

    def tout(self):
        return VGroup(self.disque, self.textes, self.moyeu, self.pointeur)

    def tourner(self, scene, k, tours=3, run_time=2.4):
        pas = TAU / self.n
        cible = (-(k * pas + pas / 2)) % TAU
        delta = (cible - self.angle) % TAU + tours * TAU
        depart = self.angle
        tr = ValueTracker(0)

        def maj(m):
            self.angle = depart + tr.get_value()
            self._placer_textes()
        self.textes.add_updater(maj)
        scene.play(Rotate(self.disque, delta, about_point=self.centre), tr.animate.set_value(delta), run_time=run_time, rate_func=rate_functions.ease_out_quart)
        self.textes.remove_updater(maj)
        self.angle = (depart + delta) % TAU
        self._placer_textes()


def confettis(scene, origine_pt, n=36):
    cs = VGroup(*[Rectangle(width=0.2, height=0.11, fill_color=random.choice(SECTEURS + [CIEL, BLANC]), fill_opacity=1, stroke_width=0)
                  .move_to(origine_pt).rotate(random.uniform(0, PI)) for _ in range(n)])
    scene.add(cs)
    scene.play(*[c.animate.shift(np.array([random.uniform(-3.0, 3.0), random.uniform(-2.6, 2.2), 0])).rotate(random.uniform(-2, 2)).set_opacity(0)
                 for c in cs], run_time=0.9, rate_func=rate_functions.ease_out_sine)
    scene.remove(cs)


def carte_resultat(texte_code, centre):
    cadre = RoundedRectangle(width=2.6, height=1.0, corner_radius=0.15, fill_color=BLANC, fill_opacity=1, stroke_width=0).move_to(centre)
    return VGroup(cadre, code(texte_code, 30, FOND).move_to(cadre))


class LeHasard(Scene):
    def construct(self):
        # 1. La roue à six nombres.
        self.next_section("math.random(1, 6) : la roue s'arrête sur un nombre")
        ligne = code("de = math.random(1, 6)", 32).move_to(UP * 3.0)
        self.play(Write(ligne), run_time=0.7)
        roue = Roue(LEFT * 2.6 + DOWN * 0.3, 2.5, [1, 2, 3, 4, 5, 6], SECTEURS)
        p = phrase("math.random(1, 6) : la roue s'arrête sur un nombre de 1 à 6")
        self.play(FadeIn(roue.tout()), FadeIn(p), run_time=0.5)
        bande = VGroup()
        for n, tirage in enumerate((4, 1, 6)):
            s = surligne(ligne[3:], LU)
            self.play(Create(s), run_time=0.15)
            roue.tourner(self, tirage - 1, tours=3 if n == 0 else 2, run_time=2.0 if n == 0 else 1.1)
            confettis(self, roue.centre + RIGHT * roue.rayon)
            carte = carte_resultat(f"de = {tirage}", RIGHT * 3.2 + UP * 1.2)
            self.play(FadeIn(carte, scale=0.6), FadeOut(s), run_time=0.3)
            self.wait(1.0)
            jeton = VGroup(Square(side_length=0.6, fill_color=SECTEURS[tirage - 1], fill_opacity=1, stroke_width=0),
                           code(str(tirage), 26, FOND if SECTEURS[tirage - 1] in (ALERTE, VERT, ORANGE) else BLANC)).move_to(RIGHT * (1.6 + n * 0.8) + DOWN * 0.6)
            self.play(FadeTransform(carte, jeton), run_time=0.4)
            bande.add(jeton)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("trois appels, trois nombres : un nouveau à chaque appel")
        self.play(FadeIn(p), run_time=0.3); self.wait(1.0)

        # 2. La roue de 0 à 136 : elle tombe sur 101.
        self.next_section("math.random(0, 136) : la roue tombe sur 101")
        self.play(FadeOut(p), FadeOut(bande), FadeOut(roue.tout()), run_time=0.4)
        l2 = code("math.random(0, 136)", 32).move_to(UP * 3.0)
        self.play(FadeTransform(ligne, l2), run_time=0.5)
        grad = [str(k * 136 // 16) if k % 2 == 0 else "" for k in range(16)]
        roue2 = Roue(LEFT * 2.6 + DOWN * 0.3, 2.5, grad, [BLEU if k % 2 == 0 else "#29366f" for k in range(16)], taille_texte=22)
        # Le repère entre 136 et 0 : un trait blanc épais sur le rayon de départ, avec « 136 | 0 ».
        repere = Line(roue2.centre, roue2.centre + RIGHT * roue2.rayon, stroke_color=BLANC, stroke_width=6)
        rep_t = code("136 | 0", 20, BLANC).next_to(roue2.centre + RIGHT * roue2.rayon * 0.5, DOWN, buff=0.08)
        roue2.disque.add(repere, rep_t)
        p = phrase("de 0 à 136 : la roue tombe sur 101")
        self.play(FadeIn(roue2.tout()), FadeIn(p), run_time=0.5)
        s = surligne(l2, LU)
        self.play(Create(s), run_time=0.15)
        roue2.tourner(self, int(101 * 16 / 137), tours=2, run_time=1.8)
        confettis(self, roue2.centre + RIGHT * roue2.rayon)
        carte = carte_resultat("101", RIGHT * 3.4 + UP * 1.4)
        self.play(FadeIn(carte, scale=0.6), FadeOut(s), run_time=0.3); self.wait(1.0)

        # 3. Le 101 devient le y de l'ennemi.
        self.next_section("101 devient ey : la hauteur de l'ennemi")
        self.play(FadeOut(p), FadeOut(roue2.tout()), FadeOut(l2), run_time=0.4)
        ecran = Ecran(px=0.03, centre=LEFT * 1.2 + DOWN * 0.2)
        ex, ey = ValueTracker(232), ValueTracker(101)
        ennemi = always_redraw(lambda: ecran.sprite_clippe("ennemi", int(ex.get_value()), int(ey.get_value()), 1))
        point = always_redraw(lambda: origine(ecran.pos(ex.get_value(), ey.get_value())))
        etiq = always_redraw(lambda: VGroup(etiquette(f"ex = {int(ex.get_value())}", CHANGE, 22), etiquette(f"ey = {int(ey.get_value())}", CHANGE, 22))
                             .arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ecran.pos(ex.get_value(), ey.get_value()), UP, buff=0.25).shift(LEFT * 0.9))
        guide_y = always_redraw(lambda: DashedLine(ecran.pos(0, ey.get_value()), ecran.pos(ex.get_value(), ey.get_value()), stroke_color=CHANGE, stroke_width=2))
        p = phrase("101 est la hauteur de l'ennemi : ey = 101. Son x : 232, le bord droit")
        self.play(FadeIn(ecran.cadre), FadeIn(ecran.axes()), FadeIn(p), run_time=0.5)
        ey_t = code("ey = 101", 30, CHANGE).move_to(carte)
        self.play(FadeTransform(carte, ey_t), run_time=0.6)
        self.add(ennemi, point)
        self.play(FadeTransform(ey_t, etiq), FadeIn(guide_y), run_time=0.8)
        self.wait(1.2)

        # 4. L'ennemi avance : x baisse, y ne change plus.
        self.next_section("l'ennemi avance : ex baisse, ey reste 101")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("l'ennemi avance vers la gauche : ex baisse, ey reste 101")
        self.play(FadeIn(p), run_time=0.3)
        self.play(ex.animate.set_value(20), run_time=3.0, rate_func=linear)
        self.wait(1.2)
