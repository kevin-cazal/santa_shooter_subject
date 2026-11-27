# Partie 1, boîte à outils « Incrémenter », étape de modelage : la ligne reste
# affichée. Le bonnet porte son nombre x ; à chaque exécution de x = x + 1, x
# prend 1 de plus et le bonnet avance d'un pixel sur une loupe où chaque pixel
# se voit. Puis la loupe se referme sur l'écran réel, x continue, et à vitesse
# réelle le bonnet avance d'un pixel par image.
#
#   capture.py anim anim/incrementer.py Incrementer -o img/outil-incrementer.webp --fps 30
from manim import *
from commun import *

PX = 0.15
X0, X1, Y0, Y1 = 16, 76, 52, 76
COIN = LEFT * (X1 - X0) * PX / 2 + UP * ((Y1 - Y0) * PX / 2 - 0.3)


def pos(x, y):
    return COIN + RIGHT * (x - X0) * PX + DOWN * (y - Y0) * PX


class Incrementer(Scene):
    def construct(self):
        ligne = code("x = x + 1", 40).move_to(UP * 3.0)
        grille = VGroup(*[Line(pos(x, Y0), pos(x, Y1), stroke_color=DOUX, stroke_width=1, stroke_opacity=0.18) for x in range(X0, X1 + 1)],
                        *[Line(pos(X0, y), pos(X1, y), stroke_color=DOUX, stroke_width=1, stroke_opacity=0.18) for y in range(Y0, Y1 + 1)])
        cadre = Rectangle(width=(X1 - X0) * PX, height=(Y1 - Y0) * PX, stroke_color=DOUX, stroke_width=2).move_to(pos((X0 + X1) / 2, (Y0 + Y1) / 2))
        regle = VGroup(*[VGroup(Line(pos(x, Y1), pos(x, Y1) + DOWN * (0.22 if x % 5 == 0 else 0.1), stroke_color=DOUX, stroke_width=2),
                                code(str(x), 22, DOUX).next_to(pos(x, Y1) + DOWN * 0.22, DOWN, buff=0.08) if x % 5 == 0 else VGroup())
                         for x in range(X0, X1 + 1)])
        x = ValueTracker(20)
        bonnet = always_redraw(lambda: VGroup(sprite("joueur", PX, 1, pos(int(x.get_value()), 60)), origine(pos(int(x.get_value()), 60), rayon=0.08)))
        etiq = always_redraw(lambda: var(f"x = {int(x.get_value())}", C_JOUEUR, 26).next_to(pos(int(x.get_value()) + 4, 60), UP, buff=0.25))
        repere = always_redraw(lambda: DashedLine(pos(int(x.get_value()), 68), pos(int(x.get_value()), Y1) + DOWN * 0.22, stroke_color=CHANGE, stroke_width=2))

        self.next_section("x = 20 : le bonnet est à 20")
        p = phrase("le bonnet a un nombre, x : sa position. Ici x = 20")
        self.play(FadeIn(grille), FadeIn(cadre), FadeIn(regle), run_time=0.5)
        self.play(FadeIn(bonnet), FadeIn(repere), FadeIn(p), run_time=0.5)
        c = bapteme(self, "player x = 20", "x = 20", C_JOUEUR, 26, etiq.get_center())
        self.remove(c); self.add(etiq)
        self.wait(1.0)

        self.next_section("x = x + 1 : 21, un pixel plus à droite")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("x = x + 1 : x prend 1 de plus, le bonnet avance d'un pixel")
        self.play(Write(ligne), FadeIn(p), run_time=0.7)
        s = surligne(ligne, LU)
        self.play(Create(s), run_time=0.3)
        self.play(x.animate.set_value(21), run_time=0.6); self.wait(1.0)

        self.next_section("encore : 22, 23, 24")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("la même ligne, encore : 22, 23, 24, un pixel à chaque fois")
        self.play(FadeIn(p), run_time=0.3)
        for v in (22, 23, 24):
            self.play(FadeOut(s), run_time=0.1)
            self.play(Create(s), x.animate.set_value(v), run_time=0.45); self.wait(0.3)
        self.play(FadeOut(s), run_time=0.15)
        self.play(x.animate.set_value(44), run_time=1.6, rate_func=linear); self.wait(0.6)

        self.next_section("la loupe se referme : 60 fois par seconde, le bonnet avance")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("la loupe se referme sur l'écran : x continue, 60 fois par seconde")
        ecran = Ecran(px=0.03, centre=DOWN * 0.3)
        bonnet2 = always_redraw(lambda: VGroup(ecran.sprite("joueur", int(x.get_value()), 60, 2), origine(ecran.pos(int(x.get_value()), 60), rayon=0.05)))
        etiq2 = always_redraw(lambda: var(f"x = {int(x.get_value())}", C_JOUEUR, 22).next_to(ecran.pos(int(x.get_value()) + 8, 60), UP, buff=0.2))
        self.remove(bonnet, etiq, repere)
        self.play(FadeIn(p), FadeOut(grille), FadeOut(regle), FadeOut(cadre), FadeIn(ecran.cadre), FadeIn(bonnet2), FadeIn(etiq2), run_time=1.2)
        img = ValueTracker(0)
        cpt = Compteur("image", img.get_value, chiffres=3, couleur=LU).scale(0.65)
        cpt.shift(RIGHT * 5.3 + DOWN * 0.3 - cpt.fenetre.get_center())
        self.add(cpt)
        self.play(x.animate.set_value(44 + 150), img.animate.set_value(150), run_time=2.5, rate_func=linear)
        self.wait(1.0)
