import unittest

from examen_civique_france import (
    THEMES,
    acquisitions_by_year,
    all_questions,
    by_level,
    by_mention,
    by_theme,
    mock_exam,
    random_question,
)


class DatasetTests(unittest.TestCase):
    def test_all_questions_count(self):
        questions = all_questions()
        self.assertEqual(len(questions), 523)
        self.assertEqual(len({q["question_key"] for q in questions}), 523)

    def test_mention_filters(self):
        self.assertEqual(len(by_mention("CSP")), 190)
        self.assertEqual(len(by_mention("CR")), 209)
        self.assertEqual(len(by_mention("NAT")), 258)
        self.assertEqual(len(by_level("carte de séjour pluriannuelle")), 190)
        self.assertEqual(len(by_mention("naturalisation")), 258)

    def test_theme_filters(self):
        self.assertEqual(len(by_theme("T1")), 93)
        self.assertEqual(len(by_theme("T2")), 111)
        self.assertEqual(len(by_theme("T3")), 94)
        self.assertEqual(len(by_theme("T4")), 143)
        self.assertEqual(len(by_theme("T5")), 83)
        self.assertEqual(len(by_theme("Histoire, géographie et culture")), 143)
        self.assertEqual(
            sum(len(by_theme(code)) for code in THEMES),
            524,
        )

    def test_two_theme_question(self):
        key = "Q93946df581"
        self.assertTrue(any(q["question_key"] == key for q in by_theme("T1")))
        self.assertTrue(any(q["question_key"] == key for q in by_theme("T3")))

    def test_mock_exam_is_deterministic_with_seed(self):
        first = mock_exam(28, mention="NAT", seed=42)
        second = mock_exam(28, mention="NAT", seed=42)
        self.assertEqual(len(first), 28)
        self.assertEqual(len({q["question_key"] for q in first}), 28)
        self.assertEqual([q["question_key"] for q in first], [q["question_key"] for q in second])
        self.assertTrue(all(q["in_nat"] for q in first))

    def test_random_question_respects_filters(self):
        question = random_question(mention="CSP", theme="T4", seed=7)
        self.assertTrue(question["in_csp"])
        self.assertIn("T4", question["theme_codes"])

    def test_acquisitions_by_year(self):
        all_years = acquisitions_by_year()
        self.assertEqual(len(all_years), 18)
        self.assertEqual(all_years[0]["year"], 2008)
        self.assertEqual(all_years[-1]["year"], 2025)
        self.assertEqual(acquisitions_by_year(2010)["modes"]["decree_total"]["count"], 94573)
        self.assertEqual(acquisitions_by_year(2025)["modes"]["decree_total"]["count"], 42246)
        self.assertIsNone(acquisitions_by_year(2008)["modes"]["declaration_ascendant_sibling"]["count"])

    def test_invalid_input(self):
        with self.assertRaisesRegex(ValueError, "unknown mention"):
            by_mention("XYZ")
        with self.assertRaisesRegex(ValueError, "unknown theme"):
            by_theme("T9")
        with self.assertRaisesRegex(ValueError, "positive integer"):
            mock_exam(0)
        with self.assertRaisesRegex(ValueError, "only 523"):
            mock_exam(10_000)


if __name__ == "__main__":
    unittest.main()
