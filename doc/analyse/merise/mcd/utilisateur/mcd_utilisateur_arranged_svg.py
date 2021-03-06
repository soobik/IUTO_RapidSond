#!/usr/bin/env python
# encoding: utf-8
# Généré par Mocodo 2.3.7 le Mon, 03 Apr 2017 20:29:11

from __future__ import division
from math import hypot

import time, codecs

(width,height) = (480,554)
cx = {
    u"TYPE_UTILISATEUR"      :  215,
    u"AVOIR_TYPE_UTILISATEUR":  215,
    u"UTILISATEUR"           :  215,
    u"CREER"                 :   38,
    u"QUESTIONNAIRE"         :  215,
    u"ANALYSER"              :  417,
    u"DATE"                  :  215,
}
cy = {
    u"TYPE_UTILISATEUR"      :   44,
    u"AVOIR_TYPE_UTILISATEUR":  129,
    u"UTILISATEUR"           :  241,
    u"CREER"                 :  398,
    u"QUESTIONNAIRE"         :  398,
    u"ANALYSER"              :  398,
    u"DATE"                  :  519,
}
shift = {
    u"AVOIR_TYPE_UTILISATEUR,UTILISATEUR"     :    0,
    u"AVOIR_TYPE_UTILISATEUR,TYPE_UTILISATEUR":    0,
    u"CREER,UTILISATEUR"                      :    0,
    u"CREER,QUESTIONNAIRE"                    :    0,
    u"CREER,DATE"                             :    0,
    u"ANALYSER,UTILISATEUR"                   :    0,
    u"ANALYSER,QUESTIONNAIRE"                 :    0,
    u"ANALYSER,DATE"                          :    0,
}
ratio = {
    u"AVOIR_TYPE_UTILISATEUR,TYPE_UTILISATEUR":  1.00,
    u"CREER,UTILISATEUR"                      :  1.00,
    u"ANALYSER,UTILISATEUR"                   :  1.00,
}
colors = {
    u"annotation_color"                : '#060707',
    u"annotation_text_color"           : '#E2EED0',
    u"association_attribute_text_color": '#607734',
    u"association_cartouche_color"     : '#b2bba4',
    u"association_cartouche_text_color": '#27360c',
    u"association_color"               : '#ccd6ba',
    u"association_stroke_color"        : '#85956b',
    u"background_color"                : 'none',
    u"card_text_color"                 : '#726f83',
    u"entity_attribute_text_color"     : '#3e3c42',
    u"entity_cartouche_color"          : '#97b8ff',
    u"entity_cartouche_text_color"     : '#131114',
    u"entity_color"                    : '#c0d4ff',
    u"entity_stroke_color"             : '#578dff',
    u"label_text_color"                : '#726f83',
    u"leg_stroke_color"                : '#726f83',
    u"transparent_color"               : 'none',
}
card_max_width = 23
card_max_height = 14
card_margin = 5
arrow_width = 12
arrow_half_height = 6
arrow_axis = 8
card_baseline = 3

def cmp(x, y):
    return (x > y) - (x < y)

def offset(x, y):
    return (x + card_margin, y - card_baseline - card_margin)

def line_intersection(ex, ey, w, h, ax, ay):
    if ax == ex:
        return (ax, ey + cmp(ay, ey) * h)
    if ay == ey:
        return (ex + cmp(ax, ex) * w, ay)
    x = ex + cmp(ax, ex) * w
    y = ey + (ay-ey) * (x-ex) / (ax-ex)
    if abs(y-ey) > h:
        y = ey + cmp(ay, ey) * h
        x = ex + (ax-ex) * (y-ey) / (ay-ey)
    return (x, y)

def straight_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch):
    
    def card_pos(twist, shift):
        compare = (lambda x1_y1: x1_y1[0] < x1_y1[1]) if twist else (lambda x1_y1: x1_y1[0] <= x1_y1[1])
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal) - shift
        (xg, yg) = line_intersection(ex, ey, ew, eh + ch, ax, ay)
        (xb, yb) = line_intersection(ex, ey, ew + cw, eh, ax, ay)
        if compare((xg, xb)):
            if compare((xg, ex)):
                if compare((yb, ey)):
                    return (xb - correction, yb)
                return (xb - correction, yb + ch)
            if compare((yb, ey)):
                return (xg, yg + ch - correction)
            return (xg, yg + correction)
        if compare((xb, ex)):
            if compare((yb, ey)):
                return (xg - cw, yg + ch - correction)
            return (xg - cw, yg + correction)
        if compare((yb, ey)):
            return (xb - cw + correction, yb)
        return (xb - cw + correction, yb + ch)
    
    def arrow_pos(direction, ratio):
        (x0, y0) = line_intersection(ex, ey, ew, eh, ax, ay)
        (x1, y1) = line_intersection(ax, ay, aw, ah, ex, ey)
        if direction == "<":
            (x0, y0, x1, y1) = (x1, y1, x0, y0)
        (x, y) = (ratio * x0 + (1 - ratio) * x1, ratio * y0 + (1 - ratio) * y1)
        return (x, y, x1 - x0, y0 - y1)
    
    straight_leg_factory.card_pos = card_pos
    straight_leg_factory.arrow_pos = arrow_pos
    return straight_leg_factory


