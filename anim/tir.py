# Partie 1, boîte à outils « Un seul missile » : ses trois nombres sont
# d'abord collés au sprite, puis rangés sur le côté, reliés par un fil. Deux
# états, dits avec le mot exact : « prêt à être tiré », « tiré ». Au ralenti,
# vmx s'ajoute à mx image par image. Puis un curseur vmx : 0, le missile
# ne part pas ; 8, plus vite ; -3, il recule. Sorti à droite, il est remis
# prêt à être tiré.
#
#   capture.py anim anim/tir.py LeTir -o img/tir-cycle.webp --fps 30
from manim import *
from commun import *

JX, JY = 20, 60
REPOS = (-24, -24)


class LeTir(Scene):
    def construct(self):
        ecran = Ecran(px=0.03, centre=LEFT * 1.4 + UP * 0.5)
        mx, my, vmx = ValueTracker(REPOS[0]), ValueTracker(REPOS[1]), ValueTracker(0)
        cote = ValueTracker(0)        # 0 : les nombres collés au missile ; 1 : rangés sur le côté
        joueur = ecran.sprite("joueur", JX, JY, 2)
        missile = always_redraw(lambda: ecran.sprite_clippe("missile", int(mx.get_value()), int(my.get_value()), 2))
        point = always_redraw(lambda: origine(ecran.pos(mx.get_value(), my.get_value())))
        LOIN = RIGHT * 4.6 + UP * 1.6

        def pres():
            # Au repos le missile est hors de l'écran : ses nombres se posent juste sous le coin, lisibles.
            if mx.get_value() < 0:
                return ecran.cadre.get_corner(UL) + RIGHT * 1.5 + DOWN * 0.75
            return ecran.pos(mx.get_value() + 20, my.get_value() + 6) + RIGHT * 0.9

        def tags_f():
            g = VGroup(etiquette(f"mx  = {int(mx.get_value()):>4}", BLANC, 26),
                       etiquette(f"my  = {int(my.get_value()):>4}", BLANC, 26),
                       etiquette(f"vmx = {int(vmx.get_value()):>4}", CHANGE, 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
            return g.move_to(interpolate(pres(), LOIN, cote.get_value()))

        tags = always_redraw(tags_f)
        lien = always_redraw(lambda: fil(ecran.pos(mx.get_value(), my.get_value()), tags.get_left() + LEFT * 0.1).set_opacity(cote.get_value()))
        etat = always_redraw(lambda: (badge("tiré", LU) if mx.get_value() >= 0 else badge("prêt à être tiré", GRIS)).next_to(joueur, DOWN, buff=0.3))
        fleche = always_redraw(lambda: fleche_vitesse(ecran.pos(mx.get_value(), my.get_value() + 8), vmx.get_value(), 0, echelle=0.05)
                               .set_opacity(1 if vmx.get_value() != 0 and 0 <= mx.get_value() < W else 0))
        touche = manette("Z").move_to(RIGHT * 4.6 + DOWN * 0.4)
        self.add(ecran.cadre, joueur, missile, point, lien, tags, etat, fleche, touche)

        def appui():
            self.play(Transform(touche, manette("Z", True).move_to(touche)), run_time=0.12)
            self.play(Transform(touche, manette("Z").move_to(touche)), run_time=0.12)

        def retour():
            # Remis d'un coup, comme dans le code : pas de trajet visible.
            mx.set_value(REPOS[0]); my.set_value(REPOS[1]); vmx.set_value(0)
            self.wait(0.3)

        # 1. Prêt à être tiré.
        self.next_section("prêt à être tiré : hors de l'écran, vmx = 0")
        p = phrase("prêt à être tiré : hors de l'écran, vitesse 0")
        self.play(FadeIn(p), Indicate(point, color=CHANGE, scale_factor=2), run_time=1.0); self.wait(1.2)

        # 2. Le tir.
        self.next_section("appui sur Z : tiré depuis le joueur")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("appui sur Z : le missile est tiré depuis le joueur, vmx = 3")
        self.play(FadeIn(p), run_time=0.3)
        appui()
        self.play(mx.animate.set_value(JX + 16), my.animate.set_value(JY), vmx.animate.set_value(3), run_time=0.4)
        self.wait(0.8)
        self.play(cote.animate.set_value(1), run_time=0.9); self.wait(0.6)

        # 3. Au ralenti : vmx s'ajoute à mx.
        self.next_section("au ralenti : mx = mx + vmx à chaque image")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("au ralenti : à chaque image, vmx s'ajoute à mx")
        ligne = code("mx = mx + vmx", 26, BLANC).move_to(RIGHT * 4.6 + DOWN * 1.6)
        img = ValueTracker(0)
        cpt = Compteur("image", img.get_value, chiffres=1, couleur=LU).scale(0.6)
        cpt.shift(RIGHT * 4.6 + DOWN * 2.9 - cpt.fenetre.get_center())
        self.add(cpt)
        self.play(FadeIn(p), Write(ligne), run_time=0.6)
        for k in range(1, 7):
            jeton = VGroup(Circle(radius=0.22, fill_color=CHANGE, fill_opacity=1, stroke_width=0), code("+3", 18, FOND)).move_to(tags[2].get_right() + LEFT * 0.3)
            self.play(FadeIn(jeton, scale=0.5), run_time=0.1)
            self.play(jeton.animate.move_to(tags[0].get_right() + LEFT * 0.3), run_time=0.3)
            self.play(FadeOut(jeton, scale=0.3), mx.animate.set_value(mx.get_value() + 3), img.animate.set_value(k), run_time=0.2, rate_func=linear)
        self.wait(0.6)
        self.play(FadeOut(p), FadeOut(ligne), FadeOut(cpt), run_time=0.3)
        p = phrase("à vitesse réelle : il avance tout droit")
        self.play(FadeIn(p), mx.animate.set_value(W + 20), run_time=1.6, rate_func=linear)

        # 4. Sorti : remis prêt à être tiré.
        self.next_section("sorti à droite : remis prêt à être tiré")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("sorti à droite : remis hors de l'écran, vitesse 0, prêt à être tiré")
        retour()
        self.play(FadeIn(p), run_time=0.3); self.wait(1.2)

        # 5. Le curseur vmx : une bonne valeur, et deux qui ne marchent pas.
        self.next_section("vmx : 0, 8, -3")
        self.play(FadeOut(p), run_time=0.2)
        reg = Reglage("vmx", -4, 10, 0, CHANGE).placer(RIGHT * 4.6 + DOWN * 2.2)
        p = phrase("vmx = 0 : appui sur Z, mais le missile ne part pas")
        self.play(FadeIn(reg), FadeIn(p), run_time=0.4)
        appui()
        self.play(mx.animate.set_value(JX + 16), my.animate.set_value(JY), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("vmx = 8 : il va plus vite")
        self.play(FadeIn(p), reg.t.animate.set_value(8), vmx.animate.set_value(8), run_time=0.6)
        self.play(mx.animate.set_value(W + 20), run_time=0.8, rate_func=linear)
        retour()
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("vmx = -3 : il recule, vers le joueur")
        self.play(FadeIn(p), reg.t.animate.set_value(-3), run_time=0.5)
        appui()
        self.play(mx.animate.set_value(JX + 60), my.animate.set_value(JY), vmx.animate.set_value(-3), run_time=0.3)
        self.play(mx.animate.set_value(-24), run_time=1.6, rate_func=linear)
        retour()
        self.play(FadeOut(p), reg.t.animate.set_value(3), run_time=0.3)
        p = phrase("vmx = 3 : tiré, il sort à droite, remis prêt à être tiré")
        self.play(FadeIn(p), run_time=0.3)
        appui()
        self.play(mx.animate.set_value(JX + 16), my.animate.set_value(JY), vmx.animate.set_value(3), run_time=0.3)
        self.play(mx.animate.set_value(W + 20), run_time=1.6, rate_func=linear)
        retour(); self.wait(1.2)
