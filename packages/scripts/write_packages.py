#!/usr/bin/env python3
"""Write source trees for the five language packages (does not publish)."""
from __future__ import annotations

import shutil
from pathlib import Path

ROOT = Path("/workspace/packages")
SHARED = ROOT / "shared"

HOMEPAGE = "https://examen-civique-test.fr/"
REPO = "https://github.com/nesravomigarbi/examen-civique-france-2026"
DOI = "10.5281/zenodo.24496692"
EMAIL = "data@examen-civique-test.fr"
AUTHOR = "Nesra Vomigarbi"
VERSION = "1.0.0"

CITATION = (
    "Vomigarbi, N. (2026). French Civic Exam (Examen civique) 2026: Official Question Lists "
    "for All Three Mentions and Nationality Acquisition Statistics 2008–2025 (Version 1.0.1) "
    "[Data set]. Examen Civique Test. https://examen-civique-test.fr/ "
    "https://doi.org/10.5281/zenodo.24496692"
)

CTA_EN = "Interactive practice tool built on this dataset: [Examen Civique Test](https://examen-civique-test.fr/)"
CTA_FR = "Outil d'entraînement interactif construit à partir de ce jeu de données : [Examen Civique Test](https://examen-civique-test.fr/)"

LICENSE_NOTICE = """This package contains both software and data.

- The library code is licensed under the MIT License. See LICENSE-MIT.
- The bundled dataset (question lists and nationality-acquisition statistics)
  is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).
  See LICENSE-DATA.

Source texts and official figures remain French public sector information
(Licence Ouverte / etalab-2.0 where the publisher states it). Attribution to
the original publishers is kept in the bundled records. Compilation, stable
keys and cross-matching are by Nesra Vomigarbi for Examen Civique Test
(https://examen-civique-test.fr/).
"""

CITATION_CFF = f"""cff-version: 1.2.0
message: "If you use this package, please cite the underlying dataset."
type: software
title: "examen-civique-france"
version: "{VERSION}"
authors:
  - family-names: Vomigarbi
    given-names: Nesra
    email: "{EMAIL}"
    affiliation: "Examen Civique Test (examen-civique-test.fr)"
license: "MIT AND CC-BY-4.0"
repository-code: "{REPO}"
url: "{HOMEPAGE}"
preferred-citation:
  type: dataset
  authors:
    - family-names: Vomigarbi
      given-names: Nesra
      affiliation: "Examen Civique Test (examen-civique-test.fr)"
  title: "French Civic Exam (Examen civique) 2026: Official Question Lists for All Three Mentions and Nationality Acquisition Statistics 2008–2025"
  version: "1.0.1"
  doi: "{DOI}"
  year: 2026
  publisher: "Examen Civique Test"
  url: "{HOMEPAGE}"
"""

KEYWORDS_COMMON = [
    "examen civique",
    "French civic exam",
    "naturalisation",
    "naturalization",
    "French citizenship",
    "nationalité française",
    "carte de séjour pluriannuelle",
    "carte de résident",
    "immigration France",
    "integration test",
    "citizenship test",
    "DGEF",
    "Insee",
    "open data",
    "France",
]