def curved_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch, spin):
    
    def bisection(predicate):
        (a, b) = (0, 1)
        while abs(b - a) > 0.0001:
            m = (a + b) / 2
            if predicate(bezier(m)):
                a = m
            else:
                b = m
        return m
    
    def intersection(left, top, right, bottom):
       (x, y) = bezier(bisection(lambda p: left <= p[0] <= right and top <= p[1] <= bottom))
       return (int(round(x)), int(round(y)))
    
    def card_pos(shift):
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal)
        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        if spin > 0:
            if (yr == BOT and xr <= rig) or (xr == LEF and yr >= bot):
                return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - correction + shift, bot + ch)
            if (xr == RIG and yr >= top) or yr == BOT:
                return (rig, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) + correction + shift)
            if (yr == TOP and xr >= lef) or xr == RIG:
                return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) + correction + shift - cw, TOP + ch)
            return (LEF, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - correction + shift + ch)
        if (yr == BOT and xr >= lef) or (xr == RIG and yr >= bot):
            return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) + correction + shift - cw, bot + ch)
        if xr == RIG or (yr == TOP and xr >= rig):
            return (rig, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - correction + shift + ch)
        if yr == TOP or (xr == LEF and yr <= top):
            return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - correction + shift, TOP + ch)
        return (LEF, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) + correction + shift)
    
    def arrow_pos(direction, ratio):
        t0 = bisection(lambda p: abs(p[0] - ax) > aw or abs(p[1] - ay) > ah)
        t3 = bisection(lambda p: abs(p[0] - ex) < ew and abs(p[1] - ey) < eh)
        if direction == "<":
            (t0, t3) = (t3, t0)
        tc = t0 + (t3 - t0) * ratio
        (xc, yc) = bezier(tc)
        (x, y) = derivate(tc)
        if direction == "<":
            (x, y) = (-x, -y)
        return (xc, yc, x, -y)
    
    diagonal = hypot(ax - ex, ay - ey)
    (x, y) = line_intersection(ex, ey, ew + cw / 2, eh + ch / 2, ax, ay)
    k = (cw *  abs((ay - ey) / diagonal) + ch * abs((ax - ex) / diagonal))
    (x, y) = (x - spin * k * (ay - ey) / diagonal, y + spin * k * (ax - ex) / diagonal)
    (hx, hy) = (2 * x - (ex + ax) / 2, 2 * y - (ey + ay) / 2)
    (x1, y1) = (ex + (hx - ex) * 2 / 3, ey + (hy - ey) * 2 / 3)
    (x2, y2) = (ax + (hx - ax) * 2 / 3, ay + (hy - ay) * 2 / 3)
    (kax, kay) = (ex - 2 * hx + ax, ey - 2 * hy + ay)
    (kbx, kby) = (2 * hx - 2 * ex, 2 * hy - 2 * ey)
    bezier = lambda t: (kax*t*t + kbx*t + ex, kay*t*t + kby*t + ey)
    derivate = lambda t: (2*kax*t + kbx, 2*kay*t + kby)
    
    curved_leg_factory.points = (ex, ey, x1, y1, x2, y2, ax, ay)
    curved_leg_factory.card_pos = card_pos
    curved_leg_factory.arrow_pos = arrow_pos
    return curved_leg_factory


def upper_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w - r, y, "a", r, r, 90, 0, 1, r, r, "V", y + h, "h", -w, "V", y + r, "a", r, r, 90, 0, 1, r, -r]])

def lower_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w, y, "v", h - r, "a", r, r, 90, 0, 1, -r, r, "H", x + r, "a", r, r, 90, 0, 1, -r, -r, "V", y, "H", w]])

def arrow(x, y, a, b):
    c = hypot(a, b)
    (cos, sin) = (a / c, b / c)
    return " ".join([str(x) for x in [ "M", x, y, "L", x + arrow_width * cos - arrow_half_height * sin, y - arrow_half_height * cos - arrow_width * sin, "L", x + arrow_axis * cos, y - arrow_axis * sin, "L", x + arrow_width * cos + arrow_half_height * sin, y + arrow_half_height * cos - arrow_width * sin, "Z"]])

