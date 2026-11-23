# Partie 1, « Logique additionnelle » : la vie d'un seul missile, en boucle.
# Au repos hors de l'écran avec une vitesse nulle ; au tir il prend la position
# du joueur et une vitesse ; il avance ; sorti à droite, il revient au repos.
# La condition du tir reste à écrire : on montre les états, pas le if.
#
#   capture.py anim anim/tir.py LeTir -o img/tir-cycle.webp
from manim import *
from commun import *

JX, JY = 20, 60      # le joueur ne bouge pas ici
REPOS = (-10, -10)


class LeTir(Scene):
    def construct(self):
        ecran = Ecran(px=0.03, centre=LEFT * 1.4 + UP * 0.3)
        mx, my, vmx = ValueTracker(REPOS[0]), ValueTracker(REPOS[1]), ValueTracker(0)
        joueur = ecran.sprite("joueur", JX, JY, 2)
        missile = always_redraw(lambda: ecran.sprite("missile", int(mx.get_value()), int(my.get_value()), 2))
        tags = always_redraw(lambda: VGroup(
            etiquette(f"mx  = {int(mx.get_value()):>4}", BLANC, 26),
            etiquette(f"my  = {int(my.get_value()):>4}", BLANC, 26),
            etiquette(f"vmx = {int(vmx.get_value()):>4}", ALERTE, 26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.6 + UP * 1.2))
        touche = manette("Z").next_to(tags, DOWN, buff=0.8)
        self.add(ecran.cadre, joueur, missile, tags, touche)

        def tir():
            allumee = manette("Z", True).move_to(touche)
            self.play(Transform(touche, allumee), run_time=0.15)
            self.play(mx.animate.set_value(JX + 16), my.animate.set_value(JY + 6), vmx.animate.set_value(3), run_time=0.3)
            self.play(Transform(touche, manette("Z").move_to(touche)), run_time=0.15)

        def vol(duree):
            self.play(mx.animate.set_value(W + 10), run_time=duree, rate_func=linear)

        def retour():
            self.play(mx.animate.set_value(REPOS[0]), my.animate.set_value(REPOS[1]), vmx.animate.set_value(0), run_time=0.4)

        # 1. Au repos.
        self.next_section("au repos : hors de l'écran, vitesse 0")
        p = phrase("le missile attend hors de l'écran : on ne le voit pas, mais il existe")
        self.play(FadeIn(p), Indicate(missile, color=ALERTE, scale_factor=1.6), run_time=1.2)
        self.wait(1.2)

        # 2. Le tir.
        self.next_section("le tir : il part de la position du joueur")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("appui sur Z : le missile prend la position du joueur, et une vitesse")
        self.play(FadeIn(p), run_time=0.3)
        tir()
        self.wait(1.2)

        # 3. Il avance.
        self.next_section("il avance : mx = mx + vmx, à chaque image")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("à chaque image, mx = mx + vmx : il avance tout droit")
        self.play(FadeIn(p), run_time=0.3)
        vol(2.4)

        # 4. Retour au repos.
        self.next_section("sorti par la droite : retour au repos")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("sorti par la droite : il revient au repos, prêt pour le tir suivant")
        retour()
        self.play(FadeIn(p), run_time=0.3)
        self.wait(1.2)
        # Un deuxième tour, plus vite : c'est une boucle.
        tir()
        vol(1.2)
        retour()
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("un seul missile, qui fait des tours")
        self.play(FadeIn(p), run_time=0.4)
        self.wait(1.4)
