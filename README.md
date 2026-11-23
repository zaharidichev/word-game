# Word Game

A small spelling game for a child learning English. Each turn shows a simple meaning;
the child types the word into letter boxes, with an example sentence and a picture as hints.
Letters turn green or red as they are typed, and stars are counted for the session.

Words are organised **by school week** (from the notebook and homework sheets), with the class
textbook's words available as an optional extra.

## Play

Open the GitHub Pages site for this repository, or build it locally:

```bash
python3 scripts/build.py
open site/index.html        # or: python3 -m http.server -d site 8000
```

On a phone, add the page to the home screen to use it like an app.

## Add a week

See [docs/weekly-update.md](docs/weekly-update.md). In short: photos in `inbox/`, a new file in
`data/weeks/`, pictures with `scripts/picture.py`, then `scripts/check.py` and `scripts/build.py`.

## How it is built

| Path | What it is |
|---|---|
| `data/` | All words: weekly lists, textbook words, textbook units |
| `pictures/` | One SVG per word |
| `src/template.html` | The game (plain HTML/CSS/JS) |
| `scripts/` | `build.py`, `check.py`, `picture.py` (Python standard library only) |
| `.github/workflows/pages.yml` | Checks, builds and publishes to GitHub Pages on every push to `main` |

Agents working on this repo: start with [AGENTS.md](AGENTS.md).

## Setup on GitHub (once)

1. Push this repository to GitHub.
2. **Settings → Pages → Build and deployment → Source: GitHub Actions.**
3. Push to `main` (or run the workflow from the Actions tab). The site URL appears in the workflow run.

## Credits

Pictures are mostly [Microsoft Fluent Emoji](https://github.com/microsoft/fluentui-emoji) (MIT);
see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
