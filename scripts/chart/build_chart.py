"""Build the portfolio's chart assets from the JSON made by extract_osm.py.

Usage: python3 -I scripts/chart/build_chart.py <parsed.json> src/assets/chart
"""
import json, math, sys, collections, re

src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))
S = 430          # pixels per degree
LON0 = 72.50     # left edge, leaves room for the sea haze to fade out
LAT0 = 7.15      # top edge
W = 610
H = int((LAT0 + 0.78) * S)
X = lambda lo, s=S, l0=LON0: (lo - l0) * s
Y = lambda la, s=S, l0=LAT0: (l0 - la) * s
land = d["land"]

# Count mapped buildings on each island: the light tiers follow this.
cell = 0.02
grid = collections.defaultdict(list)
for lo, la in d["buildings"]:
    grid[(int(lo / cell), int(la / cell))].append((lo, la))


def pip(p, r):
    x, y = p
    c = False
    for i in range(len(r) - 1):
        x0, y0 = r[i]
        x1, y1 = r[i + 1]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            c = not c
    return c


for i in land:
    xs = [p[0] for p in i["ring"]]
    ys = [p[1] for p in i["ring"]]
    n = 0
    for gx in range(int(min(xs) / cell), int(max(xs) / cell) + 1):
        for gy in range(int(min(ys) / cell), int(max(ys) / cell) + 1):
            for b in grid.get((gx, gy), []):
                if min(xs) <= b[0] <= max(xs) and min(ys) <= b[1] <= max(ys) and pip(b, i["ring"]):
                    n += 1
    i["b"] = n
T1 = [i for i in land if i["b"] >= 500]
T2 = [i for i in land if 80 <= i["b"] < 500]
T3 = [i for i in land if 15 <= i["b"] < 80]
T0 = [i for i in land if i["b"] < 15]
print("islands", len(land), "tiers", len(T1), len(T2), len(T3), len(T0))


def circ(x, y, r):
    return f"M{x-r:.1f} {y:.1f}a{r:.2f} {r:.2f} 0 1 0 {2*r:.2f} 0a{r:.2f} {r:.2f} 0 1 0 {-2*r:.2f} 0z"


def dp(pts, t):
    if len(pts) < 3:
        return pts
    keep = [0, len(pts) - 1]
    st = [(0, len(pts) - 1)]
    while st:
        a, b = st.pop()
        ax, ay = pts[a]
        bx, by = pts[b]
        dx, dy = bx - ax, by - ay
        L = dx * dx + dy * dy
        mx = -1
        mi = None
        for i in range(a + 1, b):
            px, py = pts[i]
            if L == 0:
                q = (px - ax) ** 2 + (py - ay) ** 2
            else:
                u = max(0, min(1, ((px - ax) * dx + (py - ay) * dy) / L))
                q = (px - ax - u * dx) ** 2 + (py - ay - u * dy) ** 2
            if q > mx:
                mx = q
                mi = i
        if mx > t * t:
            keep.append(mi)
            st += [(a, mi), (mi, b)]
    return [pts[i] for i in sorted(keep)]


def lp(p):
    return f"M{p[0][0]:.1f} {p[0][1]:.1f}" + "".join(f"L{q[0]:.1f} {q[1]:.1f}" for q in p[1:])


