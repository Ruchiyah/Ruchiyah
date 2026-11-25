"""Section graphics for the profile README (about bento, heading, open-sections,
hobbies, mindset). Run:  python3 scripts/generate_sections.py
Shares helpers with generate_assets.py.
"""
import math
import textwrap
from html import escape

from generate_assets import MONO, SANS, iso_box, shade, write

DEFS = """
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#030712"/><stop offset="1" stop-color="#06201f"/></linearGradient>
  <filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3.5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0" gradientUnits="objectBoundingBox">
    <stop offset="0" stop-color="#5eead4"/><stop offset=".35" stop-color="#ffffff"/><stop offset=".65" stop-color="#22c55e"/><stop offset="1" stop-color="#5eead4"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
"""

CSS = """
  .bob{animation:bob 4.5s ease-in-out infinite}
  @keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
  .pulse{animation:pulse 2.4s ease-in-out infinite}
  @keyframes pulse{0%,100%{opacity:.25}50%{opacity:1}}
  .run{stroke-dasharray:90 2400;animation:run 7s linear infinite}
  @keyframes run{to{stroke-dashoffset:-2490}}
  .flow{stroke-dasharray:6 8;animation:flow 1.2s linear infinite}
  @keyframes flow{to{stroke-dashoffset:-14}}
"""


def svg(name, W, H, label, body, css=""):
    write(name, f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(label)}">
