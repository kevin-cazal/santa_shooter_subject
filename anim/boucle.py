# Partie 1, « Intro » : la boucle de jeu. x = 0 une seule fois, puis TIC()
# tourne : x = x + 1 (on voit x = 0 + 1 devenir x = 1), cls efface l'écran
# (le bonnet disparaît), spr le redessine. Puis 60 fois par seconde.
#
#   capture.py anim anim/boucle.py LaBoucleDeJeu -o img/intro-boucle.webp --fps 30
from manim import *
from commun import *


class LaBoucleDeJeu(Scene):
    def construct(self):
        prog = bloc_code(["x = 0", "", "function TIC()", "  x = x + 1", "  cls(0)", "  spr(0, x, 60)", "end"], 28).to_edge(LEFT, buff=0.7).shift(UP * 1.0)
        large = max(l.width for l in prog) + 0.2
        haut = prog[0].height + 0.2

        def cadre(k, couleur=LU):
            r = Rectangle(width=large, height=haut, stroke_color=couleur, stroke_width=3, fill_opacity=0)
            return r.move_to(prog[k].get_left() + RIGHT * large / 2 + LEFT * 0.1).set_y(prog[k].get_y())

        ecran = Ecran(px=0.028, centre=RIGHT * 3.4 + UP * 1.6)
        x = ValueTracker(0)
        visible = ValueTracker(1)      # 0 pendant cls : l'écran est vide
        valeur = Compteur("x", x.get_value, chiffres=3).scale(0.75)
        valeur.shift(ecran.cadre.get_bottom() + DOWN * 1.5 - valeur.fenetre.get_center())
        self.add(ecran.cadre, prog, valeur)
        s = cadre(0)

        # 1. Avant TIC : une seule fois.
        self.next_section("x = 0 : une seule fois, au lancement")
        self.play(Create(s), run_time=0.5)
        p = phrase("x = 0 s'exécute une seule fois, au lancement")
        self.play(FadeIn(p)); self.wait(1.2)

        # 2. Update : x = 0 + 1 devient x = 1.
        self.next_section("x = x + 1 : x = 0 + 1, donc x = 1")
        s.set_y(prog[3].get_y())
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("x = x + 1 : x vaut 0, donc x = 0 + 1")
        calc = code("x = 0 + 1", 30, CHANGE).next_to(prog, DOWN, buff=0.6).align_to(prog, LEFT)
        self.play(FadeIn(p), FadeTransform(prog[3].copy(), calc), run_time=0.8)
        self.wait(1.0)
        res = code("x = 1", 30, CHANGE).move_to(calc).align_to(calc, LEFT)
        self.play(FadeTransform(calc, res), x.animate.set_value(1), run_time=0.8)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("x = 0 devient x = 1. L'écran, lui, n'a pas bougé")
        self.play(FadeIn(p)); self.wait(1.2)
        self.play(FadeOut(res), run_time=0.3)

        # 3. Draw : cls vide l'écran, spr dessine.
        self.next_section("cls efface l'écran, spr dessine le bonnet")
        s.set_y(prog[4].get_y())
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("cls(0) : l'écran est effacé, il est vide")
        voile = ecran.cadre.copy().set_fill(BLANC, opacity=0.3).set_stroke(width=0)
        self.play(FadeIn(p), FadeIn(voile), run_time=0.3)
        self.play(FadeOut(voile), run_time=0.3); self.wait(0.8)
        s.set_y(prog[5].get_y())
        joueur = always_redraw(lambda: ecran.sprite("joueur", int(x.get_value()), 60, 2).set_opacity(visible.get_value()))
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("spr(0, x, 60) : le bonnet est dessiné à la position x")
        self.play(FadeIn(joueur, scale=0.6), FadeIn(p), run_time=0.6); self.wait(1.2)

        # 4. Et on recommence : d'abord lentement, le bonnet disparaît entre cls et spr.
        self.next_section("et on recommence : 60 fois par seconde")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("tour suivant : x = 1 + 1, cls efface, spr redessine un pixel plus loin")
        self.play(FadeIn(p), run_time=0.4)
        for duree in (0.45, 0.45, 0.3, 0.3, 0.2, 0.2, 0.12, 0.12, 0.12):
            s.set_y(prog[3].get_y())
            self.play(x.animate.set_value(x.get_value() + 1), run_time=duree, rate_func=linear)
            s.set_y(prog[4].get_y()); visible.set_value(0); self.wait(duree * 0.6)
            s.set_y(prog[5].get_y()); visible.set_value(1); self.wait(duree * 0.6)
        self.remove(s)
        boucle = SurroundingRectangle(prog[3:6], color=LU, buff=0.08, stroke_width=3)
        self.add(boucle)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("60 tours par seconde : le bonnet avance d'un pixel par image")
        self.play(FadeIn(p), x.animate.set_value(x.get_value() + 100), run_time=1.8, rate_func=linear)
        self.wait(1.2)
