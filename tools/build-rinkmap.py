"""Build the isometric rink diagram (SVG) and inline it into index.html between the rinkmap markers.

Run from the site root:  python tools/build-rinkmap.py
Also writes assets/rinkmap.svg for reuse (og image, docs).
"""
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

# Rink in local metres, centred: 60 x 26 (IIHF-ish), scaled by S for drawing.
S = 16
W, H, R = 60 * S, 26 * S, 8.5 * S
CX, CY = 600, 330           # screen centre of the rink
BOARD = 22                  # extruded board height in screen px
# isometric projection (30 degrees)
COS, SIN = math.cos(math.radians(30)), math.sin(math.radians(30))
ISO = f"matrix({COS:.4f},{SIN:.4f},{-COS:.4f},{SIN:.4f},{CX},{CY})"


def iso(x, y, lift=0):
    """local rink coords (metres*S, origin centre) -> screen coords; lift raises in screen space."""
    return (COS * x - COS * y + CX, SIN * x + SIN * y + CY - lift)


def rr_path(w, h, r):
    x, y = -w / 2, -h / 2
    return (f"M{x + r},{y} H{x + w - r} A{r},{r} 0 0 1 {x + w},{y + r} V{y + h - r} A{r},{r} 0 0 1 {x + w - r},{y + h} "
            f"H{x + r} A{r},{r} 0 0 1 {x},{y + h - r} V{y + r} A{r},{r} 0 0 1 {x + r},{y} Z")


def circle(cx, cy, r, stroke, width, fill="none"):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'


def rink_markings():
    out = []
    out.append(f'<path d="{rr_path(W, H, R)}" fill="#F3F7FB"/>')
    # subtle ice sheen
    out.append(f'<path d="{rr_path(W, H, R)}" fill="url(#sheen)"/>')
    out.append(f'<clipPath id="iceclip"><path d="{rr_path(W, H, R)}"/></clipPath>')
    out.append('<g clip-path="url(#iceclip)">')
    out.append(f'<rect x="-3" y="{-H/2}" width="6" height="{H}" fill="#E0273F"/>')
    for x in (-8.6 * S, 8.6 * S):
        out.append(f'<rect x="{x - 3}" y="{-H/2}" width="6" height="{H}" fill="#2458C5"/>')
    for x in (-26 * S, 26 * S):
        out.append(f'<rect x="{x - 1.5}" y="{-H/2}" width="3" height="{H}" fill="#E0273F"/>')
    out.append(circle(0, 0, 4.5 * S, "#2458C5", 4))
    out.append(circle(0, 0, 4, "#2458C5", 0, "#2458C5"))
    for x in (-16 * S, 16 * S):
        for y in (-6.5 * S, 6.5 * S):
            out.append(circle(x, y, 4.5 * S, "#E0273F", 4))
            out.append(circle(x, y, 4, "#E0273F", 0, "#E0273F"))
    for x in (-5 * S, 5 * S):
        for y in (-6.5 * S, 6.5 * S):
            out.append(circle(x, y, 4, "#E0273F", 0, "#E0273F"))
    # creases + goals
    for sign in (-1, 1):
        gx = sign * 26 * S
        out.append(f'<path d="M{gx},{-1.8*S} A{1.8*S},{1.8*S} 0 0 {1 if sign<0 else 0} {gx},{1.8*S} Z" fill="rgba(80,160,230,0.5)" stroke="#E0273F" stroke-width="3"/>')
        out.append(f'<rect x="{gx if sign>0 else gx - 1.1*S}" y="{-0.95*S}" width="{1.1*S}" height="{1.9*S}" fill="none" stroke="#E0273F" stroke-width="5"/>')
    # training lane for Analytic Cam
    out.append(f'<rect x="{-24*S}" y="{-11*S}" width="{14*S}" height="{5*S}" rx="8" fill="rgba(139,92,246,0.18)" stroke="#8B5CF6" stroke-width="3" stroke-dasharray="10 8"/>')
    out.append('</g>')
    # centre logo
    out.append(f'<text x="0" y="{0}" text-anchor="middle" dominant-baseline="middle" font-family="Outfit, sans-serif" font-weight="900" font-size="{2.6*S}" fill="rgba(224,39,63,0.85)" transform="translate(0,{-9*S})">FULLRINK</text>')
    return "\n".join(out)


