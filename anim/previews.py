# Aperçus fixes des propositions de la page de choix (26/11/2026) : une image
# par option, l'état clé de la scène proposée. Rendus en une image :
#
#   manim render -ql -s anim/previews.py <Scene>
#
# Rien de ceci n'est dans le sujet ; c'est pour choisir.
import random
from manim import *
from commun import *
from hasard import Roue, SECTEURS
from self_ import Carte

random.seed(2)


def ecran_jeu(centre=RIGHT * 3.4 + DOWN * 0.3, px=0.022):
    return Ecran(px=px, centre=centre)


def bonnet_avec_x(ecran, x, y=60):
    return VGroup(ecran.sprite("joueur", x, y, 2), origine(ecran.pos(x, y)),
                  etiquette(f"x = {x}", ALERTE, 20).next_to(ecran.pos(x + 8, y), UP, buff=0.15))


def barriere(pivot, ouverte):
    poteau = Dot(pivot, radius=0.12, color=DOUX)
    chemin = Line(pivot + LEFT * 1.4, pivot + RIGHT * 2.4, stroke_color=GRIS, stroke_width=2)
    if ouverte:
        b = Line(pivot, pivot + UP * 1.6, stroke_color=VERT, stroke_width=10)
    else:
        b = Line(pivot, pivot + RIGHT * 1.6, stroke_color=ROUGE, stroke_width=10)
    return VGroup(chemin, poteau, b)


def pile_pieces(centre, n):
    g = VGroup()
    for k in range(n):
        g.add(Ellipse(width=1.1, height=0.32, fill_color=ALERTE, fill_opacity=1, stroke_color=ORANGE, stroke_width=2).move_to(centre + UP * k * 0.18))
    return g


# ---------------------------------------------------------------- Incrémenter
class IncA(Scene):
    def construct(self):
        self.add(code("pieces = pieces + 1", 36).move_to(UP * 2.9))
        pile = pile_pieces(LEFT * 3.2 + DOWN * 1.2, 4)
        self.add(pile, Boite("pieces", 4, centre=LEFT * 3.2 + UP * 1.0).cadre)
        b = Boite("pieces", 4, centre=LEFT * 3.2 + UP * 1.0); self.add(*b.mobjects())
        self.add(Ellipse(width=1.1, height=0.32, fill_color=ALERTE, fill_opacity=1, stroke_color=ORANGE, stroke_width=2).move_to(LEFT * 3.2 + UP * 0.1),
                 Arrow(LEFT * 3.2 + UP * 0.0, LEFT * 3.2 + DOWN * 0.3, buff=0, color=ALERTE))
        e = ecran_jeu(); self.add(e.cadre, bonnet_avec_x(e, 21))
        self.add(phrase("A · pieces = pieces + 1 : une pièce de plus sur la pile. Puis le bonnet : x prend 1, un pixel de plus"))


class IncB(Scene):
    def construct(self):
        self.add(bloc_code(["function TIC()", "  t = t + 1", "end"], 28).to_edge(LEFT, buff=0.8).shift(UP * 2.0))
        t = ValueTracker(7)
        c = Compteur("t", t.get_value, chiffres=2).scale(0.9); c.shift(LEFT * 3.2 + DOWN * 1.4 - c.fenetre.get_center()); self.add(c)
        cadran = Circle(radius=1.0, stroke_color=DOUX, stroke_width=3).move_to(RIGHT * 0.4 + UP * 0.6)
        aig = Line(cadran.get_center(), cadran.get_center() + 0.8 * np.array([np.cos(PI / 2 - 7 * TAU / 12), np.sin(PI / 2 - 7 * TAU / 12), 0]), stroke_color=CIEL, stroke_width=6)
        self.add(cadran, aig, *[Dot(cadran.get_center() + 0.92 * np.array([np.cos(k * TAU / 12), np.sin(k * TAU / 12), 0]), radius=0.04, color=DOUX) for k in range(12)])
        e = ecran_jeu(RIGHT * 4.2 + DOWN * 1.6, 0.018); self.add(e.cadre, bonnet_avec_x(e, 27))
        self.add(phrase("B · t = t + 1 : un cran d'horloge à chaque tour de TIC. Puis le bonnet, sans la ligne"))


