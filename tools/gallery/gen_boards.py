"""Generate the six TrustSlice gallery boards (1200x800, 3:2).

Writes each board twice: as a Design-canvas .dc.html file and as a standalone
HTML page used to render the PNG. Same markup and CSS in both.
"""
import pathlib, sys

DC_DIR = pathlib.Path(sys.argv[1])        # design project folder (.dc.html)
HTML_DIR = pathlib.Path(sys.argv[2])      # standalone html for rendering
HTML_DIR.mkdir(parents=True, exist_ok=True)

NAVY, TEAL, DTEAL, MINT = "#112636", "#31BCA9", "#167D84", "#BFEFE6"
CARD, INK, GREY = "#F4F8F8", "#1B2A36", "#5F7380"
OK, NO, WAIT = "#1F9D55", "#C8432E", "#B07400"

CSS = f"""
body{{margin:0}}
.b{{position:relative;width:1200px;height:800px;overflow:hidden;font-family:Inter,system-ui,sans-serif;box-sizing:border-box;padding:56px 64px 84px;display:flex;flex-direction:column}}
.mid{{flex:1;display:flex;flex-direction:column;justify-content:center}}
.chk>span:first-child{{flex:none}}
.dark{{background:{NAVY};color:#fff}} .light{{background:#fff;color:{INK}}}
.bar{{position:absolute;left:0;top:0;width:1200px;height:8px;background:{TEAL}}}
.kick{{font-size:14px;font-weight:700;letter-spacing:.12em;color:{DTEAL}}} .dark .kick{{color:#9FC4CC}}
.h{{font-family:Poppins,sans-serif;font-weight:700;margin:10px 0 0;font-size:40px;line-height:50px}}
.sub{{font-size:19px;line-height:28px;color:{GREY};margin-top:8px}} .dark .sub{{color:#C9D6DB}}
.pill{{display:inline-block;background:{TEAL};color:{NAVY};font-weight:700;font-size:15px;letter-spacing:.1em;padding:7px 16px;border-radius:8px}}
.note{{position:absolute;left:64px;right:64px;bottom:40px;font-size:14px;line-height:20px;color:{GREY}}} .dark .note{{color:#9FC4CC}}
.ex{{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.1em;color:{DTEAL};border:1.5px solid {TEAL};border-radius:6px;padding:3px 8px;margin-right:8px}}
.dark .ex{{color:{MINT}}}
.card{{background:{CARD};border-radius:12px;box-sizing:border-box}}
.vcard{{background:#fff;color:{INK};border-radius:12px;padding:12px 18px;box-sizing:border-box}}
.vt{{font-size:13px;font-weight:700;letter-spacing:.1em;color:{DTEAL}}}
.vl{{font-size:16px;line-height:23px;display:flex;align-items:center;gap:8px}}
.y{{color:{OK};font-weight:700;width:18px;display:inline-block;text-align:center}} .n{{color:{NO};font-weight:700;width:18px;display:inline-block;text-align:center}} .w{{color:{WAIT};font-weight:700;width:18px;display:inline-block;text-align:center}}
.grey{{color:{GREY}}}
table.m{{border-collapse:separate;border-spacing:0 7px;width:100%;font-size:19px}}
table.m th{{text-align:center;font-size:14px;letter-spacing:.08em;color:{DTEAL};padding:6px 8px}}
table.m th:first-child{{text-align:left}}
table.m td{{background:{CARD};padding:15px 16px;text-align:center}}
table.m td:first-child{{text-align:left;font-weight:600;border-radius:10px 0 0 10px}}
table.m td:last-child{{border-radius:0 10px 10px 0;color:{GREY};font-size:16px}}
.step{{width:140px;height:196px;border-radius:12px;background:{CARD};padding:14px 12px;box-sizing:border-box;display:flex;flex-direction:column;gap:6px}}
.step b{{font-size:17px;letter-spacing:.06em;color:{NAVY}}} .step span{{font-size:15px;line-height:21px;color:{GREY}}} .step i{{font-style:normal;font-size:13px;line-height:18px;color:{DTEAL};font-family:ui-monospace,Menlo,monospace}}
.step.p{{background:{NAVY}}} .step.p b{{color:#fff}} .step.p span{{color:#C9D6DB}} .step.p i{{color:{MINT}}}
.arrow{{color:{TEAL};font-size:22px;font-weight:700;align-self:center}}
.gp{{display:inline-block;border:1.5px solid {TEAL};border-radius:18px;padding:6px 12px;font-size:14px;font-weight:600;color:{DTEAL};margin:0 8px 8px 0}}
.chk{{display:flex;gap:10px;font-size:18px;line-height:25px;margin-bottom:13px}}
.chk .y{{color:{TEAL}}}
.code{{font-family:ui-monospace,Menlo,monospace;font-size:13px;color:{DTEAL}}}
.row{{display:flex;align-items:center;gap:16px;border-radius:12px;padding:20px 24px;margin-bottom:12px;background:{CARD}}}
.row b{{width:330px;font-size:20px;flex:none}} .row span{{font-size:19px;color:{GREY}}}
.row.me{{background:{NAVY};color:#fff}} .row.me span{{color:{MINT}}}
"""