def safe_print_for_PHP(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("utf8"))


lines = '<?xml version="1.0" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
lines += '\n\n<svg width="%s" height="%s" view_box="0 0 %s %s"\nxmlns="http://www.w3.org/2000/svg"\nxmlns:link="http://www.w3.org/1999/xlink">' % (width,height,width,height)
lines += u'\\n\\n<desc>Généré par Mocodo 2.3.7 le %s</desc>' % time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
lines += '\n\n<rect id="frame" x="0" y="0" width="%s" height="%s" fill="%s" stroke="none" stroke-width="0"/>' % (width,height,colors['background_color'] if colors['background_color'] else "none")

lines += u"""\n\n<!-- Association CREER -->"""
(x,y) = (cx[u"CREER"],cy[u"CREER"])
(ex,ey) = (cx[u"UTILISATEUR"],cy[u"UTILISATEUR"])
leg=straight_leg_factory(ex,ey,90,62,x,y,29,26,23+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"CREER,UTILISATEUR"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Courier New" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
path=arrow(*leg.arrow_pos(">",ratio[u"CREER,UTILISATEUR"]))
lines += u"""\n<path d="%(path)s" fill="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'stroke_color': colors['leg_stroke_color']}
(ex,ey) = (cx[u"QUESTIONNAIRE"],cy[u"QUESTIONNAIRE"])
leg=straight_leg_factory(ex,ey,115,71,x,y,29,26,23+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"CREER,QUESTIONNAIRE"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Courier New" font-size="12">0,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"DATE"],cy[u"DATE"])
leg=straight_leg_factory(ex,ey,98,26,x,y,29,26,23+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"CREER,DATE"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Courier New" font-size="12">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-CREER">""" % {}
path = upper_round_rect(-29+x,-26+y,58,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-29+x,0.0+y,58,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="58" height="52" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -29+x, 'y': -26+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -29+x, 'y0': 0+y, 'x1': 29+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">CREER</text>""" % {'x': -22+x, 'y': -7.4+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association ANALYSER -->"""
(x,y) = (cx[u"ANALYSER"],cy[u"ANALYSER"])
(ex,ey) = (cx[u"UTILISATEUR"],cy[u"UTILISATEUR"])
leg=straight_leg_factory(ex,ey,90,62,x,y,54,26,23+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"ANALYSER,UTILISATEUR"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Courier New" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
path=arrow(*leg.arrow_pos(">",ratio[u"ANALYSER,UTILISATEUR"]))
lines += u"""\n<path d="%(path)s" fill="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'stroke_color': colors['leg_stroke_color']}
(ex,ey) = (cx[u"QUESTIONNAIRE"],cy[u"QUESTIONNAIRE"])
leg=straight_leg_factory(ex,ey,115,71,x,y,54,26,23+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"ANALYSER,QUESTIONNAIRE"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Courier New" font-size="12">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"DATE"],cy[u"DATE"])
leg=straight_leg_factory(ex,ey,98,26,x,y,54,26,23+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"ANALYSER,DATE"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Courier New" font-size="12">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-ANALYSER">""" % {}
path = upper_round_rect(-54+x,-26+y,108,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-54+x,0.0+y,108,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="108" height="52" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -54+x, 'y': -26+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -54+x, 'y0': 0+y, 'x1': 54+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">ANALYSER</text>""" % {'x': -34+x, 'y': -7.4+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">url_analyse</text>""" % {'x': -47+x, 'y': 18.6+y, 'text_color': colors['association_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association AVOIR_TYPE_UTILISATEUR -->"""
(x,y) = (cx[u"AVOIR_TYPE_UTILISATEUR"],cy[u"AVOIR_TYPE_UTILISATEUR"])
(ex,ey) = (cx[u"UTILISATEUR"],cy[u"UTILISATEUR"])
leg=straight_leg_factory(ex,ey,90,62,x,y,100,26,23+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"AVOIR_TYPE_UTILISATEUR,UTILISATEUR"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Courier New" font-size="12">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"TYPE_UTILISATEUR"],cy[u"TYPE_UTILISATEUR"])
leg=straight_leg_factory(ex,ey,73,35,x,y,100,26,23+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"AVOIR_TYPE_UTILISATEUR,TYPE_UTILISATEUR"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Courier New" font-size="12">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
path=arrow(*leg.arrow_pos(">",ratio[u"AVOIR_TYPE_UTILISATEUR,TYPE_UTILISATEUR"]))
lines += u"""\n<path d="%(path)s" fill="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'stroke_color': colors['leg_stroke_color']}
lines += u"""\n<g id="association-AVOIR_TYPE_UTILISATEUR">""" % {}
path = upper_round_rect(-100+x,-26+y,200,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-100+x,0.0+y,200,26,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="200" height="52" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -100+x, 'y': -26+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -100+x, 'y0': 0+y, 'x1': 100+x, 'y1': 0+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">AVOIR_TYPE_UTILISATEUR</text>""" % {'x': -93+x, 'y': -7.4+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity DATE -->"""
(x,y) = (cx[u"DATE"],cy[u"DATE"])
lines += u"""\n<g id="entity-DATE">""" % {}
lines += u"""\n	<g id="frame-DATE">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="196" height="26" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -98+x, 'y': -26+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="196" height="26" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -98+x, 'y': 0.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="196" height="52" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -98+x, 'y': -26+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -98+x, 'y0': 0+y, 'x1': 98+x, 'y1': 0+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">DATE</text>""" % {'x': -18+x, 'y': -7.4+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">aaaa-mm-jj_hh:mm:ss'ms</text>""" % {'x': -93+x, 'y': 18.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -93+x, 'y0': 21.0+y, 'x1': 93+x, 'y1': 21.0+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity UTILISATEUR -->"""
(x,y) = (cx[u"UTILISATEUR"],cy[u"UTILISATEUR"])
lines += u"""\n<g id="entity-UTILISATEUR">""" % {}
lines += u"""\n	<g id="frame-UTILISATEUR">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="180" height="26" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -90+x, 'y': -62+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="180" height="98" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -90+x, 'y': -36.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="180" height="124" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -90+x, 'y': -62+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -90+x, 'y0': -36+y, 'x1': 90+x, 'y1': -36+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">UTILISATEUR</text>""" % {'x': -47+x, 'y': -43.4+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">id_utilisateur</text>""" % {'x': -85+x, 'y': -17.4+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -85+x, 'y0': -15.0+y, 'x1': 34+x, 'y1': -15.0+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">nom_utilisateur</text>""" % {'x': -85+x, 'y': 0.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">prenom_utilisateur</text>""" % {'x': -85+x, 'y': 18.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">login_utilisateur</text>""" % {'x': -85+x, 'y': 36.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">password_utilisateur</text>""" % {'x': -85+x, 'y': 54.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity QUESTIONNAIRE -->"""
(x,y) = (cx[u"QUESTIONNAIRE"],cy[u"QUESTIONNAIRE"])
lines += u"""\n<g id="entity-QUESTIONNAIRE">""" % {}
lines += u"""\n	<g id="frame-QUESTIONNAIRE">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="230" height="26" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -115+x, 'y': -71+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="230" height="116" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -115+x, 'y': -45.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="230" height="142" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -115+x, 'y': -71+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -115+x, 'y0': -45+y, 'x1': 115+x, 'y1': -45+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">QUESTIONNAIRE</text>""" % {'x': -55+x, 'y': -52.4+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">id_questionnaire</text>""" % {'x': -110+x, 'y': -26.4+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -110+x, 'y0': -24.0+y, 'x1': 26+x, 'y1': -24.0+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">intitule_questionnaire</text>""" % {'x': -110+x, 'y': -8.4+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">dateheurelim_questionnaire</text>""" % {'x': -110+x, 'y': 9.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">accessible_questionnaire</text>""" % {'x': -110+x, 'y': 27.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">termine_questionnaire</text>""" % {'x': -110+x, 'y': 45.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">analyse_questionnaire</text>""" % {'x': -110+x, 'y': 63.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity TYPE_UTILISATEUR -->"""
(x,y) = (cx[u"TYPE_UTILISATEUR"],cy[u"TYPE_UTILISATEUR"])
lines += u"""\n<g id="entity-TYPE_UTILISATEUR">""" % {}
lines += u"""\n	<g id="frame-TYPE_UTILISATEUR">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="146" height="26" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -73+x, 'y': -35+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="146" height="44" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -73+x, 'y': -9.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="146" height="70" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -73+x, 'y': -35+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -73+x, 'y0': -9+y, 'x1': 73+x, 'y1': -9+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">TYPE_UTILISATEUR</text>""" % {'x': -68+x, 'y': -16.4+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">id_typeutil</text>""" % {'x': -68+x, 'y': 9.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -68+x, 'y0': 12.0+y, 'x1': 26+x, 'y1': 12.0+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Courier New" font-size="14">libelle_typeutil</text>""" % {'x': -68+x, 'y': 27.6+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}
lines += u'\n</svg>'

with codecs.open("mcd_utilisateur_arranged.svg", "w", "utf8") as f:
    f.write(lines)
safe_print_for_PHP(u'Fichier de sortie "mcd_utilisateur_arranged.svg" généré avec succès.')