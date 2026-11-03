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

AW, AH = 342, 148
crops = {
    "noonu": (5.78, 73.38, 560),
    "kaafu": (4.33, 73.56, 520),
    "laamu": (1.95, 73.40, 560),
    "ari": (3.86, 72.90, 470),
    "raa": (5.5, 72.98, 520),
    "addu": (-0.63, 73.13, 820),
}
for n, (la, lo, z) in crops.items():
    l0 = lo - (AW / 2) / z
    t0 = la + (AH / 2) / z
    xf = lambda a, l0=l0, z=z: (a - l0) * z
    yf = lambda b, t0=t0, z=z: (t0 - b) * z
    open(f"{out}/atoll-{n}.svg", "w").write(svg(render(xf, yf, z, AW, AH, minreef=1.5, hazeR=10, m=24), AW, AH))

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
