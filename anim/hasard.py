# Partie 1, boîte à outils « math.random » : une roue de loterie comme sur
# spinthewheel.io. Six secteurs de couleur, les nombres écrits le long du
# rayon, un moyeu blanc, un pointeur bleu à droite ; la roue fait plusieurs
# tours, ralentit, s'arrête : confettis, et le résultat sur une carte. Puis
# la même roue graduée de 0 à 136 : le nombre devient la hauteur de l'ennemi.
#
#   capture.py anim anim/hasard.py LeHasard -o img/outil-random.webp --fps 30
import random
from manim import *
from commun import *

random.seed(11)
SECTEURS = [ROUGE, ORANGE, VERT, "#7b5ea7", ALERTE, BLEU]   # les couleurs plates du site, dans la palette du jeu


class Roue:
    """Une roue de loterie : `n` secteurs, le pointeur à droite, le secteur gagnant est
    celui qui passe sous le pointeur (angle 0)."""

    def __init__(self, centre, rayon, etiquettes, couleurs, taille_texte=30):
        self.centre, self.rayon, self.n = centre, rayon, len(etiquettes)
        self.disque = VGroup()
        pas = TAU / self.n
        for k, (et, coul) in enumerate(zip(etiquettes, couleurs)):
            a0 = k * pas
            self.disque.add(AnnularSector(inner_radius=0, outer_radius=rayon, angle=pas, start_angle=a0, fill_color=coul,
                                          fill_opacity=1, stroke_color=BLANC, stroke_width=2).move_arc_center_to(centre))
            if et:
                a = a0 + pas / 2
                t = code(str(et), taille_texte, FOND if coul in (ALERTE, VERT, ORANGE) else BLANC)
                t.rotate(a).move_to(centre + rayon * 0.62 * np.array([np.cos(a), np.sin(a), 0]))
                self.disque.add(t)
        self.moyeu = Circle(radius=rayon * 0.16, fill_color=BLANC, fill_opacity=1, stroke_color=DOUX, stroke_width=2).move_to(centre)
        self.pointeur = Triangle(fill_color=BLEU, fill_opacity=1, stroke_color=BLANC, stroke_width=2).scale(0.32).rotate(PI / 2)
        self.pointeur.move_to(centre + RIGHT * (rayon + 0.12))
        self.angle = 0.0

    def tout(self):
        return VGroup(self.disque, self.moyeu, self.pointeur)

    def tourner(self, scene, k, tours=3, run_time=2.4):
        """Fait tourner la roue pour que le secteur k s'arrête sous le pointeur."""
        pas = TAU / self.n
        cible = (-(k * pas + pas / 2)) % TAU
        delta = (cible - self.angle) % TAU + tours * TAU
        scene.play(Rotate(self.disque, delta, about_point=self.centre), run_time=run_time, rate_func=rate_functions.ease_out_quart)
        self.angle = (self.angle + delta) % TAU


def confettis(scene, origine, n=36):
    cs = VGroup(*[Rectangle(width=0.2, height=0.11, fill_color=random.choice(SECTEURS + [CIEL, BLANC]), fill_opacity=1, stroke_width=0)
                  .move_to(origine).rotate(random.uniform(0, PI)) for _ in range(n)])
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
        p = phrase("math.random(1, 6) : la roue tourne, ralentit, et s'arrête sur un nombre entre 1 et 6")
        self.play(FadeIn(roue.tout()), FadeIn(p), run_time=0.5)
        bande = VGroup()
        for n, tirage in enumerate((4, 1, 6)):
            s = surligne(ligne[3:], CIEL)
            self.play(Create(s), run_time=0.15)
            roue.tourner(self, tirage - 1, tours=3 if n == 0 else 2, run_time=2.0 if n == 0 else 1.1)
            confettis(self, roue.centre + RIGHT * roue.rayon)
            carte = carte_resultat(f"de = {tirage}", RIGHT * 3.2 + UP * 1.2)
            self.play(FadeIn(carte, scale=0.6), FadeOut(s), run_time=0.3)
            self.wait(0.2)
            jeton = VGroup(Square(side_length=0.6, fill_color=SECTEURS[tirage - 1], fill_opacity=1, stroke_width=0),
                           code(str(tirage), 26, FOND if SECTEURS[tirage - 1] in (ALERTE, VERT, ORANGE) else BLANC)).move_to(RIGHT * (1.6 + n * 0.8) + DOWN * 0.6)
            self.play(FadeTransform(carte, jeton), run_time=0.4)
            bande.add(jeton)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("trois appels, trois nombres : nouveau à chaque appel")
        self.play(FadeIn(p), run_time=0.3)
        self.wait(0.6)

        # 2. La même roue, graduée de 0 à 136.
        self.next_section("math.random(0, 136) : une hauteur sur l'écran")
        self.play(FadeOut(p), FadeOut(bande), FadeOut(roue.tout()), run_time=0.4)
        l2 = code("ey = math.random(0, 136)", 32).move_to(UP * 3.0)
        self.play(FadeTransform(ligne, l2), run_time=0.5)
        # 16 secteurs de deux couleurs, gradués toutes les 17 unités : 0, 17, 34 … 119.
        etiq = [k * 17 if k % 2 == 0 else "" for k in range(8)] * 2
        couleurs = [BLEU if k % 2 == 0 else "#29366f" for k in range(16)]
        grad = [str(k * 136 // 16) if k % 2 == 0 else "" for k in range(16)]
        roue2 = Roue(LEFT * 2.6 + DOWN * 0.3, 2.5, grad, couleurs, taille_texte=20)
        ecran = Ecran(px=0.022, centre=RIGHT * 3.4 + DOWN * 0.3)
        p = phrase("math.random(0, 136) : la même roue, graduée de 0 à 136. Le nombre est une hauteur sur l'écran")
        self.play(FadeIn(roue2.tout()), FadeIn(ecran.cadre), FadeIn(ecran.axes()), FadeIn(p), run_time=0.5)
        ennemi = None
        for n, h in enumerate((12, 101, 55)):
            s = surligne(l2[3:], CIEL)
            self.play(Create(s), run_time=0.15)
            roue2.tourner(self, int(h * 16 / 137), tours=2, run_time=1.2)
            carte = carte_resultat(f"ey = {h}", RIGHT * 3.4 + DOWN * 2.5)
            self.play(FadeIn(carte, scale=0.6), FadeOut(s), run_time=0.3)
            e = ecran.sprite("ennemi", 224, h, 1)
            if ennemi is None:
                self.play(FadeIn(e, scale=0.5), run_time=0.4)
            else:
                self.play(FadeTransform(ennemi, e), run_time=0.4)
            ennemi = e
            self.play(FadeOut(carte), run_time=0.25)
        self.wait(1.0)
