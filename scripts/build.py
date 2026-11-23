#!/usr/bin/env python3
"""Build the word game into a single self-contained page: site/index.html.

Reads:
  data/book.json      textbook picture words (with page numbers)
  data/units.json     letter units of the textbook (page ranges)
  data/weeks/*.json   weekly word lists from the notebook
  pictures/*.svg      one picture per word (referenced by stem)
  src/template.html   the game page, with /*..._DATA*/ placeholders
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def picture(stem):
    path = ROOT / "pictures" / f"{stem}.svg"
    if not path.exists():
        sys.exit(f"missing picture: pictures/{stem}.svg")
    return path.read_text(encoding="utf-8")


def main():
    book = load_json(ROOT / "data" / "book.json")
    units = load_json(ROOT / "data" / "units.json")
    weeks = [load_json(p) for p in sorted((ROOT / "data" / "weeks").glob("*.json"))]

    words = [{"p": w["page"], "w": w["word"], "m": w["meaning"], "e": w["example"], "s": picture(w["picture"])}
             for w in book]
    unit_data = []
    for u in units:
        count = sum(1 for w in book if u["from"] <= w["page"] <= u["to"])
        if count:
            unit_data.append({"a": u["from"], "b": u["to"], "n": u["name"], "c": count})
    week_data = [{
        "id": wk["id"],
        "label": wk["label"],
        "words": [{"w": w["word"], "m": w["meaning"], "e": w["example"], "s": picture(w["picture"]), "wk": wk["id"]}
                  for w in wk["words"]],
    } for wk in sorted(weeks, key=lambda x: x["id"], reverse=True)]

    page = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
    for key, value in (("BOOK_DATA", words), ("UNITS_DATA", unit_data), ("WEEKS_DATA", week_data)):
        marker = f"/*{key}*/"
        if marker not in page:
            sys.exit(f"template is missing {marker}")
        page = page.replace(marker, json.dumps(value, ensure_ascii=False))

    out = ROOT / "site" / "index.html"
    out.parent.mkdir(exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"built {out.relative_to(ROOT)}: {len(words)} book words, {len(week_data)} weeks, {len(page) // 1024} KB")


if __name__ == "__main__":
    main()
