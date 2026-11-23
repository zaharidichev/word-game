# AGENTS.md

Guidance for AI coding agents (Claude Code, Codex, Copilot, etc.) working in this repository.

## What this is

A spelling and vocabulary game for a 1st-grade child learning English as a second language.
The child sees a simple meaning, can ask for an example sentence or a picture as a hint,
and types the word into letter boxes. Words come from two sources:

- **Weekly words** from the child's school notebook and homework sheets (the main way the game is used).
- **Book words** from the class textbook, grouped by the book's letter units and page numbers.

The output is one self-contained page, `site/index.html`, published to GitHub Pages.
It must work offline, on a phone, and with no build step at runtime.

## Layout

```
data/book.json        textbook picture words: page, word, meaning, example, picture
data/units.json       textbook letter units (page ranges), used for the "Book pages" filter
data/weeks/*.json     one file per school week, named by the week's Monday (YYYY-MM-DD.json)
pictures/*.svg        one picture per word; referenced by file stem from the data files
src/template.html     the game page (HTML/CSS/JS), with /*BOOK_DATA*/ /*UNITS_DATA*/ /*WEEKS_DATA*/ placeholders
scripts/build.py      data + pictures + template -> site/index.html
scripts/check.py      validates the data against the rules below (CI runs this)
scripts/picture.py    makes a picture from Microsoft Fluent Emoji names
docs/weekly-update.md step-by-step for adding a new week
site/                 build output (not committed)
inbox/                photos waiting to be processed (not committed; they show the child's handwriting)
```

## Commands

```bash
python3 scripts/check.py     # validate data (must pass before committing)
python3 scripts/build.py     # build site/index.html
python3 -m http.server -d site 8000   # preview at http://localhost:8000
```

Python 3.9+ with only the standard library. No other dependencies.

## Adding a new week (the most common task)

Follow `docs/weekly-update.md`. In short:

1. Read every photo. List every English word or short phrase the child practised that week,
   in the order it appears. Include homework-sheet words. Skip Bulgarian translations,
   names of people (e.g. Stella, Simon), dates, and exercise instructions.
2. Find the date written in the notebook. The week id is the **Monday** of that week (YYYY-MM-DD),
   and the label is `Week of <day> <Mon>` (e.g. `Week of 16 Nov`). If there is no date, ask, or use the
   Monday of the week the photos were taken and say so.
3. **Show the word list to the person and get it confirmed before writing files** — handwriting is
   easy to misread.
4. Create `data/weeks/<id>.json` (copy the shape of an existing week).
5. For each word:
   - **meaning**: one or two very short sentences a 6-year-old understands. It must NOT contain the word
     (not even as part of another word or a plural). For small grammar words, use a fill-in example
     with `___`, e.g. `"\"___ name is Stella.\""`.
   - **example**: one short sentence that contains the word exactly as spelled (the game blanks it out).
     Use simple words the child already knows.
   - **picture**: reuse an existing picture stem if the word already has one (search `data/`), otherwise make one:
     `python3 scripts/picture.py <stem> "Fluent name" ["Fluent name" ...]`.
6. Run `scripts/check.py` and `scripts/build.py`. Open the page and play one round with the new week ticked.
7. Commit with a message like `Add week of 16 Nov (24 words)`.

## Content rules

- Audience is a 6-year-old. Short sentences, common words, friendly tone. British spelling (colour, favourite, rubber).
- A meaning never contains its word. An example always does. `check.py` enforces both.
- No real personal information about the child (name, school, photos of the notebook) in the repo — it is public.
- Pictures: Microsoft Fluent Emoji (MIT) for consistency. No letters or words inside a picture — it would give the answer away.
  Hand-drawn SVGs are fine when no emoji fits; match the soft, shaded style (no thick black outlines).
- Words with `(?)` in `data/book.json` are best guesses from unlabelled textbook drawings; leave them unless the person confirms.

## Changing the game itself

- All game code is in `src/template.html` (plain HTML/CSS/JS, no framework, no external scripts).
  The only external resource is the Fredoka font from Google Fonts; the page must still work without it.
- Keep it phone-friendly: the letter boxes use a transparent input laid over them so tapping opens the phone keyboard.
- Scoring: 2 stars without hints, 1 star with any hint (example or picture), 0 for skip.
- After changing the template, rebuild and test a full round on a narrow (phone-width) window.

## Deployment

Pushing to `main` runs `.github/workflows/pages.yml`: check -> build -> publish `site/` to GitHub Pages.
Pull requests run the check and build only.
