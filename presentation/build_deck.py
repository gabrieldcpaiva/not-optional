#!/usr/bin/env python3
"""
Lights, Camera, Agent.
A friendly PDF teach-in deck: agentic workflows for video people, with Higgsfield
as the working example. Built with fpdf2 + DejaVu fonts. All facts verified
against Higgsfield's own help pages (fetched 2026-09-03); uncertain items are
tagged [VERIFY] in the copy itself.

Output: presentation/lights-camera-agent.pdf  (28 pages, 16:9 landscape)
"""
import re, os
from fpdf import FPDF

# ---------------- palette & metrics ----------------
PW, PH = 297.0, 167.06          # 16:9, A4-landscape width
M      = 16.0                   # margin
CW     = PW - 2 * M             # content width (265)

INK      = (43, 32, 24)         # warm near-black
PAPER    = (250, 245, 236)      # cream
CARD     = (255, 253, 248)      # card white
CREAM2   = (243, 235, 219)      # deeper cream for strips
TERRA    = (190, 82, 43)        # terracotta
TERRA_D  = (148, 60, 28)        # dark terracotta
TERRA_T  = (246, 226, 214)      # terracotta tint
TEAL     = (26, 92, 86)
TEAL_T   = (222, 236, 232)
MUST     = (214, 158, 60)       # mustard
MUST_T   = (247, 234, 205)
MUTED    = (105, 91, 76)
LINE     = (214, 200, 175)
SOFTSH   = (233, 222, 199)      # card "shadow"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"

