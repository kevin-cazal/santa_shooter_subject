# Partie 1, boîte à outils « Une fonction » : une machine à hublot sur un
# tapis. 4 entre, l'engrenage « * 2 » tourne, 8 sort et s'affiche sur l'écran
# du jeu. 10 entre, 20 sort : le même calcul. Puis la machine s'appelle
# check_collision : deux sprites entrent, une lampe verte s'allume.
#
#   capture.py anim anim/fonction.py LaFonction -o img/outil-fonction.webp --fps 30
from manim import *
from commun import *


def engrenage(centre, rayon=0.5, dents=8, couleur=GRIS):
    g = VGroup(Circle(radius=rayon, stroke_color=couleur, stroke_width=6, fill_color=PANNEAU, fill_opacity=1).move_to(centre))
    for k in range(dents):
        a = k * TAU / dents
        g.add(Line(centre + rayon * np.array([np.cos(a), np.sin(a), 0]), centre + (rayon + 0.18) * np.array([np.cos(a), np.sin(a), 0]),
                   stroke_color=couleur, stroke_width=8))
    return g


class LaFonction(Scene):
    def construct(self):
        prog = bloc_code(["function double(n)", "  return n * 2", "end"], 26).to_edge(LEFT, buff=0.6).shift(UP * 2.0)
        self.play(FadeIn(prog), run_time=0.5)
        # Le tapis, la machine et son hublot.
        y = DOWN * 0.2
        tapis = Line(LEFT * 4.5 + y, RIGHT * 4.6 + y, stroke_color=GRIS, stroke_width=3)
        machine = RoundedRectangle(width=3.2, height=2.2, corner_radius=0.2, stroke_color=ALERTE, stroke_width=4, fill_color=PANNEAU, fill_opacity=1).move_to(y + UP * 0.9)
        hublot = Circle(radius=0.75, stroke_color=DOUX, stroke_width=3, fill_color=FOND, fill_opacity=1).move_to(machine.get_center() + RIGHT * 0.45)
        roue = engrenage(hublot.get_center(), rayon=0.42)
        fois = code("* 2", 22, ALERTE).move_to(hublot.get_center())
        nom = code("double", 26, ALERTE).next_to(machine, UP, buff=0.15)
        entree = Boite("n", "", couleur=CIEL, largeur=0.9, centre=machine.get_center() + LEFT * 0.95)
        self.play(FadeIn(tapis), FadeIn(machine), FadeIn(hublot), FadeIn(roue), FadeIn(fois), FadeIn(nom), run_time=0.6)
        entree.poser(self, run_time=0.3)
        # L'écran du jeu, au bout du tapis.
        ecran = Ecran(px=0.016, centre=RIGHT * 4.6 + DOWN * 2.2)
        self.play(FadeIn(ecran.cadre), run_time=0.3)
        sorties = []

        def appel(val, lent):
            r = 1.0 if lent else 0.55
            ligne = code(f"print(double({val}))", 24).next_to(prog, DOWN, buff=0.5).align_to(prog, LEFT)
            self.play(FadeIn(ligne), run_time=0.3 * r)
            jeton = VGroup(Circle(radius=0.32, fill_color=CIEL, fill_opacity=1, stroke_width=0), code(str(val), 24, FOND)).move_to(ligne[12:12 + len(str(val))].get_center())
            self.play(jeton.animate.move_to(tapis.get_start() + RIGHT * 0.5 + UP * 0.32), run_time=0.4 * r)
            self.play(jeton.animate.move_to(entree.cadre.get_center()), run_time=0.5 * r)
            entree.changer(self, val, run_time=0.2 * r)
            self.remove(jeton)
            s = surligne(prog[1], ALERTE)
            res = VGroup(Circle(radius=0.32, fill_color=ALERTE, fill_opacity=1, stroke_width=0), code(str(val * 2), 24, FOND)).move_to(hublot.get_center())
            self.play(Create(s), Rotate(roue, TAU, about_point=hublot.get_center()), FadeIn(res, scale=0.3), run_time=0.9 * r)
            self.play(res.animate.move_to(machine.get_right() + RIGHT * 0.6 + DOWN * 0.78), run_time=0.4 * r)
            self.play(res.animate.move_to(tapis.get_end() + LEFT * 0.3 + UP * 0.32), run_time=0.4 * r)
            affiche = code(str(val * 2), 20, BLANC).move_to(ecran.pos(40 + 50 * len(sorties), 20))
            self.play(FadeTransform(res, affiche), FadeOut(s), FadeOut(ligne), run_time=0.4 * r)
            sorties.append(affiche)
            entree.changer(self, "", run_time=0.15)

        self.next_section("une fonction : une machine avec un nom")
        p = phrase("function double(n) : une machine nommée double, avec une entrée n")
        self.play(FadeIn(p), run_time=0.3)
        self.wait(1.0)

        self.next_section("double(4) : 4 entre, 8 sort")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("double(4) : 4 entre, 8 sort")
        self.play(FadeIn(p), run_time=0.3)
        appel(4, True)
        self.wait(0.5)

        self.next_section("double(10) : le même calcul, réutilisé")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("double(10) : la même machine, 20 sort")
        self.play(FadeIn(p), run_time=0.3)
        appel(10, False)
        self.wait(0.5)

        self.next_section("dans le jeu : check_collision allume une lampe")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("check_collision : deux sprites entrent, la lampe répond true ou false")
        nom2 = code("check_collision", 24, ALERTE).move_to(nom)
        lampe = Dot(radius=0.2, color=GRIS).move_to(machine.get_corner(UR) + LEFT * 0.35 + DOWN * 0.3)
        self.play(FadeIn(p), FadeTransform(nom, nom2), FadeTransform(fois, code("?", 22, ALERTE).move_to(fois)), FadeIn(lampe), run_time=0.6)
        a = sprite("joueur", 0.05, 1, tapis.get_start() + RIGHT * 0.3 + UP * 0.5)
        b = sprite("ennemi", 0.05, 1, tapis.get_start() + RIGHT * 0.9 + UP * 0.5)
        self.play(FadeIn(a), FadeIn(b), run_time=0.3)
        self.play(VGroup(a, b).animate.move_to(entree.cadre.get_center()), run_time=0.6)
        self.play(Rotate(roue, TAU, about_point=hublot.get_center()), lampe.animate.set_color(VERT), run_time=0.8)
        vrai = code("true", 24, VERT).next_to(lampe, RIGHT, buff=0.2)
        self.play(FadeIn(vrai), run_time=0.3)
        self.wait(1.2)