def render(xf, yf, scale, w, h, minreef=2.0, hazeR=9, hazeCell=8, m=30):
    inb = lambda x, y: -m <= x <= w + m and -m <= y <= h + m
    hz = set()
    rf = []
    for r in d["reefs"]:
        raw = [(xf(a), yf(b)) for a, b in r]
        if not any(inb(*p) for p in raw):
            continue
        for p in raw:
            if inb(*p):
                hz.add((int(p[0] / hazeCell), int(p[1] / hazeCell)))
        pts = dp(raw, 0.6)
        if len(pts) < 2:
            continue
        ex = max(abs(p[0] - pts[0][0]) + abs(p[1] - pts[0][1]) for p in pts)
        if ex < minreef:
            continue
        rf.append(lp(pts))
    for i in land:
        x, y = xf(i["lon"]), yf(i["lat"])
        if inb(x, y):
            hz.add((int(x / hazeCell), int(y / hazeCell)))
    haze = "".join(circ((a + 0.5) * hazeCell, (b + 0.5) * hazeCell, hazeR) for a, b in hz)
    k = max(0.8, min(1.5, scale / 430))
    lay = lambda L, r: "".join(
        circ(xf(i["lon"]), yf(i["lat"]), r * k) for i in L if inb(xf(i["lon"]), yf(i["lat"]))
    )
    return {
        "haze": haze,
        "reef": "".join(rf),
        "dim": lay(T0, 0.72),
        "bloomWide": lay(T1, 9),
        "bloom": lay(T1, 5) + lay(T2, 3.2),
        "mid": lay(T3, 1.15) + lay(T2, 1.55),
        "core": lay(T1, 2.4),
    }


def svg(l, w, h):
    f = lambda i, s: (
        f'<filter id="{i}" filterUnits="userSpaceOnUse" x="-60" y="-60" width="{w+120}" height="{h+120}" '
        f'color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="{s}"/></filter>'
    )
    o = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs>'
    o += f("a", 13) + f("b", 9) + f("c", 3) + "</defs>"
    # Colours match the chart/* variables in the Figma file.
    if l["haze"]:
        o += f'<path fill="#2E7CA8" fill-opacity=".2" filter="url(#a)" d="{l["haze"]}"/>'
    if l["reef"]:
        o += f'<path fill="none" stroke="#6C9DBA" stroke-opacity=".42" stroke-width=".5" d="{l["reef"]}"/>'
    if l["dim"]:
        o += f'<path fill="#9DBFD4" fill-opacity=".85" d="{l["dim"]}"/>'
    if l["bloomWide"]:
        o += f'<path fill="#FFB869" fill-opacity=".1" filter="url(#b)" d="{l["bloomWide"]}"/>'
    if l["bloom"]:
        o += f'<path fill="#FFC98A" fill-opacity=".32" filter="url(#c)" d="{l["bloom"]}"/>'
    if l["mid"]:
        o += f'<path fill="#FFF3E2" d="{l["mid"]}"/>'
    if l["core"]:
        o += f'<path fill="#FFF" d="{l["core"]}"/>'
    return o + "</svg>"


