# frozen_string_literal: true

require_relative "lib/examen_civique_france/version"

Gem::Specification.new do |spec|
  spec.name = "examen_civique_france"
  spec.version = ExamenCiviqueFrance::VERSION
  spec.authors = ["Nesra Vomigarbi"]
  spec.email = ["data@examen-civique-test.fr"]

  spec.summary = "Official French civic exam (examen civique) 2026 questions and nationality statistics 2008–2025."
  spec.description = <<~TEXT
    Bundles 523 distinct official knowledge questions from the three mentions of
    France's civic exam (CSP, CR and naturalisation) and Insee/DGEF statistics
    on acquisitions of French nationality, 2008–2025. Answers are not included.
    Compiled by Nesra Vomigarbi for Examen Civique Test.
  TEXT
  spec.homepage = "https://examen-civique-test.fr/"
  spec.licenses = ["MIT", "CC-BY-4.0"]
  spec.required_ruby_version = ">= 2.7.0"

  spec.metadata["homepage_uri"] = spec.homepage
  spec.metadata["source_code_uri"] = "https://github.com/nesravomigarbi/examen-civique-france-2026"
  spec.metadata["documentation_uri"] = "https://github.com/nesravomigarbi/examen-civique-france-2026/tree/main/packages/ruby"
  spec.metadata["bug_tracker_uri"] = "https://github.com/nesravomigarbi/examen-civique-france-2026/issues"
  spec.metadata["allowed_push_host"] = "https://rubygems.org"

  spec.files = Dir.chdir(__dir__) do
    Dir[
      "lib/**/*",
      "data/**/*",
      "LICENSE",
      "LICENSE-MIT",
      "LICENSE-DATA",
      "LICENSE-NOTICE",
      "README.md",
      "CITATION.cff"
    ].select { |path| File.file?(path) }
  end
  spec.require_paths = ["lib"]
end
