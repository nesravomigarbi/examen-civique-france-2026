# frozen_string_literal: true

require "minitest/autorun"
require_relative "../lib/examen_civique_france"

class DatasetTest < Minitest::Test
  def test_all_questions_count
    questions = ExamenCiviqueFrance.all_questions
    assert_equal 523, questions.length
    assert_equal 523, questions.map { |q| q["question_key"] }.uniq.length
  end

  def test_mention_filters
    assert_equal 190, ExamenCiviqueFrance.by_mention("CSP").length
    assert_equal 209, ExamenCiviqueFrance.by_mention("CR").length
    assert_equal 258, ExamenCiviqueFrance.by_mention("NAT").length
    assert_equal 190, ExamenCiviqueFrance.by_level("carte de séjour pluriannuelle").length
    assert_equal 258, ExamenCiviqueFrance.by_mention("naturalisation").length
  end

  def test_theme_filters
    assert_equal 93, ExamenCiviqueFrance.by_theme("T1").length
    assert_equal 111, ExamenCiviqueFrance.by_theme("T2").length
    assert_equal 94, ExamenCiviqueFrance.by_theme("T3").length
    assert_equal 143, ExamenCiviqueFrance.by_theme("T4").length
    assert_equal 83, ExamenCiviqueFrance.by_theme("T5").length
    assert_equal 143, ExamenCiviqueFrance.by_theme("Histoire, géographie et culture").length
    total = ExamenCiviqueFrance::THEMES.keys.sum { |code| ExamenCiviqueFrance.by_theme(code).length }
    assert_equal 524, total
  end

  def test_two_theme_question
    key = "Q93946df581"
    assert ExamenCiviqueFrance.by_theme("T1").any? { |q| q["question_key"] == key }
    assert ExamenCiviqueFrance.by_theme("T3").any? { |q| q["question_key"] == key }
  end

  def test_mock_exam_is_deterministic_with_seed
    first = ExamenCiviqueFrance.mock_exam(28, mention: "NAT", seed: 42)
    second = ExamenCiviqueFrance.mock_exam(28, mention: "NAT", seed: 42)
    assert_equal 28, first.length
    assert_equal 28, first.map { |q| q["question_key"] }.uniq.length
    assert_equal first.map { |q| q["question_key"] }, second.map { |q| q["question_key"] }
    assert first.all? { |q| q["in_nat"] }
  end

  def test_random_question_respects_filters
    question = ExamenCiviqueFrance.random_question(mention: "CSP", theme: "T4", seed: 7)
    assert question["in_csp"]
    assert_includes question["theme_codes"], "T4"
  end

  def test_acquisitions_by_year
    all = ExamenCiviqueFrance.acquisitions_by_year
    assert_equal 18, all.length
    assert_equal 2008, all[0]["year"]
    assert_equal 2025, all[-1]["year"]
    assert_equal 94_573, ExamenCiviqueFrance.acquisitions_by_year(2010)["modes"]["decree_total"]["count"]
    assert_equal 42_246, ExamenCiviqueFrance.acquisitions_by_year(2025)["modes"]["decree_total"]["count"]
    assert_nil ExamenCiviqueFrance.acquisitions_by_year(2008)["modes"]["declaration_ascendant_sibling"]["count"]
  end

  def test_invalid_input
    err = assert_raises(ArgumentError) { ExamenCiviqueFrance.by_mention("XYZ") }
    assert_match(/unknown mention/, err.message)
    err = assert_raises(ArgumentError) { ExamenCiviqueFrance.by_theme("T9") }
    assert_match(/unknown theme/, err.message)
    err = assert_raises(ArgumentError) { ExamenCiviqueFrance.mock_exam(0) }
    assert_match(/positive integer/, err.message)
    err = assert_raises(ArgumentError) { ExamenCiviqueFrance.mock_exam(10_000) }
    assert_match(/only 523/, err.message)
  end
end
