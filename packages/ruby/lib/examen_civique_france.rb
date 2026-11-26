# frozen_string_literal: true

require "json"
require_relative "examen_civique_france/version"

module ExamenCiviqueFrance
  THEMES = {
    "T1" => "Principes et valeurs de la République",
    "T2" => "Système institutionnel et politique",
    "T3" => "Droits et devoirs",
    "T4" => "Histoire, géographie et culture",
    "T5" => "Vivre dans la société française"
  }.freeze

  DATA_DIR = File.expand_path("../data", __dir__)

  MENTION_ALIASES = {
    "csp" => "CSP",
    "carte de sejour pluriannuelle" => "CSP",
    "cr" => "CR",
    "carte de resident" => "CR",
    "nat" => "NAT",
    "naturalisation" => "NAT",
    "naturalization" => "NAT",
    "nationalite" => "NAT",
    "nationalite francaise" => "NAT"
  }.freeze

  MENTION_FLAG = { "CSP" => "in_csp", "CR" => "in_cr", "NAT" => "in_nat" }.freeze

  class << self
    def all_questions
      questions.dup
    end

    def by_mention(mention)
      flag = MENTION_FLAG[normalize_mention(mention)]
      questions.select { |question| question[flag] }
    end

    def by_level(mention)
      by_mention(mention)
    end

    def by_theme(theme)
      code, = normalize_theme(theme)
      questions.select { |question| question["theme_codes"].include?(code) }
    end

    def random_question(mention: nil, level: nil, theme: nil, seed: nil)
      items = pool(mention: mention, level: level, theme: theme)
      raise ArgumentError, "no questions match the given filters" if items.empty?

      items[rng(seed).rand(items.length)]
    end

    def mock_exam(n, mention: nil, level: nil, theme: nil, seed: nil)
      raise ArgumentError, "n must be a positive integer" unless n.is_a?(Integer) && n >= 1

      items = pool(mention: mention, level: level, theme: theme)
      if n > items.length
        raise ArgumentError,
              "cannot build a mock exam of #{n} questions; only #{items.length} match the filters"
      end
      random = rng(seed)
      n.times do |i|
        j = i + random.rand(items.length - i)
        items[i], items[j] = items[j], items[i]
      end
      items[0, n]
    end

    def acquisitions_by_year(year = nil)
      if year.nil?
        return acquisitions.map { |row| { "year" => row["year"], "modes" => row["modes"].dup } }
      end
      raise ArgumentError, "year must be an integer" unless year.is_a?(Integer)

      row = acquisitions.find { |item| item["year"] == year }
      raise ArgumentError, "no acquisition statistics for year #{year}" if row.nil?

      { "year" => row["year"], "modes" => row["modes"].dup }
    end

    def normalize_mention(mention)
      raise ArgumentError, "mention is required (CSP, CR or NAT)" if mention.nil? || mention.to_s.strip.empty?

      mapped = MENTION_ALIASES[fold(mention)]
      raise ArgumentError, "unknown mention: #{mention} (use CSP, CR or NAT)" if mapped.nil?

      mapped
    end

    def normalize_theme(theme)
      raise ArgumentError, "theme is required (T1–T5 or an official theme name)" if theme.nil? || theme.to_s.strip.empty?

      key = fold(theme)
      THEMES.each do |code, name|
        return [code, name] if key == fold(code) || key == fold(name)
      end
      raise ArgumentError, "unknown theme: #{theme} (use T1–T5 or an official theme name)"
    end

    private

    def questions
      @questions ||= JSON.parse(File.read(File.join(DATA_DIR, "questions.json"), encoding: "UTF-8"))
    end

    def acquisitions
      @acquisitions ||= JSON.parse(File.read(File.join(DATA_DIR, "acquisitions.json"), encoding: "UTF-8"))
    end

    def fold(value)
      value.to_s.strip.downcase.unicode_normalize(:nfd).gsub(/\p{M}/, "")
    end

    def pool(mention:, level:, theme:)
      items = questions
      selected = mention.nil? ? level : mention
      unless selected.nil?
        flag = MENTION_FLAG[normalize_mention(selected)]
        items = items.select { |question| question[flag] }
      end
      unless theme.nil?
        code, = normalize_theme(theme)
        items = items.select { |question| question["theme_codes"].include?(code) }
      end
      items.dup
    end

    def rng(seed)
      seed.nil? ? Random.new : Random.new(Integer(seed))
    end
  end
end