def check(): return '<span class="y">✓</span>'
def cross(): return '<span class="n">✗</span>'
def wait(): return '<span class="w"><svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="#B07400" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" style="vertical-align:-2px"><circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15 14"/></svg></span>'


BOARDS = {}

# ------------------------------------------------------------------ 01 Main (cover)
BOARDS["Main"] = ("TrustSlice cover", "dark", f"""
<div class="bar"></div>
<div class="kick">UGREEN AI NAS HACKATHON 2026 · AUTOMATE YOUR WORKFLOW</div>
<div style="margin-top:22px"><span class="pill">TRUSTSLICE</span></div>
<div id="hero" style="font-family:Poppins,sans-serif;font-weight:700;font-size:52px;line-height:64px;margin-top:18px;white-space:nowrap">Each team sees only what it needs.</div>
<div style="font-family:Poppins,sans-serif;font-weight:600;font-size:30px;line-height:40px;margin-top:4px">Share the know-how, <span style="color:{TEAL}">not the whole document.</span></div>
<svg width="1200" height="800" viewBox="0 0 1200 800" style="position:absolute;left:0;top:0" aria-hidden="true">
  <polygon points="284,452 452,500 452,560 284,610" fill="#9FC4CC" fill-opacity="0.14"/>
  <line x1="290" y1="530" x2="452" y2="530" stroke="#9FC4CC" stroke-width="2" stroke-opacity="0.7"/>
  <line x1="612" y1="530" x2="706" y2="404" stroke="{TEAL}" stroke-width="2"/>
  <line x1="612" y1="530" x2="706" y2="504" stroke="{TEAL}" stroke-width="2"/>
  <line x1="612" y1="530" x2="706" y2="604" stroke="{TEAL}" stroke-width="2"/>
  <line x1="612" y1="530" x2="706" y2="686" stroke="{TEAL}" stroke-width="2" stroke-dasharray="5 5"/>
</svg>
<div style="position:absolute;left:64px;top:414px;width:220px;height:232px;background:#fff;border-radius:12px;padding:20px;box-sizing:border-box;display:flex;flex-direction:column;gap:11px">
  <div style="font-size:12px;font-weight:700;letter-spacing:.1em;color:{NAVY}">CLIENT CONTRACT</div>
  <div style="height:10px;width:100%;border-radius:5px;background:{TEAL}"></div>
  <div style="height:10px;width:78%;border-radius:5px;background:{TEAL}"></div>
  <div style="height:10px;width:92%;border-radius:5px;background:#7AA7FF"></div>
  <div style="height:10px;width:64%;border-radius:5px;background:#7AA7FF"></div>
  <div style="height:10px;width:84%;border-radius:5px;background:#F0B44C"></div>
  <div style="height:10px;width:56%;border-radius:5px;background:#C3CCD4"></div>
  <div style="font-size:12px;color:{GREY}">synthetic example</div>
</div>
<div style="position:absolute;left:452px;top:450px;width:160px;height:160px;border:6px solid {TEAL};border-radius:50%;box-sizing:border-box;background:rgba(49,188,169,.08);display:flex;align-items:center;justify-content:center;text-align:center;font-size:16px;line-height:22px;font-weight:600;color:#E8F6F6">owner<br>reviews once</div>
<div style="position:absolute;left:430px;top:622px;width:204px;text-align:center;font-size:14px;color:#9FC4CC">exact approved words only</div>
<div style="position:absolute;left:706px;top:330px;width:430px;font-size:12px;font-weight:700;letter-spacing:.1em;color:{MINT}">THESE VIEWS ARE EXAMPLES, NOT A LIMIT</div>
<div class="vcard" style="position:absolute;left:706px;top:360px;width:430px;height:88px">
  <div class="vt">SALES</div>
  <div class="vl">{check()}value proposition, word for word</div>
  <div class="vl">{wait()}client, price: only on approved request</div>
</div>
<div class="vcard" style="position:absolute;left:706px;top:460px;width:430px;height:88px">
  <div class="vt">DELIVERY</div>
  <div class="vl">{check()}commitments, deadlines</div>
  <div class="vl grey">{cross()}fee, payment terms</div>
</div>
<div class="vcard" style="position:absolute;left:706px;top:560px;width:430px;height:88px">
  <div class="vt">FINANCE</div>
  <div class="vl">{check()}fee, payment terms</div>
  <div class="vl grey">{cross()}sales wording</div>
</div>
<div style="position:absolute;left:706px;top:664px;width:430px;height:40px;border:1.5px dashed {TEAL};border-radius:20px;box-sizing:border-box;display:flex;align-items:center;justify-content:center;font-size:15px;font-weight:600;color:#CFE9EA">+ any other view: Legal, HR, Auditor…</div>
<div style="position:absolute;left:64px;bottom:40px;font-size:17px;color:#C9D6DB">The original stays private → The owner approves parts → Each team gets its own file</div>
""")

