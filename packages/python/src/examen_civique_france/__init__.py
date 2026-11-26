"""Official French civic exam (examen civique) 2026 questions and nationality statistics."""

from __future__ import annotations

import json
import random
import unicodedata
from importlib.resources import files
from typing import Any, Mapping

__version__ = "1.0.0"
__author__ = "Nesra Vomigarbi"
__email__ = "data@examen-civique-test.fr"
__doi__ = "10.5281/zenodo.24496692"

THEMES: dict[str, str] = {
    "T1": "Principes et valeurs de la République",
    "T2": "Système institutionnel et politique",
    "T3": "Droits et devoirs",
    "T4": "Histoire, géographie et culture",
    "T5": "Vivre dans la société française",
}

_MENTION_ALIASES = {
    "csp": "CSP",
    "carte de sejour pluriannuelle": "CSP",
    "cr": "CR",
    "carte de resident": "CR",
    "nat": "NAT",
    "naturalisation": "NAT",
    "naturalization": "NAT",
    "nationalite": "NAT",
    "nationalite francaise": "NAT",
}

_MENTION_FLAG = {"CSP": "in_csp", "CR": "in_cr", "NAT": "in_nat"}


def _load_json(name: str) -> Any:
    return json.loads(files("examen_civique_france").joinpath("data", name).read_text(encoding="utf-8"))


_QUESTIONS: list[dict[str, Any]] = _load_json("questions.json")
_ACQUISITIONS: list[dict[str, Any]] = _load_json("acquisitions.json")


def _fold(value: str) -> str:
    normalized = unicodedata.normalize("NFD", str(value).strip().lower())
    return "".join(ch for ch in normalized if unicodedata.category(ch) != "Mn")


def normalize_mention(mention: str) -> str:
    if mention is None or not str(mention).strip():
        raise ValueError("mention is required (CSP, CR or NAT)")
    mapped = _MENTION_ALIASES.get(_fold(mention))
    if mapped is None:
        raise ValueError(f"unknown mention: {mention} (use CSP, CR or NAT)")
    return mapped


def normalize_theme(theme: str) -> tuple[str, str]:
    if theme is None or not str(theme).strip():
        raise ValueError("theme is required (T1–T5 or an official theme name)")
    key = _fold(theme)
    for code, name in THEMES.items():
        if key == _fold(code) or key == _fold(name):
            return code, name
    raise ValueError(f"unknown theme: {theme} (use T1–T5 or an official theme name)")


def _pool(mention: str | None = None, level: str | None = None, theme: str | None = None) -> list[dict[str, Any]]:
    items = _QUESTIONS
    selected = mention if mention is not None else level
    if selected is not None:
        flag = _MENTION_FLAG[normalize_mention(selected)]
        items = [question for question in items if question[flag]]
    if theme is not None:
        code, _ = normalize_theme(theme)
        items = [question for question in items if code in question["theme_codes"]]
    return items


def _rng(seed: int | None) -> random.Random:
    if seed is None:
        return random
    return random.Random(seed)


def all_questions() -> list[dict[str, Any]]:
    """Return all 523 distinct questions."""
    return list(_QUESTIONS)


def by_mention(mention: str) -> list[dict[str, Any]]:
    """Return distinct questions that appear in the given official list (CSP, CR or NAT)."""
    flag = _MENTION_FLAG[normalize_mention(mention)]
    return [question for question in _QUESTIONS if question[flag]]


def by_level(mention: str) -> list[dict[str, Any]]:
    """Alias of ``by_mention``."""
    return by_mention(mention)


def by_theme(theme: str) -> list[dict[str, Any]]:
    """Return distinct questions tagged with the given official theme code or name."""
    code, _ = normalize_theme(theme)
    return [question for question in _QUESTIONS if code in question["theme_codes"]]


def random_question(
    mention: str | None = None,
    level: str | None = None,
    theme: str | None = None,
    seed: int | None = None,
) -> dict[str, Any]:
    """Return one question drawn from the (optionally filtered) pool."""
    items = _pool(mention=mention, level=level, theme=theme)
    if not items:
        raise ValueError("no questions match the given filters")
    return _rng(seed).choice(items)


def mock_exam(
    n: int,
    mention: str | None = None,
    level: str | None = None,
    theme: str | None = None,
    seed: int | None = None,
) -> list[dict[str, Any]]:
    """Return ``n`` distinct questions drawn without replacement."""
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("n must be a positive integer")
    items = list(_pool(mention=mention, level=level, theme=theme))
    if n > len(items):
        raise ValueError(
            f"cannot build a mock exam of {n} questions; only {len(items)} match the filters"
        )
    rng = _rng(seed)
    # Partial Fisher-Yates so a seed is independent of Python's sample() implementation.
    for i in range(n):
        j = i + rng.randrange(len(items) - i)
        items[i], items[j] = items[j], items[i]
    return items[:n]


def acquisitions_by_year(year: int | None = None) -> list[dict[str, Any]] | dict[str, Any]:
    """Return acquisition statistics for every year 2008–2025, or for a single year."""
    if year is None:
        return [{"year": row["year"], "modes": dict(row["modes"])} for row in _ACQUISITIONS]
    if not isinstance(year, int) or isinstance(year, bool):
        raise ValueError("year must be an integer")
    for row in _ACQUISITIONS:
        if row["year"] == year:
            return {"year": row["year"], "modes": dict(row["modes"])}
    raise ValueError(f"no acquisition statistics for year {year}")


DATASET: Mapping[str, Any] = {
    "question_count": len(_QUESTIONS),
    "acquisition_years": [row["year"] for row in _ACQUISITIONS],
    "doi": __doi__,
    "homepage": "https://examen-civique-test.fr/",
}

__all__ = [
    "THEMES",
    "DATASET",
    "__version__",
    "__doi__",
    "normalize_mention",
    "normalize_theme",
    "all_questions",
    "by_mention",
    "by_level",
    "by_theme",
    "random_question",
    "mock_exam",
    "acquisitions_by_year",
]