def readme(lang: str, install: str, usage: str, api_names: str) -> str:
    titles = {
        "npm": "JavaScript / Node.js library",
        "python": "Python library",
        "rust": "Rust crate",
        "ruby": "Ruby gem",
        "php": "PHP library",
    }
    title = titles[lang]
    install_fr = {
        "npm": "```bash\nnpm install examen-civique-france\n```",
        "python": "```bash\npip install examen-civique-france\n```",
        "rust": "```toml\n[dependencies]\nexamen-civique-france = \"1.0.0\"\n```",
        "ruby": "```ruby\ngem \"examen_civique_france\", \"1.0.0\"\n```\n\n```bash\ngem install examen_civique_france\n```",
        "php": "```bash\ncomposer require nesravomigarbi/examen-civique-france\n```",
    }[lang]
    return f"""# examen-civique-france

{title} for the official knowledge-question lists of France's civic exam (*examen civique*, 2026) and Insee/DGEF statistics on acquisitions of French nationality, 2008–2025.

The package bundles **523** distinct questions compiled from the three official lists (CSP, CR and naturalisation; 659 published lines) and yearly acquisition counts for **2008–2025** (18 years). Answers are not included.

Compiled by {AUTHOR} for [Examen Civique Test](https://examen-civique-test.fr/), an independent exam-preparation site not affiliated with the French State.

{CTA_EN}

## Install

{install}

These packages have not been published to the public registries yet. Until they are, install from this repository, for example after cloning [{REPO}]({REPO}).

## Usage

{usage}

## API

{api_names}

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

- Homepage: <{HOMEPAGE}>
- Repository: <{REPO}>
- Dataset DOI: [https://doi.org/{DOI}](https://doi.org/{DOI})
- Version of this package: {VERSION}
- Dataset version cited here: 1.0.1

## Citation

> {CITATION}

## License

- **Code:** [MIT](LICENSE-MIT)
- **Bundled data:** [CC BY 4.0](LICENSE-DATA)

The source texts and official figures are French public sector information, reused under the Licence Ouverte / etalab-2.0 where the publisher states it, with attribution kept in each record.

---

## Français

Bibliothèque pour les listes officielles de questions de connaissance de l'examen civique 2026 et les statistiques Insee/DGEF des acquisitions de la nationalité française, 2008-2025.

Le paquet inclut **523** questions distinctes, établies à partir des trois listes officielles (CSP, CR et naturalisation ; 659 lignes publiées), ainsi que les totaux annuels d'acquisitions pour **2008-2025**. Les réponses ne sont pas incluses.

Compilé par {AUTHOR} pour [Examen Civique Test](https://examen-civique-test.fr/), site d'entraînement indépendant, sans lien avec l'administration française.

{CTA_FR}

### Installation

{install_fr}

### Citation

> {CITATION}

### Licence

Code : MIT. Données incluses : CC BY 4.0.
"""


