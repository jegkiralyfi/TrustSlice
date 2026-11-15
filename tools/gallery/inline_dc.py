"""Turn the standalone boards into Design-canvas .dc.html files with inline styles only."""
import pathlib, re, sys, warnings, logging
warnings.filterwarnings("ignore"); logging.disable(logging.CRITICAL)
from premailer import Premailer
from lxml import html as LH
src, dc_dir, check_dir = map(pathlib.Path, sys.argv[1:4])
check_dir.mkdir(exist_ok=True)
FONT = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&amp;family=Poppins:wght@500;600;700&amp;display=swap" rel="stylesheet">'
TITLES = {"Main": "TrustSlice cover", "Views": "TrustSlice: one contract, many views", "Flow": "TrustSlice: how it works",
          "Checks": "TrustSlice: the release gate", "Compare": "TrustSlice: why not just use the usual tools", "Status": "TrustSlice: status"}
for name, title in TITLES.items():
    raw = (src / f"{name}.html").read_text()
    out = Premailer(raw, keep_style_tags=False, remove_classes=True, strip_important=False,
                    disable_validation=True, cssutils_logging_level=logging.CRITICAL).transform()
    doc = LH.fromstring(out)
    root = doc.xpath("//body/div")[0]
    inner = LH.tostring(root, encoding="unicode", method="html")
    assert "class=" not in inner, name
    (check_dir / f"{name}.html").write_text(f"<!doctype html><html><head><meta charset='utf-8'><style>body{{margin:0}}</style></head><body>{inner}</body></html>")
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
{FONT}
<style>
body{{margin:0}}
a{{color:#167D84}}a:hover{{color:#112636}}
</style>
</helmet>
{inner}
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
    (dc_dir / f"{name}.dc.html").write_text(dc)
    print(name, len(dc))
