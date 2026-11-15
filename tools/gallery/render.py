import sys, pathlib
from playwright.sync_api import sync_playwright
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
order = ["Main", "Views", "Flow", "Checks", "Compare", "Status"]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1200, "height": 800}, device_scale_factor=2)
    for i, n in enumerate(order, 1):
        pg.goto((src / f"{n}.html").resolve().as_uri())
        pg.wait_for_timeout(300)
        # overflow check: any element extending past the board edges
        bad = pg.evaluate("""() => { const B=document.body.firstElementChild.getBoundingClientRect(); const r=[];
          for (const e of document.body.firstElementChild.querySelectorAll('*')) { const q=e.getBoundingClientRect(); if(!q.width) continue;
            if (q.right>B.right+0.5||q.bottom>B.bottom+0.5) r.push(e.tagName+':'+(e.textContent||'').trim().slice(0,40)); }
          return r.slice(0,5); }""")
        pg.screenshot(path=str(out / f"{i:02d}_{n}.png"), clip={"x": 0, "y": 0, "width": 1200, "height": 800})
        print(n, "overflow:", bad)
    b.close()
