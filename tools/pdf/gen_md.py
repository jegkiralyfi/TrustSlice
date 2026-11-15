"""Write the Markdown twin of the Round 1 proposal from content30.py."""
import sys
import content30 as C

KEEP = {"skill": "Skill", "ai": "AI", "ugreen": "UGREEN", "nas": "NAS", "trustslice": "TrustSlice"}


def sentence_case(text):
    out = []
    for sent in text.split(". "):
        words = [KEEP.get(w.lower().strip(",.?"), w.lower()) + ("," if w.endswith(",") and w.lower().strip(",.?") in KEEP else "")
                 if w.lower().strip(",.?") in KEEP else w.lower() for w in sent.split(" ")]
        s = " ".join(words)
        out.append(s[:1].upper() + s[1:])
    return ". ".join(out)


out = sys.argv[1] if len(sys.argv) > 1 else "PROPOSAL.md"
L = [f"# {C.TITLE} · Round 1 Proposal ({C.VERSION})", "",
     f"**{sentence_case(' '.join(C.HERO_H1))}** {sentence_case(C.HERO_H2)}", "",
     C.HERO_FLOW.replace("  ", " "), "",
     "| Example view | Sees | Held back |", "|---|---|---|"]
for t, sees, held in C.CARDS:
    L.append(f"| {t.title().replace('+ Any Other View', '+ Any other view')} | {sees} | {held} |")
L += ["", f"*{sentence_case(C.CARDS_NOTE)}*", ""]
for n, t, x in C.ITEMS:
    L += [f"## {n} · {sentence_case(t)}", "", x, ""]
L += ["## Release gate", "", " → ".join(f"{s} ({sub})" for s, sub in C.GATE_STEPS), "",
      "In private staging (STAGE and VERIFY), any failed check blocks the copy.", "",
      f"## {sentence_case(C.BOX_TITLE)}", "", C.BOX_TEXT, ""]
words = sum(len(x.split()) for _, _, x in C.ITEMS)
L.append(f"*The ten responses contain {words} words (the limit is 500).*")
open(out, "w").write("\n".join(L) + "\n")
print(out, words, "words")
