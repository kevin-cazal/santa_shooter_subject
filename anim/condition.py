# Partie 1, boîte à outils « if » : trois panneaux. À gauche la touche
# « flèche droite », au milieu le schéma de la condition (quelle branche est
# prise selon l'état de la touche), à droite l'écran du jeu où le bonnet
# avance seulement quand la touche est appuyée.
#
#   capture.py anim anim/condition.py LaCondition -o img/outil-if.webp --fps 30
from manim import *
from commun import *


class LaCondition(Scene):
    def construct(self):
        # La touche, à gauche.
        touche = manette("→", False, taille=0.9).move_to(LEFT * 5.2 + UP * 0.4)
        nom_t = texte("flèche droite", 22, DOUX).next_to(touche, DOWN, buff=0.2)
        # Le schéma, au milieu : btn(3) ? puis deux branches.
        losange = VGroup(Square(side_length=1.7, stroke_color=LU, stroke_width=3, fill_color=PANNEAU, fill_opacity=1).rotate(PI / 4),
                         code("btn(3) ?", 24)).move_to(LEFT * 1.6 + UP * 1.6)
        vrai_b = RoundedRectangle(width=2.4, height=0.8, corner_radius=0.15, stroke_color=VRAI, stroke_width=3, fill_color=PANNEAU, fill_opacity=1).move_to(LEFT * 1.6 + DOWN * 1.4)
        vrai_t = texte("le bonnet avance", 20).move_to(vrai_b)
        faux_b = RoundedRectangle(width=2.0, height=0.8, corner_radius=0.15, stroke_color=FAUX, stroke_width=3, fill_color=PANNEAU, fill_opacity=1).move_to(RIGHT * 1.4 + DOWN * 1.4)
        faux_t = texte("rien", 20).move_to(faux_b)
        br_vrai = Arrow(losange.get_bottom(), vrai_b.get_top(), buff=0.05, color=VRAI, stroke_width=4)
        br_faux = Arrow(losange.get_right(), faux_b.get_top(), buff=0.05, color=FAUX, stroke_width=4)
        et_vrai = texte("vrai", 22, VRAI).next_to(br_vrai, LEFT, buff=0.1)
        et_faux = texte("faux", 22, FAUX).next_to(br_faux, UP, buff=0.05).shift(RIGHT * 0.5)
        schema = VGroup(losange, br_vrai, br_faux, et_vrai, et_faux, vrai_b, vrai_t, faux_b, faux_t)
        # L'écran, à droite.
        ecran = Ecran(px=0.022, centre=RIGHT * 4.3 + UP * 0.4)
        x = ValueTracker(30)
        joueur = always_redraw(lambda: ecran.sprite("joueur", int(x.get_value()), 60, 2))
        self.add(touche, nom_t, schema, ecran.cadre, joueur)

        def allumer(vrai):
            """La branche prise s'allume, l'autre s'éteint."""
            self.play(br_vrai.animate.set_opacity(1 if vrai else 0.25), vrai_b.animate.set_stroke(opacity=1 if vrai else 0.25),
                      et_vrai.animate.set_opacity(1 if vrai else 0.25), vrai_t.animate.set_opacity(1 if vrai else 0.3),
                      br_faux.animate.set_opacity(0.25 if vrai else 1), faux_b.animate.set_stroke(opacity=0.25 if vrai else 1),
                      et_faux.animate.set_opacity(0.25 if vrai else 1), faux_t.animate.set_opacity(0.3 if vrai else 1), run_time=0.4)

        self.next_section("touche relâchée : btn(3) est faux, rien")
        p = phrase("touche relâchée : btn(3) est faux, branche « rien »")
        self.play(FadeIn(p), run_time=0.3)
        allumer(False); self.wait(1.4)

        self.next_section("touche appuyée : btn(3) est vrai, le bonnet avance")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("touche appuyée : btn(3) est vrai, le bonnet avance")
        self.play(FadeIn(p), Transform(touche, manette("→", True, taille=0.9).move_to(touche)), run_time=0.3)
        allumer(True)
        self.play(x.animate.set_value(110), run_time=1.6, rate_func=linear)
        self.wait(0.6)

        self.next_section("relâchée : faux, le bonnet s'arrête")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("relâchée : faux, le bonnet s'arrête aussitôt")
        self.play(FadeIn(p), Transform(touche, manette("→", False, taille=0.9).move_to(touche)), run_time=0.3)
        allumer(False); self.wait(1.2)

        self.next_section("appuyée encore : vrai, il avance de nouveau")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("60 fois par seconde, la question est posée : vrai, il avance")
        self.play(FadeIn(p), Transform(touche, manette("→", True, taille=0.9).move_to(touche)), run_time=0.3)
        allumer(True)
        self.play(x.animate.set_value(190), run_time=1.6, rate_func=linear)
        self.play(Transform(touche, manette("→", False, taille=0.9).move_to(touche)), run_time=0.3)
        allumer(False); self.wait(1.2)