class IncC(Scene):
    def construct(self):
        b = Boite("x", 21, centre=LEFT * 3.6 + UP * 0.6); self.add(*b.mobjects())
        jeton = VGroup(Circle(radius=0.3, fill_color=ALERTE, fill_opacity=1, stroke_width=0), code("+1", 22, FOND)).move_to(LEFT * 3.6 + UP * 2.2)
        self.add(jeton, Arrow(LEFT * 3.6 + UP * 1.85, LEFT * 3.6 + UP * 1.15, buff=0, color=ALERTE))
        PX = 0.15; X0, X1, Y0, Y1 = 16, 56, 52, 76
        coin = RIGHT * 0.3 + UP * 1.6
        pos = lambda x, y: coin + RIGHT * (x - X0) * PX + DOWN * (y - Y0) * PX
        self.add(VGroup(*[Line(pos(x, Y0), pos(x, Y1), stroke_color=DOUX, stroke_width=1, stroke_opacity=0.18) for x in range(X0, X1 + 1)],
                        *[Line(pos(X0, y), pos(X1, y), stroke_color=DOUX, stroke_width=1, stroke_opacity=0.18) for y in range(Y0, Y1 + 1)]))
        self.add(Rectangle(width=(X1 - X0) * PX, height=(Y1 - Y0) * PX, stroke_color=DOUX, stroke_width=2).move_to(pos((X0 + X1) / 2, (Y0 + Y1) / 2)))
        self.add(*[code(str(x), 16, DOUX).next_to(pos(x, Y1), DOWN, buff=0.1) for x in range(20, 56, 5)])
        self.add(sprite("joueur", PX, 1, pos(21, 60)), origine(pos(21, 60), rayon=0.08), etiquette("x = 21", ALERTE, 24).next_to(pos(25, 60), UP, buff=0.25))
        self.add(phrase("C · la boîte x reçoit un jeton +1, le bonnet avance d'un pixel. Aucune ligne de code à l'écran"))


# ---------------------------------------------------------------- if
class IfA(Scene):
    def construct(self):
        self.add(manette("→", True).move_to(LEFT * 4.6 + DOWN * 0.3), barriere(LEFT * 2.6 + DOWN * 0.3, True))
        e = ecran_jeu(RIGHT * 3.4 + DOWN * 0.3, 0.02); self.add(e.cadre, e.sprite("joueur", 110, 60, 2))
        self.add(Arrow(e.pos(130, 68), e.pos(170, 68), buff=0, color=CIEL, stroke_width=4))
        self.add(texte("touche appuyée = barrière ouverte = le bonnet avance", 22, DOUX).move_to(UP * 2.6))
        self.add(phrase("A · la barrière et la touche dès le début : aucun code, l'exemple température reste dans le texte"))


class IfB(Scene):
    def construct(self):
        # Un videur : un rectangle avec une tête, la carte « 12 ans » montrée, la barrière ouverte.
        corps = RoundedRectangle(width=1.0, height=1.6, corner_radius=0.2, fill_color=GRIS, fill_opacity=1, stroke_width=0).move_to(LEFT * 3.4 + DOWN * 0.5)
        tete = Circle(radius=0.35, fill_color=DOUX, fill_opacity=1, stroke_width=0).next_to(corps, UP, buff=0.05)
        carte = VGroup(RoundedRectangle(width=1.4, height=0.9, corner_radius=0.1, fill_color=BLANC, fill_opacity=1, stroke_width=0), code("15 ans", 22, FOND)).move_to(LEFT * 1.2 + DOWN * 0.2)
        ok = code(">= 12 : vrai", 24, VERT).next_to(carte, UP, buff=0.3)
        self.add(corps, tete, carte, ok, barriere(RIGHT * 1.0 + DOWN * 0.5, True))
        self.add(texte("le videur : la condition se voit sur la carte", 22, DOUX).move_to(UP * 2.6))
        self.add(phrase("B · le videur du cinéma, comme l'exemple and de l'étape suivante : la barrière s'ouvre ou pas, puis la touche"))


class IfC(Scene):
    def construct(self):
        tube = RoundedRectangle(width=0.5, height=3.0, corner_radius=0.25, stroke_color=DOUX, stroke_width=3).move_to(LEFT * 4.8 + UP * 0.6)
        merc = Rectangle(width=0.26, height=1.9, fill_color=ROUGE, fill_opacity=1, stroke_width=0).move_to(tube.get_bottom() + UP * (0.3 + 0.95))
        seuil = Line(tube.get_left() + LEFT * 0.2, tube.get_right() + RIGHT * 0.2, stroke_color=ALERTE, stroke_width=4).set_y(tube.get_bottom()[1] + 1.4)
        self.add(tube, merc, seuil, code("35", 22).next_to(tube, UP, buff=0.1), code("30", 18, ALERTE).next_to(seuil, LEFT, buff=0.1))
        self.add(barriere(LEFT * 2.8 + UP * 0.6, True))
        self.add(manette("→", True).move_to(LEFT * 4.6 + DOWN * 2.3), barriere(LEFT * 2.8 + DOWN * 2.3, True))
        e = ecran_jeu(RIGHT * 3.4 + DOWN * 0.8, 0.02); self.add(e.cadre, e.sprite("joueur", 120, 60, 2))
        self.add(texte("vrai / faux au thermomètre, puis la touche : sans bloc if btn(3)", 22, DOUX).move_to(UP * 2.9))
        self.add(phrase("C · garder le thermomètre, couper le code de la partie jeu"))


