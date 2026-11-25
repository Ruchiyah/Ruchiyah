"""Generate the animated SVG assets used by the profile README.

Run:  python3 scripts/generate_assets.py   (writes into ./assets)
Everything is hand-built SVG + CSS/SMIL animation, so it renders inside
GitHub's <img> sandbox (no JavaScript, no external fonts).
"""
import math
import random
import textwrap
from html import escape
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

SANS = "'Segoe UI',Ubuntu,'Helvetica Neue',Arial,sans-serif"
MONO = "'JetBrains Mono','Fira Code',Consolas,Menlo,monospace"
COS30 = math.cos(math.radians(30))


def shade(hex_color, f):
    """f > 0 lightens towards white, f < 0 darkens towards black."""
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    t = 255 if f > 0 else 0
    f = abs(f)
    r, g, b = (round(c + (t - c) * f) for c in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"


def pts(*p):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in p)


def iso_box(x, yb, s, h, color, extra=""):
    """Isometric box whose front-bottom vertex is (x, yb); s = edge, h = height."""
    a = COS30 * s
    F, L, R = (x, yb), (x - a, yb - s / 2), (x + a, yb - s / 2)
    Ft, Lt, Rt, Bt = (x, yb - h), (x - a, yb - s / 2 - h), (x + a, yb - s / 2 - h), (x, yb - s - h)
    return (
        f'<g {extra}>'
        f'<polygon points="{pts(L, F, Ft, Lt)}" fill="{color}"/>'
        f'<polygon points="{pts(F, R, Rt, Ft)}" fill="{shade(color, -0.35)}"/>'
        f'<polygon points="{pts(Lt, Ft, Rt, Bt)}" fill="{shade(color, 0.35)}"/>'
        f'<polyline points="{pts(Lt, Bt, Rt)}" fill="none" stroke="{shade(color, 0.7)}" stroke-width="1" opacity=".8"/>'
        "</g>"
    )


def write(name, body):
    (OUT / name).write_text(body.strip() + "\n", encoding="utf-8")
    print("wrote", OUT / name)


