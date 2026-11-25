# Partie 1, « Intro » : le concept du jeu. Une variable se crée une seule fois,
# puis TIC() tourne 60 fois par seconde : mettre à jour les nombres, effacer
# l'écran, dessiner. Le mouvement, c'est des images qui se suivent.
# Pas de btn ici : c'est la boucle qu'on montre, pas l'étape Input.
#
#   capture.py anim anim/boucle.py LaBoucleDeJeu -o img/intro-boucle.webp --fps 30
from manim import *
from commun import *


class LaBoucleDeJeu(Scene):
    def construct(self):
        prog = bloc_code([
            "x = 0",
            "",
            "function TIC()",
            "  x = x + 1",
            "  cls(0)",
            "  spr(0, x, 60)",
            "end",
        ], 28).to_edge(LEFT, buff=0.7).shift(UP * 0.5)
        large = max(l.width for l in prog) + 0.2
        haut = prog[0].height + 0.2

        def surligne(ligne, couleur=ALERTE):
            # Même taille pour toutes les lignes : passer de l'une à l'autre est
            # un glissement, pas un morphing qui raye le code à mi-chemin.
            r = Rectangle(width=large, height=haut, stroke_color=couleur, stroke_width=3, fill_opacity=0)
            return r.move_to(ligne.get_left() + RIGHT * large / 2 + LEFT * 0.1).set_y(ligne.get_y())
        ecran = Ecran(px=0.028, centre=RIGHT * 3.4 + UP * 1.4)
        x = ValueTracker(0)
        # Le compteur à rouleaux : la façon convenue de montrer une boucle qui tourne.
        valeur = Compteur("x", x.get_value, chiffres=3).scale(0.75)
        # Assez bas pour que ses caches, couleur du fond, ne coupent pas le bord de l'écran.
        valeur.shift(ecran.cadre.get_bottom() + DOWN * 1.6 - valeur.fenetre.get_center())
        self.add(ecran.cadre, prog)

        # 1. Avant TIC : une seule fois.
        self.next_section("avant TIC : les variables, une seule fois")
        s = surligne(prog[0])

        def aller(k):
            s.set_y(prog[k].get_y())
            return Wait(0)   # le saut est immédiat ; on garde la forme d'une animation

        self.add(valeur)
        self.play(Create(s), run_time=0.6)
        p = phrase("cette ligne s'exécute une seule fois, au lancement")
        self.play(FadeIn(p))
        self.wait(1.4)

        # 2. Update : les nombres changent, l'écran non.
        self.next_section("update : les nombres changent")
        aller(3)
        self.play(FadeOut(p), run_time=0.4)
        p = phrase("x change… mais l'écran ne bouge pas encore")
        self.play(x.animate.set_value(1), FadeIn(p), run_time=0.8)
        self.wait(1.2)

        # 3. Draw : cls efface, spr dessine.
        self.next_section("draw : cls efface, spr dessine")
        aller(4)
        self.play(FadeOut(p), run_time=0.4)
        voile = ecran.cadre.copy().set_fill(BLANC, opacity=0.35).set_stroke(width=0)
        p = phrase("cls efface tout l'écran…")
        self.play(FadeIn(voile, run_time=0.2), FadeIn(p))
        self.play(FadeOut(voile), run_time=0.3)
        self.wait(0.5)
        aller(5)
        self.play(FadeOut(p), run_time=0.4)
        joueur = always_redraw(lambda: ecran.sprite("joueur", int(x.get_value()), 60, 2))
        p = phrase("…puis spr dessine le joueur, à la position x")
        self.play(FadeIn(joueur, scale=0.6), FadeIn(p), run_time=0.6)
        self.wait(1.2)

        # 4. Et on recommence, de plus en plus vite.
        self.next_section("et on recommence : 60 fois par seconde")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("et on recommence : update, cls, spr… 60 fois par seconde")
        self.play(FadeIn(p), run_time=0.4)
        for duree, tours in ((0.28, 3), (0.14, 4), (0.06, 8)):
            for _ in range(tours):
                aller(3)
                self.play(x.animate.set_value(x.get_value() + 1), run_time=duree, rate_func=linear)
                aller(4)
                self.wait(duree)
                aller(5)
                self.wait(duree)
        self.remove(s)
        boucle = SurroundingRectangle(prog[3:6], color=CIEL, buff=0.08, stroke_width=3)
        self.add(boucle)
        self.play(x.animate.set_value(x.get_value() + 48), run_time=0.8, rate_func=linear)
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("le joueur avance d'un pixel par image : c'est ça, le mouvement")
        self.play(x.animate.set_value(x.get_value() + 48), FadeIn(p), run_time=0.8, rate_func=linear)
        self.wait(1.2)
