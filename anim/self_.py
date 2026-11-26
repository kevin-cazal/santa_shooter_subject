# Partie 3, boîte à outils « Une fonction dans une table, et self » : le chat
# est une carte avec une jauge de faim. chat:manger() fait entrer la carte dans
# la fonction, où elle s'appelle self ; la jauge baisse d'un cran ; la carte
# ressort changée. Puis la carte player entre dans player:update() et ressort
# déplacée d'un pixel.
#
#   capture.py anim anim/self_.py LeSelf -o img/outil-self.webp --fps 30
from manim import *
from commun import *


class Carte:
    """Une table dessinée : un nom, une case texte, une jauge à crans pour la case nombre."""

    def __init__(self, nom, texte_case, jauge_nom, crans, max_crans=5, couleur=VERT, centre=ORIGIN):
        self.cadre = RoundedRectangle(width=2.6, height=1.5, corner_radius=0.15, stroke_color=couleur, stroke_width=3,
                                      fill_color=PANNEAU, fill_opacity=1).move_to(centre)
        self.titre = code(nom, 24, couleur).next_to(self.cadre, UP, buff=0.12)
        self.ligne1 = code(texte_case, 20).move_to(self.cadre.get_center() + UP * 0.4)
        self.jnom = code(jauge_nom, 20).move_to(self.cadre.get_center() + DOWN * 0.3 + LEFT * 0.85)
        self.crans = VGroup(*[Rectangle(width=0.22, height=0.32, stroke_color=DOUX, stroke_width=1.5,
                                        fill_color=ALERTE if k < crans else PANNEAU, fill_opacity=1)
                              .move_to(self.cadre.get_center() + DOWN * 0.3 + RIGHT * (-0.1 + k * 0.28)) for k in range(max_crans)])
        self.n = crans
        self.tout = VGroup(self.cadre, self.ligne1, self.jnom, self.crans, self.titre)

    def baisser(self, scene, run_time=0.5):
        self.n -= 1
        scene.play(self.crans[self.n].animate.set_fill(PANNEAU), Flash(self.crans[self.n], color=ALERTE, flash_radius=0.35), run_time=run_time)


class LeSelf(Scene):
    def construct(self):
        self.next_section("chat : une table avec des cases")
        prog = bloc_code(['chat = {nom = "Félix", faim = 3}', "", "function chat:manger()", "  self.faim = self.faim - 1", "end", "",
                          "chat:manger()"], 22).to_edge(LEFT, buff=0.6).shift(UP * 1.2)
        self.play(FadeIn(prog), run_time=0.6)
        chat = Carte("chat", 'nom = "Félix"', "faim", 3, centre=RIGHT * 3.4 + UP * 2.0)
        p = phrase("chat est une table : une case nom, une jauge faim à 3")
        self.play(FadeIn(p), FadeIn(chat.tout), run_time=0.5)
        self.wait(0.8)

        self.next_section("function chat:manger() : une fonction de la table")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("avec deux-points, manger est une fonction de la table chat")
        s = surligne(prog[2:5], ALERTE)
        fn = RoundedRectangle(width=4.2, height=2.3, corner_radius=0.2, stroke_color=ALERTE, stroke_width=3,
                              fill_color=PANNEAU, fill_opacity=0.5).move_to(RIGHT * 3.4 + DOWN * 1.2)
        fn_nom = code("manger", 24, ALERTE).next_to(fn, UP, buff=0.12)
        self.play(FadeIn(p), Create(s), FadeIn(fn), FadeIn(fn_nom), run_time=0.6)
        self.wait(0.9)

        self.next_section("chat:manger() : la carte entre, sous le nom self")
        self.play(FadeOut(p), FadeOut(s), run_time=0.2)
        p = phrase("chat:manger() : la carte entre dans la fonction, sous le nom self")
        s = surligne(prog[6], CIEL)
        self.play(FadeIn(p), Create(s), run_time=0.4)
        self.play(VGroup(chat.cadre, chat.ligne1, chat.jnom, chat.crans).animate.move_to(fn.get_center() + DOWN * 0.1), FadeOut(chat.titre), run_time=0.8)
        etiq = code("self", 22, CIEL).next_to(chat.cadre, UP, buff=0.1)
        self.play(FadeIn(etiq), run_time=0.3)
        self.wait(0.4)
        self.play(FadeOut(p), Transform(s, surligne(prog[3], ALERTE)), run_time=0.3)
        p = phrase("self.faim : la jauge de cette carte, moins 1")
        self.play(FadeIn(p), run_time=0.3)
        chat.baisser(self)
        self.wait(0.6)

        self.next_section("la carte ressort changée")
        self.play(FadeOut(p), FadeOut(s), FadeOut(etiq), run_time=0.2)
        p = phrase("la carte ressort : sa jauge est à 2, la table a changé")
        self.play(FadeIn(p), VGroup(chat.cadre, chat.ligne1, chat.jnom, chat.crans).animate.move_to(RIGHT * 3.4 + UP * 2.0), run_time=0.8)
        chat.titre.next_to(chat.cadre, UP, buff=0.12)
        self.play(FadeIn(chat.titre), run_time=0.3)
        self.wait(0.8)

        self.next_section("dans le jeu : player:update() reçoit la table player")
        self.play(FadeOut(p), FadeOut(prog), FadeOut(chat.tout), run_time=0.3)
        prog2 = bloc_code(["function player:update()", "  -- bouger", "end", "", "player:update()"], 22).to_edge(LEFT, buff=0.6).shift(UP * 1.2)
        fn_nom2 = code("update", 24, ALERTE).move_to(fn_nom)
        p = phrase("dans le jeu : player entre dans player:update() et ressort déplacée")
        self.play(FadeIn(prog2), FadeTransform(fn_nom, fn_nom2), FadeIn(p), run_time=0.5)
        pl = RoundedRectangle(width=2.6, height=1.5, corner_radius=0.15, stroke_color=VERT, stroke_width=3, fill_color=PANNEAU, fill_opacity=1).move_to(RIGHT * 3.4 + UP * 2.0)
        pt = code("player", 24, VERT).next_to(pl, UP, buff=0.12)
        x = ValueTracker(20)
        px = always_redraw(lambda: code(f"x = {int(x.get_value())}", 20).move_to(pl.get_center() + UP * 0.4 + LEFT * 0.5))
        hat = sprite("joueur", 0.06, 1, pl.get_center() + RIGHT * 0.3 + DOWN * 0.1)
        self.play(FadeIn(pl), FadeIn(pt), FadeIn(px), FadeIn(hat), run_time=0.4)
        grp = VGroup(pl, hat)
        self.play(grp.animate.move_to(fn.get_center() + DOWN * 0.1), FadeOut(pt), run_time=0.7)
        etiq = code("self", 22, CIEL).next_to(pl, UP, buff=0.1)
        s = surligne(prog2[1], ALERTE)
        self.play(FadeIn(etiq), Create(s), run_time=0.3)
        self.play(x.animate.set_value(21), hat.animate.shift(RIGHT * 0.18), run_time=0.5)
        self.play(FadeOut(etiq), FadeOut(s), grp.animate.move_to(RIGHT * 3.4 + UP * 2.0), run_time=0.7)
        self.play(FadeIn(pt), run_time=0.3)
        self.wait(1.2)
