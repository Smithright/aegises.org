# Beyond the Bill Count

AEGISES State AI Legislative Maturity Atlas — research edition 1.0, observation date September 14, 2026.

## Delivery

The native static publication is `../index.html`, intended for `https://aegises.org/ai-legislation/`. It includes six original vector figures, a 51-jurisdiction ledger (50 states plus DC), CSV/JSON evidence, plain text, a PDF and a social preview. The repository homepage, sitemap and reader index link to the publication.

Publication was authorized on September 14, 2026. The source is prepared for the existing GitHub Pages release workflow; a successful workflow and live content readback establish delivery. The existing repository uses GitHub Pages; no hosting or domain migration is required. The local review server uses `http://127.0.0.1:8874/ai-legislation/` while its process is running.

## Research contract

The corpus contains representative legislative anchors, not every relevant instrument. State colors describe selected anchors, not entire portfolios. Category keys are not ordinal maturity scores. Empty domain cells mean not assessed, not no law. Legislation, implementation artifacts, agency-reported operation and evaluated outcomes are distinct evidence states.

The ledger flags Idaho's secondary verification, Alabama and Alaska's mixed verification, Missouri's proposal and DC's unclassified research gap. Connecticut's selected anchor is the 2023 public-sector mechanism; the complete 2026 package was not assessed. The edition is not an exhaustive 2026 amendment, litigation, regulation or federal-interaction census. Do not promote it as one.

NCSL was used for discovery and the specified mixed-source cross-checks. Its historical snapshot totals and database are not reproduced. The state ledger and diagrams are original analytical work. Primary-source links include statutes, enacted text, official histories, official enacted-law summaries and agency materials; those source forms should not be conflated.

## Source and generation files

- `build_data.py`: curated observations, source links, source types and interpretation boundaries; emits `../data/states.json` and CSV.
- `build_figures.py`: deterministic SVG layouts and categorical editorial placements. Six figures; no invented quantitative maturity scores.
- `article.html`: source article template.
- `build_page.py`: inserts figures and ledger into initial HTML; emits the text edition and SVG archive.
- `../styles.css`, `../page.js`: responsive and print styles; progressive ledger filtering and citation recovery. No external browser dependencies, fonts or trackers.
- `render_verify.cjs`: browser verification, social plate and PDF rendering. Requires Playwright and Sharp; `NODE_PATH` can identify the available installation. `ATLAS_CHROME`, `ATLAS_PREVIEW_URL` and `ATLAS_REVIEW_DIR` override local defaults.
- `validation.json`: observed browser verification results. A browser check is not a substantive legal review or proof of deployment.

Run from the repository root:

```sh
python3 ai-legislation/research/build_data.py
python3 ai-legislation/research/build_figures.py
python3 ai-legislation/research/build_page.py
python3 -m http.server 8874 --bind 127.0.0.1
# In a separate terminal, with Node dependencies available:
node ai-legislation/research/render_verify.cjs
```

The browser check validates jurisdiction/figure counts, internal anchors, local downloads, search, empty results, reset, pathway filtering, citation recovery, 390px and 768px layouts, initial HTML without JavaScript, browser errors and SVG text clipping/overlap. Review PNGs and PDF renders were inspected locally. PDF pagination received additional print-only adjustments after the recorded browser checks.

## Updating the research

Verify the exact final instrument and latest amendments before changing an entry. Record the source, narrow supported claim, observation date and uncertainty. Keep effective dates, adoption deadlines and reporting starts distinct. Do not turn a prospective date in a bill record into an enacted obligation. Update every affected diagram, narrative, data export and print edition together.

Do not infer effectiveness from an available portal, an inventory, a rule, or an agency's account of program operation. Any future state-wide rank requires a broader, systematic corpus and an explicit scoring and uncertainty method.
