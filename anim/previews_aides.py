# Aperçus fixes des aides visuelles proposées (26/11/2026), une image par aide,
# toutes sur le même bonnet pour comparer. Pour la page de choix, pas pour le sujet.
#
#   manim render -ql -s anim/previews_aides.py <Scene>
from manim import *
from commun import *

X, Y = 96, 60


def base(scene, px=0.03, centre=UP * 0.4):
    e = Ecran(px=px, centre=centre)
    scene.add(e.cadre, e.sprite("joueur", X, Y, 2), origine(e.pos(X, Y)))
    return e


class AideFleche(Scene):
    def construct(self):
        e = base(self)
        self.add(Arrow(e.pos(X + 8, Y + 8), e.pos(X + 8 + 36, Y + 8), buff=0, color=CIEL, stroke_width=5, max_tip_length_to_length_ratio=0.25),
                 etiquette("vx = 3", CIEL, 22).next_to(e.pos(X + 30, Y), UP, buff=0.3))
        self.add(phrase("la flèche de vitesse : part de l'origine, sa longueur dit la vitesse, son sens le signe"))


class AideRegle(Scene):
    def construct(self):
        e = base(self)
        for v in range(0, 241, 40):
            self.add(Line(e.pos(v, 136), e.pos(v, 136) + DOWN * 0.15, stroke_color=DOUX, stroke_width=2), code(str(v), 14, DOUX).next_to(e.pos(v, 136) + DOWN * 0.15, DOWN, buff=0.05))
        for v in range(0, 137, 34):
            self.add(Line(e.pos(0, v), e.pos(0, v) + LEFT * 0.15, stroke_color=DOUX, stroke_width=2), code(str(v), 14, DOUX).next_to(e.pos(0, v) + LEFT * 0.15, LEFT, buff=0.05))
        self.add(Line(e.pos(X, 136), e.pos(X, 136) + DOWN * 0.15, stroke_color=ALERTE, stroke_width=4), code(str(X), 16, ALERTE).next_to(e.pos(X, 136) + DOWN * 0.3, DOWN, buff=0.05),
                 Line(e.pos(0, Y), e.pos(0, Y) + LEFT * 0.15, stroke_color=ALERTE, stroke_width=4), code(str(Y), 16, ALERTE).next_to(e.pos(0, Y) + LEFT * 0.3, LEFT, buff=0.05))
        self.add(phrase("les règles graduées : x en bas, y à gauche, la valeur courante allumée"))


class AideGuides(Scene):
    def construct(self):
        e = base(self)
        self.add(DashedLine(e.pos(X, Y), e.pos(X, 136), stroke_color=ALERTE, stroke_width=2), DashedLine(e.pos(X, Y), e.pos(0, Y), stroke_color=ALERTE, stroke_width=2),
                 code("x = 96", 18, ALERTE).next_to(e.pos(X, 136), DOWN, buff=0.1), code("y = 60", 18, ALERTE).next_to(e.pos(0, Y), LEFT, buff=0.1))
        self.add(phrase("les guides pointillés : de l'origine jusqu'à chaque bord, pour dire quel nombre est x et lequel est y"))


class AideBoite(Scene):
    def construct(self):
        e = base(self)
        self.add(e.boite(X, Y, 16, 16, couleur=ALERTE, largeur=2), e.sprite("ennemi", X + 40, Y + 4, 2), e.boite(X + 40, Y + 4, 16, 16, couleur=VERT, largeur=2))
        self.add(phrase("la boîte de collision toujours visible dès qu'une collision compte"))


class AideFantome(Scene):
    def construct(self):
        e = Ecran(px=0.03, centre=UP * 0.4); self.add(e.cadre)
        for k, op in ((0, 0.18), (1, 0.32), (2, 0.5), (3, 0.72)):
            self.add(e.sprite("joueur", X - 48 + k * 12, Y, 2).set_opacity(op))
        self.add(e.sprite("joueur", X, Y, 2), origine(e.pos(X, Y)))
        self.add(phrase("les fantômes : les positions des images précédentes restent en transparence, on voit le pas"))


class AideImage(Scene):
    def construct(self):
        e = base(self)
        t = ValueTracker(37); c = Compteur("image", t.get_value, chiffres=2, couleur=CIEL).scale(0.6); c.shift(e.cadre.get_corner(DR) + RIGHT * 1.0 + UP * 0.6 - c.fenetre.get_center()); self.add(c)
        self.add(phrase("le compteur d'images : chaque fois qu'on dit « à chaque image », il tourne"))