# ---------------------------------------------------------------- math.random
class RndA(Scene):
    def construct(self):
        self.add(code("math.random(0, 136)", 32).move_to(UP * 3.0))
        grad = [str(k * 136 // 16) if k % 2 == 0 else "" for k in range(16)]
        r = Roue(LEFT * 3.2 + DOWN * 0.3, 2.2, grad, [BLEU if k % 2 == 0 else "#29366f" for k in range(16)], taille_texte=18); self.add(r.tout())
        e = ecran_jeu(RIGHT * 3.2 + DOWN * 0.3, 0.02); self.add(e.cadre, e.sprite("ennemi", 224, 101, 1), origine(e.pos(224, 101)))
        carte = VGroup(RoundedRectangle(width=1.6, height=0.8, corner_radius=0.15, fill_color=BLANC, fill_opacity=1, stroke_width=0), code("101", 28, FOND)).move_to(RIGHT * 0.1 + UP * 1.6)
        self.add(carte, Arrow(carte.get_right(), e.pos(220, 101), buff=0.1, color=ALERTE, stroke_width=3))
        self.add(phrase("A · la même roue, sans « ey = » : la carte 101 devient la hauteur de l'ennemi"))


class RndB(Scene):
    def construct(self):
        self.add(code("math.random(0, 7)", 32).move_to(UP * 3.0))
        r = Roue(LEFT * 3.2 + DOWN * 0.3, 2.2, list(range(8)), [SECTEURS[k % 6] for k in range(8)], taille_texte=24); self.add(r.tout())
        e = ecran_jeu(RIGHT * 3.2 + DOWN * 0.3, 0.02); self.add(e.cadre)
        for k in range(8):
            self.add(Line(e.pos(0, k * 17), e.pos(240, k * 17), stroke_color=DOUX, stroke_width=1, stroke_opacity=0.4), code(str(k), 14, DOUX).move_to(e.pos(6, k * 17 + 8)))
        self.add(e.sprite("ennemi", 224, 5 * 17 + 4, 1))
        self.add(phrase("B · huit couloirs : la roue choisit le couloir 5, l'ennemi y apparaît. Les bornes 0 à 136 restent à trouver"))


class RndC(Scene):
    def construct(self):
        self.add(code("math.random(1, 6)", 32).move_to(UP * 3.0))
        r = Roue(LEFT * 3.2 + DOWN * 0.3, 2.2, [1, 2, 3, 4, 5, 6], SECTEURS); self.add(r.tout())
        e = ecran_jeu(RIGHT * 3.2 + DOWN * 0.3, 0.02); self.add(e.cadre)
        for h, op in ((12, 0.35), (101, 0.6), (55, 1.0)):
            self.add(e.sprite("ennemi", 224, h, 1).set_opacity(op))
        self.add(texte("un nombre au hasard peut être une hauteur", 22, DOUX).move_to(RIGHT * 3.2 + UP * 2.0))
        self.add(phrase("C · rester sur le dé : l'ennemi apparaît à des hauteurs différentes, sans nombre ni code affiché"))


# ---------------------------------------------------------------- self
def boite_fonction(nom, centre):
    fn = RoundedRectangle(width=4.2, height=2.3, corner_radius=0.2, stroke_color=ALERTE, stroke_width=3, fill_color=PANNEAU, fill_opacity=0.5).move_to(centre)
    return VGroup(fn, code(nom, 24, ALERTE).next_to(fn, UP, buff=0.12))


class SelfA(Scene):
    def construct(self):
        self.add(bloc_code(["function player:update()", "  -- bouger", "end", "", "player:update()"], 22).to_edge(LEFT, buff=0.6).shift(UP * 1.2))
        fn = boite_fonction("update", RIGHT * 3.4 + DOWN * 1.0); self.add(fn)
        pl = RoundedRectangle(width=2.6, height=1.5, corner_radius=0.15, stroke_color=VERT, stroke_width=3, fill_color=PANNEAU, fill_opacity=1).move_to(fn[0].get_center() + DOWN * 0.1)
        self.add(pl, code("self", 22, CIEL).next_to(pl, UP, buff=0.1), code("x = 21", 20).move_to(pl.get_center() + UP * 0.4 + LEFT * 0.5), sprite("joueur", 0.06, 1, pl.get_center() + RIGHT * 0.4 + DOWN * 0.1))
        self.add(phrase("A · la carte player entre dans update, le bonnet bouge, le corps affiché est « -- bouger »"))


class SelfB(Scene):
    def construct(self):
        self.add(bloc_code(["function enemy:update()", "  -- avancer vers la gauche", "end", "", "enemy:update()"], 22).to_edge(LEFT, buff=0.6).shift(UP * 1.2))
        fn = boite_fonction("update", RIGHT * 3.4 + DOWN * 1.0); self.add(fn)
        pl = RoundedRectangle(width=2.6, height=1.5, corner_radius=0.15, stroke_color=VERT, stroke_width=3, fill_color=PANNEAU, fill_opacity=1).move_to(fn[0].get_center() + DOWN * 0.1)
        self.add(pl, code("self", 22, CIEL).next_to(pl, UP, buff=0.1), code("x = 200", 20).move_to(pl.get_center() + UP * 0.4 + LEFT * 0.4), sprite("ennemi", 0.06, 1, pl.get_center() + RIGHT * 0.4 + DOWN * 0.1))
        self.add(phrase("B · un autre objet que celui de l'étape : enemy:update(), « -- avancer vers la gauche »"))


class SelfC(Scene):
    def construct(self):
        self.add(bloc_code(['chat = {nom = "Félix", faim = 3}', "", "function chat:manger()", "  self.faim = self.faim - 1", "end", "", "chat:manger()"], 22).to_edge(LEFT, buff=0.6).shift(UP * 1.2))
        c = Carte("chat", 'nom = "Félix"', "faim", 2, centre=RIGHT * 3.4 + UP * 1.6); self.add(c.tout)
        self.add(boite_fonction("manger", RIGHT * 3.4 + DOWN * 1.6))
        self.add(phrase("C · s'arrêter au chat ; la phrase finale fait le lien : dans le jeu, player:update() reçoit la table player"))


# ---------------------------------------------------------------- la boucle de jeu
class BoucleA(Scene):
    def construct(self):
        prog = bloc_code(["x = 0", "", "function TIC()", "  x = x + 1", "  cls(0)", "  spr(0, x, 60)", "end"], 28).to_edge(LEFT, buff=0.7).shift(UP * 0.5)
        self.add(prog, surligne(prog[3]))
        e = Ecran(px=0.028, centre=RIGHT * 3.4 + UP * 1.4); self.add(e.cadre, e.sprite("joueur", 40, 60, 2))
        self.add(phrase("A · laisser : l'intro de modelage, avant toute étape"))


class BoucleB(Scene):
    def construct(self):
        prog = bloc_code(["t = 0", "", "function TIC()", "  t = t + 1", "  cls(0)", "  spr(0, 100, 60)", "end"], 28).to_edge(LEFT, buff=0.7).shift(UP * 0.5)
        self.add(prog, surligne(prog[3]))
        e = Ecran(px=0.028, centre=RIGHT * 3.4 + UP * 1.4); self.add(e.cadre, e.sprite("joueur", 100, 60, 2))
        t = ValueTracker(42); c = Compteur("t", t.get_value, chiffres=3).scale(0.75); c.shift(e.cadre.get_bottom() + DOWN * 1.6 - c.fenetre.get_center()); self.add(c)
        self.add(phrase("B · un compteur d'images et un sprite fixe : la boucle sans mouvement"))


class BoucleC(Scene):
    def construct(self):
        prog = bloc_code(["x = 0", "", "function TIC()", "  -- mettre à jour", "  cls(0)", "  spr(0, x, 60)", "end"], 28).to_edge(LEFT, buff=0.7).shift(UP * 0.5)
        self.add(prog, surligne(prog[3]))
        e = Ecran(px=0.028, centre=RIGHT * 3.4 + UP * 1.4); self.add(e.cadre, e.sprite("joueur", 40, 60, 2), Arrow(e.pos(60, 68), e.pos(100, 68), buff=0, color=CIEL, stroke_width=4))
        self.add(phrase("C · masquer la mise à jour : le mouvement est montré, la ligne qui le fait ne l'est pas"))