s = svg(render(X, Y, S, W, H), W, H)
open(out + "/chart.svg", "w").write(s)
print("chart.svg KB", len(s) // 1024)

# Scrollbar art
ms = 150 / (LAT0 + 0.78)
ml = 72.58
mw = round(1.26 * ms, 1)
a = "".join(circ(X(i["lon"], ms, ml), Y(i["lat"], ms), 0.3) for i in T0 + T3)
b = "".join(circ(X(i["lon"], ms, ml), Y(i["lat"], ms), 0.55) for i in T1 + T2)
open(out + "/mini.svg", "w").write(
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{mw}" height="150" viewBox="0 0 {mw} 150">'
    f'<path fill="#9DBFD4" fill-opacity=".85" d="{a}"/><path fill="#FFF3E2" d="{b}"/></svg>'
)

# Atoll labels: islands are clustered to the nearest centre, then labelled beside the rim.
AT = [
    ("Haa Alif", 6.93, 73.03, "E"), ("Haa Dhaalu", 6.58, 73.02, "E"), ("Shaviyani", 6.2, 73.2, "E"),
    ("Noonu", 5.8, 73.38, "E"), ("Raa", 5.55, 72.93, "W"), ("Baa", 5.15, 73.03, "W"),
    ("Lhaviyani", 5.38, 73.53, "E"), ("Kaafu", 4.45, 73.5, "E"), ("Alif Alif", 4.2, 72.9, "W"),
    ("Alif Dhaal", 3.75, 72.85, "W"), ("Vaavu", 3.45, 73.5, "E"), ("Meemu", 2.95, 73.5, "E"),
    ("Faafu", 3.2, 72.95, "W"), ("Dhaalu", 2.8, 72.9, "W"), ("Thaa", 2.35, 73.05, "W"),
    ("Laamu", 1.95, 73.4, "E"), ("Gaafu Alif", 0.72, 73.2, "E"), ("Gaafu Dhaalu", 0.28, 73.2, "E"),
    ("Gnaviyani", -0.3, 73.43, "E"), ("Seenu", -0.63, 73.12, "E"),
]
cl = collections.defaultdict(list)
for i in land:
    cl[min(AT, key=lambda a: (a[1] - i["lat"]) ** 2 + (a[2] - i["lon"]) ** 2)[0]].append(i)
labels = []
for n, la, lo, side in AT:
    if n == "Seenu":  # Clustered so its islands don't join Gnaviyani, but shown as "Addu" on the page.
        continue
    xs = [X(i["lon"]) for i in cl[n]]
    ys = [Y(i["lat"]) for i in cl[n]]
    labels.append({"name": n, "x": round((max(xs) + 10) if side == "E" else (min(xs) - 10), 1),
                   "y": round(sum(ys) / len(ys) - 8, 1), "side": side})

# Project cards: each chart is drawn at the scale the project works at.
# Warm light means "this project". Every other island stays dim.
CW, CH = 640, 184
MALE = (4.178, 73.5107)
# Stops in sailing order, from the operators' own timetables.
FURAAQU = [
    MALE, (5.4916, 73.4118), (5.7665, 73.4127), (5.7762, 73.3625), (5.7905, 73.3629), (5.816, 73.3779),
    (5.8828, 73.4), (5.9513, 73.4165), (5.9678, 73.393), (6.0359, 73.2835), (6.15, 73.2905),
    (6.1641, 73.2521), (6.2643, 73.2181), (6.2862, 73.2434), (6.3272, 73.1489),
]
YOOSUF = [MALE, (4.1917, 73.529), (5.1031, 73.071), (5.1345, 73.1076), (5.2757, 73.0099), (5.3002, 73.0703)]


def num(v):
    s = f"{v:.1f}".rstrip("0").rstrip(".")
    return "0" if s in ("", "-0") else s


def dots(pts):
    """Draw points as tiny round-capped strokes, which is far smaller than circles."""
    return "".join(f"M{num(x)} {num(y)}h.01" for x, y in pts)


class CardChart:
    def __init__(self, la, lo, z):
        self.x = lambda a: CW / 2 + (a - lo) * z
        self.y = lambda b: CH / 2 + (la - b) * z
        self.parts = []
        self.marks = []

    def xy(self, p):
        return self.x(p[1]), self.y(p[0])

    def seen(self, x, y, m=20):
        return -m <= x <= CW + m and -m <= y <= CH + m

    def sea(self, cell=8, reach=10, minreef=1.2, islands=True):
        hz = set()
        rf = []
        for r in d["reefs"]:
            raw = [(self.x(a), self.y(b)) for a, b in r]
            if not any(self.seen(*p) for p in raw):
                continue
            hz.update((int(p[0] / cell), int(p[1] / cell)) for p in raw if self.seen(*p))
            pts = dp(raw, 0.6)
            if len(pts) > 1 and max(abs(p[0] - pts[0][0]) + abs(p[1] - pts[0][1]) for p in pts) >= minreef:
                rf.append(lp(pts))
        dim = [(self.x(i["lon"]), self.y(i["lat"])) for i in land]
        dim = [p for p in dim if self.seen(*p)]
        hz.update((int(x / cell), int(y / cell)) for x, y in dim)
        centres = [((a + 0.5) * cell, (b + 0.5) * cell) for a, b in sorted(hz)]
        self.parts.append(
            f'<path fill="none" stroke="#2E7CA8" stroke-opacity=".2" stroke-width="{reach * 2}" '
            f'stroke-linecap="round" filter="url(#a)" d="{dots(centres)}"/>'
        )
        if rf:
            self.parts.append(
                f'<path fill="none" stroke="#6C9DBA" stroke-opacity=".34" stroke-width=".5" d="{"".join(rf)}"/>'
            )
        if islands and dim:
            self.parts.append(
                f'<path fill="none" stroke="#9DBFD4" stroke-opacity=".6" stroke-width="1.1" '
                f'stroke-linecap="round" d="{dots(dim)}"/>'
            )
        return self

    def route(self, stops, opacity=0.8):
        self.parts.append(
            f'<path fill="none" stroke="#FFC98A" stroke-opacity="{opacity}" stroke-dasharray="3 3" '
            f'd="{lp([self.xy(p) for p in stops])}"/>'
        )
        return self

    def lights(self, points, core=2.6, bloom=3.6):
        pts = dots(self.xy(p) for p in points)
        self.parts.append(
            f'<path fill="none" stroke="#FFC98A" stroke-opacity=".5" stroke-width="{bloom * 2}" '
            f'stroke-linecap="round" filter="url(#c)" d="{pts}"/>'
            f'<path fill="none" stroke="#FFF3E2" stroke-width="{core}" stroke-linecap="round" d="{pts}"/>'
        )
        return self

    def hub(self, p):
        x, y = self.xy(p)
        self.parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="#FFB869" fill-opacity=".22" filter="url(#b)"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#FFC98A" fill-opacity=".5" filter="url(#c)"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#FFF"/>'
        )
        return self

    def mark(self, text, p, side="E", gap=8):
        x, y = self.xy(p)
        ox, oy = {"E": (gap, 0), "W": (-gap, 0), "S": (0, gap)}[side]
        self.marks.append({"text": text, "x": round(x + ox - CW / 2, 1), "y": round(y + oy, 1), "side": side})
        return self

    def write(self, name):
        f = lambda i, s: (
            f'<filter id="{i}" filterUnits="userSpaceOnUse" x="-60" y="-60" width="{CW + 120}" height="{CH + 120}" '
            f'color-interpolation-filters="sRGB"><feGaussianBlur stdDeviation="{s}"/></filter>'
        )
        open(f"{out}/card-{name}.svg", "w").write(
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}"><defs>'
            + f("a", 13) + f("b", 9) + f("c", 3) + "</defs>" + "".join(self.parts) + "</svg>"
        )
        return self.marks


