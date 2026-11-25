"""Render the 'Currently learning' Quest Log from data/learning.json.

Edit data/learning.json, then run:  python3 scripts/generate_learning.py
(.github/workflows/learning-quest.yml also does this automatically on push.)
"""
import datetime
import json
from html import escape
from pathlib import Path

from generate_assets import write

ROOT = Path(__file__).resolve().parent.parent
PIX = "'JetBrains Mono','Courier New',Consolas,Menlo,monospace"
GOLD, CYAN, PINK, GREEN, DIM = "#ffd23f", "#3be8ff", "#ff4ecd", "#4ade80", "#6b7280"
BAR_COLORS = [CYAN, PINK, GOLD, GREEN, "#a78bfa", "#fb923c"]


def txt(x, y, s, size=16, fill="#f8fafc", weight=700, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" fill="{fill}" font-family="{PIX}" font-size="{size}" font-weight="{weight}" '
            f'text-anchor="{anchor}" {extra}>{s}</text>')


def pixel_frame(x, y, w, h, col, step=6, fill="none", sw=4):
    """Rectangle with stepped 'pixel' corners."""
    s = step
    pts = [(x + s, y), (x + w - s, y), (x + w - s, y + s), (x + w, y + s), (x + w, y + h - s), (x + w - s, y + h - s),
           (x + w - s, y + h), (x + s, y + h), (x + s, y + h - s), (x, y + h - s), (x, y + s), (x + s, y + s)]
    p = " ".join(f"{a},{b}" for a, b in pts)
    return f'<polygon points="{p}" fill="{fill}" stroke="{col}" stroke-width="{sw}" stroke-linejoin="miter"/>'