def copy_common(dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    data = dest / "data"
    data.mkdir(exist_ok=True)
    shutil.copy(SHARED / "questions.json", data / "questions.json")
    shutil.copy(SHARED / "acquisitions.json", data / "acquisitions.json")
    shutil.copy(SHARED / "LICENSE-MIT", dest / "LICENSE")
    shutil.copy(SHARED / "LICENSE-MIT", dest / "LICENSE-MIT")
    shutil.copy(SHARED / "LICENSE-CC-BY-4.0", dest / "LICENSE-DATA")
    (dest / "LICENSE-NOTICE").write_text(LICENSE_NOTICE, encoding="utf-8")
    (dest / "CITATION.cff").write_text(CITATION_CFF, encoding="utf-8")


# ---------------------------------------------------------------------------
# npm
# ---------------------------------------------------------------------------

NPM_INDEX_JS = r'''import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const QUESTIONS = JSON.parse(
  readFileSync(join(here, "../data/questions.json"), "utf8"),
);
const ACQUISITIONS = JSON.parse(
  readFileSync(join(here, "../data/acquisitions.json"), "utf8"),
);

export const THEMES = Object.freeze({
  T1: "Principes et valeurs de la République",
  T2: "Système institutionnel et politique",
  T3: "Droits et devoirs",
  T4: "Histoire, géographie et culture",
  T5: "Vivre dans la société française",
});

const MENTION_FLAG = { CSP: "in_csp", CR: "in_cr", NAT: "in_nat" };

const MENTION_ALIASES = new Map([
  ["csp", "CSP"],
  ["carte de sejour pluriannuelle", "CSP"],
  ["cr", "CR"],
  ["carte de resident", "CR"],
  ["nat", "NAT"],
  ["naturalisation", "NAT"],
  ["naturalization", "NAT"],
  ["nationalite", "NAT"],
  ["nationalite francaise", "NAT"],
]);

function fold(value) {
  return String(value)
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{M}/gu, "");
}

export function normalizeMention(mention) {
  if (mention == null || String(mention).trim() === "") {
    throw new Error("mention is required (CSP, CR or NAT)");
  }
  const mapped = MENTION_ALIASES.get(fold(mention));
  if (!mapped) {
    throw new Error(`unknown mention: ${mention} (use CSP, CR or NAT)`);
  }
  return mapped;
}

export function normalizeTheme(theme) {
  if (theme == null || String(theme).trim() === "") {
    throw new Error("theme is required (T1–T5 or an official theme name)");
  }
  const key = fold(theme);
  for (const [code, name] of Object.entries(THEMES)) {
    if (key === fold(code) || key === fold(name)) {
      return { code, name };
    }
  }
  throw new Error(`unknown theme: ${theme} (use T1–T5 or an official theme name)`);
}

function mentionFlag(mention) {
  return MENTION_FLAG[normalizeMention(mention)];
}

function pool(options = {}) {
  let items = QUESTIONS;
  if (options.mention != null || options.level != null) {
    const flag = mentionFlag(options.mention ?? options.level);
    items = items.filter((question) => question[flag]);
  }
  if (options.theme != null) {
    const { code } = normalizeTheme(options.theme);
    items = items.filter((question) => question.theme_codes.includes(code));
  }
  return items;
}

function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function randomSource(seed) {
  if (seed === undefined || seed === null) {
    return Math.random;
  }
  const value = Number(seed);
  if (!Number.isFinite(value)) {
    throw new Error("seed must be a finite number");
  }
  return mulberry32(value);
}

export function allQuestions() {
  return QUESTIONS.slice();
}

export function byMention(mention) {
  const flag = mentionFlag(mention);
  return QUESTIONS.filter((question) => question[flag]);
}

export const byLevel = byMention;

export function byTheme(theme) {
  const { code } = normalizeTheme(theme);
  return QUESTIONS.filter((question) => question.theme_codes.includes(code));
}

export function randomQuestion(options = {}) {
  const items = pool(options);
  if (items.length === 0) {
    throw new Error("no questions match the given filters");
  }
  const random = randomSource(options.seed);
  return items[Math.floor(random() * items.length)];
}

export function mockExam(n, options = {}) {
  if (!Number.isInteger(n) || n < 1) {
    throw new Error("n must be a positive integer");
  }
  const items = pool(options).slice();
  if (n > items.length) {
    throw new Error(
      `cannot build a mock exam of ${n} questions; only ${items.length} match the filters`,
    );
  }
  const random = randomSource(options.seed);
  for (let i = 0; i < n; i += 1) {
    const j = i + Math.floor(random() * (items.length - i));
    const swap = items[i];
    items[i] = items[j];
    items[j] = swap;
  }
  return items.slice(0, n);
}

export function acquisitionsByYear(year) {
  if (year === undefined || year === null) {
    return ACQUISITIONS.map((row) => ({ year: row.year, modes: { ...row.modes } }));
  }
  const value = Number(year);
  if (!Number.isInteger(value)) {
    throw new Error("year must be an integer");
  }
  const row = ACQUISITIONS.find((item) => item.year === value);
  if (!row) {
    throw new Error(`no acquisition statistics for year ${year}`);
  }
  return { year: row.year, modes: { ...row.modes } };
}

export const dataset = Object.freeze({
  questionCount: QUESTIONS.length,
  acquisitionYears: ACQUISITIONS.map((row) => row.year),
  doi: "10.5281/zenodo.24496692",
  homepage: "https://examen-civique-test.fr/",
});
'''

NPM_INDEX_CJS = r'''const { readFileSync } = require("node:fs");
const { join } = require("node:path");

const QUESTIONS = JSON.parse(
  readFileSync(join(__dirname, "../data/questions.json"), "utf8"),
);
const ACQUISITIONS = JSON.parse(
  readFileSync(join(__dirname, "../data/acquisitions.json"), "utf8"),
);

const THEMES = Object.freeze({
  T1: "Principes et valeurs de la République",
  T2: "Système institutionnel et politique",
  T3: "Droits et devoirs",
  T4: "Histoire, géographie et culture",
  T5: "Vivre dans la société française",
});

const MENTION_FLAG = { CSP: "in_csp", CR: "in_cr", NAT: "in_nat" };

const MENTION_ALIASES = new Map([
  ["csp", "CSP"],
  ["carte de sejour pluriannuelle", "CSP"],
  ["cr", "CR"],
  ["carte de resident", "CR"],
  ["nat", "NAT"],
  ["naturalisation", "NAT"],
  ["naturalization", "NAT"],
  ["nationalite", "NAT"],
  ["nationalite francaise", "NAT"],
]);

function fold(value) {
  return String(value)
    .trim()
    .toLowerCase()
    .normalize("NFD")
    .replace(/\p{M}/gu, "");
}

function normalizeMention(mention) {
  if (mention == null || String(mention).trim() === "") {
    throw new Error("mention is required (CSP, CR or NAT)");
  }
  const mapped = MENTION_ALIASES.get(fold(mention));
  if (!mapped) {
    throw new Error(`unknown mention: ${mention} (use CSP, CR or NAT)`);
  }
  return mapped;
}

function normalizeTheme(theme) {
  if (theme == null || String(theme).trim() === "") {
    throw new Error("theme is required (T1–T5 or an official theme name)");
  }
  const key = fold(theme);
  for (const [code, name] of Object.entries(THEMES)) {
    if (key === fold(code) || key === fold(name)) {
      return { code, name };
    }
  }
  throw new Error(`unknown theme: ${theme} (use T1–T5 or an official theme name)`);
}

function mentionFlag(mention) {
  return MENTION_FLAG[normalizeMention(mention)];
}

function pool(options = {}) {
  let items = QUESTIONS;
  if (options.mention != null || options.level != null) {
    const flag = mentionFlag(options.mention ?? options.level);
    items = items.filter((question) => question[flag]);
  }
  if (options.theme != null) {
    const { code } = normalizeTheme(options.theme);
    items = items.filter((question) => question.theme_codes.includes(code));
  }
  return items;
}

function mulberry32(seed) {
  let a = seed >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function randomSource(seed) {
  if (seed === undefined || seed === null) {
    return Math.random;
  }
  const value = Number(seed);
  if (!Number.isFinite(value)) {
    throw new Error("seed must be a finite number");
  }
  return mulberry32(value);
}

function allQuestions() {
  return QUESTIONS.slice();
}

function byMention(mention) {
  const flag = mentionFlag(mention);
  return QUESTIONS.filter((question) => question[flag]);
}

const byLevel = byMention;

function byTheme(theme) {
  const { code } = normalizeTheme(theme);
  return QUESTIONS.filter((question) => question.theme_codes.includes(code));
}

function randomQuestion(options = {}) {
  const items = pool(options);
  if (items.length === 0) {
    throw new Error("no questions match the given filters");
  }
  const random = randomSource(options.seed);
  return items[Math.floor(random() * items.length)];
}

function mockExam(n, options = {}) {
  if (!Number.isInteger(n) || n < 1) {
    throw new Error("n must be a positive integer");
  }
  const items = pool(options).slice();
  if (n > items.length) {
    throw new Error(
      `cannot build a mock exam of ${n} questions; only ${items.length} match the filters`,
    );
  }
  const random = randomSource(options.seed);
  for (let i = 0; i < n; i += 1) {
    const j = i + Math.floor(random() * (items.length - i));
    const swap = items[i];
    items[i] = items[j];
    items[j] = swap;
  }
  return items.slice(0, n);
}

function acquisitionsByYear(year) {
  if (year === undefined || year === null) {
    return ACQUISITIONS.map((row) => ({ year: row.year, modes: { ...row.modes } }));
  }
  const value = Number(year);
  if (!Number.isInteger(value)) {
    throw new Error("year must be an integer");
  }
  const row = ACQUISITIONS.find((item) => item.year === value);
  if (!row) {
    throw new Error(`no acquisition statistics for year ${year}`);
  }
  return { year: row.year, modes: { ...row.modes } };
}

const dataset = Object.freeze({
  questionCount: QUESTIONS.length,
  acquisitionYears: ACQUISITIONS.map((row) => row.year),
  doi: "10.5281/zenodo.24496692",
  homepage: "https://examen-civique-test.fr/",
});

module.exports = {
  THEMES,
  normalizeMention,
  normalizeTheme,
  allQuestions,
  byMention,
  byLevel,
  byTheme,
  randomQuestion,
  mockExam,
  acquisitionsByYear,
  dataset,
};
'''

NPM_DTS = r'''export type Mention = "CSP" | "CR" | "NAT";
export type ThemeCode = "T1" | "T2" | "T3" | "T4" | "T5";

export interface Question {
  question_key: string;
  question_text: string;
  in_csp: boolean;
  in_cr: boolean;
  in_nat: boolean;
  n_mentions: number;
  themes: string[];
  theme_codes: ThemeCode[];
  line_ids: string[];
}

export interface AcquisitionMode {
  mode_code: string;
  mode_label_fr: string;
  count: number | null;
  note: string;
  source: string;
  source_url: string;
  checked_on: string;
}

export interface AcquisitionsYear {
  year: number;
  modes: Record<string, AcquisitionMode>;
}

export interface QueryOptions {
  mention?: Mention | string;
  level?: Mention | string;
  theme?: ThemeCode | string;
  seed?: number;
}

export const THEMES: Readonly<Record<ThemeCode, string>>;

export const dataset: Readonly<{
  questionCount: number;
  acquisitionYears: number[];
  doi: string;
  homepage: string;
}>;

export function normalizeMention(mention: Mention | string): Mention;
export function normalizeTheme(theme: ThemeCode | string): { code: ThemeCode; name: string };

/** All 523 distinct questions. */
export function allQuestions(): Question[];

/** Distinct questions that appear in the given official list (CSP, CR or NAT). */
export function byMention(mention: Mention | string): Question[];

/** Alias of `byMention`. */
export function byLevel(mention: Mention | string): Question[];

/** Distinct questions tagged with the given official theme code or name. */
export function byTheme(theme: ThemeCode | string): Question[];

/** One question drawn from the (optionally filtered) pool. */
export function randomQuestion(options?: QueryOptions): Question;

/**
 * `n` distinct questions drawn without replacement.
 * The official exam has 28 knowledge questions; situational questions are not in this dataset.
 */
export function mockExam(n: number, options?: QueryOptions): Question[];

/** Acquisition statistics for every year 2008–2025, or for a single year. */
export function acquisitionsByYear(year?: number): AcquisitionsYear[] | AcquisitionsYear;
'''

NPM_TEST = r'''import assert from "node:assert/strict";
import { createRequire } from "node:module";
import { test } from "node:test";
import {
  THEMES,
  acquisitionsByYear,
  allQuestions,
  byLevel,
  byMention,
  byTheme,
  mockExam,
  randomQuestion,
} from "../src/index.js";

const require = createRequire(import.meta.url);
const cjs = require("../src/index.cjs");

test("allQuestions returns 523 distinct questions", () => {
  const questions = allQuestions();
  assert.equal(questions.length, 523);
  assert.equal(new Set(questions.map((q) => q.question_key)).size, 523);
});

test("mention filters match the unique-question table", () => {
  assert.equal(byMention("CSP").length, 190);
  assert.equal(byMention("CR").length, 209);
  assert.equal(byMention("NAT").length, 258);
  assert.equal(byLevel("carte de séjour pluriannuelle").length, 190);
  assert.equal(byMention("naturalisation").length, 258);
});

test("theme filters match the unique-question table", () => {
  assert.equal(byTheme("T1").length, 93);
  assert.equal(byTheme("T2").length, 111);
  assert.equal(byTheme("T3").length, 94);
  assert.equal(byTheme("T4").length, 143);
  assert.equal(byTheme("T5").length, 83);
  assert.equal(byTheme("Histoire, géographie et culture").length, 143);
  assert.equal(
    byTheme("T1").length +
      byTheme("T2").length +
      byTheme("T3").length +
      byTheme("T4").length +
      byTheme("T5").length,
    524,
  );
  assert.equal(Object.keys(THEMES).length, 5);
});

test("the two-theme question is in T1 and T3", () => {
  const key = "Q93946df581";
  assert.ok(byTheme("T1").some((q) => q.question_key === key));
  assert.ok(byTheme("T3").some((q) => q.question_key === key));
});

test("mockExam draws n distinct questions and is deterministic with a seed", () => {
  const first = mockExam(28, { mention: "NAT", seed: 42 });
  const second = mockExam(28, { mention: "NAT", seed: 42 });
  assert.equal(first.length, 28);
  assert.equal(new Set(first.map((q) => q.question_key)).size, 28);
  assert.deepEqual(
    first.map((q) => q.question_key),
    second.map((q) => q.question_key),
  );
  assert.ok(first.every((q) => q.in_nat));
});

test("randomQuestion respects filters", () => {
  const question = randomQuestion({ mention: "CSP", theme: "T4", seed: 7 });
  assert.equal(question.in_csp, true);
  assert.ok(question.theme_codes.includes("T4"));
});

test("acquisitionsByYear uses the Insee yearly totals", () => {
  const all = acquisitionsByYear();
  assert.equal(all.length, 18);
  assert.equal(all[0].year, 2008);
  assert.equal(all[all.length - 1].year, 2025);
  const y2010 = acquisitionsByYear(2010);
  assert.equal(y2010.modes.decree_total.count, 94573);
  const y2025 = acquisitionsByYear(2025);
  assert.equal(y2025.modes.decree_total.count, 42246);
  assert.equal(acquisitionsByYear(2008).modes.declaration_ascendant_sibling.count, null);
});

test("invalid input throws", () => {
  assert.throws(() => byMention("XYZ"), /unknown mention/);
  assert.throws(() => byTheme("T9"), /unknown theme/);
  assert.throws(() => mockExam(0), /positive integer/);
  assert.throws(() => mockExam(10_000), /only 523/);
});

test("CommonJS export matches the ESM API surface", () => {
  assert.equal(cjs.allQuestions().length, 523);
  assert.equal(cjs.byMention("CR").length, 209);
  assert.equal(cjs.acquisitionsByYear(2010).modes.decree_total.count, 94573);
  assert.deepEqual(
    mockExam(5, { seed: 99 }).map((q) => q.question_key),
    cjs.mockExam(5, { seed: 99 }).map((q) => q.question_key),
  );
});
'''

NPM_PACKAGE_JSON = {
    "name": "examen-civique-france",
    "version": VERSION,
    "description": "Official French civic exam (examen civique) 2026 question lists and nationality acquisition statistics 2008–2025.",
    "author": {
        "name": AUTHOR,
        "email": EMAIL,
        "url": HOMEPAGE,
    },
    "license": "(MIT AND CC-BY-4.0)",
    "homepage": HOMEPAGE,
    "repository": {
        "type": "git",
        "url": "git+https://github.com/nesravomigarbi/examen-civique-france-2026.git",
        "directory": "packages/npm",
    },
    "documentation": REPO,
    "bugs": {"url": f"{REPO}/issues"},
    "keywords": KEYWORDS_COMMON,
    "type": "module",
    "main": "./src/index.cjs",
    "module": "./src/index.js",
    "types": "./types/index.d.ts",
    "exports": {
        ".": {
            "types": "./types/index.d.ts",
            "import": "./src/index.js",
            "require": "./src/index.cjs",
        },
        "./data/questions.json": "./data/questions.json",
        "./data/acquisitions.json": "./data/acquisitions.json",
        "./package.json": "./package.json",
    },
    "files": [
        "src",
        "data",
        "types",
        "LICENSE",
        "LICENSE-MIT",
        "LICENSE-DATA",
        "LICENSE-NOTICE",
        "README.md",
        "CITATION.cff",
    ],
    "engines": {"node": ">=18"},
    "scripts": {"test": "node --test test/test.js"},
}


def write_npm() -> None:
    import json

    dest = ROOT / "npm"
    if dest.exists():
        shutil.rmtree(dest)
    copy_common(dest)
    (dest / "src").mkdir()
    (dest / "types").mkdir()
    (dest / "test").mkdir()
    (dest / "src" / "index.js").write_text(NPM_INDEX_JS, encoding="utf-8")
    (dest / "src" / "index.cjs").write_text(NPM_INDEX_CJS, encoding="utf-8")
    (dest / "types" / "index.d.ts").write_text(NPM_DTS, encoding="utf-8")
    (dest / "test" / "test.js").write_text(NPM_TEST, encoding="utf-8")
    (dest / "package.json").write_text(
        json.dumps(NPM_PACKAGE_JSON, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (dest / "README.md").write_text(
        readme(
            "npm",
            "```bash\nnpm install examen-civique-france\n```\n\nThe package supports both ESM (`import`) and CommonJS (`require`). TypeScript typings are included.",
            """```js
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
""",
            """- `allQuestions()` — all 523 distinct questions
- `byMention(mention)` — questions that appear in the CSP, CR or NAT list
- `byLevel(mention)` — alias of `byMention`
- `byTheme(theme)` — filter by official theme code (`T1`–`T5`) or theme name
- `randomQuestion({ mention, theme, seed })` — one question
- `mockExam(n, { mention, theme, seed })` — `n` distinct questions
- `acquisitionsByYear()` / `acquisitionsByYear(2025)` — yearly statistics
""",
        ),
        encoding="utf-8",
    )


# The rest of the packages are written by the same script in a second part
# executed below if this file is complete. We write npm first, then continue.

if __name__ == "__main__":
    write_npm()
    print("wrote npm")