# ------------------------------------------------------------------ 02 Views (matrix)
rows = [
    ("Value proposition", check(), cross(), cross()),
    ("Obligations", cross(), check(), cross()),
    ("Client name", wait(), check(), check()),
    ("Contract price", wait(), cross(), check()),
    ("Dates and deadlines", cross(), check(), check()),
    ("Payment terms", cross(), cross(), check()),
]
trs = "".join(f"<tr><td>{a}</td><td>{s}</td><td>{d}</td><td>{f}</td><td>you decide</td></tr>" for a, s, d, f in rows)
BOARDS["Views"] = ("TrustSlice: one contract, many views", "light", f"""
<div class="bar"></div>
<div class="kick">ONE CONTRACT, MANY VIEWS</div>
<div class="h">Each team sees its own slice, word for word.</div>
<div class="sub">Folder permissions work per file. TrustSlice works per passage.</div>
<div class="mid"><table class="m">
<tr><th>Part of the contract</th><th>SALES</th><th>DELIVERY</th><th>FINANCE</th><th>+ ANY OTHER VIEW</th></tr>
{trs}
</table>
<div style="margin-top:14px;font-size:17px;color:{GREY}">{check()} word for word &nbsp;&nbsp; {cross()} never in this view &nbsp;&nbsp; {wait()} only after the owner approves a request</div></div>
<div class="note"><span class="ex">EXAMPLE ONLY</span>Sales, Delivery and Finance illustrate one split of a synthetic contract. The administrator defines any views, in any number.</div>
""")

# ------------------------------------------------------------------ 03 Flow
steps = [("DEFINE", "admin writes a view card", "save-text", False),
         ("BUILD", "selected files only", "find · extract", False),
         ("REVIEW", "owner, once per source", "one decision", False),
         ("STAGE", "private folder", "save-text", True),
         ("VERIFY", "read-back, canaries", "cat · sha256sum", True),
         ("PUBLISH", "approved copy", "cpmv copy", False),
         ("ASK", "answers from the view", "qa --file", False)]
st = '<div class="arrow">→</div>'.join(
    f'<div class="step{" p" if p else ""}"><b>{n}</b><span>{d}</span><i>{t}</i></div>' for n, d, t, p in steps)
