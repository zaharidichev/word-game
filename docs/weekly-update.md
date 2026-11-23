# Adding a new week

Each week the child brings home notebook pages and a homework sheet. This turns them into a new week in the game.

## 1. Collect the photos

Put the photos in `inbox/<YYYY-MM-DD>/` (any format; iPhone HEIC is fine). This folder is git-ignored,
so the photos never reach the public repository.

## 2. Read the words

Go through the photos in order and list:

- every English word or short phrase the child wrote out (usually a word followed by a Bulgarian translation, then copied several times)
- every word on the homework sheet

Leave out: Bulgarian words, people's names, dates, "Classwork", "Homework", teacher comments ("Bravo!", "Very good!").
Keep phrases as one entry if they were taught together: `stand up`, `next to`, `Who's that?`.

Note obvious spelling slips in the child's writing (e.g. "diferent") so the parent can practise them.

## 3. Confirm

Send the list back to the parent and wait for a yes before writing files.

## 4. Write the week file

`data/weeks/2026-11-16.json`:

```json
{
 "id": "2026-11-16",
 "label": "Week of 16 Nov",
 "source": "notebook + homework sheet",
 "words": [
  {"word": "happy", "meaning": "You smile and laugh when you feel like this.",
   "example": "I am happy on my birthday.", "picture": "happy"}
 ]
}
```

- `id` = the Monday of that school week. `label` = `Week of <day> <Mon>`.
- If a word is already in the game, reuse its meaning, example and picture (`grep -ri '"word": "ball"' data/`).

## 5. Pictures

```bash
python3 scripts/picture.py happy "Grinning face with big eyes"
python3 scripts/picture.py his "Boy" "Soccer ball"
```

Browse names at https://github.com/microsoft/fluentui-emoji/tree/main/assets.
Good tricks for hard words: position words (in/on/under) as a ball and a box; pronouns as a person plus an object;
opposites as a pair (`different` = apple + banana).

## 6. Check, build, play

```bash
python3 scripts/check.py && python3 scripts/build.py
python3 -m http.server -d site 8000
```

Play a round with only the new week ticked, on a phone-width window.

## 7. Commit and push

```bash
git add data pictures && git commit -m "Add week of 16 Nov (24 words)" && git push
```

GitHub Actions publishes the site a minute or two later.