# --------------------------------------------------------------------------- hero
def hero():
    W, H, HZ = 1200, 420, 290
    rnd = random.Random(7)
    stars = "".join(
        f'<circle cx="{rnd.uniform(10, W - 10):.0f}" cy="{rnd.uniform(10, HZ - 10):.0f}" '
        f'r="{rnd.choice([0.8, 1.1, 1.5]):.1f}" class="tw" style="animation-delay:-{rnd.uniform(0, 4):.1f}s"/>'
        for _ in range(70)
    )
    # perspective floor
    vp = W * 0.5
    floor = "".join(
        f'<line x1="{vp + k * 14:.0f}" y1="{HZ}" x2="{vp + k * 120:.0f}" y2="{H}"/>' for k in range(-16, 17)
    )
    floor += "".join(
        f'<line x1="0" y1="{HZ + (H - HZ) * (i / 9) ** 1.9:.1f}" x2="{W}" y2="{HZ + (H - HZ) * (i / 9) ** 1.9:.1f}"/>'
        for i in range(1, 10)
    )
    # wireframe globe (meridians animate rx to fake rotation)
    gx, gy, gr = 925, 172, 104
    meridians = "".join(
        f'<ellipse cx="{gx}" cy="{gy}" rx="{gr}" ry="{gr}">'
        f'<animate attributeName="rx" values="{gr};0;{gr}" dur="8s" begin="-{i * 8 / 12:.2f}s" repeatCount="indefinite" '
        f'calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/></ellipse>'
        for i in range(6)
    )
    lats = "".join(
        f'<ellipse cx="{gx}" cy="{gy + gr * math.sin(math.radians(a)):.1f}" '
        f'rx="{gr * math.cos(math.radians(a)):.1f}" ry="{gr * math.cos(math.radians(a)) * 0.22:.1f}"/>'
        for a in (-60, -30, 0, 30, 60)
    )
    nodes = "".join(
        f'<circle cx="{gx + gr * 0.8 * math.cos(t):.1f}" cy="{gy + gr * 0.55 * math.sin(t * 1.7):.1f}" r="3" class="node" '
        f'style="animation-delay:-{i * 0.4:.1f}s"/>'
        for i, t in enumerate([0.3, 1.2, 2.1, 2.9, 3.8, 4.6, 5.5])
    )
    cubes = "".join(
        f'<g class="bob" style="animation-delay:-{d}s">{iso_box(x, y, s, s, c)}</g>'
        for x, y, s, c, d in [
            (765, 120, 26, "#14b8a6", 0),
            (1105, 92, 16, "#6366f1", 1.3),
            (1095, 262, 20, "#22c55e", 2.1),
            (735, 250, 14, "#0ea5e9", 0.7),
        ]
    )
    chips = ""
    x = 72
    for label, col in [("DATA SCIENCE", "#14b8a6"), ("ANALYTICS", "#0ea5e9"), ("AI / ML", "#8b5cf6"), ("SOFTWARE", "#22c55e")]:
        w = len(label) * 8.6 + 34
        chips += (
            f'<g transform="translate({x:.0f},322)"><rect width="{w:.0f}" height="34" rx="17" fill="#071318" fill-opacity=".85" '
            f'stroke="{col}" stroke-opacity=".8"/><circle cx="17" cy="17" r="4" fill="{col}"/>'
            f'<text x="29" y="22" fill="#e2e8f0" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="1">{label}</text></g>'
        )
        x += w + 12

    write("hero.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Ruchira Kotuwegedara — Data Science, Analytics, AI and Software">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#030712"/><stop offset=".55" stop-color="#071a24"/><stop offset="1" stop-color="#052e2b"/></linearGradient>
  <radialGradient id="sun" cx="{gx / W:.3f}" cy="{gy / H:.3f}" r=".45"><stop offset="0" stop-color="#14b8a6" stop-opacity=".45"/><stop offset="1" stop-color="#14b8a6" stop-opacity="0"/></radialGradient>
  <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".35" stop-color="#fff" stop-opacity=".6"/><stop offset="1" stop-color="#fff"/></linearGradient>
  <mask id="floorMask"><rect y="{HZ}" width="{W}" height="{H - HZ}" fill="url(#fade)"/></mask>
  <linearGradient id="name" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="#5eead4"/><stop offset=".35" stop-color="#ffffff"/><stop offset=".65" stop-color="#22c55e"/><stop offset="1" stop-color="#5eead4"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <linearGradient id="globe" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5eead4"/><stop offset="1" stop-color="#6366f1"/></linearGradient>
  <linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2dd4bf" stop-opacity="0"/><stop offset="1" stop-color="#2dd4bf" stop-opacity=".55"/></linearGradient>
  <clipPath id="frame"><rect width="{W}" height="{H}" rx="26"/></clipPath>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>
  .tw{{fill:#a5f3fc;animation:tw 4s ease-in-out infinite}}
  @keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:.9}}}}
  .bob{{animation:bob 5s ease-in-out infinite}}
  @keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-14px)}}}}
  .node{{fill:#5eead4;animation:pulse 2.8s ease-in-out infinite}}
  @keyframes pulse{{0%,100%{{opacity:.2}}50%{{opacity:1}}}}
  .floor line{{stroke:#14b8a6;stroke-width:1.1}}
</style>
<g clip-path="url(#frame)">
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" fill="url(#sun)"/>
  {stars}
  <g class="floor" mask="url(#floorMask)">{floor}</g>
  <rect x="0" width="{W}" height="26" fill="url(#scan)" opacity=".7">
    <animate attributeName="y" values="{HZ - 26};{H}" dur="4s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values=".1;.6;0" dur="4s" repeatCount="indefinite"/>
  </rect>
  <line x1="0" y1="{HZ}" x2="{W}" y2="{HZ}" stroke="#2dd4bf" stroke-opacity=".7" filter="url(#glow)"/>

  <g fill="none" stroke="url(#globe)" stroke-width="1.3" opacity=".85">
    <ellipse cx="{gx}" cy="{gy}" rx="{gr * 1.75}" ry="{gr * 0.36}" transform="rotate(-16 {gx} {gy})" stroke="#2dd4bf" stroke-dasharray="4 7" opacity=".7">
      <animate attributeName="stroke-dashoffset" values="0;-110" dur="5s" repeatCount="indefinite"/>
    </ellipse>
    <circle cx="{gx}" cy="{gy}" r="{gr}" stroke-width="2" filter="url(#glow)"/>
    {meridians}{lats}
  </g>
  {nodes}
  <g transform="rotate(-16 {gx} {gy})"><circle r="6" fill="#22c55e" filter="url(#glow)">
    <animateMotion dur="7s" repeatCount="indefinite" path="M{gx + gr * 1.75:.1f},{gy} A{gr * 1.75:.1f},{gr * 0.36:.1f} 0 1,1 {gx - gr * 1.75:.1f},{gy} A{gr * 1.75:.1f},{gr * 0.36:.1f} 0 1,1 {gx + gr * 1.75:.1f},{gy}"/>
  </circle></g>
  {cubes}

  <g>
    <text x="74" y="104" fill="#5eead4" font-family="{MONO}" font-size="16" font-weight="700" letter-spacing="4">&gt; HELLO WORLD, I'M</text>
  </g>
  <g>
    <text x="70" y="180" fill="url(#name)" font-family="{SANS}" font-size="74" font-weight="800" letter-spacing="-1">Ruchira</text>
  </g>
  <g>
    <text x="70" y="254" fill="url(#name)" font-family="{SANS}" font-size="74" font-weight="800" letter-spacing="-1">Kotuwegedara</text>
  </g>
  <g>{chips}</g>
  <text x="74" y="392" fill="#94a3b8" font-family="{MONO}" font-size="13" letter-spacing="1.5">BSc (Hons) IT · SLIIT · Sri Lanka  —  turning data into evidence, and evidence into systems</text>
</g>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="26" fill="none" stroke="#14b8a6" stroke-opacity=".35" stroke-width="1.5"/>
</svg>""")


# ---------------------------------------------------------------------- terminal
def terminal():
    W, H = 1000, 466
    K, S, N, F, P, C, D = "#c084fc", "#86efac", "#7dd3fc", "#fbbf24", "#e2e8f0", "#64748b", "#5eead4"
    code = [
        [("class ", K), ("Ruchira", F), ("(", P), ("DataScientist", D), (", ", P), ("Engineer", D), ("):", P)],
        [("    university ", N), ("= ", P), ('"SLIIT · Sri Lanka"', S)],
        [("    degree     ", N), ("= ", P), ('"BSc (Hons) in Information Technology"', S)],
        [("    focus      ", N), ("= ", P), ("[", P), ('"Data Science"', S), (", ", P), ('"AI / ML"', S), (", ", P), ('"Analytics"', S), ("]", P)],
        [("    builds     ", N), ("= ", P), ("[", P), ('"Full-stack apps"', S), (", ", P), ('"REST APIs"', S), (", ", P), ('"BI pipelines"', S), ("]", P)],
        [("    off_duty   ", N), ("= ", P), ("[", P), ('"🎸 guitar"', S), (", ", P), ('"📖 mysteries"', S), (", ", P), ('"🎮 games"', S), ("]", P)],
        [],
        [("    def ", K), ("solve", F), ("(", P), ("self", K), (", problem):", P)],
        [("        ", P), ("# evidence first, then build — then make the next version better", C)],
        [("        return ", K), ("understand", F), ("(problem) ", P), ("&gt;&gt; ", D), ("model", F), ("() ", P), ("&gt;&gt; ", D), ("ship", F), ("()", P)],
    ]
    T, x0, y0, lh = 18.0, 78, 104, 29
    lines = ""
    for i, segs in enumerate(code):
        y = y0 + i * lh
        lines += f'<text x="44" y="{y}" fill="#334155" font-family="{MONO}" font-size="15" text-anchor="end">{i + 1}</text>'
        if not segs:
            continue
        chars = sum(len(t.replace("&gt;", ">")) for t, _ in segs)
        wmax = min(W - x0, chars * 9.7 + 24)
        start, dur = 0.6 + i * 1.05, max(0.35, chars * 0.018)
        k = [0, start / T, (start + dur) / T, (start + dur) / T + 0.001, (T - 0.6) / T, 1]
        tsp = "".join(f'<tspan fill="{c}">{t}</tspan>' for t, c in segs)
        lines += (
            f'<clipPath id="l{i}"><rect x="{x0 - 4}" y="{y - 21}" height="{lh}" width="0">'
            f'<animate attributeName="width" dur="{T}s" repeatCount="indefinite" values="0;0;{wmax:.0f};{W};{W};0" '
            f'keyTimes="{";".join(f"{v:.4f}" for v in k)}"/></rect></clipPath>'
            f'<text clip-path="url(#l{i})" x="{x0}" y="{y}" font-family="{MONO}" font-size="16" xml:space="preserve">{tsp}</text>'
        )
    py = y0 + len(code) * lh + 10
    write("about-terminal.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="About Ruchira written as a Python class">
<defs>
  <linearGradient id="win" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset="1" stop-color="#071017"/></linearGradient>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2dd4bf"/><stop offset=".5" stop-color="#6366f1"/><stop offset="1" stop-color="#22c55e"/></linearGradient>
</defs>
<style>.cur{{animation:b 1s steps(1) infinite}}@keyframes b{{50%{{opacity:0}}}}</style>
<rect x="24" y="22" width="{W - 30}" height="{H - 26}" rx="18" fill="#0b3b38" opacity=".9"/>
<rect x="12" y="11" width="{W - 18}" height="{H - 15}" rx="18" fill="#0c2a36" opacity=".95"/>
<rect x="1" y="1" width="{W - 26}" height="{H - 26}" rx="18" fill="url(#win)" stroke="url(#edge)" stroke-width="1.5"/>
<path d="M1 46 h{W - 26}" stroke="#1e293b"/>
<circle cx="28" cy="24" r="6.5" fill="#ff5f57"/><circle cx="50" cy="24" r="6.5" fill="#febc2e"/><circle cx="72" cy="24" r="6.5" fill="#28c840"/>
<text x="{(W - 26) / 2}" y="29" fill="#64748b" font-family="{MONO}" font-size="13" text-anchor="middle">~/profile/ruchira.py — python3</text>
<g>{lines}</g>
<text x="{x0}" y="{py}" font-family="{MONO}" font-size="16" fill="#22c55e">&gt;&gt;&gt; <tspan fill="#e2e8f0">Ruchira().solve(</tspan><tspan fill="#86efac">"your problem"</tspan><tspan fill="#e2e8f0">)</tspan> <tspan class="cur" fill="#5eead4">▋</tspan></text>
</svg>""")


# ------------------------------------------------------------------ career path
def career():
    W, H = 1100, 470
    steps = [
        ("INFORMATION", "TECHNOLOGY", "#0f766e"),
        ("DATA &", "STATISTICS", "#0d9488"),
        ("ANALYTICS", "", "#0891b2"),
        ("BI · DW", "SQL · ETL", "#0284c7"),
        ("MACHINE", "LEARNING", "#6366f1"),
        ("AI", "SYSTEMS", "#8b5cf6"),
        ("REAL-WORLD", "IMPACT", "#22c55e"),
    ]
    T, yb, s = 11.0, 350, 36
    xs = [120 + i * 143 for i in range(len(steps))]
    hs = [34 + i * 27 for i in range(len(steps))]
    bars, tops = "", []
    for i, ((l1, l2, col), x, h) in enumerate(zip(steps, xs, hs)):
        d = i * 0.35
        top_y = yb - h - s / 2
        tops.append((x, top_y))
        bars += (
            f'<g class="bar" style="animation-delay:{d:.2f}s">{iso_box(x, yb, s, h, col)}</g>'
            f'<g class="lab" style="animation-delay:{d + 0.4:.2f}s">'
            f'<text x="{x}" y="{yb - h - s - 14:.0f}" fill="{shade(col, 0.45)}" font-family="{MONO}" font-size="15" font-weight="800" text-anchor="middle">0{i + 1}</text>'
            f'<text x="{x}" y="{yb + 44}" fill="#e2e8f0" font-family="{SANS}" font-size="14" font-weight="700" text-anchor="middle" letter-spacing=".8">{escape(l1)}</text>'
            f'<text x="{x}" y="{yb + 63}" fill="#94a3b8" font-family="{SANS}" font-size="14" font-weight="700" text-anchor="middle" letter-spacing=".8">{escape(l2)}</text>'
            "</g>"
        )
    path = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in tops)
    plen = sum(math.dist(tops[i], tops[i + 1]) for i in range(len(tops) - 1))
    # isometric floor grid
    grid = ""
    for k in range(0, 22):
        x = 40 + k * 48
        grid += f'<line x1="{x}" y1="{yb + 8}" x2="{x + 60}" y2="{yb - 26}"/>'
    for j in range(4):
        y = yb + 8 - j * 11.3
        grid += f'<line x1="{40 + j * 20}" y1="{y:.1f}" x2="{1040 + j * 20}" y2="{y:.1f}"/>'
    write("career-path.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Career path: Information Technology, Data and Statistics, Analytics, BI/DW/SQL/ETL, Machine Learning, AI Systems, Real-world Impact">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#030712"/><stop offset="1" stop-color="#06201f"/></linearGradient>
  <linearGradient id="trend" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2dd4bf"/><stop offset=".6" stop-color="#a78bfa"/><stop offset="1" stop-color="#4ade80"/></linearGradient>
  <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<style>
  .bar{{transform-box:fill-box;transform-origin:50% 100%;animation:grow {T}s cubic-bezier(.2,.9,.25,1) infinite}}
  @keyframes grow{{0%{{transform:scaleY(0)}}10%{{transform:scaleY(1.06)}}13%,88%{{transform:scaleY(1)}}96%,100%{{transform:scaleY(0)}}}}
  .lab{{animation:lab {T}s ease infinite}}
  @keyframes lab{{0%,6%{{opacity:0}}14%,88%{{opacity:1}}95%,100%{{opacity:0}}}}
  .trend{{stroke-dasharray:{plen:.0f};animation:draw {T}s ease-in-out infinite}}
  @keyframes draw{{0%,28%{{stroke-dashoffset:{plen:.0f}}}50%,86%{{stroke-dashoffset:0}}95%,100%{{stroke-dashoffset:{plen:.0f};opacity:0}}}}
</style>
<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>
<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="24" fill="none" stroke="#14b8a6" stroke-opacity=".3" stroke-width="1.5"/>
<text x="44" y="56" fill="#5eead4" font-family="{MONO}" font-size="14" font-weight="700" letter-spacing="4">CAREER_PATH.SVG</text>
<text x="44" y="86" fill="#f1f5f9" font-family="{SANS}" font-size="24" font-weight="800">From information technology to real-world impact</text>
<text x="{W - 44}" y="{H - 24}" fill="#64748b" font-family="{MONO}" font-size="13" text-anchor="end">growth = f(curiosity × evidence × building)</text>
<g stroke="#14b8a6" stroke-opacity=".18">{grid}</g>
{bars}
<path class="trend" d="{path}" fill="none" stroke="url(#trend)" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)"/>
<circle r="7" fill="#4ade80" filter="url(#glow)" opacity="0">
  <animateMotion dur="{T}s" repeatCount="indefinite" path="{path}" keyPoints="0;0;1;1" keyTimes="0;.3;.52;1" calcMode="linear"/>
  <animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" values="0;0;1;1;0" keyTimes="0;.28;.32;.88;.95"/>
</circle>
</svg>""")


# --------------------------------------------------------------- project cards
PROJECTS = [
    ("airiq", "AirIQ — Air Quality Forecasting", "MACHINE LEARNING · TIME-SERIES FORECASTING", "#06b6d4",
     "Live data → 33 features → Random Forest → PM2.5 (t+1)",
     "Next-hour PM2.5 forecasts for 12 Beijing stations, trained on 420K hourly records with walk-forward validation. Final hold-out R² 0.912.",
     [("Python", "#3776ab"), ("scikit-learn", "#c2410c"), ("FastAPI", "#009688"), ("React + TS", "#0e7490")]),
    ("libraai", "LibraAI — Agentic Library Desk", "AGENTIC AI · HYBRID RAG SEARCH", "#ec4899",
     "Query → Full-text + pgvector → RRF fusion → AI agent",
     "An agentic AI system that runs the library desk: answers catalog questions with hybrid retrieval, a safety policy, PII masking and audit logs.",
     [("TypeScript", "#3178c6"), ("Mastra", "#6d28d9"), ("pgvector", "#336791"), ("Claude + Gemini", "#b45309")]),
    ("patient", "Patient Satisfaction Analysis", "STATISTICAL MODELLING · HEALTHCARE", "#14b8a6",
     "Data → Statistical testing → Regression → Insights",
     "Correlation analysis, t-tests, ANOVA and multiple linear regression used to investigate the factors associated with patient satisfaction.",
     [("Python", "#3776ab"), ("R", "#276dc3"), ("Healthcare Analytics", "#0f766e")]),
    ("carsales", "Car Sales Data Warehouse & BI", "DATA WAREHOUSING · BUSINESS INTELLIGENCE", "#f59e0b",
     "Operational data → ETL → Star schema → OLAP → Dashboards",
     "A data-warehousing and business-intelligence workflow built with SQL Server, SSIS, SSAS, Excel and Power BI.",
     [("SQL Server", "#cc2927"), ("SSIS", "#742774"), ("SSAS", "#0078d4"), ("Power BI", "#b8920a")]),
    ("helamed", "Helamed Hospital Management", "FULL-STACK · HEALTHCARE SYSTEM", "#0ea5e9",
     "Patients • Doctors • Appointments • Lab • Pharmacy",
     "A full-stack healthcare system built around real-world operational workflows and role-based access control.",
     [("React", "#0e7490"), ("Node.js", "#339933"), ("MongoDB", "#47a248")]),
    ("campus", "Smart Campus Operations Hub", "FULL-STACK · REST API", "#8b5cf6",
     "Resources • Bookings • Maintenance • Dashboards • Auth",
     "A full-stack solution connecting a Spring Boot REST API with a React frontend and MongoDB Atlas.",
     [("Java 17", "#007396"), ("Spring Boot", "#4d8a2c"), ("React", "#0e7490"), ("MongoDB", "#47a248")]),
]


def card(slug, title, cat, col, pipe, desc, chips):
    W, H = 600, 320
    desc_lines = "".join(
        f'<text x="32" y="{176 + i * 23}" fill="#cbd5e1" font-family="{SANS}" font-size="15.5">{escape(l)}</text>'
        for i, l in enumerate(textwrap.wrap(desc, 62, break_on_hyphens=False))
    )
    cx, chip_svg = 32, ""
    for name, c in chips:
        w = len(name) * 7.9 + 26
        chip_svg += (
            f'<g transform="translate({cx:.0f},256)"><rect width="{w:.0f}" height="30" rx="8" fill="{c}" fill-opacity=".22" stroke="{c}"/>'
            f'<text x="{w / 2:.0f}" y="20" fill="#f1f5f9" font-family="{SANS}" font-size="13" font-weight="700" text-anchor="middle">{escape(name)}</text></g>'
        )
        cx += w + 8
    icon = (
        iso_box(530, 104, 20, 20, col)
        + f'<g class="bob">{iso_box(530, 82, 20, 20, shade(col, 0.15))}</g>'
        + f'<g class="bob2">{iso_box(504, 117, 14, 14, shade(col, -0.1))}</g>'
    )
    write(f"project-{slug}.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(title)} — {escape(desc)}">
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b1220"/><stop offset="1" stop-color="{shade(col, -0.86)}"/></linearGradient>
  <radialGradient id="halo" cx=".9" cy=".1" r=".6"><stop offset="0" stop-color="{col}" stop-opacity=".35"/><stop offset="1" stop-color="{col}" stop-opacity="0"/></radialGradient>
</defs>
<style>
  .bob{{animation:bob 4s ease-in-out infinite}}.bob2{{animation:bob 4s ease-in-out -1.5s infinite}}
  @keyframes bob{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}
  .run{{stroke-dasharray:120 1800;animation:run 6s linear infinite}}
  @keyframes run{{to{{stroke-dashoffset:-1920}}}}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="url(#bg)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="url(#halo)"/>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="none" stroke="{col}" stroke-opacity=".35" stroke-width="1.5"/>
<rect class="run" x="1" y="1" width="{W - 2}" height="{H - 2}" rx="20" fill="none" stroke="{shade(col, 0.4)}" stroke-width="2.5" stroke-linecap="round"/>
{icon}
<text x="32" y="50" fill="{shade(col, 0.35)}" font-family="{MONO}" font-size="12" font-weight="700" letter-spacing="2">{escape(cat)}</text>
<text x="32" y="88" fill="#f8fafc" font-family="{SANS}" font-size="25" font-weight="800">{escape(title)}</text>
<rect x="32" y="112" width="{len(pipe) * 7.6 + 24:.0f}" height="30" rx="8" fill="#020617" fill-opacity=".6" stroke="#1e293b"/>
<text x="44" y="132" fill="{shade(col, 0.5)}" font-family="{MONO}" font-size="12.5">{escape(pipe)}</text>
{desc_lines}
{chip_svg}
<text x="{W - 30}" y="{H - 26}" fill="#94a3b8" font-family="{MONO}" font-size="12" text-anchor="end">view repo →</text>
</svg>""")


# ---------------------------------------------------------------------- divider
def divider():
    write("divider.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 24" width="1200" height="24" role="img" aria-label="divider">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="#14b8a6" stop-opacity="0"/><stop offset=".5" stop-color="#14b8a6"/><stop offset="1" stop-color="#14b8a6" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="3"/></filter></defs>
<line x1="0" y1="12" x2="1200" y2="12" stroke="url(#g)" stroke-width="1.2" opacity=".6"/>
<g><rect y="10" width="160" height="4" rx="2" fill="#5eead4" filter="url(#glow)"/><rect y="11" width="160" height="2" rx="1" fill="#ccfbf1"/>
<animateTransform attributeName="transform" type="translate" values="-160 0;1200 0" dur="5s" repeatCount="indefinite"/></g>
<g fill="#14b8a6">{"".join(f'<rect x="{x - 4}" y="8" width="8" height="8" transform="rotate(45 {x} 12)"/>' for x in (300, 600, 900))}</g>
</svg>""")


if __name__ == "__main__":
    hero()
    terminal()
    career()
    for p in PROJECTS:
        card(*p)
    divider()