route_z = (CH - 44) / (FURAAQU[-1][0] - MALE[0])
whole_z = (CH - 16) / (7.11 + 0.72)
whole_la = (7.11 - 0.72) / 2
whole_lo = MALE[1] + 18 / whole_z  # Sits left of centre to leave room for its label.
cards = {}

# Furaaqu and Yoosuf Speed: each company's real line of stops.
cards["furaaqu"] = (
    CardChart(5.25, 73.36, route_z).sea().route(FURAAQU).lights(FURAAQU[1:]).hub(MALE)
    .mark("Malé", MALE).mark("Shaviyani", FURAAQU[-1], "W").write("furaaqu")
)
cards["yoosuf"] = (
    CardChart(4.74, 73.3, (CH - 44) / (YOOSUF[-1][0] - MALE[0])).sea().route(YOOSUF)
    .lights(YOOSUF[2:], core=3.2, bloom=4.4).hub(MALE)
    .mark("Malé", MALE).mark("Baa", YOOSUF[4], "W").write("yoosuf")
)

# The PDF service renders the tickets for both of those lines.
cards["pdf"] = (
    CardChart(5.25, 73.28, route_z).sea().route(FURAAQU, 0.65).route(YOOSUF, 0.65)
    .lights(FURAAQU[1:] + YOOSUF[2:]).hub(MALE)
    .mark("Malé", MALE).mark("Furaaqu", FURAAQU[5], "E", 14).mark("Yoosuf Speed", YOOSUF[4], "W").write("pdf")
)

