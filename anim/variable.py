# Partie 1, boîte à outils « Une variable » : un bocal avec un nom, et ce qu'il
# contient se voit dans le jeu (trois vies, trois bonnets dans le HUD). Le
# piège : créé dans TIC(), le bocal est rempli à chaque tour par la ligne
# vies = 3, et les vies ne baissent jamais. Hors de TIC(), créé une fois.
#
#   capture.py anim anim/variable.py LaVariable -o img/outil-variable.webp --fps 30
from manim import *
from commun import *

PX = 0.045   # un bonnet dans le bocal : 8 px × 0.045 = 0.36 u


def bonnet(centre):
    return sprite("joueur", PX, 1, centre + LEFT * 4 * PX + UP * 4 * PX)


class LaVariable(Scene):
    def construct(self):
        # Le bocal, à gauche ; l'écran du jeu, à droite ; le compteur de tours sous l'écran.
        bocal = RoundedRectangle(width=1.9, height=1.5, corner_radius=0.15, stroke_color=ALERTE, stroke_width=3,
                                 fill_color=PANNEAU, fill_opacity=1).move_to(LEFT * 3.4 + DOWN * 0.9)
        etiq = code("vies", 26, ALERTE).next_to(bocal, UP, buff=0.12)
        ecran = Ecran(px=0.024, centre=RIGHT * 3.4 + UP * 0.9)
        joueur = ecran.sprite("joueur", 40, 60, 2)
        tours = ValueTracker(0)
        cpt = Compteur("tour", tours.get_value, chiffres=2, couleur=CIEL).scale(0.65)
        cpt.shift(RIGHT * 3.4 + DOWN * 2.1 - cpt.fenetre.get_center())
        places = [bocal.get_center() + RIGHT * (i - 1) * 0.55 + DOWN * 0.15 for i in range(3)]
        hud = [ecran.pos(6 + i * 10, 6) for i in range(3)]

        # 1. Une boîte, trois vies dedans.
        self.next_section("vies = 3 : une boîte, trois vies dedans")
        ligne = code("vies = 3", 32).to_edge(LEFT, buff=0.8).shift(UP * 2.4)
        self.play(Write(ligne), run_time=0.7)
        p = phrase("une variable stocke une valeur : un bocal avec un nom, et trois vies dedans")
        self.play(FadeIn(p), FadeIn(bocal), FadeTransform(ligne[0:4].copy(), etiq), run_time=0.6)
        vies = []
        for pl in places:
            b = bonnet(pl + UP * 2.2)
            self.add(b)
            self.play(b.animate.shift(DOWN * 2.2), run_time=0.35)
            vies.append(b)
        self.wait(0.8)

        # 2. L'écran dessine ce qu'il y a dans la boîte.
        self.next_section("l'écran montre ce qu'il y a dans la boîte")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("le jeu dessine ce qu'il y a dans le bocal : trois bonnets en haut de l'écran")
        self.play(FadeIn(p), FadeIn(ecran.cadre), FadeIn(joueur), run_time=0.5)
        hud_v = []
        for b, h in zip(vies, hud):
            c = sprite("joueur", ecran.px, 1, h)
            self.play(FadeTransform(b.copy(), c), run_time=0.35)
            hud_v.append(c)
        self.wait(0.8)

        # 3. Le piège : dans TIC(), remplie à chaque tour.
        self.next_section("dans TIC() : la boîte est remplie à chaque tour")
        self.play(FadeOut(p), FadeOut(ligne), run_time=0.2)
        prog = bloc_code(["function TIC()", "  vies = 3", "  -- le jeu", "end"], 26).to_edge(LEFT, buff=0.8).shift(UP * 2.0)
        self.add(cpt)
        p = phrase("dans TIC(), la ligne vies = 3 remplit le bocal à chaque tour : touché, une vie part… et revient")
        coude = np.array([prog[1].get_right()[0] + 0.6, bocal.get_top()[1] + 0.25, 0])
        tuyau = VGroup(Line(prog[1].get_right() + RIGHT * 0.2, prog[1].get_right() + RIGHT * 0.6, stroke_color=ALERTE, stroke_width=5),
                       Line(prog[1].get_right() + RIGHT * 0.6, coude, stroke_color=ALERTE, stroke_width=5),
                       Line(coude, bocal.get_top() + UP * 0.25, stroke_color=ALERTE, stroke_width=5))
        self.play(FadeIn(prog), FadeIn(p), Create(tuyau), run_time=0.7)
        ennemi = ecran.sprite("ennemi", 200, 60, 2)
        self.add(ennemi)
        for t in range(1, 4):
            self.play(tours.animate.set_value(t), ennemi.animate.shift(LEFT * 160 * ecran.px), run_time=0.6, rate_func=linear)
            # Touché : une vie quitte le bocal et le HUD.
            self.play(Indicate(joueur, color=ROUGE, scale_factor=1.3), FadeOut(vies[2], shift=UP * 0.6), FadeOut(hud_v[2]), run_time=0.4)
            # ... et la ligne la remet aussitôt.
            s = surligne(prog[1])
            vies[2] = bonnet(places[2] + UP * 2.2)
            hud_v[2] = sprite("joueur", ecran.px, 1, hud[2])
            self.add(vies[2])
            self.play(Create(s), vies[2].animate.shift(DOWN * 2.2), run_time=0.35)
            self.play(FadeIn(hud_v[2]), FadeOut(s), run_time=0.2)
            ennemi.shift(RIGHT * 160 * ecran.px)
        self.wait(0.6)

        # 4. Hors de TIC() : une seule fois.
        self.next_section("hors de TIC() : créée une seule fois")
        self.play(FadeOut(p), FadeOut(tuyau), run_time=0.3)
        prog2 = bloc_code(["vies = 3", "", "function TIC()", "  -- le jeu", "end"], 26).move_to(prog).align_to(prog, LEFT)
        p = phrase("crée tes variables en haut du code, hors de TIC() : remplies une seule fois, les vies baissent")
        self.play(FadeTransform(prog, prog2), FadeIn(p), run_time=0.6)
        for t, k in ((4, 2), (5, 1)):
            self.play(tours.animate.set_value(t), ennemi.animate.shift(LEFT * 160 * ecran.px), run_time=0.6, rate_func=linear)
            self.play(Indicate(joueur, color=ROUGE, scale_factor=1.3), FadeOut(vies[k], shift=UP * 0.6), FadeOut(hud_v[k]), run_time=0.4)
            ennemi.shift(RIGHT * 160 * ecran.px)
            self.wait(0.3)
        self.wait(1.2)
