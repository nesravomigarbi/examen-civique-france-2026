# French Civic Exam (Examen civique) 2026: Official Question Lists for All Three Mentions and Nationality Acquisition Statistics 2008–2025

**Version 1.0.0 · Data checked on 24 November 2026 · License: CC BY 4.0**
**Author:** Nesra Vomigarbi, Examen Civique Test ([examen-civique-test.fr](https://examen-civique-test.fr/))
Examen Civique Test is an independent exam-preparation site. It is not a government service and does not speak for the French administration.

## Summary

Since 1 January 2026, people in France who apply for a first multi-year residence permit (*carte de séjour pluriannuelle*, CSP), a first resident card (*carte de résident*, CR) or naturalisation by decree must pass a civic exam (*examen civique*). The exam has 40 multiple-choice questions. Candidates need 32 correct answers and have at most 45 minutes. Each exam has 28 knowledge questions and 12 situational questions. The Ministry of the Interior publishes a list of knowledge questions for each of the three mentions. The situational questions are not published.

The three lists are published in different formats. The CSP and CR lists are web pages. The naturalisation list is a PDF, and 15 of its 259 lines are images, not text. This dataset:

1. puts all 659 published lines in one table, with the official wording, theme and line number;
2. gives each distinct question a stable key and shows which lists contain it (523 distinct questions across the three lists);
3. adds the exam blueprint by theme and notion, and 30 official facts about the exam and its fees;
4. adds official statistics on acquisitions of French nationality by mode for 2008–2025, plus 2025 figures for the ten main nationalities of origin.

Answers are **not** included. Only official sources are used. Derived values are marked.

## Key figures (calculated from the files)

| | CSP | CR | Naturalisation |
|---|---|---|---|
| Lines in the official list | 191 | 209 | 259 |
| Distinct questions | 190 | 209 | 258 |
| Also in the CSP list | – | 33 | 44 |
| Also in the CR list | 33 | – | 61 |
| Also in the naturalisation list | 44 | 61 | – |
| In no other list | 117 | 119 | 157 |
| Lines published as images | 0 | 0 | 15 |

Four questions appear in all three lists. Nationality acquisitions by decree fell from 94,573 in 2010 to 42,246 in 2025 (Insee). That includes 9,196 minors who acquired nationality through the collective effect (DGEF), which leaves 33,050 adults (derived).

## Files

| File | Rows | Content |
|---|---|---|
| `data/examen_civique_questions_officielles.csv` | 659 | One row per line of the three official lists |
| `data/examen_civique_questions_uniques.csv` | 523 | One row per distinct question, with list membership |
| `data/examen_civique_recouvrement_listes.csv` | 18 | Overlap between lists, by mention × theme (5 themes + total) |
| `data/examen_civique_structure_epreuve.csv` | 16 | Number of questions per exam by theme and notion |
| `data/examen_civique_faits_cles.csv` | 30 | Official facts: rules, fees, candidates, pass rate, centres |
| `data/acquisitions_nationalite_france_2008_2025.csv` | 223 | Nationality acquisitions by year and mode (long format) |
| `data/acquisitions_nationalite_par_nationalite_2025.csv` | 11 | Top 10 nationalities of origin and the total, 2024–2025 |
| `metadata.json` | – | Title, description, keywords and citation, reused on every platform |
| `scripts/` | – | Python scripts that rebuild the tables from the raw sources |

All files are UTF-8 CSV with a header row. Booleans are `True`/`False`.

## Column dictionary

### examen_civique_questions_officielles.csv
| Column | Description |
|---|---|
| `line_id` | `CSP-001`… / `CR-001`… / `NAT-001`…: mention plus line number in the official list |
| `mention` | `CSP`, `CR` or `NAT` |
| `mention_label` | Full name of the mention |
| `line_number` | Position in the official list, in its published order (the lists themselves are not numbered) |
| `theme_code`, `theme` | One of the 5 official themes (T1–T5) |
| `question_text` | Official wording, unchanged (typography as published) |
| `question_key` | Stable ID for a distinct question: the first 10 hex characters of the SHA-1 of the normalised text (lower case, accents, punctuation and spaces removed) |
| `repeat_in_list` | `True` if this line repeats a question already listed earlier in the same list |
| `in_csp`, `in_cr`, `in_nat` | Whether the same question (same key) appears in each list |
| `n_mentions` | How many of the three lists contain the question (1–3) |
| `source_format` | `html_text`, `pdf_text`, or `pdf_image_transcribed` (a PDF line published as an image, transcribed by hand and checked visually) |
| `source_url`, `source_licence`, `checked_on` | Provenance |

### examen_civique_questions_uniques.csv
`question_key`, `question_text` (first wording found), `in_csp`, `in_cr`, `in_nat`, `n_mentions`, `themes` (separated by ` | `), `line_ids` (space-separated).

### examen_civique_recouvrement_listes.csv
`mention`, `theme_code` (`ALL` = total), `theme`, `lines_in_list`, `distinct_questions`, `shared_with_csp`, `shared_with_cr`, `shared_with_nat` (empty for the list itself), `unique_to_this_list`, `image_lines_in_source`.

### examen_civique_structure_epreuve.csv
`theme_code`, `theme`, `notion`, `question_type` (`connaissance` / `mise_en_situation`), `questions_per_exam`, `applies_to`, `source`, `source_url`, `checked_on`. The rows add up to 40.

### examen_civique_faits_cles.csv
`fact_id`, `description_fr`, `value`, `unit`, `reference_date` (the date the figure refers to), `applies_to`, `source`, `source_url`, `checked_on`.

### acquisitions_nationalite_france_2008_2025.csv
`year`, `mode_code`, `mode_label_fr`, `count`, `note`, `source`, `source_url`, `checked_on`. Mode codes:
`all_acquisitions`, `registered_total`, `decree_total`, `decree_naturalisation`, `decree_reintegration`, `declaration_total`, `declaration_anticipated_minor`, `declaration_marriage`, `declaration_ascendant_sibling` (empty before 2016 because the mode did not exist), `declaration_other`, `automatic_no_formality` (2008–2025, Insee). For 2021–2025 only (DGEF figure 2): `decree_children_collective_effect`, `marriage_children_collective_effect`, `ascendant_sibling_children_collective_effect`, `interior_ministry_total`, and `decree_adults_derived` (decree total minus children, our calculation).

### acquisitions_nationalite_par_nationalite_2025.csv
`nationality_fr`, `iso3` (left empty for "Congolais" because the source does not say which Congo), `acquisitions_2024`, `acquisitions_2025`, `change_2024_2025_pct` and `share_of_all_2025_pct` (derived), the share of each acquisition mode in 2025 in % (DGEF figure 4), `scope`, `source_url`, `checked_on`.

## Method

- **CSP and CR lists:** downloaded from formation-civique.interieur.gouv.fr on 24 November 2026 and parsed from the HTML (section heading = theme, list item = question).
- **Naturalisation list:** DGEF PDF `examen-civique-naturalisation-questions-de-connaissance-20251212.pdf` (posted on 12 January 2026, 11 pages). Its tables were extracted with pdfplumber, which gives 244 text lines. The other 15 lines are embedded images. We extracted them with `pdfimages`, transcribed them by hand and checked them visually. The text-only line "?" that follows the image "Quelle mer se situe entre la France et l'Angleterre" is part of that question. The question «Qui peut se présenter aux élections présidentielles ?» appears twice in the PDF, at lines 40 and 48, so there are 258 distinct questions.
- **Cross-matching:** two lines count as the same question when their texts are identical after lower-casing and removing accents, punctuation, apostrophes and spaces. For example, "l'État" and "l'Etat" match. Differences in wording count as different questions.
- **Statistics:** transcribed from the Insee XLSX and the DGEF tables without changes. Derived values (adults by decree, percentage changes, shares) are labelled.
- **Consistency checks:** for every year, decree + declaration + no-formality equals the total, and the declaration sub-modes add up to the declaration total.

## Known limitations

- Answers and the 12 situational questions are not public and are not included.
- The exam figures (71,125 candidates, 81% pass rate, 444 centres) come from a single official snapshot dated 26 May 2026. They do not separate the three mentions. We found no later official figure as of 24 November 2026.
- DGEF figure 2 gives 32,553 anticipated declarations for 2023, while Insee and DGEF figure 1 give 32,533. This dataset uses the Insee value.
- The ministry's answer to written question no. 11488 gives 222 thematic sheets. The site itself showed more when it was counted later. This dataset only reports the official figure.
- The 2026 forecast (Senate report) and the NATALI figure (2025 annual performance report) were checked against copies of those PDFs downloaded on 22 November 2026.

## Sources

1. Ministère de l'Intérieur, *Liste officielle des questions de connaissance – CSP*, https://formation-civique.interieur.gouv.fr/examen-civique/liste-officielle-des-questions-de-connaissance-csp/ (licence etalab-2.0)
2. Ministère de l'Intérieur, *Liste officielle des questions de connaissance – CR*, https://formation-civique.interieur.gouv.fr/examen-civique/liste-officielle-des-questions-de-connaissance-cr/ (licence etalab-2.0)
3. DGEF, *Questions de connaissance pour l'examen civique – Nationalité française* (posted on 12/01/2026), https://www.immigration.interieur.gouv.fr/documentation/guides-textes-et-brochures/questions-de-connaissance-pour-lexamen-civique-nationalite-francaise.html, PDF: https://www.immigration.interieur.gouv.fr/sites/dgef/files/medias/documents/2026-01/examen-civique-naturalisation-questions-de-connaissance-20251212.pdf
4. Arrêté du 10 octobre 2025 relatif au programme, aux épreuves et aux modalités d'organisation de l'examen civique, https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000052381620
5. Ministère de l'Intérieur, *Informations générales sur l'examen civique*, https://formation-civique.interieur.gouv.fr/examen-civique/informations-g%C3%A9n%C3%A9rales-sur-lexamen-civique/
6. Assemblée nationale, written question no. 11488 and ministerial answer (JO 11 August 2026, p. 7488), https://questions.assemblee-nationale.fr/q17/17-11488QE.htm
7. Service-public.fr, F39426 (naturalisation: civic exam), https://www.service-public.gouv.fr/particuliers/vosdroits/F39426, and F39530 (CSP and CR: civic exam), https://www.service-public.gouv.fr/particuliers/vosdroits/F39530
8. Service-public.fr, A18881 (tax increases from 1 May 2026), https://www.service-public.gouv.fr/particuliers/actualites/A18881
9. Insee, *Acquisitions de la nationalité française, données annuelles de 2008 à 2025*, https://www.insee.fr/fr/statistiques/2381644
10. DGEF, *L'accès à la nationalité française pour l'année 2025*, https://www.immigration.interieur.gouv.fr/chiffres-de-limmigration-en-france/lacces-a-nationalite-francaise-pour-lannee-2025-moins-dacquisitions-de-nationalite-francaise-par (figures 1–5)
11. Sénat, rapport général no. 139 (2025-2026), tome III, annexe 15, https://www.senat.fr/rap/l25-139-315/l25-139-3151.pdf
12. Rapport annuel de performances 2025, mission « Immigration, asile et intégration », https://www.assemblee-nationale.fr/dyn/contenu/visualisation/1109864/file/Immigration_asile_integration_IA.pdf

## License and citation

The compilation, keys, cross-matching and derived tables are released under **CC BY 4.0**. The source texts and figures are French public sector information, reused under the Licence Ouverte / etalab-2.0 where the publisher states it, with attribution to the original publishers kept in every row.

> Vomigarbi, N. (2026). *French Civic Exam (Examen civique) 2026: Official Question Lists for All Three Mentions and Nationality Acquisition Statistics 2008–2025* (Version 1.0.0) [Data set]. Examen Civique Test. https://examen-civique-test.fr/

Interactive practice tool built on this dataset: [Examen Civique Test](https://examen-civique-test.fr/)

## Also available on

- [Zenodo (DOI 10.5281/zenodo.24496692)](https://doi.org/10.5281/zenodo.24496692)
- [Figshare](https://figshare.com/articles/dataset/_/35107942)
- [Hugging Face](https://huggingface.co/datasets/examen-civique-test/examen-civique-france-2026)
- [Kaggle](https://www.kaggle.com/datasets/nesravomigarbi/french-civic-exam-2026-and-naturalisation-stats)
- [DoltHub](https://www.dolthub.com/repositories/examen-civique-test/examen-civique-france-2026)
- [data.gouv.fr (FR)](https://www.data.gouv.fr/datasets/examen-civique-2026-listes-officielles-de-questions-csp-cr-naturalisation-et-statistiques-dacquisition-de-la-nationalite-2008-2025)
- [data.gouv.fr (EN)](https://www.data.gouv.fr/datasets/french-civic-exam-2026-official-question-lists-csp-cr-naturalisation-and-french-nationality-acquisition-statistics-2008-2025)
- [Wikidata (Q142273089)](https://www.wikidata.org/wiki/Q142273089)

## Code libraries

Language packages that bundle this dataset live under [`packages/`](packages/README.md): `examen-civique-france` for npm, PyPI and crates.io, `examen_civique_france` for RubyGems, and `nesravomigarbi/examen-civique-france` for Composer/Packagist. They are version 1.0.0. They have been prepared in this repository but have not been published to the public registries yet.

The PHP package is also in a dedicated repository, [nesravomigarbi/examen-civique-france-php](https://github.com/nesravomigarbi/examen-civique-france-php), so that Packagist can read `composer.json` at the repository root.