BOARDS["Flow"] = ("TrustSlice: how it works", "light", f"""
<div class="bar"></div>
<div class="kick">HOW IT WORKS</div>
<div class="h">The original is never edited or copied to a team.</div>
<div class="mid"><div style="display:flex;gap:5px">{st}</div>
<div style="position:relative;height:30px">
  <div style="position:absolute;left:464px;width:286px;top:8px;border-top:2px solid {TEAL}"></div>
  <div style="position:absolute;left:464px;width:286px;top:12px;text-align:center;font-size:13px;color:{DTEAL}">Any failed check here blocks the copy.</div>
</div>
<div style="display:flex;gap:20px;margin-top:14px">
  <div class="card" style="flex:1;padding:18px 22px"><div class="vt">REQUEST</div><div style="font-size:18px;line-height:26px;margin-top:6px">“That is not in the Sales view.” A request card goes to the owner. It never confirms that a hidden value exists.</div></div>
  <div class="card" style="flex:1;padding:18px 22px"><div class="vt">REFRESH · RETIRE</div><div style="font-size:18px;line-height:26px;margin-top:6px">A changed source makes the view STALE. A view past its date becomes VIEW_EXPIRED. The administrator removes old copies.</div></div>
</div>
<div style="margin-top:20px">
  <span class="gp">originals never modified</span><span class="gp">no auto-publish</span><span class="gp">“I am the CFO” in chat grants nothing</span><span class="gp">no direct write into team folders</span><span class="gp">search exclusion ≠ access control</span>
</div></div>
<div class="note">Tools are UGREEN expert-agent actions (file-agent, document-agent, knowledge-agent). The Skill itself is Markdown only.</div>
""")

# ------------------------------------------------------------------ 04 Checks (release gate)
checks = ["owner decision matches the current source and view version",
          "full read-back equals the approved text, footer included",
          "every approved passage is present",
          "no forbidden value, e.g. the client name or the price",
          "source unchanged right before the copy",
          "team folder exists; no file with the same name"]
cl = "".join(f'<div class="chk"><span class="y">✓</span><span>{c}</span></div>' for c in checks)
BOARDS["Checks"] = ("TrustSlice: the release gate", "light", f"""
<div class="bar"></div>
<div class="kick">THE RELEASE GATE</div>
<div class="h">Nothing reaches a team folder before it is checked.</div>
<div class="mid"><div style="display:flex;gap:18px;align-items:stretch">
  <div style="width:250px;display:flex;flex-direction:column;gap:14px">
    <div style="font-size:12px;font-weight:700;letter-spacing:.1em;color:{GREY}">BEFORE THE OWNER REVIEW</div>
    <div class="card" style="padding:14px 16px"><div class="vt">SECOND EXTRACTION</div><div style="font-size:17px;line-height:24px;margin-top:4px">Extracted ≠ original wording</div><div class="code" style="margin-top:4px">→ FIDELITY_MISMATCH</div></div>
    <div class="card" style="padding:14px 16px"><div class="vt">LEAK PROBE</div><div style="font-size:17px;line-height:24px;margin-top:4px">“largest night-shift freight depot” would point to the client.</div><div class="code" style="margin-top:4px">→ LEAK_RISK</div></div>
  </div>
  <div style="flex:1;background:{NAVY};color:#fff;border-radius:14px;padding:20px 24px">
    <div style="font-size:12px;font-weight:700;letter-spacing:.1em;color:{MINT};margin-bottom:12px">PRIVATE STAGING · ALL MUST PASS</div>
    {cl}
    <div class="code" style="color:{MINT};margin-top:4px">any failure → PUBLISH_BLOCKED, nothing is copied</div>
  </div>
  <div style="width:56px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:{DTEAL};font-size:12px;line-height:16px"><div style="font-size:28px;color:{TEAL}">→</div>approved copy</div>
  <div style="width:210px;display:flex;flex-direction:column;gap:14px">
    <div style="font-size:12px;font-weight:700;letter-spacing:.1em;color:{GREY}">TEAM FOLDER</div>
    <div class="card" style="padding:14px 16px;border:2px solid {TEAL}"><div class="vt">READ BACK AGAIN</div><div style="font-size:17px;line-height:24px;margin-top:4px">Match → PUBLISHED_VERIFIED</div><div style="font-size:17px;line-height:24px;margin-top:4px">Mismatch → POSSIBLE_EXPOSURE, never “safe”</div></div>
    <div class="code">cpmv · type copy · overwrite false</div>
  </div>
</div></div>
<div class="note">Offline release-gate simulator: 23/23 mocked cases pass. It models the rules; it is not a NAS test. Values are synthetic canaries from our worked example.</div>
""")

