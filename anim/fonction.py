# Partie 1, boîte à outils « Une fonction » : un calcul qu'on nomme, puis
# qu'on réutilise. Une valeur entre, elle devient n, n * 2 ressort par return.
# Deux appels, le même calcul.
#
#   capture.py anim anim/fonction.py LaFonction -o img/outil-fonction.webp --fps 15
from manim import *
from commun import *


class LaFonction(Scene):
    def construct(self):
        prog = bloc_code(["function double(n)", "  return n * 2", "end"], 28).to_edge(LEFT, buff=0.7).shift(UP * 1.6)
        # La machine : une boîte nommée, une entrée à gauche, une sortie à droite.
        machine = RoundedRectangle(width=3.0, height=1.8, corner_radius=0.2, stroke_color=ALERTE, stroke_width=3,
                                   fill_color=PANNEAU, fill_opacity=1).move_to(RIGHT * 2.6 + UP * 1.2)
        nom = code("double", 28, ALERTE).next_to(machine, UP, buff=0.15)
        entree = texte("n entre", 18, DOUX).next_to(machine, LEFT, buff=0.15).shift(UP * 0.6)
        sortie = texte("return sort", 18, DOUX).next_to(machine, RIGHT, buff=0.15).shift(UP * 0.6)
        con = Console(self, RIGHT * 2.6 + DOWN * 1.6, largeur=5.0, hauteur=1.9, lignes=3)

        self.next_section("une fonction : un calcul qu'on nomme")
        p = phrase("function double(n) : un calcul avec un nom. n, c'est la valeur qu'on lui donnera")
        self.play(FadeIn(prog), FadeIn(p), run_time=0.6)
        self.play(FadeIn(machine), FadeIn(nom), FadeIn(entree), FadeIn(sortie), run_time=0.5)
        self.wait(1.0)

        def appel(val, lent):
            r = 0.5 if lent else 0.3
            ligne = code(f"print(double({val}))", 28).next_to(prog, DOWN, buff=0.6).align_to(prog, LEFT)
            self.play(FadeIn(ligne), run_time=r)
            # La valeur entre et devient n.
            v = code(str(val), 30, CIEL).move_to(ligne[12:12 + len(str(val))])
            n = Boite("n", val, couleur=CIEL, largeur=1.1, centre=machine.get_center() + LEFT * 0.7)
            self.play(v.animate.move_to(n.cadre.get_center()), run_time=r)
            self.remove(v)
            n.poser(self, run_time=r * 0.6)
            s = surligne(prog[1], ALERTE)
            self.play(Create(s), run_time=r * 0.5)
            calc = code(f"{val} * 2", 26, BLANC).move_to(machine.get_center() + RIGHT * 0.6)
            res = code(str(val * 2), 30, ALERTE).move_to(calc)
            self.play(FadeIn(calc), run_time=r)
            self.play(FadeTransform(calc, res), run_time=r)
            # return : le résultat sort vers print.
            self.play(res.animate.move_to(con.cadre.get_center()), run_time=r)
            self.remove(res)
            con.ecrire(str(val * 2), run_time=r * 0.6)
            self.play(FadeOut(s), FadeOut(ligne), *[FadeOut(m) for m in n.mobjects()], run_time=r * 0.6)

        self.next_section("double(4) : 4 entre, 8 sort")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("print(double(4)) : 4 entre et devient n, return renvoie n * 2 : 8")
        self.play(FadeIn(p), run_time=0.3)
        appel(4, True)
        self.wait(0.6)

        self.next_section("double(10) : le même calcul, réutilisé")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("double(10) : le même calcul, sans le réécrire. C'est ça, une fonction")
        self.play(FadeIn(p), run_time=0.3)
        appel(10, False)
        self.wait(0.6)

        self.next_section("dans le jeu : check_collision répond true ou false")
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("dans le jeu : deux boîtes entrent dans check_collision, et true ou false ressort")
        nom2 = code("check_collision", 26, ALERTE).move_to(nom)
        self.play(FadeIn(p), FadeTransform(nom, nom2), run_time=0.6)
        a = sprite("joueur", 0.06, 1, machine.get_center() + LEFT * 1.1 + UP * 0.3)
        b = sprite("ennemi", 0.06, 1, machine.get_center() + LEFT * 0.4 + UP * 0.3)
        self.play(FadeIn(a), FadeIn(b), run_time=0.4)
        out = code("true", 30, VERT).move_to(machine.get_center() + RIGHT * 0.6)
        self.play(FadeIn(out), run_time=0.4)
        self.play(out.animate.move_to(con.cadre.get_center()), run_time=0.5)
        self.remove(out)
        con.ecrire("true", couleur=VERT)
        self.wait(1.2)