def boards():
    """Extruded boards: side wall drawn from the outline shifted down, then the top rim."""
    out = []
    # wall: fill between top outline and bottom outline, approximated by drawing the bottom outline thick and dark
    out.append(f'<g transform="translate(0,{BOARD})"><g transform="{ISO}"><path d="{rr_path(W + 14, H + 14, R + 7)}" fill="#15151B" stroke="#15151B" stroke-width="2"/></g></g>')
    for i in range(BOARD, 0, -1):
        pass
    # stack of thin outlines to fake the wall
    for i in range(BOARD, -1, -2):
        out.append(f'<g transform="translate(0,{i})"><g transform="{ISO}"><path d="{rr_path(W + 14, H + 14, R + 7)}" fill="none" stroke="#1E1E26" stroke-width="14"/></g></g>')
    # kick plate + rim
    out.append(f'<g transform="translate(0,2)"><g transform="{ISO}"><path d="{rr_path(W + 14, H + 14, R + 7)}" fill="none" stroke="#E0273F" stroke-width="5"/></g></g>')
    out.append(f'<g transform="{ISO}"><path d="{rr_path(W + 14, H + 14, R + 7)}" fill="none" stroke="#FFFFFF" stroke-width="10"/></g>')
    # glass hint
    out.append(f'<g transform="translate(0,-10)"><g transform="{ISO}"><path d="{rr_path(W + 14, H + 14, R + 7)}" fill="none" stroke="rgba(191,227,255,0.35)" stroke-width="3"/></g></g>')
    return "\n".join(out)


def furniture():
    out = []
    # benches on the near side (+y), penalty boxes on the far side (-y)
    for x in (-13 * S, 3 * S):
        out.append(f'<g transform="{ISO}"><rect x="{x}" y="{H/2 + 10}" width="{10*S}" height="{2.2*S}" fill="#2A2A33" stroke="#3A3A44" stroke-width="2"/></g>')
    for x in (-9 * S, 4 * S):
        out.append(f'<g transform="{ISO}"><rect x="{x}" y="{-H/2 - 2.2*S - 10}" width="{5*S}" height="{2.2*S}" fill="#2A2A33" stroke="#3A3A44" stroke-width="2"/></g>')
    out.append(f'<g transform="{ISO}"><rect x="{-2*S}" y="{-H/2 - 2.2*S - 10}" width="{4*S}" height="{2.2*S}" fill="#3A3A44" stroke="#4A4A55" stroke-width="2"/></g>')
    return "\n".join(out)


def scoreboard(x_local, lift):
    """Overhead scoreboard behind a goal: a panel floating above the end boards."""
    sx, sy = iso(x_local, 0, lift)
    w, h = 150, 64
    return (f'<g class="sb" transform="translate({sx - w/2},{sy - h/2})">'
            f'<rect width="{w}" height="{h}" rx="6" fill="#0B0E14" stroke="#3A4252" stroke-width="2"/>'
            f'<text x="{w*0.22}" y="42" text-anchor="middle" font-family="Outfit, sans-serif" font-weight="900" font-size="30" fill="#F43F5E">1</text>'
            f'<text x="{w/2}" y="40" text-anchor="middle" font-family="JetBrains Mono, monospace" font-weight="700" font-size="24" fill="#35D07F">7:19</text>'
            f'<text x="{w*0.78}" y="42" text-anchor="middle" font-family="Outfit, sans-serif" font-weight="900" font-size="30" fill="#8B5CF6">0</text>'
            f'<line x1="{w/2}" y1="{h}" x2="{w/2}" y2="{h + lift - 8}" stroke="#55555F" stroke-width="2" stroke-dasharray="4 4"/>'
            f'</g>')


def camera(sx, sy, angle=0, scale=1.0):
    return (f'<g transform="translate({sx},{sy}) rotate({angle}) scale({scale})">'
            f'<rect x="-14" y="-9" width="28" height="18" rx="3" fill="#15151B" stroke="#F3F7FB" stroke-width="2"/>'
            f'<circle cx="0" cy="0" r="5" fill="#15151B" stroke="#F3F7FB" stroke-width="2"/>'
            f'<path d="M14,-5 L24,-10 L24,10 L14,5 Z" fill="#F3F7FB"/></g>')


def phone(sx, sy, scale=1.0):
    return (f'<g transform="translate({sx},{sy}) scale({scale})">'
            f'<rect x="-7" y="-13" width="14" height="26" rx="3" fill="#15151B" stroke="#F3F7FB" stroke-width="2"/>'
            f'<rect x="-5" y="-10" width="10" height="18" rx="1" fill="#3B82F6"/></g>')