# ------------------------------------------------------------------ 05 Compare
comp = [("Folder permissions", "They show the whole file or nothing."),
        ("Universal Search excluded paths", "They hide folders from search but do not control access."),
        ("AI chat over all files", "It can quote anything it is able to read."),
        ("AI summary", "It rewrites the very words you wanted to reuse."),
        ("Redaction", "It hides the details, and the know-how with them.")]
cr = "".join(f'<div class="row"><b>{a}</b><span>{b}</span></div>' for a, b in comp)
BOARDS["Compare"] = ("TrustSlice: why not just use the usual tools", "light", f"""
<div class="bar"></div>
<div class="kick">WHY NOT JUST…</div>
<div class="h">The usual tools see whole files.</div>
<div class="mid"><div>{cr}
<div class="row me"><b>TrustSlice</b><span>It publishes only owner-approved passages, after checking them.</span></div></div></div>
<div class="note">TrustSlice builds on NAS folder permissions; it does not replace them.</div>
""")

# ------------------------------------------------------------------ 06 Status
def li(items, color):
    return "".join(f'<div class="chk"><span style="color:{color};font-weight:700;width:18px">•</span><span>{x}</span></div>' for x in items)
BOARDS["Status"] = ("TrustSlice: status", "dark", f"""
<div class="bar"></div>
<div class="kick">STATUS · 15 NOV 2026</div>
<div class="h">We verified this today. The NAS tests come next.</div>
<div class="mid"><div style="display:flex;gap:20px">
  <div style="flex:1;background:rgba(255,255,255,.06);border-radius:14px;padding:20px 22px">
    <div style="font-size:13px;font-weight:700;letter-spacing:.1em;color:{TEAL};margin-bottom:12px">VERIFIED NOW</div>
    {li(["Official Skill Kit checker: static-pass, 0 errors, 0 warnings", "Release-gate simulator: 23/23 mocked cases", "Synthetic fixture checks: 4/4", "Markdown only: SKILL.md + 10 linked references, no scripts"], TEAL)}
  </div>
  <div style="flex:1;background:rgba(255,255,255,.06);border-radius:14px;padding:20px 22px">
    <div style="font-size:13px;font-weight:700;letter-spacing:.1em;color:#F0B44C;margin-bottom:12px">ON THE FINALIST NAS</div>
    {li(["Staged file read back and canary-scanned before any copy", "A fresh chat quotes the approved view exactly", "A forged approval or a question about the hidden client releases nothing", "NAS permission denial logged apart from AI refusal", "Approval prompts per document counted"], "#F0B44C")}
  </div>
  <div style="width:250px;background:rgba(255,255,255,.06);border-radius:14px;padding:20px 22px">
    <div style="font-size:13px;font-weight:700;letter-spacing:.1em;color:#9FC4CC;margin-bottom:12px">NOT IN THIS ENTRY</div>
    {li(["Spreadsheet, slide and database adapters", "Stopping other Skills from reading originals", "A real NAS run (not claimed)"], "#9FC4CC")}
  </div>
</div></div>
<div class="note">TrustSlice adds a reviewed publishing workflow on top of UGREEN NAS permissions; it does not replace them.</div>
""")

FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Poppins:wght@500;600;700&amp;display=swap" rel="stylesheet">'

for name, (title, theme, inner) in BOARDS.items():
    body = f'<div class="b {theme}">{inner}</div>'
    dc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
{FONT_LINK}
<style>{CSS}</style>
</helmet>
{body}
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1200,"height":800}}}}'>
class Component extends DCLogic {{
  renderVals() {{
    return {{}};
  }}
}}
</script>
</body>
</html>
"""
    (DC_DIR / f"{name}.dc.html").write_text(dc)
    (HTML_DIR / f"{name}.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{body}</body></html>")
print("boards:", ", ".join(BOARDS))
