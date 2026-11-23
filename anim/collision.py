# Partie 1, « Collision » : deux boîtes se touchent quand leurs segments se
# chevauchent sur l'axe X et aussi sur l'axe Y. Les nombres sont ceux de la
# boîte à outils (10 à 18, 15 à 23, 20 à 28). Les comparaisons restent à
# trouver : on montre les segments, pas la condition.
#
#   capture.py anim anim/collision.py LaCollision -o img/collision-deux-axes.webp
from manim import *
from commun import *

PX = 0.14                      # un pixel du jeu, en unités manim : on zoome
AX, AY = 10, 6                 # le joueur ne bouge pas
COIN = LEFT * 2.2 + UP * 2.7   # le pixel (0, 0) de la zone zoomée


def pos(x, y):
    return COIN + RIGHT * x * PX + DOWN * y * PX


class LaCollision(Scene):
    def construct(self):
        bx, by = ValueTracker(15), ValueTracker(6)
        a = sprite("joueur", PX, 1, pos(AX, AY))
        a_boite = Rectangle(width=8 * PX, height=8 * PX, stroke_color=BLANC, stroke_width=3).move_to(pos(AX + 4, AY + 4))
        b = always_redraw(lambda: sprite("ennemi", PX, 1, pos(bx.get_value(), by.get_value())))
        b_boite = always_redraw(lambda: Rectangle(width=8 * PX, height=8 * PX, stroke_color=VERT, stroke_width=3)
                                .move_to(pos(bx.get_value() + 4, by.get_value() + 4)))
        self.add(a, a_boite, b, b_boite)

        # Les deux axes : X sous la zone, Y à sa gauche.
        y_axe, x_axe = 26, -4
        axe_x = Line(pos(0, y_axe), pos(36, y_axe), stroke_color=DOUX, stroke_width=2)
        axe_y = Line(pos(x_axe, 0), pos(x_axe, 26), stroke_color=DOUX, stroke_width=2)
        nom_x = texte("axe X", 20, DOUX).next_to(axe_x.get_end(), UR, buff=0.1)
        nom_y = texte("axe Y", 20, DOUX).next_to(axe_y.get_start(), UL, buff=0.1)

        def seg_x(x0, couleur, decal):
            return Line(pos(x0, y_axe + decal), pos(x0 + 8, y_axe + decal), stroke_color=couleur, stroke_width=10)

        def seg_y(y0, couleur, decal):
            return Line(pos(x_axe - decal, y0), pos(x_axe - decal, y0 + 8), stroke_color=couleur, stroke_width=10)

        def nombres_x(x0, couleur, decal):
            sens = UP if decal < 0 else DOWN
            return VGroup(texte(str(int(x0)), 18, couleur).next_to(pos(x0, y_axe + decal), sens, buff=0.12),
                          texte(str(int(x0) + 8), 18, couleur).next_to(pos(x0 + 8, y_axe + decal), sens, buff=0.12))

        def nombres_y(y0, couleur, decal):
            sens = RIGHT if decal < 0 else LEFT
            return VGroup(texte(str(int(y0)), 18, couleur).next_to(pos(x_axe - decal, y0), sens, buff=0.12),
                          texte(str(int(y0) + 8), 18, couleur).next_to(pos(x_axe - decal, y0 + 8), sens, buff=0.12))

        def chevauche(a0, b0):
            return max(a0, b0) < min(a0 + 8, b0 + 8)

        def zone_x():
            x0, x1 = max(AX, bx.get_value()), min(AX + 8, bx.get_value() + 8)
            if x0 >= x1:
                return VGroup()
            r = Rectangle(width=(x1 - x0) * PX, height=26 * PX, fill_color=ALERTE, fill_opacity=0.25, stroke_width=0)
            return r.move_to(pos((x0 + x1) / 2, 13))

        def zone_y():
            y0, y1 = max(AY, by.get_value()), min(AY + 8, by.get_value() + 8)
            if y0 >= y1:
                return VGroup()
            r = Rectangle(width=36 * PX, height=(y1 - y0) * PX, fill_color=ALERTE, fill_opacity=0.25, stroke_width=0)
            return r.move_to(pos(18, (y0 + y1) / 2))

        def verdict(ok, ou):
            t = texte("oui" if ok else "non", 26, VERT if ok else ROUGE)
            return t.move_to(ou)

        ou_x = pos(50, y_axe)
        ou_y = pos(x_axe - 9, 13)

        # 1. Deux boîtes.
        self.next_section("deux boîtes : de x à x + 8, de y à y + 8")
        p = phrase("chaque sprite a sa boîte : de x à x + 8, de y à y + 8")
        self.play(FadeIn(p), run_time=0.5)
        self.wait(1.4)

        # 2. Sur l'axe X.
        self.next_section("sur l'axe X : les deux segments se chevauchent ?")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("sur l'axe X : le segment du joueur, celui de l'ennemi. Ils se chevauchent ?")
        sa = seg_x(AX, BLANC, -1.6)
        na = nombres_x(AX, BLANC, -1.6)
        sb = always_redraw(lambda: seg_x(bx.get_value(), VERT, 1.6))
        nb = always_redraw(lambda: nombres_x(bx.get_value(), VERT, 1.6))
        zx = always_redraw(zone_x)
        vx = always_redraw(lambda: verdict(chevauche(AX, bx.get_value()), ou_x))
        self.play(FadeIn(axe_x), FadeIn(nom_x), FadeIn(sa), FadeIn(na), FadeIn(p), run_time=0.5)
        self.play(FadeIn(sb), FadeIn(nb), run_time=0.5)
        self.add(zx)
        self.bring_to_back(zx)
        self.play(FadeIn(vx), run_time=0.5)
        self.wait(1.2)
        self.play(FadeOut(p), run_time=0.2)
        p = phrase("de 15 à 23 : oui, entre 15 et 18. De 20 à 28 : non, il y a un trou")
        self.play(FadeIn(p), bx.animate.set_value(20), run_time=1.2)
        self.wait(1.4)

        # 3. Sur l'axe Y.
        self.next_section("sur l'axe Y : la même question")
        self.play(FadeOut(p), bx.animate.set_value(15), run_time=0.6)
        p = phrase("sur l'axe Y, la même question, avec y et y + 8")
        sa2 = seg_y(AY, BLANC, -1.6)
        na2 = nombres_y(AY, BLANC, -1.6)
        sb2 = always_redraw(lambda: seg_y(by.get_value(), VERT, 1.6))
        nb2 = always_redraw(lambda: nombres_y(by.get_value(), VERT, 1.6))
        zy = always_redraw(zone_y)
        vy = always_redraw(lambda: verdict(chevauche(AY, by.get_value()), ou_y))
        self.play(FadeIn(axe_y), FadeIn(nom_y), FadeIn(sa2), FadeIn(na2), FadeIn(p), run_time=0.5)
        self.add(zy)
        self.bring_to_back(zy)
        self.play(FadeIn(sb2), FadeIn(nb2), FadeIn(vy), run_time=0.5)
        self.wait(0.8)
        self.play(by.animate.set_value(16), run_time=1.0)
        self.wait(1.0)

        # 4. Les deux à la fois.
        self.next_section("collision : oui sur X et oui sur Y")
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("oui sur X mais non sur Y : pas de collision")
        self.play(FadeIn(p), run_time=0.4)
        self.wait(1.2)
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("non sur X mais oui sur Y : pas de collision non plus")
        self.play(bx.animate.set_value(22), by.animate.set_value(10), FadeIn(p), run_time=1.0)
        self.wait(1.2)
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("oui sur X et oui sur Y : collision !", ORANGE)
        self.play(bx.animate.set_value(15), run_time=0.8)
        flash = Rectangle(width=8 * PX, height=8 * PX, stroke_color=ORANGE, stroke_width=6).move_to(pos(AX + 4, AY + 4))
        self.play(FadeIn(p), Create(flash), run_time=0.4)
        self.play(flash.animate.scale(1.6).set_stroke(opacity=0), run_time=0.6)
        self.wait(0.4)
        self.play(FadeOut(p), run_time=0.3)
        p = phrase("une collision, c'est oui sur les deux axes en même temps")
        self.play(FadeIn(p), run_time=0.4)
        self.wait(1.6)
