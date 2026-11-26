//! Official French civic exam (examen civique) 2026 questions and nationality statistics.

use serde::{Deserialize, Serialize};
use std::collections::BTreeMap;
use std::sync::OnceLock;
use std::time::{SystemTime, UNIX_EPOCH};

const QUESTIONS_JSON: &str = include_str!("../data/questions.json");
const ACQUISITIONS_JSON: &str = include_str!("../data/acquisitions.json");

pub const DOI: &str = "10.5281/zenodo.24496692";
pub const HOMEPAGE: &str = "https://examen-civique-test.fr/";

/// Official theme codes and their French names.
pub const THEMES: &[(&str, &str)] = &[
    ("T1", "Principes et valeurs de la République"),
    ("T2", "Système institutionnel et politique"),
    ("T3", "Droits et devoirs"),
    ("T4", "Histoire, géographie et culture"),
    ("T5", "Vivre dans la société française"),
];

/// A distinct knowledge question from the official lists.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct Question {
    pub question_key: String,
    pub question_text: String,
    pub in_csp: bool,
    pub in_cr: bool,
    pub in_nat: bool,
    pub n_mentions: u8,
    pub themes: Vec<String>,
    pub theme_codes: Vec<String>,
    pub line_ids: Vec<String>,
}

/// One acquisition mode for a given year.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AcquisitionMode {
    pub mode_code: String,
    pub mode_label_fr: String,
    pub count: Option<i64>,
    pub note: String,
    pub source: String,
    pub source_url: String,
    pub checked_on: String,
}

/// Nationality-acquisition statistics for a calendar year.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct AcquisitionsYear {
    pub year: i32,
    pub modes: BTreeMap<String, AcquisitionMode>,
}

/// Optional filters for [`random_question_with`] and [`mock_exam_with`].
#[derive(Debug, Clone, Default)]
pub struct Filter {
    mention: Option<String>,
    theme: Option<String>,
    seed: Option<u64>,
}

impl Filter {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn mention(mut self, mention: impl Into<String>) -> Self {
        self.mention = Some(mention.into());
        self
    }

    pub fn level(self, mention: impl Into<String>) -> Self {
        self.mention(mention)
    }

    pub fn theme(mut self, theme: impl Into<String>) -> Self {
        self.theme = Some(theme.into());
        self
    }

    pub fn seed(mut self, seed: u64) -> Self {
        self.seed = Some(seed);
        self
    }
}

/// Error returned when a filter or argument is invalid.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Error {
    UnknownMention(String),
    UnknownTheme(String),
    InvalidCount,
    EmptyPool,
    UnknownYear(i32),
}

impl std::fmt::Display for Error {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Error::UnknownMention(value) => {
                write!(f, "unknown mention: {value} (use CSP, CR or NAT)")
            }
            Error::UnknownTheme(value) => {
                write!(
                    f,
                    "unknown theme: {value} (use T1–T5 or an official theme name)"
                )
            }
            Error::InvalidCount => write!(f, "n must be a positive integer"),
            Error::EmptyPool => write!(f, "no questions match the given filters"),
            Error::UnknownYear(year) => {
                write!(f, "no acquisition statistics for year {year}")
            }
        }
    }
}

impl std::error::Error for Error {}

fn questions() -> &'static [Question] {
    static QUESTIONS: OnceLock<Vec<Question>> = OnceLock::new();
    QUESTIONS.get_or_init(|| {
        serde_json::from_str(QUESTIONS_JSON).expect("bundled questions JSON is valid")
    })
}

fn acquisitions() -> &'static [AcquisitionsYear] {
    static ACQUISITIONS: OnceLock<Vec<AcquisitionsYear>> = OnceLock::new();
    ACQUISITIONS.get_or_init(|| {
        serde_json::from_str(ACQUISITIONS_JSON).expect("bundled acquisitions JSON is valid")
    })
}

fn fold(value: &str) -> String {
    value
        .trim()
        .to_lowercase()
        .chars()
        .filter(|ch| {
            let mut buf = [0u8; 4];
            let s = ch.encode_utf8(&mut buf);
            !s.chars().any(|c| {
                unicode_canonical_combining(c)
            })
            && !is_combining(*ch)
        })
        .flat_map(|ch| decompose_strip(ch))
        .collect()
}

fn is_combining(ch: char) -> bool {
    let u = ch as u32;
    (0x0300..=0x036F).contains(&u)
        || (0x1AB0..=0x1AFF).contains(&u)
        || (0x1DC0..=0x1DFF).contains(&u)
        || (0x20D0..=0x20FF).contains(&u)
        || (0xFE20..=0xFE2F).contains(&u)
}

fn unicode_canonical_combining(_ch: char) -> bool {
    false
}

