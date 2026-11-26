# Code packages for the French civic exam dataset

These libraries wrap the open dataset
[French Civic Exam (Examen civique) 2026](https://doi.org/10.5281/zenodo.24496692)
compiled by Nesra Vomigarbi for [Examen Civique Test](https://examen-civique-test.fr/).

They have been built and tested locally. They have **not** been published to
npm, PyPI, crates.io, RubyGems or Packagist.

| Language | Package name | Path |
|---|---|---|
| JavaScript (ESM + CommonJS, TypeScript typings) | `examen-civique-france` | [`npm/`](npm/) |
| Python | `examen-civique-france` | [`python/`](python/) |
| Rust | `examen-civique-france` | [`rust/`](rust/) |
| Ruby | `examen_civique_france` | [`ruby/`](ruby/) |
| PHP (Composer / Packagist) | `nesravomigarbi/examen-civique-france` | [`php/`](php/) |

Each package is version 1.0.0. The bundled data is the dataset version 1.0.1
(523 distinct questions; nationality acquisitions for 2008–2025). Code is MIT.
Data is CC BY 4.0.

Interactive practice tool built on this dataset: [Examen Civique Test](https://examen-civique-test.fr/)

In the GitHub repository the dataset CSV files stay at the repository root;
these libraries live under `packages/<language>/`.

The PHP package also lives in a dedicated repository, [nesravomigarbi/examen-civique-france-php](https://github.com/nesravomigarbi/examen-civique-france-php), so that Packagist can read `composer.json` at the repository root.