<defs>{DEFS}</defs>
<style>{CSS}{css}</style>
{body}
</svg>""")


def tile(x, y, w, h, col, delay=0.0, rx=18):
    """Glassy tile tinted with `col`, with a light that runs around its border."""
    gid = f"t{int(x)}_{int(y)}"
    return (
        f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{shade(col, -0.78)}"/>'
        f'<stop offset="1" stop-color="#050b14"/></linearGradient>'
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{gid})"/>'
        f'<rect x="{x + .75}" y="{y + .75}" width="{w - 1.5}" height="{h - 1.5}" rx="{rx}" fill="none" stroke="{col}" stroke-opacity=".38" stroke-width="1.5"/>'
        f'<rect class="run" style="animation-delay:-{delay:.2f}s" x="{x + .75}" y="{y + .75}" width="{w - 1.5}" height="{h - 1.5}" rx="{rx}" '
        f'fill="none" stroke="{shade(col, .45)}" stroke-width="2.5" stroke-linecap="round"/>'
    )


def t(x, y, s, size=15, fill="#e2e8f0", weight=400, font=SANS, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" {extra}>{s}</text>')


def para(x, y, text, width, size=15, fill="#cbd5e1", lh=None, anchor="start", weight=400):
    lh = lh or size * 1.5
    return "".join(t(x, y + i * lh, escape(l), size, fill, weight, anchor=anchor)
                   for i, l in enumerate(textwrap.wrap(text, width)))


# =============================================================== 1. about bento
def mini_viz(kind, cx, cy, col):
    c2 = shade(col, .4)
    if kind == "degree":  # progress bar filling + cap
        return (f'<rect x="{cx - 34}" y="{cy + 18}" width="68" height="7" rx="3.5" fill="#1e293b"/>'
                f'<rect x="{cx - 34}" y="{cy + 18}" height="7" rx="3.5" fill="{col}"><animate attributeName="width" values="4;68;68;4" keyTimes="0;.6;.9;1" dur="5s" repeatCount="indefinite"/></rect>'
                f'<g class="bob"><polygon points="{cx - 26},{cy - 6} {cx},{cy - 18} {cx + 26},{cy - 6} {cx},{cy + 6}" fill="{c2}"/>'
                f'<path d="M{cx - 14},{cy} v9 q14,8 28,0 v-9" fill="{col}"/><line x1="{cx + 22}" y1="{cy - 6}" x2="{cx + 22}" y2="{cy + 10}" stroke="{c2}" stroke-width="2"/></g>')
    if kind == "location":  # radar ping
        rings = "".join(
            f'<circle cx="{cx}" cy="{cy + 6}" r="6" fill="none" stroke="{col}" stroke-width="2">'
            f'<animate attributeName="r" values="6;32" dur="2.4s" begin="-{i * .8}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="1;0" dur="2.4s" begin="-{i * .8}s" repeatCount="indefinite"/></circle>'
            for i in range(3))
        return rings + (f'<path d="M{cx},{cy + 8} c-12,-14 -12,-30 0,-30 c12,0 12,16 0,30z" fill="{c2}"/>'
                        f'<circle cx="{cx}" cy="{cy - 10}" r="4.5" fill="#030712"/>')
    if kind == "bars":
        out = ""
        for i, hh in enumerate([16, 30, 22, 40]):
            out += (f'<rect x="{cx - 34 + i * 18}" width="12" rx="2" fill="{shade(col, i * .12)}" y="{cy + 26 - hh}" height="{hh}">'
                    f'<animate attributeName="height" values="{hh};{hh * .4:.0f};{hh}" dur="{1.8 + i * .3:.1f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="y" values="{cy + 26 - hh};{cy + 26 - hh * .4:.0f};{cy + 26 - hh}" dur="{1.8 + i * .3:.1f}s" repeatCount="indefinite"/></rect>')
        return out
    if kind == "neural":
        L = [[(cx - 30, cy - 14), (cx - 30, cy + 14)], [(cx, cy - 22), (cx, cy), (cx, cy + 22)], [(cx + 30, cy)]]
        lines = "".join(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}"/>' for l1, l2 in zip(L, L[1:]) for a in l1 for b in l2)
        nodes = "".join(f'<circle cx="{p[0]}" cy="{p[1]}" r="5" fill="{c2}" class="pulse" style="animation-delay:-{(i * .35):.2f}s"/>'
                        for i, p in enumerate(p for l in L for p in l))
        return f'<g stroke="{col}" stroke-opacity=".5" stroke-width="1.3">{lines}</g>{nodes}'
    if kind == "stack":
        return "".join(f'<g class="bob" style="animation-delay:-{i * .5}s">{iso_box(cx, cy + 26 - i * 16, 22, 8, shade(col, i * .15))}</g>' for i in range(3))
    if kind == "status":
        return (f'<circle cx="{cx}" cy="{cy}" r="10" fill="{col}" filter="url(#glow)"/>'
                f'<circle cx="{cx}" cy="{cy}" r="10" fill="none" stroke="{col}" stroke-width="2">'
                f'<animate attributeName="r" values="10;28" dur="1.8s" repeatCount="indefinite"/><animate attributeName="opacity" values=".9;0" dur="1.8s" repeatCount="indefinite"/></circle>')
    return ""


def about_bento():
    W, H = 1200, 560
    big = tile(0, 0, 584, H, "#14b8a6", 0)
    loop = ["UNDERSTAND", "BUILD", "TEST", "IMPROVE"]
    loop_svg, lx = "", 40
    for i, word in enumerate(loop):
        w = len(word) * 8.2 + 26
        loop_svg += (f'<rect x="{lx}" y="358" width="{w:.0f}" height="30" rx="15" fill="#0b1220" stroke="#14b8a6" stroke-opacity=".6"/>'
                     f'<rect x="{lx}" y="358" width="{w:.0f}" height="30" rx="15" fill="#14b8a6" opacity="0">'
                     f'<animate attributeName="opacity" values="0;.35;0;0" keyTimes="0;.08;.25;1" dur="4s" begin="{i}s" repeatCount="indefinite"/></rect>'
                     + t(lx + w / 2, 378, word, 12.5, "#99f6e4", 700, MONO, "middle", 'letter-spacing="1"'))
        lx += w
        if i < 3:
            loop_svg += t(lx + 13, 378, "→", 15, "#475569", 700, anchor="middle")
            lx += 26
    body = big + (
        t(40, 56, "$ whoami", 15, "#5eead4", 700, MONO, extra='letter-spacing="2"')
        + t(38, 122, "I'm Ruchira", 58, "url(#shine)", 800, extra='letter-spacing="-1"')
        + t(40, 160, "IT undergraduate  ·  data-science minded  ·  builder", 15, "#94a3b8", 400, MONO)
        + '<text x="40" y="214" font-family="' + SANS + '" font-size="19" fill="#cbd5e1">I enjoy the point where <tspan fill="#5eead4" font-weight="700">data becomes a decision</tspan></text>'
        + '<text x="40" y="243" font-family="' + SANS + '" font-size="19" fill="#cbd5e1">and where <tspan fill="#a78bfa" font-weight="700">a messy idea becomes a working system.</tspan></text>'
        + t(40, 290, "I'm not trying to collect technologies", 16, "#64748b", 400, extra='font-style="italic"')
        + t(40, 313, "just to make a longer list.", 16, "#64748b", 400, extra='font-style="italic"')
        + loop_svg
        + '<rect x="40" y="420" width="504" height="100" rx="14" fill="#0b1220" stroke="#1e293b"/>'
        + '<rect x="40" y="420" width="5" height="100" rx="2.5" fill="#22c55e" filter="url(#glow)"/>'
        + t(66, 460, "I want to understand things deeply,", 19, "#f8fafc", 700)
        + t(66, 490, "build them, test them, and keep improving.", 19, "#f8fafc", 700)
        + "".join(f'<g class="bob" style="animation-delay:-{d}s">{iso_box(x, y, s, s, c)}</g>'
                  for x, y, s, c, d in [(500, 70, 22, "#14b8a6", 0), (530, 120, 14, "#6366f1", 1.2), (470, 128, 12, "#22c55e", 2)])
    )
    tiles = [
        ("🎓", "DEGREE", "BSc (Hons)", "Information Technology", "#0ea5e9", "degree"),
        ("📍", "BASED AT", "SLIIT", "Sri Lanka", "#f43f5e", "location"),
        ("📊", "FOCUS", "Data Science", "stats · EDA · modelling", "#14b8a6", "bars"),
        ("🧠", "INTERESTED IN", "AI · ML", "& analytics", "#8b5cf6", "neural"),
        ("💻", "ALSO BUILDS", "Full-stack apps", "React · Node · Spring", "#f59e0b", "stack"),
        ("⚡", "STATUS", "Learning", "& shipping, always", "#22c55e", "status"),
    ]
    tw, th, gap = 292, 176, 16
    for i, (emo, lab, val, sub, col, kind) in enumerate(tiles):
        x, y = 600 + (i % 2) * (tw + gap), (i // 2) * (th + gap)
        body += (tile(x, y, tw, th, col, i * 1.1)
                 + t(x + 24, y + 52, emo, 30)
                 + t(x + 24, y + 92, lab, 12, shade(col, .4), 700, MONO, extra='letter-spacing="2"')
                 + t(x + 24, y + 124, escape(val), 24, "#f8fafc", 800)
                 + t(x + 24, y + 150, escape(sub), 14, "#94a3b8")
                 + mini_viz(kind, x + tw - 62, y + 52, col))
    svg("about-bento.svg", W, H, "About Ruchira: BSc (Hons) IT at SLIIT, Sri Lanka; focused on Data Science; interested in AI, ML and analytics; also builds full-stack apps. I want to understand things deeply, build them, test them, and keep improving.", body)


# ============================================================ 2. where heading
def heading():
    W, H = 1200, 640
    cards = [
        ("📊", "DATA SCIENCE", "Understand the data", "#14b8a6", ["Statistics", "EDA", "Visualization", "Predictive modelling", "Evaluation"], "bars"),
        ("🤖", "AI &amp; ML", "Turn patterns into intelligence", "#8b5cf6", ["Machine Learning", "AI", "Model development", "Experimentation"], "neural"),
        ("⚙️", "DATA + SOFTWARE", "Turn ideas into systems", "#f59e0b", ["Data Engineering", "APIs", "Databases", "BI", "Full-stack"], "stack"),
    ]
    body = (f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>'
            f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="24" fill="none" stroke="#14b8a6" stroke-opacity=".3" stroke-width="1.5"/>'
            + t(40, 54, "WHERE_IM_HEADING", 14, "#5eead4", 700, MONO, extra='letter-spacing="4"')
            + t(40, 88, "Three directions. One destination: real-world impact.", 26, "#f8fafc", 800))
    cw, ch, cy = 357, 300, 118
    py = 530
    for i, (emo, title, tag, col, chips, viz) in enumerate(cards):
        x = 40 + i * (cw + 24)
        body += (tile(x, cy, cw, ch, col, i * 2)
                 + f'<circle cx="{x + 52}" cy="{cy + 56}" r="28" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".5"/>'
                 + t(x + 52, cy + 67, emo, 28, anchor="middle")
                 + mini_viz(viz, x + cw - 64, cy + 52, col)
                 + t(x + 26, cy + 122, title, 22, "#f8fafc", 800, extra='letter-spacing=".5"')
                 + t(x + 26, cy + 150, tag, 15, shade(col, .45), 700))
        cx, cyy = x + 26, cy + 180
        for c in chips:
            w = len(c) * 7.6 + 22
            if cx + w > x + cw - 20:
                cx, cyy = x + 26, cyy + 38
            body += (f'<rect x="{cx:.0f}" y="{cyy}" width="{w:.0f}" height="28" rx="8" fill="{col}" fill-opacity=".14" stroke="{col}" stroke-opacity=".55"/>'
                     + t(cx + w / 2, cyy + 19, escape(c), 13, "#e2e8f0", 600, anchor="middle"))
            cx += w + 8
        # flowing connector down to the pipeline
        body += f'<path class="flow" d="M{x + cw / 2},{cy + ch} V{py - 8}" stroke="{col}" stroke-width="2" fill="none" opacity=".7"/>'
    steps = [("01", "Understand", "#0f766e"), ("02", "Analyse", "#2563eb"), ("03", "Model", "#7c3aed"), ("04", "Build", "#ea580c"), ("05", "Impact", "#16a34a")]
    x0, step = 140, 230
    body += (f'<line x1="{x0}" y1="{py}" x2="{x0 + 4 * step}" y2="{py}" stroke="#1e293b" stroke-width="6" stroke-linecap="round"/>'
             f'<line x1="{x0}" y1="{py}" x2="{x0 + 4 * step}" y2="{py}" stroke="url(#shine)" stroke-width="3" stroke-linecap="round" opacity=".8"/>')
    T = 6.0
    for i, (n, lab, col) in enumerate(steps):
        x = x0 + i * step
        k = i / 4 * 0.8
        body += (f'<circle cx="{x}" cy="{py}" r="26" fill="#0b1220" stroke="{col}" stroke-width="3"/>'
                 f'<circle cx="{x}" cy="{py}" r="26" fill="{col}" opacity=".25">'
                 f'<animate attributeName="opacity" values=".25;.25;1;.25;.25" keyTimes="0;{max(k - .02, 0):.3f};{k + .04:.3f};{min(k + .16, .99):.3f};1" dur="{T}s" repeatCount="indefinite"/></circle>'
                 + t(x, py + 6, n, 16, "#f8fafc", 800, MONO, "middle")
                 + t(x, py + 56, lab.upper(), 14, shade(col, .5), 800, anchor="middle", extra='letter-spacing="1.5"'))
    body += (f'<circle r="7" cy="{py}" fill="#ffffff" filter="url(#glow)"><animate attributeName="cx" values="{x0};{x0 + 4 * step};{x0 + 4 * step}" keyTimes="0;.8;1" dur="{T}s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values="1;1;0" keyTimes="0;.8;.85" dur="{T}s" repeatCount="indefinite"/></circle>')
    svg("heading.svg", W, H, "Where I'm heading: Data Science, AI & ML, and Data + Software, through Understand, Analyse, Model, Build, Impact", body)


# ========================================================== 3. open sections
def bring():
    W, H = 1000, 250
    items = [("📊", "DATA", "Cleaning, statistical analysis, visualization and BI", "#14b8a6"),
             ("🛠️", "ENGINEERING", "APIs, databases and full-stack development", "#0ea5e9"),
             ("🧩", "PROBLEM SOLVING", "Breaking requirements into practical, testable solutions", "#8b5cf6"),
             ("🌱", "MINDSET", "Evidence first, learn continuously, iterate quickly", "#22c55e")]
    body, w = "", 238
    for i, (emo, lab, desc, col) in enumerate(items):
        x = i * (w + 16)
        body += (tile(x, 0, w, H, col, i * 1.6)
                 + f'<g class="bob" style="animation-delay:-{i * .7}s"><circle cx="{x + 44}" cy="56" r="26" fill="{col}" fill-opacity=".16" stroke="{col}" stroke-opacity=".6"/>'
                 + t(x + 44, 66, emo, 26, anchor="middle") + "</g>"
                 + t(x + 22, 120, lab, 14, shade(col, .45), 800, MONO, extra='letter-spacing="2"')
                 + para(x + 22, 152, desc, 26, 15.5, "#e2e8f0", 23))
    svg("bring.svg", W, H, "What I bring: data, engineering, problem solving, mindset", body)


def flow_loop():
    W, H = 1000, 560
    cx, cy, rx, ry = 500, 290, 255, 190
    steps = ["Problem", "Understand the context", "Collect / prepare data", "Analyse patterns",
             "Model / engineer", "Build the solution", "Explain the evidence", "Improve the next version"]
    cols = ["#f43f5e", "#14b8a6", "#0ea5e9", "#2563eb", "#7c3aed", "#ea580c", "#f59e0b", "#22c55e"]
    T = 12.0
    path = f"M{cx},{cy - ry} A{rx},{ry} 0 1,1 {cx},{cy + ry} A{rx},{ry} 0 1,1 {cx},{cy - ry}"
    body = (f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>'
            f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="24" fill="none" stroke="#14b8a6" stroke-opacity=".3" stroke-width="1.5"/>'
            + t(32, 46, "PROBLEM_SOLVING.LOOP", 13, "#5eead4", 700, MONO, extra='letter-spacing="3"')
            + "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx * f:.0f}" ry="{ry * f:.0f}" fill="none" stroke="#14b8a6" stroke-opacity="{.08 + f * .1:.2f}"/>' for f in (.35, .6, .8))
            + f'<ellipse class="flow" cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" stroke="url(#shine)" stroke-width="2.5"/>'
            + f'<g class="bob">{iso_box(cx, cy + 30, 44, 44, "#14b8a6")}</g>'
            + t(cx, cy + 82, "EVIDENCE-DRIVEN", 13, "#99f6e4", 800, MONO, "middle", 'letter-spacing="3"')
            + t(cx, cy + 102, "repeat until it's useful", 13, "#64748b", 400, MONO, "middle"))
    for i, (lab, col) in enumerate(zip(steps, cols)):
        a = -math.pi / 2 + i * 2 * math.pi / len(steps)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        k = i / len(steps)
        right = math.cos(a) > 0.2
        left = math.cos(a) < -0.2
        anchor = "start" if right else "end" if left else "middle"
        lx = x + (24 if right else -24 if left else 0)
        ly = y + (5 if (right or left) else (-26 if math.sin(a) < 0 else 38))
        body += (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17" fill="#0b1220" stroke="{col}" stroke-width="2.5"/>'
                 f'<circle cx="{x:.1f}" cy="{y:.1f}" r="17" fill="{col}" opacity=".2">'
                 f'<animate attributeName="opacity" values=".2;1;.2;.2" keyTimes="0;.04;.16;1" dur="{T}s" begin="{k * T:.2f}s" repeatCount="indefinite"/></circle>'
                 + t(f"{x:.1f}", f"{y + 5:.1f}", i + 1, 13, "#fff", 800, MONO, "middle")
                 + f'<rect x="{(lx - (len(lab) * 7.6 + 20 if anchor == "end" else (len(lab) * 3.8 + 10 if anchor == "middle" else 0))):.1f}" y="{ly - 20:.1f}" '
                   f'width="{len(lab) * 7.6 + 20:.0f}" height="30" rx="9" fill="#0b1220" fill-opacity=".85" stroke="{col}" stroke-opacity=".5"/>'
                 + t(f"{lx + (10 if anchor == 'start' else -10 if anchor == 'end' else 0):.1f}", f"{ly:.1f}", escape(lab), 15, "#f1f5f9", 700, anchor=anchor))
    body += (f'<circle r="8" fill="#ffffff" filter="url(#glow)"><animateMotion dur="{T}s" repeatCount="indefinite" path="{path}"/></circle>')
    svg("flow-loop.svg", W, H, "Problem-solving loop: Problem, understand the context, collect and prepare data, analyse patterns, model and engineer, build the solution, explain the evidence, improve the next version", body)


def direction():
    W, H = 1000, 300
    cx, cy = 170, 160
    rings = "".join(
        f'<ellipse cx="{cx}" cy="{cy + i * 0}" rx="{120 - i * 28}" ry="{(120 - i * 28) * .45:.0f}" fill="{c}" fill-opacity=".18" stroke="{c}" stroke-width="2"/>'
        for i, c in enumerate(["#0f766e", "#0ea5e9", "#8b5cf6", "#22c55e"]))
    route = ["Raw data", "Statistical reasoning", "Machine learning", "Software engineering", "Real-world systems"]
    chips, x, y = "", 340, 186
    for i, r in enumerate(route):
        w = len(r) * 7.8 + 24
        if x + w > W - 30:
            x, y = 340, y + 44
        chips += (f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="#0b1220" stroke="#14b8a6" stroke-opacity=".6"/>'
                  f'<rect x="{x:.0f}" y="{y}" width="{w:.0f}" height="30" rx="15" fill="#14b8a6" opacity="0"><animate attributeName="opacity" values="0;.4;0;0" keyTimes="0;.06;.2;1" dur="6s" begin="{i * 1.1:.1f}s" repeatCount="indefinite"/></rect>'
                  + t(x + w / 2, y + 20, r, 13.5, "#ccfbf1", 700, anchor="middle"))
        x += w
        if i < len(route) - 1:
            chips += t(x + 12, y + 21, "→", 15, "#475569", 700, anchor="middle")
            x += 24
    body = (f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>'
            f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="24" fill="none" stroke="#14b8a6" stroke-opacity=".3" stroke-width="1.5"/>'
            + rings
            + f'<ellipse cx="{cx}" cy="{cy}" rx="10" ry="5" fill="none" stroke="#5eead4" stroke-width="2"><animate attributeName="rx" values="10;130" dur="2.6s" repeatCount="indefinite"/>'
              f'<animate attributeName="ry" values="5;58" dur="2.6s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;0" dur="2.6s" repeatCount="indefinite"/></ellipse>'
            + f'<g><line x1="{cx}" y1="{cy}" x2="{cx + 70}" y2="{cy - 110}" stroke="#f8fafc" stroke-width="3"/><polygon points="{cx + 70},{cy - 110} {cx + 82},{cy - 118} {cx + 74},{cy - 98}" fill="#f43f5e"/>'
              f'<circle cx="{cx}" cy="{cy}" r="6" fill="#f43f5e" filter="url(#glow)"/>'
              f'<animateTransform attributeName="transform" type="translate" values="40 -40;0 0;0 0;0 -4;0 0" keyTimes="0;.15;.6;.65;1" dur="5s" repeatCount="indefinite"/></g>'
            + t(340, 60, "LONG_TERM_DIRECTION", 13, "#5eead4", 700, MONO, extra='letter-spacing="3"')
            + '<text x="340" y="104" font-family="' + SANS + '" font-size="28" font-weight="800" fill="#f8fafc">Data Scientist <tspan fill="#64748b">/</tspan> <tspan fill="url(#shine)">AI-focused technologist</tspan></text>'
            + t(340, 140, "Moving comfortably from raw data and statistical reasoning", 16, "#94a3b8")
            + t(340, 163, "to machine learning, software and useful real-world systems.", 16, "#94a3b8")
            + chips)
    svg("direction.svg", W, H, "Long-term direction: grow into a Data Scientist / AI-focused technologist", body)


# ================================================================= 4. hobbies
def hobbies():
    W, H = 1200, 380
    tw, gap = 288, 16
    items = [
        ("Guitar", "One of my favourite ways to switch off.", "#f59e0b"),
        ("Mystery stories", "Stories that make me question what is actually going on.", "#8b5cf6"),
        ("Games with friends", "Because not every problem needs a terminal.", "#f43f5e"),
        ("Technology", "I end up exploring tools and ideas I don't fully understand yet.", "#14b8a6"),
    ]
    body = ""
    for i, (title, desc, col) in enumerate(items):
        x = i * (tw + gap)
        mx, my = x + tw / 2, 100
        c2 = shade(col, .4)
        body += tile(x, 0, tw, H, col, i * 1.7)
        body += f'<rect x="{x + 16}" y="16" width="{tw - 32}" height="170" rx="12" fill="#020617" fill-opacity=".55"/>'
        if i == 0:  # vibrating strings + notes
            for s in range(6):
                yy = 84 + s * 15
                body += (f'<path d="M{x + 36},{yy} Q{mx},{yy} {x + tw - 36},{yy}" stroke="{shade(col, s * .08)}" stroke-width="{2.4 - s * .3:.1f}" fill="none">'
                         f'<animate attributeName="d" dur="{.18 + s * .03:.2f}s" repeatCount="indefinite" values="M{x + 36},{yy} Q{mx},{yy - 5} {x + tw - 36},{yy};M{x + 36},{yy} Q{mx},{yy + 5} {x + tw - 36},{yy};M{x + 36},{yy} Q{mx},{yy - 5} {x + tw - 36},{yy}"/></path>')
            for k, (nx, n) in enumerate([(x + 70, "♪"), (x + 150, "♫"), (x + 220, "♩")]):
                body += (f'<text x="{nx}" y="160" fill="{c2}" font-size="26" font-family="{SANS}">{n}'
                         f'<animate attributeName="y" values="175;40" dur="3s" begin="-{k}s" repeatCount="indefinite"/>'
                         f'<animate attributeName="opacity" values="0;1;0" dur="3s" begin="-{k}s" repeatCount="indefinite"/></text>')
            body += t(x + 34, 64, "🎸", 26)
        elif i == 1:  # clue lines + sweeping magnifier
            for r in range(5):
                body += f'<rect x="{x + 40}" y="{50 + r * 24}" width="{[180, 140, 200, 120, 160][r]}" height="7" rx="3.5" fill="#334155"/>'
            body += t(x + 200, 128, "?", 34, c2, 800, extra='class="pulse"')
            body += (f'<g><circle cx="0" cy="0" r="26" fill="{col}" fill-opacity=".18" stroke="{c2}" stroke-width="4"/>'
                     f'<line x1="18" y1="18" x2="40" y2="40" stroke="{c2}" stroke-width="7" stroke-linecap="round"/>'
                     f'<animateMotion dur="6s" repeatCount="indefinite" path="M{x + 80},70 C{x + 220},60 {x + 230},140 {x + 120},140 S{x + 40},80 {x + 80},70"/></g>')
        elif i == 2:  # controller + XP pops + pixels
            body += t(mx, 128, "🎮", 64, anchor="middle")
            for k, (dx, txt) in enumerate([(-80, "+1 XP"), (70, "GG!"), (0, "WIN")]):
                body += (f'<text x="{mx + dx}" y="70" fill="{c2}" font-family="{MONO}" font-size="15" font-weight="800" text-anchor="middle" opacity="0">{txt}'
                         f'<animate attributeName="y" values="100;44" dur="2.7s" begin="{k * .9}s" repeatCount="indefinite"/>'
                         f'<animate attributeName="opacity" values="0;1;0" dur="2.7s" begin="{k * .9}s" repeatCount="indefinite"/></text>')
            for k in range(6):
                body += f'<rect x="{x + 36 + k * 40}" y="168" width="8" height="8" fill="{col}" class="pulse" style="animation-delay:-{k * .3:.1f}s"/>'
        else:  # atom
            for k, ang in enumerate((0, 60, 120)):
                body += (f'<g transform="rotate({ang} {mx} {my})"><ellipse cx="{mx}" cy="{my}" rx="70" ry="24" fill="none" stroke="{col}" stroke-opacity=".7" stroke-width="1.6"/>'
                         f'<circle r="5" fill="{c2}" filter="url(#glow)"><animateMotion dur="{2.2 + k * .5:.1f}s" repeatCount="indefinite" '
                         f'path="M{mx + 70},{my} A70,24 0 1,1 {mx - 70},{my} A70,24 0 1,1 {mx + 70},{my}"/></circle></g>')
            body += f'<circle cx="{mx}" cy="{my}" r="11" fill="{c2}" filter="url(#glow)" class="pulse"/>'
        body += (t(x + 24, 230, escape(title), 22, "#f8fafc", 800)
                 + f'<rect x="{x + 24}" y="244" width="40" height="3" rx="1.5" fill="{col}"/>'
                 + para(x + 24, 280, desc, 30, 15.5, "#cbd5e1", 23))
    svg("hobbies.svg", W, H, "Outside the code: guitar, mystery stories, games with friends, technology", body)


# ================================================================= 5. mindset
def mindset():
    W, H = 1200, 330
    items = [("?", "Curiosity", "ask better questions", "#14b8a6"),
             ("Σ", "Evidence", "don't trust assumptions blindly", "#0ea5e9"),
             ("&lt;/&gt;", "Building", "learn by doing", "#8b5cf6"),
             ("!", "Failure", "debug, don't panic", "#f43f5e"),
             ("↑", "Improvement", "make the next version better", "#22c55e")]
    step, x0, cy, R = 240, 120, 128, 58

    def hexagon(cx, cy, r):
        return " ".join(f"{cx + r * math.cos(math.radians(60 * k - 90)):.1f},{cy + r * math.sin(math.radians(60 * k - 90)):.1f}" for k in range(6))

    body = (f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>'
            f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="24" fill="none" stroke="#14b8a6" stroke-opacity=".3" stroke-width="1.5"/>')
    for i in range(4):
        body += (f'<line x1="{x0 + i * step + R}" y1="{cy}" x2="{x0 + (i + 1) * step - R}" y2="{cy}" stroke="#1e293b" stroke-width="4"/>'
                 f'<line class="flow" x1="{x0 + i * step + R}" y1="{cy}" x2="{x0 + (i + 1) * step - R}" y2="{cy}" stroke="{items[i][3]}" stroke-width="2.5"/>'
                 + t(x0 + i * step + step / 2, cy - 10, "→", 18, "#475569", 700, anchor="middle"))
    for i, (glyph, word, act, col) in enumerate(items):
        x = x0 + i * step
        body += (f'<polygon points="{hexagon(x + 6, cy + 8, R)}" fill="{shade(col, -.7)}" opacity=".8"/>'
                 f'<g class="bob" style="animation-delay:-{i * .6}s"><polygon points="{hexagon(x, cy, R)}" fill="#0b1220" stroke="{col}" stroke-width="2.5"/>'
                 f'<polygon points="{hexagon(x, cy, R - 10)}" fill="{col}" fill-opacity=".14"/>')
        if word == "Failure":  # ERR -> FIXED
            body += (f'<g><polygon points="{hexagon(x, cy, R - 10)}" fill="#f43f5e" fill-opacity=".3"/>'
                     + t(x, cy + 6, "ERR", 20, "#fecdd3", 800, MONO, "middle")
                     + f'<animate attributeName="opacity" values="1;.2;1;.3;1;1;0;0" keyTimes="0;.05;.1;.15;.2;.5;.52;1" dur="5s" repeatCount="indefinite"/></g>'
                     + f'<g opacity="0"><polygon points="{hexagon(x, cy, R - 10)}" fill="#22c55e" fill-opacity=".3"/>'
                     + t(x, cy + 13, "✓", 34, "#bbf7d0", 800, anchor="middle")
                     + '<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.5;.54;.97;1" dur="5s" repeatCount="indefinite"/></g>')
        else:
            body += t(x, cy + 11, glyph, 30 if len(glyph) == 1 else 22, shade(col, .55), 800, MONO, "middle")
        body += "</g>"
        body += (t(x, cy + 100, word.upper(), 16, "#f8fafc", 800, anchor="middle", extra='letter-spacing="1.5"')
                 + para(x, cy + 128, act, 22, 14.5, shade(col, .45), 21, "middle", 600))
    svg("mindset.svg", W, H, "My working mindset: Curiosity asks better questions; Evidence, don't trust assumptions blindly; Building, learn by doing; Failure, debug don't panic; Improvement, make the next version better", body)


# =========================================================== 0. what I'm into
def into_player():
    """A music-player take on 'What am I into?' — each interest is a track."""
    W, H, T = 1200, 600, 12.0
    vx, vy, vr = 280, 280, 200
    tracks = [
        ("📊", "DATA", "Statistics · Analytics · Visualization · BI", "3:14", ("#f472b6", "#fb923c")),
        ("🤖", "AI", "Machine Learning · Predictive Models · AI Exploration", "1:01", ("#a78bfa", "#f472b6")),
        ("💻", "BUILD", "Web Apps · REST APIs · Databases · System Design", "2:00", ("#fb923c", "#facc15")),
        ("🧠", "LEARN", "Experiment · Question · Improve · Repeat", "∞", ("#34d399", "#22d3ee")),
    ]
    slot = T / len(tracks)

    def active(i, on="1", off="0"):
        return (f'<animate attributeName="opacity" values="{off};{on};{on};{off};{off}" '
                f'keyTimes="0;.02;{1 / len(tracks) - .02:.3f};{1 / len(tracks):.3f};1" dur="{T}s" begin="{i * slot:.1f}s" repeatCount="indefinite"/>')

    defs = (
        '<linearGradient id="pbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1a0b24"/><stop offset=".55" stop-color="#2a0f2e"/><stop offset="1" stop-color="#3a1512"/></linearGradient>'
        '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="60"/></filter>'
        '<linearGradient id="wave" x1="0" x2="1"><stop offset="0" stop-color="#f472b6"/><stop offset="1" stop-color="#fb923c"/></linearGradient>'
        '<radialGradient id="disc" cx=".5" cy=".5" r=".5"><stop offset=".3" stop-color="#18181b"/><stop offset=".95" stop-color="#09090b"/><stop offset="1" stop-color="#27272a"/></radialGradient>'
        + "".join(f'<linearGradient id="lab{i}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
                  for i, (*_, (a, b)) in enumerate(tracks))
    )
    grooves = "".join(f'<circle cx="{vx}" cy="{vy}" r="{r}" fill="none" stroke="#3f3f46" stroke-opacity="{.25 + (r % 3) * .12:.2f}" stroke-width=".8"/>'
                      for r in range(78, vr - 6, 5))
    labels = "".join(f'<circle cx="{vx}" cy="{vy}" r="66" fill="url(#lab{i})" opacity="{1 if i == 0 else 0}">{active(i)}</circle>' for i in range(len(tracks)))
    body = (
        f'<defs>{defs}</defs>'
        f'<rect width="{W}" height="{H}" rx="28" fill="url(#pbg)"/>'
        f'<g filter="url(#blur)" opacity=".55"><circle cx="300" cy="260" r="200" fill="#db2777"/><circle cx="1000" cy="520" r="180" fill="#ea580c"/><circle cx="900" cy="80" r="140" fill="#7c3aed"/></g>'
        f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="28" fill="none" stroke="#f472b6" stroke-opacity=".3" stroke-width="1.5"/>'
        # vinyl
        f'<circle cx="{vx + 8}" cy="{vy + 14}" r="{vr}" fill="#000" opacity=".45"/>'
        f'<g><circle cx="{vx}" cy="{vy}" r="{vr}" fill="url(#disc)"/>{grooves}{labels}'
        f'<text x="{vx}" y="{vy - 8}" fill="#fff" font-family="{SANS}" font-size="19" font-weight="900" text-anchor="middle" letter-spacing="3">RUCHIRA</text>'
        f'<text x="{vx}" y="{vy + 14}" fill="#fff" fill-opacity=".85" font-family="{MONO}" font-size="10" text-anchor="middle" letter-spacing="2">VOL.01 · INTERESTS</text>'
        f'<text x="{vx}" y="{vy + 36}" fill="#fff" fill-opacity=".7" font-family="{MONO}" font-size="9" text-anchor="middle">SIDE A</text>'
        f'<circle cx="{vx}" cy="{vy}" r="6" fill="#09090b"/>'
        f'<animateTransform attributeName="transform" type="rotate" from="0 {vx} {vy}" to="360 {vx} {vy}" dur="4s" repeatCount="indefinite"/></g>'
        # static sheen
        f'<path d="M{vx},{vy} L{vx - 120},{vy - 160} A{vr},{vr} 0 0,1 {vx - 30},{vy - vr + 2} Z" fill="#fff" opacity=".06"/>'
        f'<path d="M{vx},{vy} L{vx + 120},{vy + 160} A{vr},{vr} 0 0,1 {vx + 30},{vy + vr - 2} Z" fill="#fff" opacity=".05"/>'
        # tonearm
        f'<g><circle cx="478" cy="92" r="22" fill="#27272a" stroke="#52525b" stroke-width="2"/><circle cx="478" cy="92" r="8" fill="#a1a1aa"/>'
        f'<path d="M478,92 L470,250 L404,334" fill="none" stroke="#d4d4d8" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>'
        f'<rect x="386" y="326" width="34" height="20" rx="4" fill="#a1a1aa" transform="rotate(-50 403 336)"/>'
        f'<animateTransform attributeName="transform" type="rotate" values="0 478 92;1.6 478 92;0 478 92" dur="2.6s" repeatCount="indefinite"/></g>'
    )
    # controls under the vinyl
    cy_c = 548
    body += (
        f'<g fill="#e4e4e7" opacity=".75">'
        f'<path d="M{vx - 150},{cy_c - 7} h8 l14,14 h8 M{vx - 150},{cy_c + 7} h8 l14,-14 h8" stroke="#e4e4e7" stroke-width="2.4" fill="none"/>'
        f'<polygon points="{vx - 62},{cy_c} {vx - 46},{cy_c - 10} {vx - 46},{cy_c + 10}"/><rect x="{vx - 66}" y="{cy_c - 10}" width="4" height="20"/>'
        f'<polygon points="{vx + 62},{cy_c} {vx + 46},{cy_c - 10} {vx + 46},{cy_c + 10}"/><rect x="{vx + 62}" y="{cy_c - 10}" width="4" height="20"/>'
        f'<path d="M{vx + 124},{cy_c - 4} a10,10 0 0,1 10,-6 h14 M{vx + 152},{cy_c + 4} a10,10 0 0,1 -10,6 h-14" stroke="#e4e4e7" stroke-width="2.4" fill="none"/>'
        f'<polygon points="{vx + 144},{cy_c - 14} {vx + 150},{cy_c - 10} {vx + 144},{cy_c - 6}"/></g>'
        f'<circle cx="{vx}" cy="{cy_c}" r="30" fill="#fafafa"/>'
        f'<g fill="#18181b"><rect x="{vx - 9}" y="{cy_c - 11}" width="6" height="22" rx="1.5"/><rect x="{vx + 3}" y="{cy_c - 11}" width="6" height="22" rx="1.5"/></g>'
        f'<circle cx="{vx}" cy="{cy_c}" r="30" fill="none" stroke="#fafafa" stroke-width="2"><animate attributeName="r" values="30;44" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".6;0" dur="2s" repeatCount="indefinite"/></circle>'
    )
    # header
    rx0 = 560
    body += (
        f'<text x="{rx0}" y="74" fill="#f9a8d4" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="4">♫ NOW PLAYING</text>'
        f'<text x="{rx0 - 3}" y="128" fill="#fff" font-family="{SANS}" font-size="50" font-weight="900" letter-spacing="-1.5">What I\'m into</text>'
    )
    for i, (emo, name, *_rest) in enumerate(tracks):
        body += (f'<text x="{rx0}" y="160" fill="#fda4af" font-family="{SANS}" font-size="16" font-weight="600" opacity="{1 if i == 0 else 0}">'
                 f'Ruchira · Track 0{i + 1} — {name} · on repeat{active(i)}</text>')
    # tracklist
    ty, rh = 186, 70
    for i, (emo, name, sub, dur, (a, b)) in enumerate(tracks):
        y = ty + i * rh
        eq = "".join(
            f'<rect x="{rx0 + 8 + k * 6}" width="4" rx="1" fill="{a}" y="{y + 26}" height="16">'
            f'<animate attributeName="height" values="4;18;8;14;4" dur="{.7 + k * .17:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{y + 40};{y + 26};{y + 36};{y + 30};{y + 40}" dur="{.7 + k * .17:.2f}s" repeatCount="indefinite"/></rect>'
            for k in range(4))
        body += (
            f'<rect x="{rx0 - 14}" y="{y + 4}" width="{W - rx0 - 26}" height="{rh - 8}" rx="14" fill="#fff" opacity="{.1 if i == 0 else 0}">{active(i, ".1")}</rect>'
            f'<rect x="{rx0 - 14}" y="{y + 4}" width="4" height="{rh - 8}" rx="2" fill="{a}" opacity="{1 if i == 0 else 0}">{active(i)}</rect>'
            f'<text x="{rx0 + 18}" y="{y + 42}" fill="#a1a1aa" font-family="{MONO}" font-size="15" text-anchor="middle" opacity="{0 if i == 0 else 1}">{i + 1}{active(i, "0", "1")}</text>'
            f'<g opacity="{1 if i == 0 else 0}">{eq}{active(i)}</g>'
            f'<rect x="{rx0 + 48}" y="{y + 13}" width="44" height="44" rx="8" fill="url(#lab{i})"/>'
            f'<text x="{rx0 + 70}" y="{y + 44}" font-size="22" text-anchor="middle">{emo}</text>'
            f'<text x="{rx0 + 108}" y="{y + 32}" fill="#fff" font-family="{SANS}" font-size="18" font-weight="800" letter-spacing="1">{name}</text>'
            f'<text x="{rx0 + 108}" y="{y + 53}" fill="#d4d4d8" font-family="{SANS}" font-size="14">{escape(sub)}</text>'
            f'<text x="{W - 56}" y="{y + 42}" fill="#a1a1aa" font-family="{MONO}" font-size="14" text-anchor="end">{dur}</text>'
        )
    # soundwave progress
    wy, n, wx0, wx1 = 508, 84, rx0, W - 56
    bw = (wx1 - wx0) / n
    bars = "".join(
        f'<rect x="{wx0 + k * bw:.1f}" y="{wy - h / 2:.1f}" width="{bw * .55:.1f}" height="{h:.1f}" rx="1.5"/>'
        for k, h in enumerate(8 + 26 * abs(math.sin(k * .45) * math.cos(k * .13)) + 6 * ((k * 7) % 3) for k in range(n)))
    body += (
        f'<clipPath id="played"><rect x="{wx0}" y="{wy - 30}" height="60" width="0"><animate attributeName="width" values="0;{wx1 - wx0}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>'
        f'<g fill="#52525b">{bars}</g><g fill="url(#wave)" clip-path="url(#played)">{bars}</g>'
        f'<text x="{wx0}" y="{wy + 46}" fill="#a1a1aa" font-family="{MONO}" font-size="12">learning…</text>'
        f'<text x="{wx1}" y="{wy + 46}" fill="#a1a1aa" font-family="{MONO}" font-size="12" text-anchor="end">∞ on repeat</text>'
    )
    svg("into-player.svg", W, H, "What I'm into, as a music player: Track 1 DATA — statistics, analytics, visualization, business intelligence; Track 2 AI — machine learning, predictive models, AI exploration; Track 3 BUILD — web apps, REST APIs, databases, system design; Track 4 LEARN — experiment, question, improve, repeat", body)


# ================================================================= contact
def contact():
    W, H = 1200, 230
    plane = (f'<g><path d="M0,-12 L30,0 L0,12 L6,0 Z" fill="#f8fafc"/><path d="M6,0 L0,12 L10,4 Z" fill="#94a3b8"/>'
             f'<animateMotion dur="6s" repeatCount="indefinite" rotate="auto" path="M760,180 C860,60 960,200 1040,110 S1140,40 1170,70"/></g>')
    body = (f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>'
            f'<rect x=".75" y=".75" width="{W - 1.5}" height="{H - 1.5}" rx="24" fill="none" stroke="#14b8a6" stroke-opacity=".3" stroke-width="1.5"/>'
            f'<path class="flow" d="M760,180 C860,60 960,200 1040,110 S1140,40 1170,70" fill="none" stroke="#5eead4" stroke-opacity=".45" stroke-width="2"/>'
            + plane
            + t(48, 64, "CONTACT.ME", 14, "#5eead4", 700, MONO, extra='letter-spacing="4"')
            + t(46, 124, "Let's connect", 52, "url(#shine)", 900, extra='letter-spacing="-1"')
            + t(48, 166, "Got an idea, a question or a data / AI project? Say hi — I'd love to talk.", 18, "#cbd5e1")
            + "".join(f'<circle cx="{620 + k * 40}" cy="{110 + (k % 2) * 30}" r="5" fill="{c}" class="pulse" style="animation-delay:-{k * .5}s"/>'
                      for k, c in enumerate(["#0a66c2", "#dd2a7b", "#25d366", "#ea4335"])))
    svg("contact-header.svg", W, H, "Let's connect — got an idea, a question or a data / AI project? Say hi.", body)

    def icon(kind, x, y):
        if kind == "linkedin":
            return (f'<rect x="{x}" y="{y}" width="52" height="52" rx="12" fill="#fff"/>'
                    f'<text x="{x + 26}" y="{y + 39}" fill="#0a66c2" font-family="{SANS}" font-size="32" font-weight="900" text-anchor="middle">in</text>')
        if kind == "instagram":
            return (f'<rect x="{x}" y="{y}" width="52" height="52" rx="15" fill="none" stroke="#fff" stroke-width="4.5"/>'
                    f'<circle cx="{x + 26}" cy="{y + 26}" r="11" fill="none" stroke="#fff" stroke-width="4.5"/>'
                    f'<circle cx="{x + 40}" cy="{y + 12}" r="3.2" fill="#fff"/>')
        if kind == "email":
            return (f'<rect x="{x}" y="{y + 6}" width="52" height="40" rx="7" fill="#fff"/>'
                    f'<path d="M{x + 3},{y + 10} L{x + 26},{y + 29} L{x + 49},{y + 10}" fill="none" stroke="#ea4335" stroke-width="4.5" stroke-linejoin="round"/>')
        return (f'<path d="M{x + 26},{y + 2} a24,24 0 1,1 -12.5,44.5 L{x + 2},{y + 50} l3.8,-11.5 A24,24 0 0,1 {x + 26},{y + 2}z" fill="none" stroke="#fff" stroke-width="4"/>'
                f'<path d="M{x + 17},{y + 15} c-3,2 -4,6 -1,11 c4,7 9,11 15,13 c4,1 7,-1 8,-4 l-5,-4 l-3,2 c-3,-1 -7,-5 -8,-8 l2,-3 z" fill="#fff"/>')

    buttons = [
        ("linkedin", "LinkedIn", "ruchira-kotuwegedara", ("#0a66c2", "#004182"), "CONNECT"),
        ("instagram", "Instagram", "@itzz.ruchy", ("#f58529", "#dd2a7b", "#8134af"), "FOLLOW"),
        ("whatsapp", "WhatsApp", "Message me directly", ("#25d366", "#128c7e"), "CHAT"),
        ("email", "Email", "ruchirakotuwegedara@gmail.com", ("#ea4335", "#b31412"), "WRITE"),
    ]
    BW, BH = 480, 120
    for kind, name, handle, cols, cta in buttons:
        stops = "".join(f'<stop offset="{k / (len(cols) - 1):.2f}" stop-color="{c}"/>' for k, c in enumerate(cols))
        b = (f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">{stops}</linearGradient>'
             f'<linearGradient id="sheen" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
             f'<clipPath id="c"><rect width="{BW}" height="{BH}" rx="22"/></clipPath></defs>'
             f'<g clip-path="url(#c)"><rect width="{BW}" height="{BH}" fill="url(#g)"/>'
             f'<circle cx="{BW - 40}" cy="-10" r="90" fill="#fff" opacity=".08"/><circle cx="{BW - 10}" cy="{BH + 20}" r="60" fill="#000" opacity=".08"/>'
             f'<rect y="0" width="90" height="{BH}" fill="url(#sheen)" transform="skewX(-20)"><animate attributeName="x" values="-160;{BW + 80};{BW + 80}" keyTimes="0;.45;1" dur="4s" repeatCount="indefinite"/></rect></g>'
             f'<g class="bob">{icon(kind, 28, 34)}</g>'
             + t(100, 56, name, 26, "#fff", 900)
             + t(100, 82, escape(handle), 15, "#fff", 500, extra='fill-opacity=".9"')
             + f'<g><rect x="{BW - 104}" y="{BH / 2 - 17}" width="80" height="34" rx="17" fill="#fff" fill-opacity=".2" stroke="#fff" stroke-opacity=".55"/>'
             + t(BW - 64, BH / 2 + 5, cta + " →", 12.5, "#fff", 800, MONO, "middle")
             + f'<animateTransform attributeName="transform" type="translate" values="0 0;5 0;0 0" dur="1.6s" repeatCount="indefinite"/></g>')
        svg(f"contact-{kind}.svg", BW, BH, f"{name} — {handle}", b)


if __name__ == "__main__":
    contact()
    into_player()
    about_bento()
    heading()
    bring()
    flow_loop()
    direction()
    hobbies()
    mindset()
