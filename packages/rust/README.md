# examen-civique-france

Rust crate for the official knowledge-question lists of France's civic exam (*examen civique*, 2026) and Insee/DGEF statistics on acquisitions of French nationality, 2008–2025.

The package bundles **523** distinct questions compiled from the three official lists (CSP, CR and naturalisation; 659 published lines) and yearly acquisition counts for **2008–2025** (18 years). Answers are not included.

Compiled by Nesra Vomigarbi for [Examen Civique Test](https://examen-civique-test.fr/), an independent exam-preparation site not affiliated with the French State.

Interactive practice tool built on this dataset: [Examen Civique Test](https://examen-civique-test.fr/)

## Install

```toml
[dependencies]
examen-civique-france = "1.0.0"
```

These packages have not been published to the public registries yet. Until they are, install from this repository, for example after cloning [https://github.com/nesravomigarbi/examen-civique-france-2026](https://github.com/nesravomigarbi/examen-civique-france-2026).

## Usage

```rust
use examen_civique_france::{
    acquisitions_by_year, all_questions, by_mention, by_theme, mock_exam, mock_exam_with,
    random_question_with, Filter,
};

assert_eq!(all_questions().len(), 523);
assert_eq!(by_mention("NAT").unwrap().len(), 258);
assert_eq!(by_theme("T4").unwrap().len(), 143);

let practice = mock_exam_with(28, &Filter::new().mention("CSP").seed(1)).unwrap();
let year_2025 = acquisitions_by_year(Some(2025)).unwrap();
// year_2025.modes["decree_total"].count == Some(42246)
```

## API

- `all_questions()` — all 523 distinct questions
- `by_mention(mention)` — questions that appear in the CSP, CR or NAT list
- `by_level(mention)` — alias of `by_mention`
- `by_theme(theme)` — filter by official theme code (`T1`–`T5`) or theme name
- `random_question()` / `random_question_with(&filter)` — one question
- `mock_exam(n)` / `mock_exam_with(n, &filter)` — `n` distinct questions
- `acquisitions_by_year(None)` / `acquisitions_by_year(Some(2025))` — yearly statistics
- `Filter::new().mention(...).theme(...).seed(...)` — optional filters for the random draws


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

```toml
[dependencies]
examen-civique-france = "1.0.0"
```

### Citation

> Vomigarbi, N. (2026). French Civic Exam (Examen civique) 2026: Official Question Lists for All Three Mentions and Nationality Acquisition Statistics 2008–2025 (Version 1.0.1) [Data set]. Examen Civique Test. https://examen-civique-test.fr/ https://doi.org/10.5281/zenodo.24496692

### Licence

Code : MIT. Données incluses : CC BY 4.0.
