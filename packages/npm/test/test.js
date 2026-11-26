import assert from "node:assert/strict";
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
