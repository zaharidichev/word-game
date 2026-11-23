#!/usr/bin/env python3
"""Check the word data against the house rules. Exits non-zero on any problem.

Rules:
  - every word has a meaning, an example sentence and an existing picture
  - the meaning must NOT contain the word (it would give the answer away)
  - the example sentence MUST contain the word, exactly as spelled (the game blanks it out)
  - week ids are dates (YYYY-MM-DD) that match the file name
  - a word appears at most once in a week
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
problems = []


def word_re(word):
    base = re.sub(r"\s*\(\?\)", "", word)
    return re.compile(r"(?i)(?<![a-z])" + re.escape(base) + r"(?![a-z])")


def check_word(where, w):
    for field in ("word", "meaning", "example", "picture"):
        if not w.get(field):
            problems.append(f"{where}: missing '{field}'")
            return
    if word_re(w["word"]).search(w["meaning"]):
        problems.append(f"{where}: meaning contains the word '{w['word']}'")
    if not word_re(w["word"]).search(w["example"]):
        problems.append(f"{where}: example does not contain the word '{w['word']}'")
    if not (ROOT / "pictures" / f"{w['picture']}.svg").exists():
        problems.append(f"{where}: picture pictures/{w['picture']}.svg not found")


def main():
    book = json.loads((ROOT / "data" / "book.json").read_text(encoding="utf-8"))
    for i, w in enumerate(book):
        check_word(f"book.json[{i}] '{w.get('word')}'", w)
        if not isinstance(w.get("page"), int):
            problems.append(f"book.json[{i}]: page must be a number")

    for path in sorted((ROOT / "data" / "weeks").glob("*.json")):
        wk = json.loads(path.read_text(encoding="utf-8"))
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", wk.get("id", "")) or path.stem != wk["id"]:
            problems.append(f"{path.name}: id must be YYYY-MM-DD and match the file name")
        if not wk.get("label"):
            problems.append(f"{path.name}: missing label")
        seen = set()
        for i, w in enumerate(wk.get("words", [])):
            check_word(f"{path.name}[{i}] '{w.get('word')}'", w)
            key = w.get("word", "").lower()
            if key in seen:
                problems.append(f"{path.name}: '{w['word']}' appears twice")
            seen.add(key)

    if problems:
        print("\n".join(problems))
        sys.exit(f"{len(problems)} problem(s)")
    print("data OK")


if __name__ == "__main__":
    main()