fn decompose_strip(ch: char) -> Vec<char> {
    // Minimal NFD-style stripping for the French letters used in theme and mention names.
    match ch {
        'à' | 'á' | 'â' | 'ä' | 'ã' => vec!['a'],
        'è' | 'é' | 'ê' | 'ë' => vec!['e'],
        'ì' | 'í' | 'î' | 'ï' => vec!['i'],
        'ò' | 'ó' | 'ô' | 'ö' | 'õ' => vec!['o'],
        'ù' | 'ú' | 'û' | 'ü' => vec!['u'],
        'ý' | 'ÿ' => vec!['y'],
        'ç' => vec!['c'],
        'ñ' => vec!['n'],
        'À' | 'Á' | 'Â' | 'Ä' | 'Ã' => vec!['A'],
        'È' | 'É' | 'Ê' | 'Ë' => vec!['E'],
        other if is_combining(other) => vec![],
        other => vec![other],
    }
}

fn normalize_mention(mention: &str) -> Result<&'static str, Error> {
    if mention.trim().is_empty() {
        return Err(Error::UnknownMention(mention.to_string()));
    }
    let key = fold(mention);
    let mapped = match key.as_str() {
        "csp" | "carte de sejour pluriannuelle" => "CSP",
        "cr" | "carte de resident" => "CR",
        "nat" | "naturalisation" | "naturalization" | "nationalite" | "nationalite francaise" => {
            "NAT"
        }
        _ => return Err(Error::UnknownMention(mention.to_string())),
    };
    Ok(mapped)
}

fn normalize_theme(theme: &str) -> Result<&'static str, Error> {
    if theme.trim().is_empty() {
        return Err(Error::UnknownTheme(theme.to_string()));
    }
    let key = fold(theme);
    for (code, name) in THEMES {
        if key == fold(code) || key == fold(name) {
            return Ok(*code);
        }
    }
    Err(Error::UnknownTheme(theme.to_string()))
}

fn mention_matches(question: &Question, mention: &str) -> bool {
    match mention {
        "CSP" => question.in_csp,
        "CR" => question.in_cr,
        "NAT" => question.in_nat,
        _ => false,
    }
}

fn pool(filter: &Filter) -> Result<Vec<&'static Question>, Error> {
    let mut items: Vec<&'static Question> = questions().iter().collect();
    if let Some(mention) = &filter.mention {
        let mention = normalize_mention(mention)?;
        items.retain(|question| mention_matches(question, mention));
    }
    if let Some(theme) = &filter.theme {
        let code = normalize_theme(theme)?;
        items.retain(|question| question.theme_codes.iter().any(|item| item == code));
    }
    Ok(items)
}

/// Mulberry32, same construction as in the other language packages.
fn mulberry32(seed: u32) -> impl FnMut() -> f64 {
    let mut a = seed;
    move || {
        a = a.wrapping_add(0x6D2B79F5);
        let mut t = a;
        t = (t ^ t.wrapping_shr(15)).wrapping_mul(t | 1);
        t ^= t.wrapping_add((t ^ t.wrapping_shr(7)).wrapping_mul(t | 61));
        ((t ^ t.wrapping_shr(14)) as f64) / 4294967296.0
    }
}

fn time_seed() -> u32 {
    SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map(|duration| duration.as_nanos() as u32)
        .unwrap_or(1)
}

fn rng(seed: Option<u64>) -> impl FnMut() -> f64 {
    mulberry32(seed.map(|value| value as u32).unwrap_or_else(time_seed))
}

/// All 523 distinct questions.
pub fn all_questions() -> &'static [Question] {
    questions()
}

/// Distinct questions that appear in the given official list (`CSP`, `CR` or `NAT`).
pub fn by_mention(mention: &str) -> Result<Vec<&'static Question>, Error> {
    let mention = normalize_mention(mention)?;
    Ok(questions()
        .iter()
        .filter(|question| mention_matches(question, mention))
        .collect())
}

/// Alias of [`by_mention`].
pub fn by_level(mention: &str) -> Result<Vec<&'static Question>, Error> {
    by_mention(mention)
}

/// Distinct questions tagged with the given official theme code or name.
pub fn by_theme(theme: &str) -> Result<Vec<&'static Question>, Error> {
    let code = normalize_theme(theme)?;
    Ok(questions()
        .iter()
        .filter(|question| question.theme_codes.iter().any(|item| item == code))
        .collect())
}

/// One question drawn from the full pool.
pub fn random_question() -> &'static Question {
    random_question_with(&Filter::new()).expect("the unfiltered pool is not empty")
}

/// One question drawn from the (optionally filtered) pool.
pub fn random_question_with(filter: &Filter) -> Result<&'static Question, Error> {
    let items = pool(filter)?;
    if items.is_empty() {
        return Err(Error::EmptyPool);
    }
    let mut random = rng(filter.seed);
    let index = (random() * items.len() as f64).floor() as usize;
    Ok(items[index.min(items.len() - 1)])
}

/// `n` distinct questions drawn without replacement from the full pool.
pub fn mock_exam(n: usize) -> Result<Vec<&'static Question>, Error> {
    mock_exam_with(n, &Filter::new())
}

