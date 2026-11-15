import subprocess, sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, KeepTogether, NextPageTemplate, PageBreak, Image)
from reportlab.pdfgen import canvas as rl_canvas
import content30 as C
from reportlab import rl_config

F = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("DV", F + "DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DVB", F + "DejaVuSans-Bold.ttf"))
rl_config.canvas_basefontname = "DV"   # no unembedded Helvetica in the PDF

NAVY, TEAL, PILL = HexColor("#112636"), HexColor("#31BCA9"), HexColor("#167D84")
CARD, GREY, INK, RULE = HexColor("#F4F8F8"), HexColor("#7E8C95"), HexColor("#1B2A36"), HexColor("#D9E2E4")
MINT = HexColor("#BFEFE6")
W, H = A4
M = 50                      # side margin
HERO_H = 205                # navy hero band on page 1
CARDS_TOP = H - HERO_H - 14
P2_BAND = 76                # navy band on page 2
OUT = sys.argv[1] if len(sys.argv) > 1 else "TrustSlice_Round1_Proposal_v031.pdf"


def footer(c, page):
    c.setFillColor(NAVY); c.rect(0, 0, W, 32, stroke=0, fill=1)
    c.setFillColor(HexColor("#C9D3D8")); c.setFont("DV", 7)
    c.drawString(M, 13, f"TRUSTSLICE  /  ROUND 1  /  {C.VERSION}")
    c.drawRightString(W - M, 13, f"{page} / 2")


def card_block(c):
    n = len(C.CARDS); gap = 8
    cw = (W - 2 * M - gap * (n - 1)) / n; ch = 50; y = CARDS_TOP - ch
    for i, (t, sees, held) in enumerate(C.CARDS):
        x = M + i * (cw + gap)
        last = i == n - 1
        c.setFillColor(HexColor("#EAF6F4") if last else CARD)
        c.setStrokeColor(TEAL if last else CARD)
        c.setDash(2, 2) if last else c.setDash()
        c.roundRect(x, y, cw, ch, 5, stroke=1 if last else 0, fill=1)
        c.setDash()
        from reportlab.pdfbase.pdfmetrics import stringWidth as sw
        for txt, fn, fs in ((t, "DVB", 7.6), (sees, "DV", 7.2), (held, "DV", 6.6)):
            assert sw(txt, fn, fs) <= cw - 16, f"card text too wide: {txt}"
        c.setFillColor(PILL); c.setFont("DVB", 7.6); c.drawString(x + 9, y + ch - 15, t)
        c.setFillColor(INK); c.setFont("DV", 7.2); c.drawString(x + 9, y + ch - 28, sees)
        c.setFillColor(GREY); c.setFont("DV", 6.6); c.drawString(x + 9, y + ch - 40, held)
    c.setFillColor(HexColor("#4F6470")); c.setFont("DVB", 6.6)
    c.drawString(M, y - 14, C.CARDS_NOTE)


def first_page(c, doc):
    c.saveState()
    c.setTitle(f"{C.TITLE}: Round 1 Proposal {C.VERSION}")
    c.setAuthor("Zoltán Fehér"); c.setSubject("UGREEN AI NAS Hackathon 2026, Round 1 proposal")
    c.setKeywords("TrustSlice, UGREEN, UGOS, Uliya, Skill, NAS, team views")
    c.setFillColor(NAVY); c.rect(0, H - HERO_H, W, HERO_H, stroke=0, fill=1)
    c.setFillColor(TEAL); c.rect(0, H - 6, W, 6, stroke=0, fill=1)
    c.roundRect(M, H - 52, 118, 22, 5, stroke=0, fill=1)
    c.setFillColor(NAVY); c.setFont("DVB", 9.5); c.drawString(M + 12, H - 44.5, C.HERO_PILL)
    from reportlab.pdfbase.pdfmetrics import stringWidth as sw
    for txt, fn, fs in ((C.HERO_H1, "DVB", 21), (C.HERO_H2, "DVB", 13.5), (C.HERO_FLOW, "DV", 9.6),
                        (C.HERO_SUB, "DV", 7.6), (C.CARDS_NOTE, "DVB", 6.6), (C.PAGE2_SUB, "DV", 7.8)):
        assert sw(txt, fn, fs) <= W - 2 * M, f"hero text too wide: {txt}"
    c.setFillColor(white); c.setFont("DVB", 21); c.drawString(M, H - 90, C.HERO_H1)
    c.setFillColor(MINT); c.setFont("DVB", 13.5); c.drawString(M, H - 116, C.HERO_H2)
    c.setFillColor(HexColor("#DCE6EA")); c.setFont("DV", 9.6); c.drawString(M, H - 144, C.HERO_FLOW)
    c.setFillColor(HexColor("#AFC0C7")); c.setFont("DV", 7.6); c.drawString(M, H - 170, C.HERO_SUB)
    card_block(c)
    footer(c, 1)
    c.restoreState()


def later_page(c, doc):
    c.saveState()
    c.setFillColor(NAVY); c.rect(0, H - P2_BAND, W, P2_BAND, stroke=0, fill=1)
    c.setFillColor(TEAL); c.rect(0, H - 6, W, 6, stroke=0, fill=1)
    c.setFillColor(white); c.setFont("DVB", 16); c.drawString(M, H - 42, C.PAGE2_TITLE)
    c.setFillColor(HexColor("#AFC0C7")); c.setFont("DV", 7.8); c.drawString(M, H - 60, C.PAGE2_SUB)
    footer(c, 2)
    c.restoreState()