# Barfume is one city, so its chart is one city: every light is a mapped building.
city = CardChart(4.196, 73.561, 1900).sea(cell=16, reach=18, minreef=2, islands=False)
rings = [
    lp(dp(ring, 0.35)) + "z"
    for ring in ([(city.x(a), city.y(b)) for a, b in i["ring"]] for i in land)
    if any(city.seen(*p) for p in ring)
]
built = sorted({(round(city.x(a) * 2) / 2, round(city.y(b) * 2) / 2) for a, b in d["buildings"]
                if city.seen(city.x(a), city.y(b), 4)})
city.parts.append(
    f'<path fill="#9DBFD4" fill-opacity=".07" stroke="#9DBFD4" stroke-opacity=".35" stroke-width=".5" d="{"".join(rings)}"/>'
    f'<path fill="none" stroke="#FFC98A" stroke-opacity=".3" stroke-width="5" stroke-linecap="round" '
    f'filter="url(#c)" d="{dots(built)}"/>'
    f'<path fill="none" stroke="#FFF3E2" stroke-opacity=".92" stroke-width=".95" stroke-linecap="round" d="{dots(built)}"/>'
)
east = max(city.x(a) for a, b in d["buildings"] if 4.2 < b < 4.23 and 73.52 < a < 73.57)
hulhumale = ((CH / 2 - 44) / 1900 + 4.196, (east - CW / 2) / 1900 + 73.561)
cards["barfume"] = (
    city.mark("Malé", (4.1755, 73.5095), "S", 16).mark("Hulhumalé", hulhumale, "E", 10).write("barfume")
)

# TaxFlow: businesses in every atoll file with one tax authority in Malé.
capitals = {n: max(cl[n], key=lambda i: i["b"]) for n, *_ in AT}
capitals = [(i["lat"], i["lon"]) for n, i in capitals.items() if n != "Kaafu"]
tax = CardChart(whole_la, whole_lo, whole_z).sea(cell=6, reach=6, minreef=9)
fan = "".join(lp([tax.xy(p), tax.xy(MALE)]) for p in capitals)
tax.parts.append(f'<path fill="none" stroke="#FFC98A" stroke-opacity=".5" stroke-width=".6" d="{fan}"/>')
cards["taxflow"] = tax.lights(capitals, core=1.9, bloom=2.4).hub(MALE).mark("Tax authority, Malé", MALE, "E", 18).write("taxflow")

# Basvaaru: a phone app, so every settled island is lit.
settled = [(i["lat"], i["lon"]) for i in T1 + T2 + T3]
cards["basvaaru"] = (
    CardChart(whole_la, whole_lo, whole_z).sea(cell=6, reach=6, minreef=9).lights(settled, core=1.5, bloom=2.6)
    .mark("On any island", MALE, "E", 26).write("basvaaru")
)
json.dump({"width": CW, "height": CH, "marks": cards}, open(out + "/cards.json", "w"), ensure_ascii=False, indent=1)

# Island names for the hover label: English names only, one entry per place.
seen = {}
for lo, la, nm, *_ in d["named"] + d["settlements"]:
    if nm and re.fullmatch(r"[A-Za-z0-9 .'’\-()é]+", nm):
        seen.setdefault(nm, (lo, la))
islands = [[round(X(lo), 1), round(Y(la), 1), nm, round(la, 3), round(lo, 3)] for nm, (lo, la) in sorted(seen.items())
           if -1 <= la <= 7.2 and 72.5 <= lo <= 73.9]
json.dump(islands, open(out + "/islands.json", "w"), ensure_ascii=False, separators=(",", ":"))
print("named islands", len(islands))

json.dump({"scale": S, "lon0": LON0, "lat0": LAT0, "width": W, "height": H, "labels": labels,
           "male": [round(X(73.5107), 1), round(Y(4.178), 1)], "addu": [round(X(73.2), 1), round(Y(-0.6), 1)],
           "equatorY": round(LAT0 * S, 1)},
          open(out + "/meta.json", "w"), ensure_ascii=False, indent=1)
