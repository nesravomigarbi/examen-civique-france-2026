#!/usr/bin/env python3
"""Build bundled JSON for the examen-civique-france language packages from the dataset CSVs."""
from __future__ import annotations

import csv
import json
from collections import OrderedDict
from pathlib import Path

DATASET = Path("/workspace/naturalisation-fr-dataset")
OUT = Path("/workspace/packages/shared")

THEME_BY_NAME = {
    "Principes et valeurs de la République": "T1",
    "Système institutionnel et politique": "T2",
    "Droits et devoirs": "T3",
    "Histoire, géographie et culture": "T4",
    "Vivre dans la société française": "T5",
}

THEME_BY_CODE = {code: name for name, code in THEME_BY_NAME.items()}


def parse_bool(value: str) -> bool:
    return value == "True"


def parse_int_or_none(value: str):
    value = (value or "").strip()
    if value == "":
        return None
    return int(value)


def build_questions() -> list[dict]:
    path = DATASET / "data" / "examen_civique_questions_uniques.csv"
    rows = []
    with path.open(encoding="utf-8", newline="") as fh:
        for raw in csv.DictReader(fh):
            themes = [part.strip() for part in raw["themes"].split("|") if part.strip()]
            theme_codes = []
            for name in themes:
                code = THEME_BY_NAME.get(name)
                if code is None:
                    raise SystemExit(f"Unknown theme name in unique questions: {name!r}")
                theme_codes.append(code)
            rows.append(
                {
                    "question_key": raw["question_key"],
                    "question_text": raw["question_text"],
                    "in_csp": parse_bool(raw["in_csp"]),
                    "in_cr": parse_bool(raw["in_cr"]),
                    "in_nat": parse_bool(raw["in_nat"]),
                    "n_mentions": int(raw["n_mentions"]),
                    "themes": themes,
                    "theme_codes": theme_codes,
                    "line_ids": raw["line_ids"].split(),
                }
            )
    return rows


def build_acquisitions() -> list[dict]:
    path = DATASET / "data" / "acquisitions_nationalite_france_2008_2025.csv"
    by_year: dict[int, dict] = OrderedDict()
    with path.open(encoding="utf-8", newline="") as fh:
        for raw in csv.DictReader(fh):
            year = int(raw["year"])
            if year not in by_year:
                by_year[year] = {"year": year, "modes": {}}
            mode = raw["mode_code"]
            by_year[year]["modes"][mode] = {
                "mode_code": mode,
                "mode_label_fr": raw["mode_label_fr"],
                "count": parse_int_or_none(raw["count"]),
                "note": raw["note"],
                "source": raw["source"],
                "source_url": raw["source_url"],
                "checked_on": raw["checked_on"],
            }
    return list(by_year.values())


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    questions = build_questions()
    acquisitions = build_acquisitions()
    meta = {
        "dataset_title": "French Civic Exam (Examen civique) 2026: Official Question Lists for All Three Mentions and Nationality Acquisition Statistics 2008–2025",
        "dataset_version": "1.0.1",
        "package_version": "1.0.0",
        "doi": "10.5281/zenodo.24496692",
        "concept_doi": "10.5281/zenodo.24496463",
        "license_data": "CC-BY-4.0",
        "license_code": "MIT",
        "author": "Nesra Vomigarbi",
        "email": "data@examen-civique-test.fr",
        "homepage": "https://examen-civique-test.fr/",
        "repository": "https://github.com/nesravomigarbi/examen-civique-france-2026",
        "question_count": len(questions),
        "acquisition_year_count": len(acquisitions),
        "acquisition_year_min": acquisitions[0]["year"],
        "acquisition_year_max": acquisitions[-1]["year"],
        "themes": THEME_BY_CODE,
        "citation": "Vomigarbi, N. (2026). French Civic Exam (Examen civique) 2026: Official Question Lists for All Three Mentions and Nationality Acquisition Statistics 2008–2025 (Version 1.0.1) [Data set]. Examen Civique Test. https://examen-civique-test.fr/ https://doi.org/10.5281/zenodo.24496692",
    }
    (OUT / "questions.json").write_text(
        json.dumps(questions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "acquisitions.json").write_text(
        json.dumps(acquisitions, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "package_meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"questions={len(questions)}")
    print(f"in_csp={sum(1 for q in questions if q['in_csp'])}")
    print(f"in_cr={sum(1 for q in questions if q['in_cr'])}")
    print(f"in_nat={sum(1 for q in questions if q['in_nat'])}")
    print(f"years={acquisitions[0]['year']}-{acquisitions[-1]['year']} n={len(acquisitions)}")
    print("wrote", OUT / "questions.json", OUT / "acquisitions.json", OUT / "package_meta.json")


if __name__ == "__main__":
    main()