def gate_png(path_pdf, path_png):
    """Release-gate strip, rasterised so machine readers see only the ten answers as text."""
    gw, gh = W - 2 * M, 92
    c = rl_canvas.Canvas(path_pdf, pagesize=(gw, gh))
    c.setFillColor(PILL); c.setFont("DVB", 7.4); c.drawString(0, gh - 10, C.GATE_TITLE)
    n = len(C.GATE_STEPS); gap = 14; bw = (gw - gap * (n - 1)) / n; bh = 44; y = 14
    for i, (s, sub) in enumerate(C.GATE_STEPS):
        x = i * (bw + gap)
        private = s in ("STAGE", "VERIFY")
        c.setFillColor(NAVY if private else CARD)
        c.roundRect(x, y, bw, bh, 5, stroke=0, fill=1)
        from reportlab.pdfbase.pdfmetrics import stringWidth as sw
        assert sw(s, "DVB", 7.4) <= bw - 8 and sw(sub, "DV", 6.0) <= bw - 8, f"gate text too wide: {s}/{sub}"
        c.setFillColor(white if private else NAVY); c.setFont("DVB", 7.4)
        c.drawCentredString(x + bw / 2, y + bh - 18, s)
        c.setFillColor(MINT if private else GREY); c.setFont("DV", 6.0)
        c.drawCentredString(x + bw / 2, y + 10, sub)
        if i < n - 1:
            ax = x + bw + 2; ay = y + bh / 2
            c.setStrokeColor(TEAL); c.setLineWidth(1.2); c.line(ax, ay, ax + gap - 5, ay)
            c.setFillColor(TEAL); p = c.beginPath()
            p.moveTo(ax + gap - 3, ay); p.lineTo(ax + gap - 7, ay + 3); p.lineTo(ax + gap - 7, ay - 3); p.close()
            c.drawPath(p, stroke=0, fill=1)
    sx = 3 * (bw + gap); ex = 5 * (bw + gap) - gap
    c.setStrokeColor(TEAL); c.setLineWidth(0.8); c.line(sx, 9, ex, 9)
    c.setFillColor(PILL); c.setFont("DV", 5.8)
    c.drawCentredString((sx + ex) / 2, 1.5, "In private staging, any failed check blocks the copy.")
    c.save()
    subprocess.run(["pdftoppm", "-r", "300", "-png", "-singlefile", path_pdf, path_png[:-4]], check=True)
    return gw, gh


body = ParagraphStyle("b", fontName="DV", fontSize=9.4, leading=13.6, textColor=INK, alignment=TA_LEFT)
head = ParagraphStyle("h", fontName="DVB", fontSize=8.6, leading=11, textColor=NAVY)
pill = ParagraphStyle("p", fontName="DVB", fontSize=8.2, leading=10, textColor=white, alignment=1)
boxh = ParagraphStyle("bh", fontName="DVB", fontSize=7.4, leading=10, textColor=PILL)
boxt = ParagraphStyle("bt", fontName="DV", fontSize=7.2, leading=10, textColor=HexColor("#4F6470"))


def item(num, title, text, first=False):
    t = Table([[Paragraph(num, pill), Paragraph(title, head)]], colWidths=[30, W - 2 * M - 30], rowHeights=[19])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), PILL), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 0), ("RIGHTPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (1, 0), (1, 0), 10), ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2), ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    parts = [] if first else [Spacer(1, 7), Table([[""]], colWidths=[W - 2 * M], rowHeights=[1],
                                                 style=[("LINEABOVE", (0, 0), (-1, -1), 0.6, RULE), ("FONTNAME", (0, 0), (-1, -1), "DV")]), Spacer(1, 7)]
    return KeepTogether(parts + [t, Spacer(1, 5), Paragraph(text, body)])


def build():
    doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=M, rightMargin=M, topMargin=0, bottomMargin=0,
                          title=f"{C.TITLE}: Round 1 Proposal {C.VERSION}", author="Zoltán Fehér", initialFontName="DV",
                          subject="UGREEN AI NAS Hackathon 2026, Round 1 proposal", creator="TrustSlice")
    top1 = CARDS_TOP - 50 - 30
    f1 = Frame(M, 44, W - 2 * M, top1 - 44, id="f1", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    f2 = Frame(M, 44, W - 2 * M, H - P2_BAND - 20 - 44, id="f2", leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0)
    doc.addPageTemplates([PageTemplate("first", [f1], onPage=first_page),
                          PageTemplate("later", [f2], onPage=later_page)])
    story = []
    for i, (n, t, x) in enumerate(C.ITEMS[:5]):
        story.append(item(n, t, x, first=(i == 0)))
    story += [NextPageTemplate("later"), PageBreak()]
    for i, (n, t, x) in enumerate(C.ITEMS[5:]):
        story.append(item(n, t, x, first=(i == 0)))
    gw, gh = gate_png("_gate.pdf", "_gate.png")
    story += [Spacer(1, 16), Image("_gate.png", width=gw, height=gh)]
    box = Table([[Paragraph(C.BOX_TITLE, boxh)], [Paragraph(C.BOX_TEXT, boxt)]], colWidths=[W - 2 * M])
    box.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CARD), ("LEFTPADDING", (0, 0), (-1, -1), 10),
                             ("RIGHTPADDING", (0, 0), (-1, -1), 10), ("TOPPADDING", (0, 0), (0, 0), 8),
                             ("BOTTOMPADDING", (0, -1), (-1, -1), 8), ("ROUNDEDCORNERS", [5, 5, 5, 5])]))
    story += [Spacer(1, 12), box]
    doc.build(story)


if __name__ == "__main__":
    build()
    from pypdf import PdfReader
    n = len(PdfReader(OUT).pages)
    print("pages", n)
    if n != 2:
        raise SystemExit("layout overflow: expected 2 pages")
