# Partie 3, boîte à outils « Une fonction dans une table, et self » : écrite
# avec deux-points, la fonction reçoit la table elle-même sous le nom self.
# chat:manger() : la boîte chat entre dans la fonction, self.faim passe de 0 à -1.
#
#   capture.py anim anim/self_.py LeSelf -o img/outil-self.webp --fps 15
from manim import *
from commun import *


def table(nom, lignes, couleur, centre):
    rangs = VGroup(*[code(l, 22) for l in lignes]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    cadre = RoundedRectangle(width=rangs.width + 0.8, height=rangs.height + 0.5, corner_radius=0.15,
                             stroke_color=couleur, stroke_width=3, fill_color=PANNEAU, fill_opacity=1)
    rangs.move_to(cadre)
    titre_ = code(nom, 24, couleur).next_to(cadre, UP, buff=0.12)
    return VGroup(cadre, rangs, titre_).move_to(centre)


class LeSelf(Scene):
    def construct(self):
        self.next_section("chat : une table avec des cases")
        prog = bloc_code(['chat = {nom = "Félix", faim = 0}', "", "function chat:manger()", "  self.faim = self.faim - 1", "end", "",
                          "chat:manger()", "print(chat.faim)"], 24).to_edge(LEFT, buff=0.6).shift(UP * 0.6)
        self.play(FadeIn(prog), run_time=0.6)
        chat = table("chat", ['nom = "Félix"', "faim = 0"], VERT, RIGHT * 3.2 + UP * 2.2)
        p = phrase("chat est une table : deux cases, nom et faim")
        self.play(FadeIn(p), FadeIn(chat), run_time=0.5)
        self.wait(0.8)

        self.next_section("function chat:manger() : une fonction dans la table")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("avec deux-points, manger est une fonction de la table chat. Elle attend qu'on l'appelle")
        s = surligne(prog[2:5], ALERTE)
        fn = RoundedRectangle(width=4.2, height=1.9, corner_radius=0.2, stroke_color=ALERTE, stroke_width=3,
                              fill_color=PANNEAU, fill_opacity=0.6).move_to(RIGHT * 3.2 + DOWN * 1.1)
        fn_nom = code("manger", 24, ALERTE).next_to(fn, UP, buff=0.12)
        self.play(FadeIn(p), Create(s), FadeIn(fn), FadeIn(fn_nom), run_time=0.6)
        self.wait(1.0)

        self.next_section("chat:manger() : la table entre sous le nom self")
        self.play(FadeOut(p), FadeOut(s), run_time=0.2)
        p = phrase("chat:manger() : la table chat entre dans la fonction, où elle s'appelle self")
        s = surligne(prog[6], CIEL)
        self.play(FadeIn(p), Create(s), run_time=0.4)
        self.play(chat.animate.scale(0.8).move_to(fn.get_center()), run_time=0.8)
        etiq = code("self", 22, CIEL).next_to(chat[0], LEFT, buff=0.15)
        self.play(FadeTransform(chat[2], etiq), run_time=0.5)
        self.wait(0.6)
        self.play(FadeOut(p), Transform(s, surligne(prog[3], ALERTE)), run_time=0.3)
        p = phrase("self.faim, c'est la case faim de cette table : 0 - 1, elle passe à -1")
        s2 = surligne(chat[1][1], ALERTE)
        self.play(FadeIn(p), Create(s2), run_time=0.4)
        nv = code("faim = -1", 22 * 0.8 / 0.8).scale(0.8).move_to(chat[1][1]).align_to(chat[1][1], LEFT)
        self.play(FadeTransform(chat[1][1], nv), run_time=0.5)
        chat[1].remove(chat[1][1]); chat[1].add(nv)
        self.play(FadeOut(s2), run_time=0.2)
        self.wait(0.6)

        self.next_section("print(chat.faim) : -1, la table a changé")
        self.play(FadeOut(p), FadeOut(s), run_time=0.2)
        p = phrase("la fonction finie, chat ressort : sa case faim vaut -1. print(chat.faim) affiche -1")
        titre2 = code("chat", 24, VERT)
        self.play(FadeIn(p), FadeOut(etiq), chat.animate.scale(1.25).move_to(RIGHT * 3.2 + UP * 2.2), run_time=0.8)
        titre2.next_to(chat[0], UP, buff=0.12)
        self.play(FadeIn(titre2), run_time=0.3)
        con = Console(self, LEFT * 3.2 + DOWN * 2.3, largeur=4.4, hauteur=1.2, lignes=1)
        s = surligne(prog[7], CIEL)
        self.play(Create(s), run_time=0.3)
        con.ecrire("-1")
        self.play(FadeOut(s), run_time=0.2)
        self.wait(0.5)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("dans le jeu : player:update() reçoit la table player sous le nom self")
        self.play(FadeIn(p), run_time=0.3)
        self.wait(1.4)