class AideLoupe(Scene):
    def construct(self):
        e = Ecran(px=0.022, centre=LEFT * 3.0 + UP * 0.4); self.add(e.cadre, e.sprite("joueur", X, Y, 1), origine(e.pos(X, Y), rayon=0.04))
        cadre = Rectangle(width=14 * e.px, height=12 * e.px, stroke_color=ALERTE, stroke_width=2).move_to(e.pos(X + 4, Y + 4))
        PX = 0.22; coin = RIGHT * 1.6 + UP * 1.7
        pos = lambda x, y: coin + RIGHT * (x - (X - 3)) * PX + DOWN * (y - (Y - 2)) * PX
        self.add(cadre, Line(cadre.get_corner(UR), pos(X - 3, Y - 2), stroke_color=ALERTE, stroke_width=1.5), Line(cadre.get_corner(DR), pos(X - 3, Y + 10), stroke_color=ALERTE, stroke_width=1.5))
        self.add(VGroup(*[Line(pos(x, Y - 2), pos(x, Y + 10), stroke_color=DOUX, stroke_width=1, stroke_opacity=0.3) for x in range(X - 3, X + 12)],
                        *[Line(pos(X - 3, y), pos(X + 11, y), stroke_color=DOUX, stroke_width=1, stroke_opacity=0.3) for y in range(Y - 2, Y + 11)]))
        self.add(Rectangle(width=14 * PX, height=12 * PX, stroke_color=ALERTE, stroke_width=2).move_to(pos(X + 4, Y + 4)), sprite("joueur", PX, 1, pos(X, Y)), origine(pos(X, Y), rayon=0.1))
        self.add(phrase("la loupe : un encart agrandi où chaque pixel est une case, quand la valeur bouge de 1"))


class AideEtat(Scene):
    def construct(self):
        e = base(self)
        m = e.sprite("missile", X + 20, Y, 2); self.add(m)
        badge = VGroup(RoundedRectangle(width=1.5, height=0.42, corner_radius=0.2, fill_color=CIEL, fill_opacity=1, stroke_width=0), texte("en vol", 18, FOND)).next_to(e.pos(X + 28, Y), UP, buff=0.35)
        badge2 = VGroup(RoundedRectangle(width=1.5, height=0.42, corner_radius=0.2, fill_color=GRIS, fill_opacity=1, stroke_width=0), texte("au repos", 18, BLANC)).next_to(e.cadre, RIGHT, buff=0.5).shift(UP * 1.0)
        self.add(badge, badge2)
        self.add(phrase("l'étiquette d'état : « au repos », « en vol », sur l'objet, quand sa vitesse dit dans quel état il est"))


class AideLien(Scene):
    def construct(self):
        e = base(self, centre=LEFT * 1.4 + UP * 0.4)
        tags = VGroup(etiquette("x = 96", BLANC, 26), etiquette("y = 60", BLANC, 26)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to(RIGHT * 4.6 + UP * 1.2)
        self.add(tags, Line(e.pos(X, Y), tags.get_left() + LEFT * 0.15, stroke_color=ALERTE, stroke_width=1.5, stroke_opacity=0.7))
        self.add(phrase("le fil : un trait fin entre l'origine du sprite et ses nombres rangés sur le côté"))


class AideCouleur(Scene):
    def construct(self):
        self.add(code("cls(0)", 32).move_to(UP * 2.6 + LEFT * 3.0), code("spr(0, x, y, 0)", 32).move_to(UP * 2.6 + RIGHT * 2.6))
        g = VGroup()
        for k in range(16):
            c = Square(side_length=0.6, fill_color=PALETTE[k], fill_opacity=1, stroke_color=BLANC if k == 0 else FOND, stroke_width=3 if k == 0 else 1)
            c.move_to(LEFT * 4.5 + RIGHT * (k % 8) * 0.68 + DOWN * (k // 8) * 0.68 + UP * 0.6)
            g.add(c, code(str(k), 14, BLANC if k in (0, 1, 2, 8, 14, 15) else FOND).move_to(c))
        self.add(g, texte("0", 20, ALERTE).next_to(g[0], UP, buff=0.15))
        self.add(phrase("la pastille de couleur : quand un numéro de couleur est nommé, la palette s'affiche avec ce numéro encadré"))
