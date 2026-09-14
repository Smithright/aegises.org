# AEGISES homepage

Editorial redesign, September 14, 2026. The page presents the existing public research collection and preserves its destinations, including the renamed Typed Policy Reactor at `/pansigna/`.

## Design decisions

- Institutional identity first: Intelligence with Integrity, the initiative's established purpose, and three connected research questions.
- Two featured publications: Reactor and the State AI Legislative Maturity Atlas. Their descriptions distinguish a reference design from a representative research corpus.
- Four technical dossiers in a compact index: Typed Policy Reactor, Sovereign Compute Architecture, the CHERI policy ontology, and the CHERI–seL4–NixOS gap map.
- The approach and participation sections retain earned autonomy, explicit authority, inspectable evidence, the existing contact address and RFC roadmap.
- Paper, navy and teal maintain continuity with the legislative atlas. Typography and rules establish hierarchy; motion is limited to link feedback and respects reduced-motion settings.
- No added frontend framework, client-side dependency, remote font, tracker or form backend. Content and navigation work without JavaScript.

`reactor-cover.svg` is a labeled conceptual cover illustration, not a completeness or implementation claim. `atlas-cover.svg` is a thumbnail of the published atlas's selected-instrument cartogram; it is not a state ranking. Readers reach the full sources, categories and qualifications through the publication links.

## Validation

`verify.cjs` uses Playwright to check local destinations, internal anchors, page widths 320–1440px, keyboard skip navigation, the research link, reduced motion, and content with JavaScript disabled. It also creates the social preview. Supply `AEGISES_HOME_URL` to select a local preview server. Playwright and a Chrome executable are development tools, not site dependencies.

Desktop and mobile renders were visually inspected. `validation.json` records browser observations for the local candidate. GitHub Actions and live content readback establish publication separately.
