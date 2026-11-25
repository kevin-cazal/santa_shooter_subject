# Partie 2, boîte à outils « Une liste » : une étagère à cartes. {} la crée
# vide, table.insert pose une carte à la fin, l'étiquette #points compte les
# cartes, points[2].x est la case x de la carte 2 : une position sur l'écran.
# La boucle passe sur chaque carte et dessine une étoile à sa position.
#
#   capture.py anim anim/liste.py LaListe -o img/outil-liste.webp --fps 30
from manim import *
from commun import *

CARTES = ((10, 20), (50, 80), (200, 110))


def carte(x, y, centre):
    cadre = RoundedRectangle(width=2.0, height=1.0, corner_radius=0.12, stroke_color=VERT, stroke_width=3,
                             fill_color=PANNEAU, fill_opacity=1).move_to(centre)
    cx = code(f"x = {x}", 22).move_to(cadre.get_center() + UP * 0.22)
    cy = code(f"y = {y}", 22).move_to(cadre.get_center() + DOWN * 0.22)
    return VGroup(cadre, cx, cy)


class LaListe(Scene):
    def construct(self):
        # L'étagère en haut, l'écran du jeu en bas à droite, le compteur en bas à gauche.
        etagere = VGroup(*[VGroup(Rectangle(width=2.2, height=1.2, stroke_color=GRIS, stroke_width=2, fill_opacity=0),
                                  code(f"[{i}]", 20, DOUX)) for i in (1, 2, 3)])
        for i, e in enumerate(etagere):
            e[0].move_to(RIGHT * (-2.4 + i * 2.4) + UP * 0.9)
            e[1].next_to(e[0], DOWN, buff=0.1)
        nom = code("points", 26, VERT).next_to(etagere, UP, buff=0.2).shift(LEFT * 2.4)
        n = ValueTracker(0)
        tag = always_redraw(lambda: VGroup(RoundedRectangle(width=2.2, height=0.5, corner_radius=0.1, stroke_color=ALERTE, stroke_width=2, fill_color=PANNEAU, fill_opacity=1),
                                           code(f"#points = {int(n.get_value())}", 18, ALERTE)).next_to(etagere, UP, buff=0.2).shift(RIGHT * 2.4))
        ecran = Ecran(px=0.02, centre=RIGHT * 3.6 + DOWN * 1.85)

        self.next_section("points = {} : une étagère vide")
        ligne = code("points = {}", 30).move_to(UP * 3.1)
        p = phrase("{} crée une liste vide : une étagère à cartes, avec des emplacements numérotés")
        self.play(Write(ligne), FadeIn(p), run_time=0.7)
        self.play(FadeIn(etagere), FadeIn(nom), FadeIn(tag), run_time=0.5)
        self.wait(0.8)

        self.next_section("table.insert pose une carte à la fin")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("table.insert pose une carte {x, y} à la fin : l'étiquette compte les cartes")
        self.play(FadeIn(p), run_time=0.3)
        cartes = []
        for i, (x, y) in enumerate(CARTES[:2]):
            l = code(f"table.insert(points, {{x = {x}, y = {y}}})", 26).move_to(ligne)
            self.play(FadeTransform(ligne, l), run_time=0.4)
            ligne = l
            c = carte(x, y, ligne.get_center())
            self.play(c.animate.move_to(etagere[i][0].get_center()), run_time=0.6)
            self.play(n.animate.set_value(i + 1), run_time=0.3)
            cartes.append(c)
        self.wait(0.5)

        self.next_section("points[2].x : la case x de la carte 2, une position sur l'écran")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("points[2].x, c'est la case x de la carte 2 : 50. Une carte, c'est une position sur l'écran")
        l = code("points[2].x", 30).move_to(ligne)
        self.play(FadeTransform(ligne, l), FadeIn(p), FadeIn(ecran.cadre), run_time=0.5)
        ligne = l
        s2 = surligne(cartes[1][1], ALERTE)
        self.play(Create(s2), run_time=0.4)
        x2, y2 = CARTES[1]
        etoile = Dot(radius=0.09, color=BLANC).move_to(ecran.pos(x2, y2))
        trait = DashedLine(cartes[1][0].get_bottom(), etoile.get_center(), stroke_color=ALERTE, stroke_width=2)
        self.play(Create(trait), FadeIn(etoile, scale=0.4), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(s2), FadeOut(trait), FadeOut(etoile), run_time=0.3)

        self.next_section("for i = 1, #points : chaque carte devient une étoile")
        self.play(FadeOut(p), FadeOut(ligne), run_time=0.3)
        prog = bloc_code(["for i = 1, #points do", "  -- une étoile en points[i]", "end"], 24).to_edge(LEFT, buff=0.6).shift(DOWN * 2.0)
        p = phrase("for i = 1, #points : la boucle passe sur chaque carte, et dessine une étoile à sa position")
        self.play(FadeIn(prog), FadeIn(p), run_time=0.4)
        v = ValueTracker(0)
        cpt = Compteur("i", v.get_value, chiffres=1, couleur=CIEL).scale(0.7)
        cpt.shift(RIGHT * 0.3 + DOWN * 2.0 - cpt.fenetre.get_center())
        self.add(cpt)
        # Une troisième carte pour que la boucle ait trois tours.
        c3 = carte(*CARTES[2], etagere[2][0].get_center())
        self.play(FadeIn(c3), n.animate.set_value(3), run_time=0.4)
        cartes.append(c3)
        for i, (x, y) in enumerate(CARTES, start=1):
            self.play(v.animate.set_value(i), run_time=0.35)
            s = surligne(cartes[i - 1], ALERTE)
            e = Dot(radius=0.09, color=BLANC).move_to(ecran.pos(x, y))
            self.play(Create(s), run_time=0.2)
            self.play(FadeTransform(cartes[i - 1].copy(), e), run_time=0.5)
            self.play(FadeOut(s), run_time=0.15)
        self.wait(0.4)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("ton ciel étoilé : 50 cartes sur l'étagère, et une boucle qui dessine chacune")
        self.play(FadeIn(p), run_time=0.3)
        self.wait(1.4)