/// `n` distinct questions drawn without replacement from the (optionally filtered) pool.
pub fn mock_exam_with(n: usize, filter: &Filter) -> Result<Vec<&'static Question>, Error> {
    if n < 1 {
        return Err(Error::InvalidCount);
    }
    let mut items = pool(filter)?;
    if n > items.len() {
        return Err(Error::InvalidCount);
    }
    let mut random = rng(filter.seed);
    for i in 0..n {
        let offset = (random() * (items.len() - i) as f64).floor() as usize;
        let j = i + offset.min(items.len() - i - 1);
        items.swap(i, j);
    }
    items.truncate(n);
    Ok(items)
}

/// Acquisition statistics for every year 2008–2025, or for a single year.
pub fn acquisitions_by_year(year: Option<i32>) -> Result<Vec<AcquisitionsYear>, Error> {
    match year {
        None => Ok(acquisitions().to_vec()),
        Some(year) => acquisitions()
            .iter()
            .find(|row| row.year == year)
            .cloned()
            .map(|row| vec![row])
            .ok_or(Error::UnknownYear(year)),
    }
}

/// Convenience: the single-year record, if present.
pub fn acquisitions_for_year(year: i32) -> Result<AcquisitionsYear, Error> {
    acquisitions()
        .iter()
        .find(|row| row.year == year)
        .cloned()
        .ok_or(Error::UnknownYear(year))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn all_questions_count() {
        let questions = all_questions();
        assert_eq!(questions.len(), 523);
        let keys: std::collections::HashSet<_> =
            questions.iter().map(|q| q.question_key.as_str()).collect();
        assert_eq!(keys.len(), 523);
    }

    #[test]
    fn mention_filters() {
        assert_eq!(by_mention("CSP").unwrap().len(), 190);
        assert_eq!(by_mention("CR").unwrap().len(), 209);
        assert_eq!(by_mention("NAT").unwrap().len(), 258);
        assert_eq!(
            by_level("carte de séjour pluriannuelle").unwrap().len(),
            190
        );
        assert_eq!(by_mention("naturalisation").unwrap().len(), 258);
    }

    #[test]
    fn theme_filters() {
        assert_eq!(by_theme("T1").unwrap().len(), 93);
        assert_eq!(by_theme("T2").unwrap().len(), 111);
        assert_eq!(by_theme("T3").unwrap().len(), 94);
        assert_eq!(by_theme("T4").unwrap().len(), 143);
        assert_eq!(by_theme("T5").unwrap().len(), 83);
        assert_eq!(
            by_theme("Histoire, géographie et culture").unwrap().len(),
            143
        );
        let total: usize = THEMES.iter().map(|(code, _)| by_theme(code).unwrap().len()).sum();
        assert_eq!(total, 524);
    }

    #[test]
    fn two_theme_question() {
        let key = "Q93946df581";
        assert!(by_theme("T1")
            .unwrap()
            .iter()
            .any(|q| q.question_key == key));
        assert!(by_theme("T3")
            .unwrap()
            .iter()
            .any(|q| q.question_key == key));
    }

    #[test]
    fn mock_exam_is_deterministic_with_seed() {
        let filter = Filter::new().mention("NAT").seed(42);
        let first = mock_exam_with(28, &filter).unwrap();
        let second = mock_exam_with(28, &filter).unwrap();
        assert_eq!(first.len(), 28);
        let keys: std::collections::HashSet<_> =
            first.iter().map(|q| q.question_key.as_str()).collect();
        assert_eq!(keys.len(), 28);
        assert_eq!(
            first
                .iter()
                .map(|q| q.question_key.as_str())
                .collect::<Vec<_>>(),
            second
                .iter()
                .map(|q| q.question_key.as_str())
                .collect::<Vec<_>>()
        );
        assert!(first.iter().all(|q| q.in_nat));
    }

    #[test]
    fn random_question_respects_filters() {
        let question = random_question_with(&Filter::new().mention("CSP").theme("T4").seed(7))
            .unwrap();
        assert!(question.in_csp);
        assert!(question.theme_codes.iter().any(|code| code == "T4"));
    }

    #[test]
    fn acquisitions_yearly_totals() {
        let all = acquisitions_by_year(None).unwrap();
        assert_eq!(all.len(), 18);
        assert_eq!(all[0].year, 2008);
        assert_eq!(all[all.len() - 1].year, 2025);
        let y2010 = acquisitions_for_year(2010).unwrap();
        assert_eq!(y2010.modes["decree_total"].count, Some(94573));
        let y2025 = acquisitions_for_year(2025).unwrap();
        assert_eq!(y2025.modes["decree_total"].count, Some(42246));
        assert_eq!(
            acquisitions_for_year(2008).unwrap().modes["declaration_ascendant_sibling"].count,
            None
        );
    }

    #[test]
    fn invalid_input() {
        assert!(matches!(by_mention("XYZ"), Err(Error::UnknownMention(_))));
        assert!(matches!(by_theme("T9"), Err(Error::UnknownTheme(_))));
        assert_eq!(mock_exam(0).unwrap_err(), Error::InvalidCount);
        assert_eq!(mock_exam(10_000).unwrap_err(), Error::InvalidCount);
    }
}
