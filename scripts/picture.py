#!/usr/bin/env python3
"""Make a word picture from Microsoft Fluent Emoji (MIT licence).

Usage:
  python scripts/picture.py <stem> "Name" ["Name" ...]

One name  -> that emoji on its own.
Several   -> the emojis side by side (e.g. "Boy" "Soccer ball" for "his").
Names are folder names in https://github.com/microsoft/fluentui-emoji/tree/main/assets
(e.g. "Red apple", "Teddy bear", "Old woman"). The picture is written to pictures/<stem>.svg.
Downloads are cached in .cache/fluent/.
"""
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / ".cache" / "fluent"
BASE = "https://raw.githubusercontent.com/microsoft/fluentui-emoji/main/assets/"


def fetch(name):
    CACHE.mkdir(parents=True, exist_ok=True)
    cached = CACHE / f"{name}.svg"
    if cached.exists():
        return cached.read_text(encoding="utf-8")
    snake = name.lower().replace(" ", "_")
    folder = urllib.parse.quote(name)
    # plain emoji, then people emoji (which have skin-tone variants)
    for path in (f"{folder}/Color/{snake}_color.svg", f"{folder}/Default/Color/{snake}_color_default.svg"):
        try:
            with urllib.request.urlopen(BASE + path, timeout=30) as r:
                svg = r.read().decode("utf-8")
            cached.write_text(svg, encoding="utf-8")
            return svg
        except Exception:
            continue
    sys.exit(f"Fluent emoji not found: '{name}' (check the folder name on GitHub)")


def prefixed(svg, prefix):
    """Return (viewBox, inner markup) with all ids made unique, so pictures can share a page."""
    svg = re.sub(r"<\?xml[^>]*\?>", "", svg).strip()
    for ident in sorted(set(re.findall(r'id="([^"]+)"', svg)), key=len, reverse=True):
        svg = (svg.replace(f'id="{ident}"', f'id="{prefix}{ident}"')
                  .replace(f"url(#{ident})", f"url(#{prefix}{ident})")
                  .replace(f'href="#{ident}"', f'href="#{prefix}{ident}"'))
    view_box = re.search(r'viewBox="([^"]+)"', svg).group(1)
    return view_box, svg[svg.index(">") + 1:svg.rindex("</svg>")]


def build(stem, names):
    pfx = "p" + re.sub(r"[^a-z0-9]", "", stem.lower())
    if len(names) == 1:
        vb, inner = prefixed(fetch(names[0]), pfx + "0")
        return f'<svg viewBox="{vb}" fill="none" xmlns="http://www.w3.org/2000/svg">{inner}</svg>'
    n = len(names)
    size = min(120 / (n * 0.8 + 0.2), 72)
    x0 = (120 - size * n * 0.85) / 2 - size * 0.075
    parts = []
    for k, name in enumerate(names):
        vb, inner = prefixed(fetch(name), f"{pfx}{k}")
        x, y = x0 + k * size * 0.85, (110 - size) / 2 + (8 if k % 2 else 0)
        parts.append(f'<svg x="{x:.1f}" y="{y:.1f}" width="{size:.1f}" height="{size:.1f}" '
                     f'viewBox="{vb}" fill="none">{inner}</svg>')
    return '<svg viewBox="0 0 120 110" xmlns="http://www.w3.org/2000/svg">' + "".join(parts) + "</svg>"


def main():
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    stem, names = sys.argv[1], sys.argv[2:]
    out = ROOT / "pictures" / f"{stem}.svg"
    out.write_text(build(stem, names), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