pdf = FPDF(orientation="L", unit="mm", format=(PH, PW))  # tuple is portrait; L swaps → 297x167
pdf.set_title("Lights, Camera, Agent. — a community teach-in deck")
pdf.set_author("[your name] · school creative community")
pdf.set_subject("Agentic workflows for video people, with Higgsfield as the working example")
pdf.set_keywords("agentic workflows, MCP, Higgsfield, video production, teach-in")
pdf.set_creator("build_deck.py (fpdf2)")
pdf.set_auto_page_break(False)
pdf.set_margins(M, M, M)
pdf.add_font("dej",  "",  f"{FONT_DIR}/DejaVuSans.ttf")
pdf.add_font("dej",  "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
pdf.add_font("serj", "",  f"{FONT_DIR}/DejaVuSerif.ttf")
pdf.add_font("serj", "B", f"{FONT_DIR}/DejaVuSerif-Bold.ttf")
pdf.add_font("mono", "",  f"{FONT_DIR}/DejaVuSansMono.ttf")
pdf.add_font("mono", "B", f"{FONT_DIR}/DejaVuSansMono-Bold.ttf")

PAGE = {"n": 0}
VERIFY_LEGEND = "[VERIFY] = from official docs / press research on Sept 3, 2026. Confirm before showtime."

# ---------------- low-level helpers ----------------

def _w(txt, font, style, size):
    pdf.set_font(font, style, size)
    return pdf.get_string_width(txt)

def parse_runs(text, base_color=INK, base_style=""):
    """Mini-markup: **bold**, <t>erracotta, <g> teal, <m> muted, <v> = bold terracotta."""
    out, bold, color, style = [], base_style == "B", base_color, base_style
    i = 0
    for mt in re.finditer(r"(</?[tgmk]>|\*\*)", text):
        seg = text[i:mt.start()]
        if seg:
            out.append((seg, style, color))
        tok = mt.group(0)
        if tok == "**":
            bold = not bold
            style = "B" if bold or base_style == "B" else ""
        elif tok.startswith("</"):
            color = base_color
        else:
            color = {"t": TERRA, "g": TEAL, "m": MUTED, "k": INK}[tok[1]]
        i = mt.end()
    if text[i:]:
        out.append((text[i:], style, color))
    return [(s, st, c) for s, st, c in out if s]

ATTACH = '.,;:!?%”’”)]'   # words starting with these hug the previous word

def layout(text, w, font="dej", size=11.5, base_color=INK, base_style=""):
    """Wrap marked-up text into lines of (word, style, color). Returns list of lines."""
    words = []
    for seg, st, col in parse_runs(text, base_color, base_style):
        for piece in seg.split(" "):
            if piece == "":
                continue
            words.append((piece, st, col))
    lines, cur, curw = [], [], 0.0
    space = _w(" ", font, "B" if base_style == "B" else "", size)
    for wd, st, col in words:
        ww = _w(wd, font, "B" if "B" in st else "", size)
        hug = bool(cur) and wd[0] in ATTACH
        add = ww if (not cur or hug) else ww + space
        if cur and curw + add > w:
            lines.append(cur); cur, curw = [(wd, st, col)], ww
        else:
            cur.append((wd, st, col)); curw += add
    if cur:
        lines.append(cur)
    return lines

def para(x, y, w, text, font="dej", size=11.5, color=INK, style="", lh=None, max_lines=None):
    """Draw wrapped rich text at (x, y top). Returns y after the block."""
    lh = lh or size * 0.46
    lines = layout(text, w, font, size, color, style)
    if max_lines:
        lines = lines[:max_lines]
    space = _w(" ", font, "B" if style == "B" else "", size)
    for ln in lines:
        cx = x
        pdf.set_y(y + lh * 0.36)
        for wd, st, col in ln:
            bst = "B" if "B" in st else ""
            if cx > x and wd[0] not in ATTACH:
                cx += space
            pdf.set_font(font, bst, size)
            pdf.set_text_color(*col)
            pdf.set_x(cx)
            pdf.cell(_w(wd, font, bst, size) + 0.01, lh * 0.7, wd)
            cx += _w(wd, font, bst, size)
        y += lh
    return y

def measure(w, text, font="dej", size=11.5, style="", lh=None):
    lh = lh or size * 0.46
    return len(layout(text, w, font, size, INK, style)) * lh

def rect(x, y, w, h, fill=None, edge=None, lw=0.3):
    if fill:
        pdf.set_fill_color(*fill)
    if edge:
        pdf.set_draw_color(*edge)
        pdf.set_line_width(lw)
    style = ("F" if fill else "") + ("D" if edge else "")
    pdf.rect(x, y, w, h, style=style or "D")

def card(x, y, w, h, fill=CARD, edge=LINE, accent=None):
    rect(x + 0.9, y + 1.1, w, h, fill=SOFTSH)          # soft offset shadow
    rect(x, y, w, h, fill=fill, edge=edge, lw=0.35)
    if accent:
        rect(x, y, 2.4, h, fill=accent)

def chip(x, y, text, fill=TEAL_T, col=TEAL, size=8.2, h=6.4):
    tw = _w(text, "dej", "B", size)
    w = tw + 6
    rect(x, y, w, h, fill=fill)
    pdf.set_font("dej", "B", size); pdf.set_text_color(*col)
    pdf.set_xy(x, y + h * 0.31)
    pdf.cell(w, h * 0.55, text, align="C")
    return x + w

def hline(x1, y, x2, col=LINE, lw=0.3):
    pdf.set_draw_color(*col); pdf.set_line_width(lw)
    pdf.line(x1, y, x2, y)

def arrow(x1, y1, x2, y2, col=TERRA, lw=1.1, head=2.6):
    pdf.set_draw_color(*col); pdf.set_line_width(lw)
    pdf.line(x1, y1, x2, y2)
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    a1, a2 = ang + 2.62, ang - 2.62
    p = [(x2, y2),
         (x2 + head * math.cos(a1), y2 + head * math.sin(a1)),
         (x2 + head * math.cos(a2), y2 + head * math.sin(a2))]
    pdf.set_fill_color(*col)
    pdf.polygon(p, style="F")

# ---------------- page scaffolding ----------------

def new_page(kicker=None, title=None, title_size=24, verify_legend=False, footer=True):
    PAGE["n"] += 1
    pdf.add_page()
    rect(0, 0, PW, PH, fill=PAPER)
    y = 14.0
    if kicker:
        pdf.set_font("dej", "B", 8.4); pdf.set_text_color(*TERRA_D)
        pdf.set_xy(M, y); pdf.cell(CW, 4, kicker.upper())
        y += 6.4
    if title:
        ty = para(M, y, CW, title, font="serj", style="B", size=title_size, lh=title_size * 0.44)
        y = ty + 2.0
    if footer:
        hline(M, PH - 9.5, PW - M, col=LINE, lw=0.4)
        pdf.set_font("dej", "", 7.6); pdf.set_text_color(*MUTED)
        left = "Lights, Camera, Agent — a community teach-in"
        pdf.set_xy(M, PH - 7.6); pdf.cell(120, 3.6, left)
        if verify_legend:
            pdf.set_xy(M + 95, PH - 7.6)
            pdf.cell(CW - 105, 3.6, VERIFY_LEGEND, align="R")
        pdf.set_font("dej", "B", 8.2); pdf.set_text_color(*TERRA_D)
        pdf.set_xy(PW - M - 22, PH - 7.6); pdf.cell(22, 3.6, f"{PAGE['n']:02d}", align="R")
    return y

def note(txt, y=PH - 26.5):
    rect(M, y, 2.0, 15, fill=TEAL)
    rect(M + 2.0, y, CW - 2.0, 15, fill=CREAM2)
    pdf.set_font("dej", "B", 7.8); pdf.set_text_color(*TEAL)
    pdf.set_xy(M + 5.5, y + 2.6); pdf.cell(60, 3.4, "SAY IT LIKE THIS")
    para(M + 5.5, y + 6.4, CW - 11, txt, size=9.2, color=MUTED, lh=4.1)

def bullets(x, y, w, items, size=10.5, lh=None, gap=2.6, color=INK, glyph="•", gcol=TERRA):
    lh = lh or size * 0.46
    for it in items:
        pdf.set_font("dej", "B", size); pdf.set_text_color(*gcol)
        pdf.set_xy(x, y + lh * 0.3); pdf.cell(4, lh * 0.7, glyph)
        yy = para(x + 5, y, w - 5, it, size=size, color=color, lh=lh)
        y = yy + gap
    return y

def qa_row(x, y, w, label, text, lab_w=37, size=10.2, fill=None):
    """Walkthrough row: label chip + wrapped text. Returns y after."""
    th = measure(w - lab_w - 4, text, size=size, lh=size * 0.45)
    h = max(7.5, th + 3.2)
    if fill:
        rect(x, y, w, h, fill=fill)
    rect(x, y, 2.0, h, fill=TERRA)
    pdf.set_font("dej", "B", 8.0); pdf.set_text_color(*TERRA_D)
    pdf.set_xy(x + 4.5, y + 2.2); pdf.cell(lab_w - 5, 3.4, label)
    para(x + lab_w + 4.5, y + 1.8, w - lab_w - 8, text, size=size, lh=size * 0.45)
    return y + h

# ============================================================
# PAGE 1 — TITLE
# ============================================================
new_page(footer=False)
# viewfinder corner marks
c = 7.0; L = 9.0
pdf.set_draw_color(*TERRA); pdf.set_line_width(0.9)
for (cx, cy, dx, dy) in [(c, c, 1, 1), (PW - c, c, -1, 1), (c, PH - c, 1, -1), (PW - c, PH - c, -1, -1)]:
    pdf.line(cx, cy, cx + L * dx, cy)
    pdf.line(cx, cy, cx, cy + L * dy)
pdf.set_font("dej", "B", 9.5); pdf.set_text_color(*TERRA)
pdf.set_xy(PW - M - 34, c + 2.5); pdf.cell(30, 4, "● REC", align="R")

para(M + 6, 30, 150, "A SCHOOL CREATIVE-COMMUNITY TEACH-IN · SPRING 2026",
     size=8.6, color=MUTED, style="B", lh=4)
para(M + 6, 42, 200, "Lights, Camera,", font="serj", style="B", size=41, lh=17)
y = para(M + 6, 60, 220, "Agent.", font="serj", style="B", size=41, color=TERRA, lh=17)
rect(M + 6, y + 4, 46, 1.6, fill=TEAL)
y = para(M + 6, y + 11, 168,
         "A friendly guide to letting an AI helper pitch in on your video work — with **Higgsfield** as our first crew member.",
         size=13, color=INK, lh=6.4)
y = para(M + 6, y + 5, 168,
         "For people who already know cameras, cuts, and story — and have never once wanted to learn “prompt engineering.”",
         size=10, color=MUTED, lh=5)
cx = M + 6
for t in ["a community teach-in", "not a product pitch", "nobody gets replaced today"]:
    cx = chip(cx, y + 4, t, fill=CREAM2, col=TEAL, size=8.6, h=6.8) + 3
para(M + 6, PH - 26, 200, "Presented by **[your name]** · roughly 30 minutes + one small exercise · yes, you may steal these slides",
     size=9, color=MUTED)

# ============================================================
# PAGE 2 — THESIS (presenter)
# ============================================================
y = new_page("The short version", "What this talk believes", verify_legend=True)
card(M, y + 2, CW, 46, accent=TERRA)
para(M + 7, y + 7, CW - 14,
     "**Agents and video absolutely work together.** The agent does not replace the filmmaker. It becomes an extra pair of "
     "hands — for planning, organizing, generating, revising, and moving creative work forward.",
     size=13.5, lh=6.6)
para(M + 7, y + 29, CW - 14,
     "That’s the whole message. The next 28 pages say it slowly, kindly, and with running examples — using Higgsfield’s "
     "**official agent connection** as the working demo, because its setup is genuinely five minutes and its docs are public.",
     size=10.5, color=MUTED, lh=5.2)
yy = y + 54
col_w = (CW - 8) / 3
for i, (h, b) in enumerate([
    ("The shape of it", "— The shape of the evening —"),
    ("Honesty tags", "— How to read the tags —"),
    ("For you, presenter", "— Before you present —"),
]):
    pass
items3 = [
    ("Shape of the evening", "28 pages ≈ 30 relaxed minutes, then a 10-minute hands-on exercise. One idea per page. No jargon without a translation."),
    ("Honesty tags", "Facts were checked against Higgsfield’s own help pages on **Sept 3, 2026**. Anything that could drift is tagged **[VERIFY]** — see it as “call before the show,” not as doubt."),
    ("Before you present", "Pages 2–3 are **for you** — hide them on the night. Page 28 is a packing checklist: screenshots to grab, facts to re-confirm, prompts to pre-load."),
]
for i, (h, b) in enumerate(items3):
    x = M + i * (col_w + 4)
    card(x, yy, col_w, 38, accent=TEAL if i == 2 else None)
    para(x + 6, yy + 4.5, col_w - 10, f"**{h}**", size=10, lh=4.6)
    para(x + 6, yy + 10.5, col_w - 10, b, size=8.6, color=MUTED, lh = 4.3)
note("If you present only three things, make it this thesis, the loop picture (page 10), and the exercise (page 22).")

# ============================================================
# PAGE 3 — FIVE FACTS TO VERIFY (presenter)
# ============================================================
y = new_page("Presenters only — 15 minutes of homework",
             "Five things worth double-checking this week", verify_legend=True)
para(M, y, CW,
     "This corner of the world moves monthly, so the deck speaks in [VERIFY] tags wherever a fact can drift. "
     "All five checks below take about fifteen minutes, and every link is repeated in the back-of-deck checklist.",
     size=10, color=MUTED, lh=4.8)
y += 13
rows = [
    ("1 · The doorway address",
     "Is the agent connection still at **mcp.higgsfield.ai/mcp**?",
     "Confirm on Higgsfield’s Help Center → “What is Higgsfield MCP, and how is it different from the web?”"),
    ("2 · What the agent may do",
     "The job list on page 9 came straight from their docs (generation, audio, reframe/upscale, clipping, balance). Anything added or removed?",
     "Same help page, plus “How do I connect Higgsfield to Claude, ChatGPT, or another AI agent?”"),
    ("3 · The price of admission",
     "MCP use needs an **active paid Higgsfield plan**, and **every** agent-made generation spends credits — even on “unlimited” web plans.",
     "Check your own plan tier and credit balance before any live demo."),
    ("4 · Where people can connect",
     "Claude = custom connector · ChatGPT = official plugin (no audio there) · Cursor = marketplace · coding agents = CLI.",
     "Confirmed in the “How do I connect…” article — re-skim it the week of the talk."),
    ("5 · The deep-end cameo",
     "Open Montage (page 21) is described from **third-party write-ups**, not its own docs. Don’t quote star counts or pipeline numbers on stage.",
     "If you mention it at all, quote only what its GitHub page says that day."),
]
for lab, a, b in rows:
    card(M, y, CW, 17.6, accent=MUST)
    para(M + 6, y + 2.6, 62, f"**{lab}**", size=9.4, lh=4.2)
    para(M + 72, y + 2.6, CW - 78, a, size=8.9, lh=4.15)
    para(M + 72, y + 10.6, CW - 78, f"<m>How to confirm:</m> {b}", size=8.0, color=MUTED, lh=3.9)
    y += 19.4
note("Nothing in this talk collapses if one of these changed overnight — the tags tell the room that updating is normal here.")

# ============================================================
# PAGE 4 — FALSE SEPARATION
# ============================================================
y = new_page("Where most of us start", "Two rooms, one hallway")
para(M, y, CW,
     "Most of us carry a quiet assumption: AI assistants live in one room, video tools live in another, and the rooms don’t talk. "
     "Fair enough — it used to be true. Let’s look at the two rooms.",
     size=10.5, color=MUTED, lh=5)
y += 14
col_w = (CW - 12) / 3
cards4 = [
    ("ROOM ONE · THE THINKER", TERRA,
     "An AI assistant is lovely company at the idea stage. Brainstorm, outline, rework the script… "
     "then it stops — and hands you a wall of text to go do something with.",
     "Great at ideas. **Stops at the idea.**"),
    ("ROOM TWO · THE MACHINE", TEAL,
     "A video platform can produce astonishing media. But you drive every single step: every prompt, "
     "every pick, every export. It never once offers to carry anything.",
     "Makes media. **You run every step.**"),
    ("THE HALLWAY", MUST,
     "Connect an assistant to the right video tools, and the idea starts walking toward the footage "
     "by itself — with you watching at every doorway, holding the final yes.",
     "The idea **carried into action.**"),
]
for i, (k, ac, body, foot) in enumerate(cards4):
    x = M + i * (col_w + 6)
    card(x, y, col_w, 69, accent=ac, fill=CARD if i < 2 else MUST_T)
    para(x + 6, y + 6, col_w - 12, f"**{k}**", size=8.8, color=ac if i < 2 else TERRA_D, lh=4.2)
    para(x + 6, y + 13, col_w - 12, body, size=9.8, lh=4.9)
    hline(x + 6, y + 55, x + col_w - 6)
    para(x + 6, y + 58, col_w - 12, foot, size=9.8, lh=4.6)
note("Ask for a show of hands: who’s used AI to brainstorm? Who’s generated AI video? Keep your hand up if you’ve connected the two. (Usually: nobody. That gap is the whole talk.)")

# ============================================================
# PAGE 5 — METAPHOR
# ============================================================
y = new_page("The picture to keep", "An extra pair of hands")
y = para(M, y, 165,
         "On a real set, the director does not personally coil the cables.",
         size=15, font="serj", style="B", lh=7.4)
y += 5
for t in [
    "Think of the agent as a new production assistant. One who has somehow read every manual you own, never sleeps, "
    "never sighs, and will happily draft the fourteenth variation at midnight.",
    "Now the honest part — and honestly, it’s the whole deal: **this assistant has no taste. None at all.** "
    "It renders the fourteenth variation with the same confidence as the first.",
    "So taste stays in your chair. Judgment stays in your chair. The final yes stays in your chair. "
    "That isn’t a flaw in the arrangement. <t>**That is the arrangement.**</t>",
]:
    y = para(M, y, 165, t, size=11, lh=5.6) + 4.5
# right crew card
cx0 = M + 173
card(cx0, 42, CW - 173, 84, accent=TEAL)
para(cx0 + 6, 47, CW - 173 - 12, "**CALL SHEET · THE NEW PA**", size=8.2, color=TEAL, lh=4)
crew = [
    ("Name", "“The agent” — answers to plain English"),
    ("Skills", "drafting, organizing, tool-wrangling, infinite patience"),
    ("Cannot do", "taste, context, caring whether it’s good"),
    ("Works for", "you. Reviews daily. Union of one."),
]
cy = 53
for k, v in crew:
    para(cx0 + 6, cy, 30, f"**{k}**", size=8.6, color=TERRA_D, lh=4)
    cy = para(cx0 + 34, cy, CW - 173 - 40, v, size=8.6, lh=4.1) + 2.2
hline(cx0 + 6, cy + 1, cx0 + CW - 173 - 6)
para(cx0 + 6, cy + 3.5, CW - 173 - 12, "<m>Start date: tonight, if you want. Notice period: also tonight.</m>", size=8.2, lh=3.9)
note("If the room remembers one sentence tonight, make it “taste is your department.”")

# ============================================================
# PAGE 6 — WHAT IS AN AGENT
# ============================================================
y = new_page("No jargon, promise", "So what is an “agent,” really?")
para(M, y, CW,
     "An agent is an AI assistant that can **do** things, not just **say** things. A chatbot is the friend who gives great "
     "advice from the couch. An agent is the intern who gets up off the couch: you name the goal, it walks over to the (very "
     "short) list of tools you’ve allowed it, picks one, and uses it.",
     size=11, lh=5.6)
y += 17
para(M, y, CW,
     "Then it looks at what came back, tells you what happened, and takes the next step — or stops and asks you. You watch "
     "all of this happen out loud. There’s no hidden deliberation to trust or distrust: there are just **visible steps and visible results**, "
     "like an assistant thinking out loud while they work.",
     size=11, lh=5.6)
y += 18
# five-step strip
steps = ["You name\nthe goal", "It picks an\nallowed tool", "It does\nthe task", "It checks\nthe result", "It reports\nback to you"]
bw = (CW - 4 * 8) / 5
for i, s in enumerate(steps):
    x = M + i * (bw + 8)
    card(x, y, bw, 21, fill=CARD, accent=None)
    t, s2 = s.split("\n")
    para(x + 3.5, y + 3.5, bw - 7, f"**{t}**", size=9.2, lh=4.2)
    para(x + 3.5, y + 8.6, bw - 7, s2, size=9.2, lh=4.2)
    pdf.set_font("dej", "B", 7.4); pdf.set_text_color(*MUTED)
    pdf.set_xy(x + 3.5, y + 16.6); pdf.cell(10, 3, f"step {i+1}")
    if i < 4:
        arrow(x + bw + 1.5, y + 10.5, x + bw + 6.5, y + 10.5, col=TEAL, lw=1.0)
y += 25
rect(M, y, CW, 9.5, fill=TEAL_T)
para(M + 5, y + 2.2, CW - 10, "**The tools are the key.** An agent with no tools is back on the couch, giving advice. "
     "Give it a doorway to Higgsfield and suddenly the intern can run to the machine room — page 9 shows exactly how far (and no further).",
     size=9.3, lh=4.4)
note("Lean on “a very short list of tools we’ve allowed.” Permission and visibility are the entire safety story — say that plainly.")

# ============================================================
# PAGE 7 — MCP SIMPLY
# ============================================================
y = new_page("One idea, sixty seconds", "MCP is the standard socket")
para(M, y, CW,
     "Once upon a time, every lamp shipped with its own plug, and every new lamp meant calling an electrician. Then the world "
     "agreed on a standard socket — and plugging in a lamp became boring, in the best possible way.",
     size=11.5, lh=5.8)
y += 17.5
para(M, y, CW,
     "**MCP is that agreement, but between AI assistants and tools.** A shared, published way for an assistant to ask a service: "
     "“what can you do?” — and then “please do this one, with these details.” If both sides follow the agreement, any assistant "
     "can plug into any tool that offers itself. No custom wiring per pair.",
     size=11.5, lh=5.8)
y += 19
para(M, y, CW, "That is genuinely all you need to know to use one. Cross my heart.", size=11.5, style="B", lh=5.8)
y += 10
card(M, y, CW, 22, fill=CREAM2, accent=TEAL)
para(M + 7, y + 3.5, CW - 14, "**For the curious — one line only:**", size=9, lh=4.2)
para(M + 7, y + 8.6, CW - 14,
     "<m>MCP = **Model Context Protocol** — an open standard. Higgsfield runs a public MCP doorway (a “server”), one web address long, "
     "listed on page 25. No schemas, no JSON, no auth talk tonight; the appendix has the keys if you want them.</m>",
     size=9, lh=4.3)
note("If someone asks a deep technical question here, smile warmly and point at the appendix. That is what the appendix is for.")

# ============================================================
# PAGE 8 — MEET HIGGSFIELD
# ============================================================
y = new_page("Our working example", "Meet Higgsfield (the video side)", verify_legend=True)
para(M, y, CW,
     "For anyone who hasn’t met it: **Higgsfield is a browser-based studio for AI-generated images and video** — and its personality "
     "is refreshingly film-set. It’s known for camera moves with actual cinematography instincts (crash zooms, dolly glides, FPV "
     "swoops), for keeping a character’s face consistent across shots (a feature called **Soul**), and for putting many different "
     "video models — Veo, Kling, Seedance, Minimax Hailuo and friends — behind one login.",
     size=11, lh=5.6)
y += 24.5
para(M, y, CW,
     "Why it stars in this talk: **its agent doorway is official, documented in plain language by Higgsfield itself, and takes about "
     "five minutes to set up.** We’ll use it as the example all evening — but every idea transfers to any tool that opens a similar door.",
     size=11, lh=5.6)
y += 16.5
para(M, y, 200, "Things it’s documented to do through the agent connection:", size=9.5, style="B", lh=4.6)
y += 6
cx = M
chips8 = ["image & video generation", "deliberate camera moves", "Soul characters", "voiceover · dubbing",
          "upscale · reframe · background removal", "YouTube → short clips", "credit balance on demand"]
for t in chips8:
    tw = _w(t, "dej", "B", 8.4) + 6
    if cx + tw > PW - M:
        cx = M; y += 8.2
    cx = chip(cx, y, t, fill=TEAL_T, col=TEAL, size=8.4, h=6.6) + 2.6
para(M, y + 11, CW, "<m>Sources: Higgsfield Help Center integration pages + higgsfield.ai, re-read on Sept 3, 2026. Full citations on page 26.</m>",
     size=8, lh=3.8)
note("If half the room already uses Higgsfield on the web: wonderful — tonight is about the other front door, the one the assistant uses.")

# ============================================================
# PAGE 9 — THE CONNECTION
# ============================================================
y = new_page("The bridge", "The connection: Higgsfield’s agent doorway", verify_legend=True)
colL, colR = 118, CW - 118 - 6
card(M, y, colL, 92, accent=TEAL)
para(M + 7, y + 4, colL - 14, "**THE FIVE-MINUTE VERSION** <m>(Claude example)</m>", size=8.6, color=TEAL, lh=4.2)
setup = [
    "Open Claude → **Settings → Connectors**.",
    "Choose **Add custom connector**; name it “Higgsfield.”",
    "Paste the doorway address from page 25 (yes, that’s the whole trick).",
    "Click **Connect** and sign in to Higgsfield once to approve it.",
    "Test it by asking: **“What’s my Higgsfield credit balance?”** If it answers with a number, you’re connected. Really.",
]
sy = y + 10
for i, s in enumerate(setup):
    pdf.set_font("dej", "B", 10.5); pdf.set_text_color(*TERRA)
    pdf.set_xy(M + 7, sy + 0.6); pdf.cell(6, 4, f"{i+1}")
    sy = para(M + 14.5, sy, colL - 21, s, size=8.9, lh=4.2) + 3.4
para(M + 7, sy + 1, colL - 14,
     "<m>Needs an **active paid plan**. ChatGPT uses an official plugin instead; Cursor has it in its marketplace. Same sign-in idea everywhere. [VERIFY plan + app list]</m>",
     size=7.9, lh=3.9)
xR = M + colL + 6
card(xR, y, colR, 64, accent=TERRA)
para(xR + 7, y + 4, colR - 14, "**WHAT THE AGENT MAY THEN DO** <m>(straight from the docs)</m>", size=8.6, color=TERRA_D, lh=4.2)
rights = [
    "Generate **images and video** on any of its models — models you can name in plain words",
    "Make **audio**: voiceover, voice change, dubbing",
    "**Tidy-up jobs**: upscale, reframe/expand, remove backgrounds",
    "Use **Soul characters** and saved reference Elements by name",
    "**Personal Clipper**: turn a long YouTube video into short clips",
    "Report your **credit balance** and past generations",
]
sy = y + 10.5
for r in rights:
    pdf.set_font("dej", "B", 9); pdf.set_text_color(*TEAL)
    pdf.set_xy(xR + 7, sy + 0.8); pdf.cell(4, 3.6, "✓")
    sy = para(xR + 12, sy, colR - 19, r, size=8.7, lh=4.1) + 2.5
card(xR, y + 68, colR, 24, fill=CREAM2, accent=MUST)
para(xR + 7, y + 71.5, colR - 14,
     "**What we are NOT claiming tonight:** it does not drive your editing timeline, does not judge your cut, and never "
     "generates free work — **every agent-made generation spends credits.**",
     size=8.9, lh=4.4)
para(M, y + 96, CW, "<m>Results land in your normal Higgsfield Assets, tagged as agent-made — so nothing is stranded inside the chat.</m>",
     size=8.6, lh=4)
note("The credit-balance question is Higgsfield’s own official connection test. It’s also a lovely first “the machine answered!” moment for the room.")

# ============================================================
# PAGE 10 — THE LOOP (diagram)
# ============================================================
y = new_page("The whole game, one picture", "It’s a loop, not a vending machine")
bw, bh, gap = 80, 27, 12.5
r1, r2 = y + 6, y + 47
loop_boxes = [
    (M + 0 * (bw + gap), r1, "1 · YOUR IDEA", "rough is fine — a mood, an event, a half-sentence", INK, CARD),
    (M + 1 * (bw + gap), r1, "2 · TELL THE AGENT", "what and why, in ordinary words", TERRA_D, CARD),
    (M + 2 * (bw + gap), r1, "3 · AGENT DOES A STEP", "plans it — or calls a Higgsfield tool", TEAL, TEAL_T),
    (M + 2 * (bw + gap), r2, "4 · SOMETHING COMES BACK", "a plan, a frame, a clip", TEAL, TEAL_T),
    (M + 1 * (bw + gap), r2, "5 · YOU WATCH", "with director’s eyes, not operator’s hands", TERRA_D, CARD),
    (M + 0 * (bw + gap), r2, "6 · KEEP · FIX · KILL", "your call. always.", TERRA_D, MUST_T),
]
for bx, by, t, s, tc, fl in loop_boxes:
    card(bx, by, bw, bh, fill=fl)
    para(bx + 4, by + 3.2, bw - 8, f"**{t}**", size=8.8, color=tc, lh=4)
    para(bx + 4, by + 9.5, bw - 8, s, size=8.4, color=MUTED, lh=4)
arrow(M + bw, r1 + bh / 2, M + bw + gap, r1 + bh / 2)
arrow(M + 2 * bw + gap, r1 + bh / 2, M + 2 * bw + 2 * gap, r1 + bh / 2)
arrow(M + 2 * (bw + gap) + bw / 2, r1 + bh, M + 2 * (bw + gap) + bw / 2, r2, col=TEAL)
arrow(M + 2 * (bw + gap), r2 + bh / 2, M + bw + gap + bw, r2 + bh / 2)
arrow(M + bw + gap, r2 + bh / 2, M + bw, r2 + bh / 2)
# return arrow: box6 top -> box1 bottom
arrow(M + bw / 2, r2, M + bw / 2, r1 + bh, col=MUST, lw=1.3)
para(M + bw / 2 + 3, r1 + bh + 2, 90, "**again, until it’s right** — each lap is cheap", size=8.6, color=TERRA_D, lh=4)
para(M, r2 + bh + 8, CW,
     "Expect **lap three** to be where it starts getting good. The agent isn’t supposed to nail your taste on the first try — it’s supposed "
     "to hand you something real to react to, fast, so your taste has something to push against.",
     size=11, lh=5.6)
note("Walk this picture once with the showcase story before the step pages: ‘watch how often a human makes a decision.’ (Answer: every lap.)")

# ============================================================
# PAGE 11 — SCENARIO
# ============================================================
y = new_page("Tonight’s demo", "One small win: a fifteen-second showcase promo")
para(M, y, CW,
     "Our pretend job: **a 15-second promo inviting people to the spring student film showcase.** Small on purpose, and that’s the point. "
     "Tonight’s trophy is not a finished promo — it’s **one full lap around the loop**, so your hands remember the shape of it.",
     size=11.5, lh=5.8)
y += 19
para(M, y, CW, "Three steps, each on its own page, and we’ll say out loud who does what at every one:", size=11, lh=5.6)
y += 9
items11 = [
    ("Step 1", "Idea → **shot list**", "pure planning — works with any assistant, zero setup, zero credits"),
    ("Step 2", "Shot → **one key frame**", "the agent calls Higgsfield for a still you can judge — cheap, fast, low-stakes"),
    ("Step 3", "Frame → **one moving draft**", "the kept frame becomes a short clip with a deliberate camera move"),
]
for i, (s, t, d) in enumerate(items11):
    x = M + i * ((CW - 12) / 3 + 6)
    w3 = (CW - 12) / 3
    card(x, y, w3, 26, accent=TERRA if i < 2 else TEAL)
    para(x + 6, y + 3.5, w3 - 12, f"<t>**{s}**</t>", size=8.4, lh=3.9)
    para(x + 6, y + 8.4, w3 - 12, t, size=10.5, lh=4.8)
    para(x + 6, y + 14.6, w3 - 12, d, size=8.4, color=MUTED, lh=4)
y += 31
card(M, y, CW, 15, fill=CREAM2)
para(M + 6, y + 3, CW - 12,
     "**The cast:** <t>**YOU**</t> — director, taste, final yes · <t>**THE AGENT**</t> — planning & tool-wrangling · "
     "<g>**HIGGSFIELD**</g> — makes the actual media",
     size=9.6, lh=4.6)
note("Swap in a real event from your own community — a screening, a gig, a fund-raiser. Familiar stakes make the demo land much harder.")

# ============================================================
# PAGES 12–14 — WALKTHROUGH STEPS
# ============================================================
def loop_progress(y, done):
    names = ["1 · idea", "2 · tell", "3 · agent acts", "4 · result", "5 · you watch", "6 · keep-fix-kill"]
    cw_, gap = 40, 6
    total = 6 * cw_ + 5 * gap
    x0 = M + (CW - total) / 2
    pdf.set_font("dej", "B", 7.8); pdf.set_text_color(*MUTED)
    pdf.set_xy(M, y); pdf.cell(CW, 3.4, "— WHERE WE ARE IN THE LOOP —", align="C")
    y += 5
    for i, n in enumerate(names):
        x = x0 + i * (cw_ + gap)
        on = i < done
        rect(x, y, cw_, 8.5, fill=TEAL_T if on else CREAM2, edge=TEAL if on else LINE, lw=0.4)
        pdf.set_font("dej", "B" if on else "", 7.4)
        pdf.set_text_color(*(TEAL if on else MUTED))
        pdf.set_xy(x, y + 2.6); pdf.cell(cw_, 3.4, n, align="C")
    return y + 8.5

def step_page(kick, ttl, rows, lap):
    y = new_page(kick, ttl, verify_legend=True)
    for i, (lab, txt) in enumerate(rows):
        y = qa_row(M, y, CW, lab, txt, size=10.6, fill=CARD if i % 2 == 0 else None) + 3.0
    loop_progress(y + 2.5, lap)
    return y

step_page("Walkthrough · Step 1 of 3", "From fuzzy idea to shot list — no connection needed", [
    ("YOU SAY", "“I’m making a 15-second promo for our spring student film showcase. Mood: handmade, a little mischievous, "
     "ends on the date. Give me six shots?”"),
    ("THE AGENT DOES", "Thinks in beats: proposes six shots with rough timings, a hook shot up front, and one line of voice-over. "
     "Zero credits spent — this is the planning muscle, and <t>**any assistant can do this part**</t>. Seriously, any of them."),
    ("HIGGSFIELD DOES", "Nothing yet. The machine room stays quiet and your wallet stays shut."),
    ("YOU REVIEW", "Cross out shot 4 (too moody for us) and ask for “more paper-craft, less lens flare.” Thirty seconds of taste, applied."),
    ("YOU NOW HAVE", "A shot list you’d actually shoot — in about four minutes, without booking a meeting room."),
], lap=3)
note("Land this quietly: that step alone saves real prep time, and it worked before anything was connected to anything.")

step_page("Walkthrough · Step 2 of 3", "One frame you can judge — the agent calls Higgsfield", [
    ("YOU SAY", "“Take shot 1 and make me one key frame to react to — paper-craft look. And tell me the credit cost first, "
     "then wait for my yes.”"),
    ("THE AGENT DOES", "Checks the price and <t>**waits**</t>. On your yes, it writes the generation request — look, framing, format — "
     "and calls the Higgsfield image tool. [verified: image generation + “cost first” prompting are both in the docs]"),
    ("HIGGSFIELD DOES", "Generates the frame. It lands in your normal Higgsfield Assets, tagged as agent-made, so you also own it on the website. [verified]"),
    ("YOU REVIEW", "“Warmer. Less symmetry. Keep the scissors.” (You are now directing software the way you’d direct a storyboard artist.)"),
    ("YOU NOW HAVE", "A key frame — plus the one sentence you’ll reuse forever: **“cost first, wait for my yes.”**"),
], lap=5)
note("That sentence is Higgsfield’s own suggested best practice from their docs. Steal it proudly and teach it as a reflex.")

step_page("Walkthrough · Step 3 of 3", "Same shot, now in motion — with a camera move on purpose", [
    ("YOU SAY", "“Animate the frame we kept: slow push-in, about four seconds, gentle. Then one alternate take with a slightly "
     "faster push.”"),
    ("THE AGENT DOES", "Uses the kept frame as the starting image and requests two versions — same scene, two camera behaviors. "
     "[verified: video generation + referencing an earlier generation]"),
    ("HIGGSFIELD DOES", "Renders two short drafts into your Assets. Credits spent: exactly what you approved, not a penny more."),
    ("YOU REVIEW", "The slow push wins the opening; the faster take is filed under “maybe shot 5.” Notice who decided. "
     "<t>**It wasn’t the agent.**</t>"),
    ("YOU NOW HAVE", "One lap, complete: shot list + key frame + two motion drafts. Next lap: voice-over, the date card, the other five shots."),
], lap=6)
note("If someone asks about fancier control: yes, a “motion control” mode exists that accepts a motion-reference video [verified] — and no, we do not need it tonight. Chapter two.")

# ============================================================
# PAGE 15 — THE COPYABLE PROMPT
# ============================================================
y = new_page("Steal this prompt", "The one-sentence starter")
card(M, y, CW, 34, fill=(250, 246, 238), accent=TERRA)
para(M + 7, y + 4, CW - 14,
     "“Help me turn this rough idea into the next useful video-production step: a 15-second promo for our spring student film "
     "showcase — handmade mood, a bit mischievous, ends on the date. Ask me only the questions you actually need. Then use the "
     "available Higgsfield tools to draft one key image — tell me the credit cost first and wait for my go-ahead. Show me what "
     "you did, and give me a result I can react to.”",
     font="mono", size=9.6, lh=5.0, color=INK)
y += 38.5
para(M, y, 90, "**Why this works:**", size=10.5, lh=5)
y2 = y
why = [
    "It gives **real context** — event, length, mood. Agents run on specifics the way crews do.",
    "“Only the questions you actually need” means no twenty-question interviews.",
    "It names **one concrete, allowed action** — nothing vague, nothing heroic.",
    "The cost-first clause keeps your **wallet in the director’s chair**.",
    "“Something I can react to” asks for a **sketch, not a masterpiece** — sketches invite taste.",
    "And notice the language: none. It’s a brief. If you can brief a camera operator, you can brief an agent.",
]
y2 += 6
for i, wtxt in enumerate(why):
    col = i % 2; row = i // 2
    x = M + col * (CW / 2)
    yy = y2 + row * 15.5
    para(x + 2, yy, 3.5, "**•**", size=9.4, color=TERRA, lh=4.2)
    para(x + 7, yy, CW / 2 - 12, wtxt, size=9.4, lh=4.3)
note("Invite everyone to photograph this page. The prompt matters less than the posture: brief like a director, review like a director.")

# ============================================================
# PAGE 16 — REAL PRACTICE
# ============================================================
y = new_page("Back at your desk", "Where this actually pays rent", verify_legend=True)
prac = [
    ("Developing a visual concept", "Talk it out, then ask for draft frames on demand to argue with.", "works today"),
    ("Shot lists & pre-pro paperwork", "Pure agent muscle — no connection, no credits, no excuses left.", "always available"),
    ("Alternate directions", "“Same brief, three flavors” is one sentence. Each take spends credits — budget for it.", "works today"),
    ("Rough versions & previz", "Kept frame → short motion drafts with named camera moves.", "works today"),
    ("Consistent characters", "Call your Soul character by name across shots and sessions.", "works today · [VERIFY plan]"),
    ("Voice-over & dub drafts", "Audio from the same chat. (Heads-up: the ChatGPT plugin skips audio.)", "works today"),
    ("Repurposing", "Short clips from a long video; reframe for vertical. Mind footage rights, as ever.", "works today"),
    ("The boring 40%", "Briefs, checklists, plans, status summaries — the agent’s natural habitat.", "always available"),
]
gx, gy = M, y + 1
cw2, ch2 = (CW - 5) / 2, 24.5
for i, (t, d, s) in enumerate(prac):
    col, row = i % 2, i // 2
    x = gx + col * (cw2 + 5); yy = gy + row * (ch2 + 2.6)
    card(x, yy, cw2, ch2)
    para(x + 4.5, yy + 2.8, cw2 - 34, f"**{t}**", size=9.4, lh=4.2)
    para(x + 4.5, yy + 8.6, cw2 - 9, d, size=8.2, color=MUTED, lh=3.95)
    ok = "[VERIFY" not in s
    sw = _w(s, "dej", "B", 6.8) + 5
    chip(x + cw2 - sw - 2.5, yy + 2.5, s, fill=TEAL_T if ok else MUST_T,
         col=TEAL if ok else TERRA_D, size=6.8, h=5.4)
yy = gy + 4 * (ch2 + 2.6) + 1
para(M, yy, CW,
     "<m>“Works today” = listed in Higgsfield’s current docs as of Sept 3, 2026. Professional habit: try each once yourself before promising a crowd.</m>",
     size=8, lh=3.9)
note("Open the floor for one minute: which row would save **you** the most time this month? Their answers are your best word-of-mouth.", y=yy + 6)

# ============================================================
# PAGES 17–18 — FEARS
# ============================================================
def fear_page(kick, ttl, fears, pg_note):
    y = new_page(kick, ttl)
    for q, a in fears:
        card(M, y, CW, 29.5, accent=TERRA)
        para(M + 7, y + 3.6, CW - 14, f"“{q}”", font="serj", style="B", size=12, lh=5.4)
        para(M + 7, y + 11.5, CW - 14, a, size=9.6, lh=4.6)
        y += 32
    note(pg_note)
    return y

fear_page("The worries, taken seriously · 1 of 2", "Fair questions deserve straight answers", [
    ("I’m not technical.",
     "You don’t need to be. Setup is: paste one address, sign in once, talk normally. If you can export a ProRes with the "
     "correct audio mapping, you are **wildly overqualified** for this."),
    ("The agent will replace my creative judgment.",
     "It can’t — it doesn’t have any. Watch the demo pages again: it proposed, you disposed. **Every lap ends in a human decision.** "
     "That’s the design, not a limitation."),
    ("I already know video software.",
     "Perfect — you’re exactly who this is for. The agent never touches your timeline or your NLE license. It **feeds** them: "
     "shot lists, reference frames, drafts, voice-over tests. Your craft stays yours; the legwork gets lighter."),
], "Never argue with these worries — each one is perfectly rational. Show the loop picture again; the loop is the answer.")

fear_page("The worries, taken seriously · 2 of 2", "…and the quieter ones too", [
    ("I have plenty of tokens, but no idea what to ask for.",
     "Completely normal — it’s like owning film stock in a quiet week. The next page is a fill-in-the-blanks recipe, and the "
     "exercise at the end is your first shoot. **Tokens expire; habits don’t.**"),
    ("I don’t want an AI making creative decisions for me.",
     "Then don’t let it — generation is not decision. The loop puts a gate between “made” and “used,” and **you are the gate**. "
     "If a workflow ever hides that gate, leave the workflow, not your judgment."),
    ("This sounds like another complicated platform to learn.",
     "It’s mostly one address pasted into an app you already have, then talking like a director. Give it a month; if it earns "
     "nothing, unplug it. No sunk cathedral, no hurt feelings."),
], "With experienced creators, respect lands better than reassurance. Their skepticism is professional equipment, working as intended.")

# ============================================================
# PAGE 19 — TOKENS → WORKFLOW
# ============================================================
y = new_page("The quiet truth", "“I have tokens” is not a plan")
para(M, y, CW,
     "Tokens are film stock. Lovely to own, completely inert on the shelf. A **workflow** is knowing your next three shots. "
     "Here’s the five-part recipe that closes the gap — it works in any assistant, connected or not:",
     size=11, lh=5.6)
y += 15.5
parts = [("CONTEXT", "what the project actually is"), ("GOAL", "the very next useful thing"),
         ("CONSTRAINTS", "length · mood · budget · deadline"), ("ACTION", "one concrete, allowed step"),
         ("REVIEW", "“I’ll know it’s right if…”")]
bw5 = (CW - 4 * 5) / 5
for i, (t, d) in enumerate(parts):
    x = M + i * (bw5 + 5)
    card(x, y, bw5, 20, accent=MUST if i in (1, 4) else None)
    para(x + 4, y + 3, bw5 - 8, f"**{t}**", size=9.6, color=TERRA_D, lh=4.2)
    para(x + 4, y + 8.8, bw5 - 8, d, size=8.1, color=MUTED, lh=3.9)
    if i < 4:
        pdf.set_font("dej", "B", 10); pdf.set_text_color(*TERRA)
        pdf.set_xy(x + bw5 + 0.7, y + 8); pdf.cell(4, 4, "+")
y += 25
para(M, y, CW, "**Filled in, it sounds like this:**", size=10.5, lh=5)
y += 7
card(M, y, CW, 26, fill=TEAL_T, accent=TEAL)
para(M + 7, y + 3.5, CW - 14,
     "<m>CONTEXT</m> promo for the spring showcase · <m>GOAL</m> a test opening frame · <m>CONSTRAINTS</m> 15 seconds total, "
     "paper-craft mood, tiny credit budget · <m>ACTION</m> draft one frame, cost-first · <m>REVIEW</m> I’ll know it’s right "
     "when it looks handmade, not glossy.",
     size=9.8, lh=4.8)
para(M, y + 30.5, CW,
     "That’s the whole pattern. Five pieces of information you already carry around — said out loud, in order, to something that never forgets them.",
     size=10.5, color=MUTED, lh=5.2)
note("This page doubles as a handout: five blanks on paper, filled in during the exercise. Nobody needs usernames and passwords to practice this part.")

# ============================================================
# PAGE 20 — HUMAN IN THE LOOP
# ============================================================
y = new_page("The most important page", "The deal: you’re the director of this too")
col_w = (CW - 10) / 3
cols = [
    ("YOU BRING", TERRA, TERRA_T, ["taste", "context", "priorities", "the final yes"]),
    ("THE AGENT HANDLES", TEAL, TEAL_T, ["drafts & variations", "tool-wrangling", "the boring 40%", "remembering details"]),
    ("YOU DECIDE", TERRA, MUST_T, ["what ships", "what dies", "what’s next", "when to stop"]),
]
for i, (h, ac, fl, its) in enumerate(cols):
    x = M + i * (col_w + 5)
    card(x, y, col_w, 40, fill=fl)
    para(x + 6, y + 4, col_w - 12, f"**{h}**", size=9.8, color=ac if ac != TERRA else TERRA_D, lh=4.4)
    yy = y + 11
    for it in its:
        para(x + 6, yy, col_w - 12, it, size=9.6, lh=4.4)
        yy += 6
y += 45
card(M, y, CW, 18, accent=TERRA)
para(M + 7, y + 3.2, CW - 14,
     "Recommended first words in any session, quoted straight from Higgsfield’s own docs:",
     size=9.2, color=MUTED, lh=4.2)
para(M + 7, y + 8.4, CW - 14,
     "“Before generating anything, tell me the credit cost and wait for my confirmation.”",
     font="serj", style="B", size=12.5, color=TERRA_D, lh=5.6)
y += 23
para(M, y, CW,
     "**Nothing spends, nothing generates, nothing ships without your nod.** If a workflow ever makes you feel like the audience "
     "instead of the director, the workflow is set up wrong. Fix the setup — never yourself.",
     size=11, lh=5.6)
note("Slow down here and give it air. For a room full of craftspeople, this page — not the technology — is what makes tonight safe.")

# ============================================================
# PAGE 21 — OPEN MONTAGE / DEEP END
# ============================================================
y = new_page("Optional peek · chapter two", "Where this road leads (no homework)", verify_legend=True)
para(M, y, CW,
     "Once the small loop feels ordinary, there’s a deeper end of the pool. The most interesting current example is **Open Montage**, "
     "an open-source project that turns a coding assistant into something closer to a whole production office: you describe a video "
     "in a sentence, and a crew of agents researches, scripts, storyboards, generates assets, and assembles a cut for your review. "
     "It runs on your own machine — no cloud login, no shiny website.",
     size=10.8, lh=5.4)
y += 26
card(M, y, CW, 26, fill=MUST_T, accent=MUST)
para(M + 7, y + 3.5, CW - 14, "**Honesty corner**", size=9.4, lh=4.2)
para(M + 7, y + 8.6, CW - 14,
     "That description comes from third-party write-ups (Aug–Sep 2026), not from running it ourselves. **[VERIFY]** Treat star counts, "
     "pipeline numbers, and superlatives as stage-whispers, not facts — or check its GitHub page yourself before quoting. Early users "
     "both rave and grumble, which is the normal sound of frontier open source.",
     size=9, lh=4.4)
y += 30.5
para(M, y, CW,
     "Do you need it tonight? Not remotely. It’s simply nice to know the road keeps going — from “one shot at a time” all the way to "
     "“an assistant that organizes a small crew for you.” Start with tonight’s loop; everything else is the same idea wearing bigger boots.",
     size=10.8, lh=5.4)
note("If asked “should we adopt it?”: try the small loop for a month first. Tools change monthly; the habit you build transfers to all of them.")

# ============================================================
# PAGE 22 — EXERCISE
# ============================================================
y = new_page("Ten minutes, starting now", "Your first lap — pick a lane")
col_w = (CW - 6) / 2
card(M, y, col_w, 74, accent=TERRA)
para(M + 7, y + 4, col_w - 14, "**LANE A · CONNECTED** <m>(if tonight’s link is set up)</m>", size=8.8, color=TERRA_D, lh=4.2)
laneA = [
    "Handshake: ask **“What’s my Higgsfield credit balance?”** If it answers with a number, the doorway works. (That’s their official test.)",
    "Paste the page-15 prompt, swapping in **your own rough idea** — a real one from your desk.",
    "Approve **one** draft. Then react like a director: two adjectives and a verb.",
    "Ask for one change. Watch the loop turn.",
    "**Trophy:** one frame you’re willing to show a neighbor.",
]
sy = y + 10.5
for i, s in enumerate(laneA):
    pdf.set_font("dej", "B", 10); pdf.set_text_color(*TERRA)
    pdf.set_xy(M + 7, sy + 0.5); pdf.cell(5.5, 4, f"{i+1}")
    sy = para(M + 13.5, sy, col_w - 20.5, s, size=8.9, lh=4.25) + 3.2
x2 = M + col_w + 6
card(x2, y, col_w, 74, accent=TEAL)
para(x2 + 7, y + 4, col_w - 14, "**LANE B · NO SETUP AT ALL** <m>(works everywhere, forever)</m>", size=8.8, color=TEAL, lh=4.2)
para(x2 + 7, y + 10.5, col_w - 14, "Open any AI assistant — the one you already have — and paste:", size=8.9, lh=4.2)
rect(x2 + 7, y + 15.5, col_w - 14, 17, fill=CREAM2)
para(x2 + 10, y + 17.5, col_w - 20,
     "“Here’s my rough video idea: ______. Turn it into 5 numbered production steps. For each step, flag which parts a connected "
     "video tool could do for me — and which parts need my human judgment.”",
     font="mono", size=8.2, lh=4.1)
laneB = [
    "Circle one **tool-shaped** step and one **judgment-shaped** step.",
    "Notice: you just designed an agentic workflow. With a pencil.",
    "**Trophy:** the shape of a workflow with your name on it.",
]
sy = y + 35.5
for i, s in enumerate(laneB):
    pdf.set_font("dej", "B", 10); pdf.set_text_color(*TEAL)
    pdf.set_xy(x2 + 7, sy + 0.5); pdf.cell(5.5, 4, f"{i+1}")
    sy = para(x2 + 13.5, sy, col_w - 20.5, s, size=8.9, lh=4.25) + 3
para(M, y + 78.5, CW,
     "Then swap with a neighbor. The best question to ask each other: **“Where did it surprise you?”**",
     size=10.5, lh=5.2)
note("Lane B is secretly the entire philosophy in one exercise: the agent plans, tools make things, humans judge. Many people find B more convincing than the demo.")

# ============================================================
# PAGE 23 — CLOSING / CTA
# ============================================================
y = new_page("To take home", "Agents aren’t a different art form")
cx0 = M + 178
card(cx0, y, CW - 178, 80, fill=MUST_T, accent=MUST)
para(cx0 + 6, y + 4, CW - 178 - 12, "**THIS WEEK’S HOMEWORK** <m>(small, promise)</m>", size=8.2, color=TERRA_D, lh=4)
hw = ["Take **one rough idea** — a real one.",
      "Get **one shot list** (any assistant can do this).",
      "Make **one draft** — frame or clip, your call.",
      "Bring whatever happens to the next session — glorious or hilariously broken. We take it apart together; first round of troubleshooting is on me."]
sy = y + 10.5
for i, s in enumerate(hw):
    pdf.set_font("dej", "B", 9.5); pdf.set_text_color(*TERRA)
    pdf.set_xy(cx0 + 6, sy + 0.4); pdf.cell(4, 3.8, "→")
    sy = para(cx0 + 11.5, sy, CW - 178 - 18, s, size=8.9, lh=4.3) + 3.4
ly = para(M, y, 166,
          "They’re one more crew position on a set you’ve already been running for years — a way to keep projects moving "
          "on the nights when energy is low but taste is still wide awake.",
          size=12.5, font="serj", style="B", lh=6.2)
ly += 4
ly = para(M, ly, 166,
          "You already understand video. That part was never in question. Starting tonight, there’s an extra pair of hands "
          "for the parts that slow you down — the blank-page part, the fourteenth-variation part, the “someone has to "
          "organize this” part.",
          size=10.5, lh=5.4)
y2 = max(ly, sy) + 8
card(M, y2, CW, 16.5, fill=TEAL_T, accent=TEAL)
para(M + 7, y2 + 3.4, CW - 14,
     "**First-timer tip:** start with images (cheap, fast, easy to judge) before motion (pricier, slower, harder). "
     "Confidence is a resource too — budget it like credits.",
     size=9.8, lh=4.8)
note("End on generosity, not features. Then open the floor — the Q&A after this talk is always about people’s own projects. Budget time for it.")

# ============================================================
# PAGE 24 — GLOSSARY
# ============================================================
y = new_page("Translate-on-demand", "Glossary: ten terms, zero snobbery")
gloss = [
    ("Agent", "an AI assistant that can use tools you’ve allowed — it does steps, not just suggestions."),
    ("Agentic workflow", "working with an agent in laps: brief → it acts → you review → next lap."),
    ("MCP (Model Context Protocol)", "the “standard socket” — a shared, open way for assistants and tools to connect."),
    ("Connector", "the plug end: the named link you add inside your assistant (e.g. “Higgsfield” in Claude’s settings)."),
    ("Tool call", "one visible action the agent takes through the connection — e.g. “generate one image.” You see each one."),
    ("Prompt", "your brief to the assistant. Plain words beat clever words."),
    ("Credits", "Higgsfield’s pay-per-generation meter. Agent-made generations always spend them."),
    ("Soul (Higgsfield)", "their consistent-character feature — a cast member whose face survives across shots."),
    ("Assets", "your media library on higgsfield.ai; agent-made results land here, tagged as such."),
    ("Human-in-the-loop", "the rule that a person reviews and approves before anything ships. Tonight’s entire religion."),
]
col_w = (CW - 8) / 2
for i, (t, d) in enumerate(gloss):
    col, row = i % 2, i // 2
    x = M + col * (col_w + 8); yy = y + row * 18.5
    card(x, yy, col_w, 16.5)
    para(x + 4.5, yy + 2.6, 44, f"**{t}**", size=8.8, color=TERRA_D, lh=4)
    para(x + 50, yy + 2.6, col_w - 54, d, size=8.2, color=MUTED, lh=3.95)
note("Photograph this page too. Vocabulary is half the intimidation — naming things kindly disarms it.", y=y + 5 * 18.5 + 3)

# ============================================================
# PAGE 25 — APPENDIX A1: SETUP (verified)
# ============================================================
y = new_page("Appendix · the technical stuff, moved politely to the back", "A1 · The connection, exactly", verify_legend=True)
para(M, y, CW,
     "Everything on this page comes from Higgsfield’s own Help Center, re-read on **September 3, 2026**. If you’re reading "
     "this much later, skim the two source articles on page 26 and update whatever drifted.",
     size=9.5, color=MUTED, lh=4.6)
y += 12
col_w = (CW - 6) / 2
card(M, y, col_w, 72, accent=TEAL)
para(M + 7, y + 4, col_w - 14, "**THE FACTS OF THE DOORWAY**", size=8.8, color=TEAL, lh=4.2)
a1 = [
    ("Doorway address (MCP server)", True),
    ("Sign-in: authorize with your Higgsfield account (OAuth — no API key to copy or leak)", False),
    ("Requirement: an active **paid** Higgsfield subscription", False),
    ("Your results appear in Higgsfield → Assets, tagged as agent-made", False),
    ("Official connection test: ask “What is my Higgsfield credit balance?”", False),
]
sy = y + 10.5
para(M + 7, sy, col_w - 14, "Doorway address **(MCP server URL)**:", size=8.8, lh=4.1)
rect(M + 7, sy + 5.5, col_w - 14, 7.2, fill=CREAM2)
pdf.set_font("mono", "B", 9.2); pdf.set_text_color(*TERRA_D)
pdf.set_xy(M + 10, sy + 7.4); pdf.cell(col_w - 20, 4, "https://mcp.higgsfield.ai/mcp")
sy += 15.5
for t, _ in a1[1:]:
    pdf.set_font("dej", "B", 8.6); pdf.set_text_color(*TEAL)
    pdf.set_xy(M + 7, sy + 0.5); pdf.cell(4, 3.6, "✓")
    sy = para(M + 12, sy, col_w - 19, t, size=8.6, lh=4.05) + 2.6
x2 = M + col_w + 6
card(x2, y, col_w, 72, accent=TERRA)
para(x2 + 7, y + 4, col_w - 14, "**CONNECTING, PER APP** <m>(each is “add + sign in once”)</m>", size=8.8, color=TERRA_D, lh=4.2)
apps = [
    ("Claude (web & desktop)", "Settings → Connectors → Add custom connector → paste the address → Connect → sign in."),
    ("ChatGPT", "the official **Higgsfield plugin** from the plugin directory. (No audio or website-building via ChatGPT.)"),
    ("Cursor", "find Higgsfield in **Customize → Marketplace** → Add → sign in."),
    ("Claude Code · OpenClaw · Hermes", "these install the **Higgsfield CLI** themselves; you just approve and sign in via the browser."),
    ("Any other MCP-compatible agent", "paste the same doorway address in its connector settings."),
]
sy = y + 11
for h, d in apps:
    para(x2 + 7, sy, col_w - 14, f"**{h}** — {d}", size=8.6, lh=4.05)
    sy += measure(col_w - 14, f"**{h}** — {d}", size=8.6, lh=4.05) + 3.2
note("Everything here is deliberately boring: one address, one sign-in, one paid plan. The magic is what you say after it’s connected.")

# ============================================================
# PAGE 26 — APPENDIX A2: OPERATIONS + MONEY + SOURCES
# ============================================================
y = new_page("Appendix · continued", "A2 · What it may do, what it costs, where we checked", verify_legend=True)
card(M, y, CW, 37, accent=TEAL)
para(M + 7, y + 3.5, CW - 14, "**OPERATIONS LISTED IN THE DOCS** <m>(checked Sept 3, 2026)</m>", size=8.8, color=TEAL, lh=4.2)
ops = [
    "Image & video generation, all models (name the model in ordinary words)",
    "Upscale · background removal · expand image / reframe video",
    "Kling 3.0 Motion Control (character image + motion-reference clip)",
    "Soul characters & reference Elements, called by name",
    "Audio: voiceover, voice cloning, voice change, video dubbing",
    "Personal Clipper: YouTube video → short clips (mind footage rights)",
    "“Skills”: preset multi-step workflows (marketing, UGC, motion & design…)",
    "Utility: check credit balance, list generations & uploads",
]
ocw = (CW - 14) / 2
for i, o in enumerate(ops):
    col, row = i // 4, i % 4
    x = M + 7 + col * ocw; yy = y + 9.5 + row * 6.6
    pdf.set_font("dej", "B", 8.4); pdf.set_text_color(*TEAL)
    pdf.set_xy(x, yy + 0.4); pdf.cell(4, 3.4, "✓")
    para(x + 5, yy, ocw - 10, o, size=8.3, lh=3.95, max_lines=2)
y += 41
card(M, y, CW, 27, accent=MUST)
para(M + 7, y + 3.5, (CW - 14) / 2, "**MONEY & FINE PRINT**", size=8.8, color=TERRA_D, lh=4.2)
para(M + 7, y + 9.5, (CW - 21) / 2,
     "**Every agent-made generation deducts credits** at standard rates — even on web plans with free or unlimited use. "
     "The connection falls under Higgsfield’s **Developer Terms**: you’re responsible for what an agent generates through your account.",
     size=8.5, lh=4.1)
x2 = M + (CW - 14) / 2 + 7
hline(x2 - 3.5, y + 5, x2 - 3.5)
pdf.line(x2 - 3.5, y + 5, x2 - 3.5, y + 22)
para(x2, y + 3.5, (CW - 21) / 2, "**PASSING REFERENCE IMAGES**", size=8.8, color=TERRA_D, lh=4.2)
para(x2, y + 9.5, (CW - 21) / 2,
     "The agent can’t see files pasted into the chat. Tell it what you want to use and it opens an **upload window** "
     "right in the conversation (or give it a public image link, or the name of a past generation).",
     size=8.5, lh=4.1)
y += 31
card(M, y, CW, 26, fill=CREAM2, accent=TERRA)
para(M + 7, y + 3.5, CW - 14, "**SOURCES (all re-read Sept 3, 2026)**", size=8.4, color=TERRA_D, lh=4)
srcL = [
    "higgsfield.ai/creator-hub/help-center/integrations/what-is-higgsfield-mcp",
    "higgsfield.ai/creator-hub/help-center/integrations/how-do-i-connect-higgsfield-to-ai-agent",
]
srcR = [
    "higgsfield.ai/claude-ai-video-generator · higgsfield.ai/skills",
    "Open Montage: third-party write-ups (aitecharchive.com · riffkit.ai) — [VERIFY] on GitHub before quoting any numbers",
]
for xi, group in [(M + 7, srcL), (x2, srcR)]:
    sy = y + 9.5
    for s in group:
        pdf.set_font("dej", "B", 7.6); pdf.set_text_color(*TERRA)
        pdf.set_xy(xi, sy + 0.3); pdf.cell(3.5, 3.2, "→")
        sy = para(xi + 4.5, sy, (CW - 28) / 2, s, size=7.8, color=MUTED, lh=3.8) + 2.2
note("If you print handouts, this page and the next two are the handout. The talk is better conversational; let the paper carry the URLs.")

# ============================================================
# PAGE 27 — APPENDIX B: FULL WALKTHROUGH SCRIPT
# ============================================================
y = new_page("Appendix · the demo on one page", "A3 · The full walkthrough, copy-paste ready", verify_legend=True)
scripts = [
    ("SCRIPT 1 · PLANNING (any assistant, no connection, no credits)",
     "“I’m making a 15-second promo for our spring student film showcase. Mood: handmade, a little mischievous, ends on the "
     "date. Give me six shots with rough timings and one line of voice-over.”",
     "Expect: six usable beats in under a minute. You cut shot 4; it rebalances the rest."),
    ("SCRIPT 2 · ONE FRAME (agent + Higgsfield, image generation)",
     "“Take shot 1 and make me one key frame to react to — paper-craft look. Tell me the credit cost first and wait for my yes.”",
     "Expect: a price, a pause, then one frame in your Assets. You review: “warmer, less symmetry, keep the scissors.”"),
    ("SCRIPT 3 · MOTION (agent + Higgsfield, video generation)",
     "“Animate the frame we kept: slow push-in, about four seconds, gentle. Then one alternate take with a slightly faster push.”",
     "Expect: two short drafts, charged as approved. You pick the slow one for the opening; file the fast one under shot 5."),
]
for h, p, e in scripts:
    para(M, y, CW, f"**{h}**", size=9.2, color=TEAL, lh=4.2)
    y += 5.4
    rect(M, y, CW, 11.5, fill=CREAM2)
    para(M + 4, y + 2, CW - 8, p, font="mono", size=8.2, lh=4.05)
    y += 13.8
    y = para(M, y, CW, f"<m>{e}</m>", size=8.4, lh=4) + 4.6
card(M, y, CW, 22, fill=MUST_T, accent=MUST)
para(M + 7, y + 3, CW - 14, "**If things go sideways on stage**", size=9.2, lh=4.2)
para(M + 7, y + 8.2, CW - 14,
     "Agent answers without using any tools → reconnect the connector (their own troubleshooting tip). · Wi-Fi dies → narrate over the "
     "screenshots from your checklist (page 28). · The frame comes back odd → congratulations, you’ve got the perfect excuse to model lap "
     "two out loud: “taste is why the loop exists.”",
     size=8.8, lh=4.3)
note("Prompts are scripts, not spells: keep the bones (context, questions-only-as-needed, one allowed action, cost-first), change every noun to fit your room.")

# ============================================================
# PAGE 28 — FINAL CHECKLIST
# ============================================================
y = new_page("Before showtime", "Packing checklist for the presenter", verify_legend=True)
para(M, y, CW, "Fifteen quiet minutes, the week of the talk. Check things off; cross out what you verified; delete what you can’t.",
     size=9.5, color=MUTED, lh=4.6)
y += 11
gw, gh = (CW - 5) / 2, 46.5
quads = [
    ("FACTS TO RE-VERIFY", [
        "Doorway address still **mcp.higgsfield.ai/mcp**",
        "Operation list on page 9 unchanged",
        "Paid-plan requirement + your credit balance",
        "Per-app connection list (Claude / ChatGPT plugin / Cursor / CLI)",
        "Open Montage numbers — or skip that page",
    ]),
    ("SCREENSHOTS & ASSETS TO COLLECT", [
        "Settings → Connectors, Higgsfield listed as active",
        "The Higgsfield sign-in / authorize window",
        "One good generated frame + one draft clip (fallback for dead Wi-Fi)",
        "Assets page showing an agent-made tag",
        "Links to pre-load: the two Help-Center articles + the page-15 prompt in your notes app",
    ]),
    ("SETUP TO CONFIRM ON THE DAY", [
        "Paid plan active; credits topped up past the demo’s appetite",
        "Balance question answered live once before the room arrives",
        "Claims to **remove** if unverified: model names beyond Soul/Veo/Kling/Seedance/Hailuo, preset counts, anything about timeline editing, Open Montage numbers",
    ]),
    ("ACCESSIBILITY & READABILITY", [
        "Big text held up at the back of the room? (body ≥ ~14pt equiv.)",
        "High contrast: warm ink on cream, no gray-on-gray",
        "One idea per page; numbered pages for “go back two” moments",
        "Describe every visual out loud; printed handout = appendix pages",
        "~30 min talk + 10 min exercise; leave air for project questions",
    ]),
]
for i, (h, items) in enumerate(quads):
    col, row = i % 2, i // 2
    x = M + col * (gw + 5); yy = y + row * (gh + 3)
    card(x, yy, gw, gh, accent=[TERRA, TEAL, MUST, TERRA][i])
    para(x + 6, yy + 3, gw - 12, f"**{h}**", size=8.8, color=TERRA_D, lh=4)
    iy = yy + 9
    for it in items:
        pdf.set_draw_color(*TERRA); pdf.set_line_width(0.4)
        pdf.rect(x + 6, iy + 0.9, 2.6, 2.6, style="D")
        iy = para(x + 11.5, iy, gw - 17.5, it, size=8.0, lh=3.85) + 2.3
para(M, y + 2 * gh + 6.5, CW, "<m>The exact demo prompt lives on page 15; the long script on page 27; the honesty tags live everywhere. Good luck — it’ll be great.</m>",
     size=8.4, lh=4)

# ---------------- done ----------------
assert PAGE["n"] == 28, f"expected 28 pages, got {PAGE['n']}"
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lights-camera-agent.pdf")
pdf.output(out)
print(f"wrote {out} ({PAGE['n']} pages)")
