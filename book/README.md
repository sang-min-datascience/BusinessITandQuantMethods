# IBL103 Mathematics for Business (Quarto book)

Course book for the mathematics block of IBL103. Students read it on the web (GitHub Pages for now); Moodle links to it.

## Work on it in RStudio

1. Open `ibl103-book.Rproj` in RStudio (Quarto ships with RStudio; no R packages are needed, because the book runs no code).
2. **Build > Render Book** (or `quarto render` in the Terminal). The site is written to `public/`.
3. To preview while writing: `quarto preview` in the Terminal.

## Publish

**GitHub (current):** every push to `main` that changes `book/` runs `.github/workflows/publish-book.yml`, which renders the book in the cloud and publishes it with GitHub Pages. You do not commit `public/`. In the repository's **Settings > Pages**, *Source* must be set to **GitHub Actions** (once).

**THM GitLab (later, if Pages is available there):** render locally, commit `public/` (remove it from `.gitignore`), and push. `.gitlab-ci.yml` publishes it; set Pages visibility to *Everyone*.

## Writing conventions

| What | How |
|------|-----|
| Video | `::: {.video panopto="SESSION-ID" minutes="10"}` + title + `:::`. Without an id it shows "Video coming soon". Set `panopto-host` in `_quarto.yml` once. |
| Spreadsheet grid | A code block with class `sheet`: cells separated by `|`, formulas start with `=`, add `-> value` to show the result. Options: `title`, `highlight="B6"`, `start-row`, `start-col`, `header="false"`. See `assets/filters/sheet.lua`. |
| R / Python | Normal code blocks ```` ```r ```` and ```` ```python ```` inside `::: {.panel-tabset group="language"}`. They get a coloured frame and label automatically. |
| Worked example | `::: {.callout-note}` with heading `## Worked example: ...` |
| Self-check / practice | `::: {.callout-tip}` with heading `## Check yourself`. Put each answer in `::: {.hidden-solution}` (indent 3 spaces inside a numbered list) to get a "Show solution" button; `title="..."` changes the button text. Do not use the class `solution`, which Quarto reserves. |
| Common mistake | `::: {.callout-warning}` |
| Goals / business case | `::: {.goals}` and `::: {.business}`; the first line is the box title. |
| Citations | Keys in `references.bib`, written as `@olivier2023, sec. 2.1–2.4, pp. 11–45` so the wording matches the syllabus. |

## Moodle quizzes

`moodle/entry-quiz-1-sample.xml` is a sample of 4 calculated questions (Moodle XML) to test the import: Question bank > Import > Moodle XML format. `moodle/make_quiz.py` generates it.

## Not public

Solutions to the in-class problem sets and instructor notes do not belong in this repository while it is published openly.
