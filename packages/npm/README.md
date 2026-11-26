# examen-civique-france

JavaScript / Node.js library for the official knowledge-question lists of France's civic exam (*examen civique*, 2026) and Insee/DGEF statistics on acquisitions of French nationality, 2008–2025.

The package bundles **523** distinct questions compiled from the three official lists (CSP, CR and naturalisation; 659 published lines) and yearly acquisition counts for **2008–2025** (18 years). Answers are not included.

Compiled by Nesra Vomigarbi for [Examen Civique Test](https://examen-civique-test.fr/), an independent exam-preparation site not affiliated with the French State.

Interactive practice tool built on this dataset: [Examen Civique Test](https://examen-civique-test.fr/)

## Install

```bash
npm install examen-civique-france
```

The package supports both ESM (`import`) and CommonJS (`require`). TypeScript typings are included.

These packages have not been published to the public registries yet. Until they are, install from this repository, for example after cloning [https://github.com/nesravomigarbi/examen-civique-france-2026](https://github.com/nesravomigarbi/examen-civique-france-2026).

## Usage

```js
import {
  allQuestions,
  byMention,
  byTheme,
  randomQuestion,
  mockExam,
  acquisitionsByYear,
} from "examen-civique-france";

allQuestions().length;                 // 523
byMention("NAT").length;               // 258
byTheme("T4").length;                  // 143
const practice = mockExam(28, { mention: "CSP", seed: 1 });
const year2025 = acquisitionsByYear(2025);
year2025.modes.decree_total.count;     // 42246
```

```js
const { allQuestions } = require("examen-civique-france");
```


## API

- `allQuestions()` — all 523 distinct questions
- `byMention(mention)` — questions that appear in the CSP, CR or NAT list
- `byLevel(mention)` — alias of `byMention`
- `byTheme(theme)` — filter by official theme code (`T1`–`T5`) or theme name
- `randomQuestion({ mention, theme, seed })` — one question
- `mockExam(n, { mention, theme, seed })` — `n` distinct questions
- `acquisitionsByYear()` / `acquisitionsByYear(2025)` — yearly statistics


Filters:

- `mention` / `level`: `CSP`, `CR` or `NAT` (also the full French labels *carte de séjour pluriannuelle*, *carte de résident*, *naturalisation*).
- `theme`: official theme code `T1`–`T5`, or the official theme name (accent-insensitive).
  - T1 — Principes et valeurs de la République
  - T2 — Système institutionnel et politique
  - T3 — Droits et devoirs
  - T4 — Histoire, géographie et culture
  - T5 — Vivre dans la société française
- `seed`: optional integer; when set, the draw is deterministic.

`mockExam` / `mock_exam` draws without replacement. The official exam has 40 questions, of which 28 are knowledge questions taken from these lists; the 12 situational questions are not published and are not in this package.

Counts derived from the bundled tables (do not treat them as a new official source):

| Filter | Distinct questions |
|---|---|
| All | 523 |
| CSP | 190 |
| CR | 209 |
| NAT | 258 |
| T1 | 93 |
| T2 | 111 |
| T3 | 94 |
| T4 | 143 |
| T5 | 83 |

One question is tagged with two themes, so the theme counts add up to 524. Nationality acquisitions by decree: 94,573 in 2010 and 42,246 in 2025 (Insee), as recorded in the bundled table.

## Dataset, homepage and source

- Homepage: <https://examen-civique-test.fr/>
- Repository: <https://github.com/nesravomigarbi/examen-civique-france-2026>
- Dataset DOI: [https://doi.org/10.5281/zenodo.24496692](https://doi.org/10.5281/zenodo.24496692)
- Version of this package: 1.0.0
- Dataset version cited here: 1.0.1

## Citation

> Vomigarbi, N. (2026). French Civic Exam (Examen civique) 2026: Official Question Lists for All Three Mentions and Nationality Acquisition Statistics 2008–2025 (Version 1.0.1) [Data set]. Examen Civique Test. https://examen-civique-test.fr/ https://doi.org/10.5281/zenodo.24496692

## License

- **Code:** [MIT](LICENSE-MIT)
- **Bundled data:** [CC BY 4.0](LICENSE-DATA)

The source texts and official figures are French public sector information, reused under the Licence Ouverte / etalab-2.0 where the publisher states it, with attribution kept in each record.

---

## Français

Bibliothèque pour les listes officielles de questions de connaissance de l'examen civique 2026 et les statistiques Insee/DGEF des acquisitions de la nationalité française, 2008-2025.

Le paquet inclut **523** questions distinctes, établies à partir des trois listes officielles (CSP, CR et naturalisation ; 659 lignes publiées), ainsi que les totaux annuels d'acquisitions pour **2008-2025**. Les réponses ne sont pas incluses.

Compilé par Nesra Vomigarbi pour [Examen Civique Test](https://examen-civique-test.fr/), site d'entraînement indépendant, sans lien avec l'administration française.

Outil d'entraînement interactif construit à partir de ce jeu de données : [Examen Civique Test](https://examen-civique-test.fr/)

### Installation

```bash
npm install examen-civique-france
```

### Citation

> Vomigarbi, N. (2026). French Civic Exam (Examen civique) 2026: Official Question Lists for All Three Mentions and Nationality Acquisition Statistics 2008–2025 (Version 1.0.1) [Data set]. Examen Civique Test. https://examen-civique-test.fr/ https://doi.org/10.5281/zenodo.24496692

### Licence

Code : MIT. Données incluses : CC BY 4.0.