# ---- app pins: (id, number, name, local x, local y, lift, note) ----
PINS = [
    ("liveby", "01", "Live By", 0, H / 2 + 2.8 * S, 0, "Centre ice, side boards: the live broadcast camera on a tripod"),
    ("dejavucam", "02", "DejaVu Cam", -13 * S, -8.5 * S, 0, "Training lane: tap after the move and replay it in slow motion"),
    ("mobilevar", "03", "Mobile VAR", -34 * S, 0, 0, "Behind both goals: frame-by-frame review of what happened at the net"),
    ("mobilevar", "03", "Mobile VAR", 34 * S, 0, 0, None),
    ("analytic-cam", "04", "Analytic Cam", -21 * S, -8.5 * S, 0, "Training lane: skating technique from a clip, lean and knee angles"),
    ("scoreboard", "05", "Live By Scoreboard", -36 * S, 0, 150, "Overhead behind both goals: period, clock, score on any screen"),
    ("scoreboard", "05", "Live By Scoreboard", 36 * S, 0, 150, None),
    ("gamemap", "06", "GameMap · Game Cam", 0, -H / 2 - 9 * S, 190, "One high camera films the whole rink for the video session and the rink map"),
]


def pins():
    out = []
    for pid, n, name, x, y, lift, note in PINS:
        sx, sy = iso(x, y, lift)
        gx, gy = iso(x, y, 0)
        if lift:
            out.append(f'<line x1="{sx}" y1="{sy}" x2="{gx}" y2="{gy}" stroke="rgba(250,250,250,0.35)" stroke-width="2" stroke-dasharray="4 4"/>')
        out.append(f'<g class="pin" data-app="{pid}" transform="translate({sx},{sy - 26})">'
                   f'<path d="M0,26 L-9,8 A13,13 0 1 1 9,8 Z" fill="#F43F5E"/>'
                   f'<circle cx="0" cy="4" r="11" fill="#09090B"/>'
                   f'<text x="0" y="8" text-anchor="middle" font-family="JetBrains Mono, monospace" font-weight="700" font-size="11" fill="#FAFAFA">{n}</text></g>')
    return "\n".join(out)


def build_svg():
    parts = [
        '<svg class="rinkmap" viewBox="0 0 1200 620" xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="rinkmap-title">',
        '<title id="rinkmap-title">Isometric rink diagram showing where each FullRink app is used</title>',
        '<defs><linearGradient id="sheen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.35"/><stop offset="1" stop-color="#9CC8F0" stop-opacity="0.25"/></linearGradient></defs>',
        # floor shadow
        f'<g transform="translate(0,{BOARD + 18})"><g transform="{ISO}"><path d="{rr_path(W + 120, H + 120, R + 60)}" fill="rgba(0,0,0,0.35)"/></g></g>',
        boards(),
        f'<g transform="{ISO}">{rink_markings()}</g>',
        furniture(),
    ]
    # equipment icons
    lx, ly = iso(0, H / 2 + 2.8 * S); parts.append(camera(lx, ly + 6, -150, 1.1))
    gx, gy = iso(0, -H / 2 - 9 * S, 190); parts.append(camera(gx, gy + 8, 20, 1.2))
    for sign in (-1, 1):
        vx, vy = iso(sign * 34 * S, 0); parts.append(phone(vx, vy + 8))
        parts.append(scoreboard(sign * 36 * S, 150))
    bx, by = iso(-13 * S, -8.5 * S); parts.append(phone(bx, by + 8, 0.9))
    ax, ay = iso(-21 * S, -8.5 * S); parts.append(phone(ax, ay + 8, 0.9))
    parts.append(pins())
    parts.append('</svg>')
    return "\n".join(parts)


def legend_html():
    seen, items = set(), []
    for pid, n, name, x, y, lift, note in PINS:
        if pid in seen:
            continue
        seen.add(pid)
        items.append(f'<li><a href="apps/{pid}" data-app="{pid}"><b>{n}</b><span>{name}</span><small>{note}</small></a></li>')
    return '<ol class="rink-legend">\n' + "\n".join(items) + '\n</ol>'


def main():
    svg = build_svg()
    (ROOT / "assets" / "rinkmap.svg").write_text(svg, encoding="utf-8", newline="\n")
    idx = ROOT / "index.html"
    s = idx.read_text(encoding="utf-8")
    a, b = "<!-- rinkmap:start -->", "<!-- rinkmap:end -->"
    i, j = s.index(a) + len(a), s.index(b)
    s = s[:i] + "\n" + svg + "\n" + legend_html() + "\n" + s[j:]
    idx.write_text(s, encoding="utf-8", newline="\n")
    print("rinkmap inlined; svg bytes:", len(svg))


if __name__ == "__main__":
    main()
