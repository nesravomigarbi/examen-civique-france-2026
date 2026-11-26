import { readFileSync } from "node:fs";
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