def main():
    data = json.loads((ROOT / "data/learning.json").read_text(encoding="utf-8"))
    quests = data["quests"]
    active = [q for q in quests if q.get("status") == "active"]
    done = [q for q in quests if q.get("status") == "completed"]
    nxt = [q for q in quests if q.get("status") == "next"]
    level = 1 + len(done) * 2 + sum(int(q.get("xp", 0)) for q in active) // 50
    today = datetime.date.today().isoformat()

    W, T = 1200, 8.0
    top, row_h = 150, 82
    lists_y = top + len(active) * row_h + 30
    list_rows = max(len(done), len(nxt), 1)
    H = lists_y + 60 + list_rows * 40 + 90

    b = []
    b.append(f'<rect width="{W}" height="{H}" fill="#0b0b1e"/>')
    b.append('<rect width="100%" height="100%" fill="url(#grid)"/>')
    b.append(pixel_frame(10, 10, W - 20, H - 20, GOLD, 10, sw=5))
    b.append(pixel_frame(22, 22, W - 44, H - 44, "#3b2f0b", 8, sw=2))

    # header
    b.append(txt(52, 82, "QUEST LOG", 46, PINK, 900, extra='letter-spacing="6"'))
    b.append(txt(48, 78, "QUEST LOG", 46, GOLD, 900, extra='letter-spacing="6"'))
    b.append(txt(52, 114, "▸ CURRENTLY LEARNING", 15, CYAN, 700, extra='letter-spacing="3"'))
    b.append(txt(W - 52, 66, f"PLAYER: {escape(data.get('player', 'PLAYER'))}", 16, "#e5e7eb", 800, "end", 'letter-spacing="2"'))
    b.append(txt(W - 52, 94, f"LV.{level:02d}", 26, GREEN, 900, "end", 'letter-spacing="3"'))
    b.append(txt(W - 52, 118, f"SAVED {today}", 12, DIM, 700, "end", 'letter-spacing="2"'))
    b.append(f'<rect x="48" y="{top - 18}" width="{W - 96}" height="4" fill="{GOLD}" opacity=".5"/>')

    # active quests
    seg_n, seg_w, seg_gap = 20, 22, 4
    bar_x = W - 52 - seg_n * (seg_w + seg_gap) - 90
    for i, q in enumerate(active):
        y = top + i * row_h
        col = BAR_COLORS[i % len(BAR_COLORS)]
        xp = max(0, min(100, int(q.get("xp", 0))))
        filled = round(xp / 100 * seg_n)
        b.append(f'<rect x="48" y="{y}" width="{W - 96}" height="{row_h - 12}" fill="#13132e"/>')
        b.append(f'<rect x="48" y="{y}" width="6" height="{row_h - 12}" fill="{col}"/>')
        b.append(pixel_frame(72, y + 11, 48, 48, col, 5, "#0b0b1e", 3))
        b.append(f'<text x="96" y="{y + 44}" font-size="24" text-anchor="middle">{q.get("icon", "⭐")}</text>')
        b.append(txt(140, y + 32, escape(q["name"].upper()), 19, "#f8fafc", 900, extra='letter-spacing="1.5"'))
        b.append(txt(140, y + 55, escape(q.get("detail", "")), 13.5, "#9ca3af", 500))
        segs = []
        for k in range(seg_n):
            x = bar_x + k * (seg_w + seg_gap)
            segs.append(f'<rect x="{x}" y="{y + 22}" width="{seg_w}" height="24" fill="#26264a"/>')
            if k < filled:
                t0 = 0.05 + 0.5 * k / seg_n
                segs.append(f'<rect x="{x}" y="{y + 22}" width="{seg_w}" height="24" fill="{col}">'
                            f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t0:.3f};{t0 + .02:.3f};.92;1" dur="{T}s" repeatCount="indefinite"/></rect>'
                            f'<rect x="{x}" y="{y + 22}" width="{seg_w}" height="6" fill="#fff" opacity=".25"/>')
            elif k == filled:
                segs.append(f'<rect x="{x}" y="{y + 22}" width="{seg_w}" height="24" fill="{col}" opacity=".0">'
                            f'<animate attributeName="opacity" values="0;.7;0" dur="1s" repeatCount="indefinite"/></rect>')
        b.extend(segs)
        b.append(txt(W - 60, y + 40, f"{xp}%", 18, col, 900, "end"))
        b.append(txt(bar_x, y + 16, "XP", 10, DIM, 800, extra='letter-spacing="2"'))

    # completed + next
    cw = (W - 96 - 24) / 2
    for c, (title, items, col, mark) in enumerate([("✓ COMPLETED", done, GREEN, "✓"), ("🔒 NEXT QUESTS", nxt, DIM, "🔒")]):
        x = 48 + c * (cw + 24)
        b.append(pixel_frame(x, lists_y, cw, 50 + list_rows * 40 + 10, col, 6, "#10102a", 3))
        b.append(txt(x + 24, lists_y + 34, title, 16, col if c == 0 else "#cbd5e1", 900, extra='letter-spacing="3"'))
        for j, q in enumerate(items):
            yy = lists_y + 74 + j * 40
            name_col = "#f8fafc" if c == 0 else "#9ca3af"
            b.append(f'<text x="{x + 30}" y="{yy}" font-size="18" text-anchor="middle">{q.get("icon", "⭐")}</text>')
            b.append(txt(x + 52, yy, escape(q["name"]), 16, name_col, 800))
            b.append(txt(x + cw - 24, yy, mark if c == 0 else "LOCKED", 13 if c else 18, col, 900, "end",
                         '' if c == 0 else 'letter-spacing="2"'))
        if not items:
            b.append(txt(x + 24, lists_y + 74, "— none yet —", 14, DIM, 600))

    # footer
    fy = H - 52
    b.append(f'<g>{txt(W / 2, fy, "▶ PRESS START TO CONTINUE LEARNING", 17, GOLD, 900, "middle", chr(32) + "letter-spacing=" + chr(34) + "3" + chr(34))}'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.2s" repeatCount="indefinite"/></g>')
    # scanlines on top
    b.append('<rect width="100%" height="100%" fill="url(#scan)" pointer-events="none"/>')
    b.append(f'<rect width="{W}" height="6" y="0" fill="#fff" opacity=".04"><animate attributeName="y" values="0;{H}" dur="5s" repeatCount="indefinite"/></rect>')

    label = "Quest Log — currently learning: " + ", ".join(f"{q['name']} ({q.get('xp', 0)}%)" for q in active)
    if done:
        label += ". Completed: " + ", ".join(q["name"] for q in done)
    if nxt:
        label += ". Next: " + ", ".join(q["name"] for q in nxt)
    write("learning-quest.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(label)}">
<defs>
  <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="#1a1a3a" stroke-width="1"/></pattern>
  <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".18"/></pattern>
</defs>
{''.join(b)}
</svg>""")


if __name__ == "__main__":
    main()
