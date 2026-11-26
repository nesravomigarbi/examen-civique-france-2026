export type Mention = "CSP" | "CR" | "NAT";
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
