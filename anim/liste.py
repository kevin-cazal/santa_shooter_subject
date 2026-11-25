# Partie 2, boîte à outils « Une liste » : {} la crée vide, table.insert ajoute
# une carte à la fin, #liste compte, liste[2].x lit une case d'une carte, et
# for i = 1, #liste passe sur chaque carte.
#
#   capture.py anim anim/liste.py LaListe -o img/outil-liste.webp --fps 30
from manim import *
from commun import *


def carte(x, y, centre):
    cadre = RoundedRectangle(width=2.0, height=1.0, corner_radius=0.12, stroke_color=VERT, stroke_width=3,
                             fill_color=PANNEAU, fill_opacity=1).move_to(centre)
    cx = code(f"x = {x}", 22).move_to(cadre.get_center() + UP * 0.22)
    cy = code(f"y = {y}", 22).move_to(cadre.get_center() + DOWN * 0.22)
    return VGroup(cadre, cx, cy)


class LaListe(Scene):
    def construct(self):
        # L'étagère : trois emplacements numérotés.
        etagere = VGroup(*[VGroup(Rectangle(width=2.2, height=1.2, stroke_color=GRIS, stroke_width=2, fill_opacity=0),
                                  code(f"[{i}]", 20, DOUX)) for i in (1, 2, 3)])
        for i, e in enumerate(etagere):
            e[0].move_to(RIGHT * (-2.4 + i * 2.4) + DOWN * 0.3)
            e[1].next_to(e[0], DOWN, buff=0.1)
        nom = code("points", 26, VERT).next_to(etagere, UP, buff=0.25)
        con = Console(self, RIGHT * 3.6 + DOWN * 2.2, largeur=5.0, hauteur=1.5, lignes=2)

        self.next_section("points = {} : une liste vide")
        ligne = code("points = {}", 30).move_to(UP * 2.9)
        p = phrase("{} crée une liste vide : des emplacements numérotés, rien dedans")
        self.play(Write(ligne), FadeIn(p), run_time=0.7)
        self.play(FadeIn(etagere), FadeIn(nom), run_time=0.5)
        self.wait(0.8)

        self.next_section("table.insert ajoute une carte à la fin")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("table.insert pose une table {x, y} à la fin : une carte dans le premier emplacement libre")
        self.play(FadeIn(p), run_time=0.3)
        cartes = []
        for i, (x, y) in enumerate(((10, 20), (50, 80))):
            l = code(f"table.insert(points, {{x = {x}, y = {y}}})", 26).move_to(ligne)
            self.play(FadeTransform(ligne, l), run_time=0.5)
            ligne = l
            c = carte(x, y, ligne.get_center())
            self.play(c.animate.move_to(etagere[i][0].get_center()), run_time=0.7)
            cartes.append(c)
            self.wait(0.3)
        self.wait(0.6)

        self.next_section("#points compte, points[2].x lit une case")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("#points, c'est le nombre de cartes : 2. points[2].x, c'est la case x de la carte 2 : 50")
        l = code("print(#points, points[2].x)", 26).move_to(ligne)
        self.play(FadeTransform(ligne, l), FadeIn(p), run_time=0.5)
        ligne = l
        s1 = surligne(VGroup(*cartes), CIEL)
        self.play(Create(s1), run_time=0.4)
        self.wait(0.5)
        s2 = surligne(cartes[1][1], ALERTE)
        self.play(FadeOut(s1), Create(s2), run_time=0.4)
        con.ecrire("2   50", run_time=0.3)
        self.play(FadeOut(s2), run_time=0.2)
        self.wait(0.8)

        self.next_section("for i = 1, #points : chaque carte à son tour")
        self.play(FadeOut(p), FadeOut(con.cadre), FadeOut(con.titre), *[FadeOut(x) for x in con.lignes], run_time=0.3)
        prog = bloc_code(["for i = 1, #points do", "  print(points[i].y)", "end"], 24).move_to(UP * 2.8)
        self.play(FadeOut(ligne), run_time=0.2)
        self.play(FadeIn(prog), run_time=0.4)
        p = phrase("for i = 1, #points : i vaut 1 puis 2, et points[i] est la carte numéro i")
        self.play(FadeIn(p), run_time=0.3)
        v = ValueTracker(0)
        cpt = Compteur("i", v.get_value, chiffres=1, couleur=CIEL).scale(0.7)
        cpt.shift(LEFT * 4.6 + DOWN * 2.5 - cpt.fenetre.get_center())
        self.add(cpt)
        con = Console(self, RIGHT * 3.6 + DOWN * 2.2, largeur=5.0, hauteur=1.5, lignes=2)
        for i in (1, 2):
            self.play(v.animate.set_value(i), run_time=0.4)
            s = surligne(cartes[i - 1][2], ALERTE)
            self.play(Create(s), run_time=0.3)
            con.ecrire(str((20, 80)[i - 1]), run_time=0.3)
            self.play(FadeOut(s), run_time=0.2)
        self.wait(0.4)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("tes 50 étoiles : une liste de 50 cartes, et une boucle qui passe sur chacune")
        self.play(FadeIn(p), run_time=0.3)
        self.wait(1.4)
