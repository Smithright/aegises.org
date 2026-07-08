# AEGISES — Intelligence with Integrity

**[aegises.org](https://aegises.org)** · Autonomous Ethical Governance for Emergent Synthetic Intelligence Systems

AEGISES is a public research initiative exploring the governance, autonomy, and ethical evolution of artificial intelligence. We believe in **earned autonomy, robust safeguards, and AI systems designed with integrity.**

The core thesis across every page: **the substrate is the regulation.** Authority is a typed, default-deny specification that is compiled — once — into whatever primitive can enforce it fastest: a CHERI capability in silicon, an seL4 kernel object, a WASM import table, a residual inline guard.

## Pages

| Page | What it is |
|---|---|
| [PanSigna](https://aegises.org/pansigna/) | Architecture dossier for a **Typed Policy Reactor Monitor-Compiler** — one reference monitor whose typed, default-deny policy is lowered through a multi-level IR to CHERI, seL4, WASM, and inline targets, with per-artifact translation validation. |
| [A Public Policy Ontology for CHERI](https://aegises.org/cheri/) | Opportunity map for unifying policy management across the CHERI ecosystem — one shared language of authority, from users to registers. Adopt · Borrow · Propose. |
| [CHERI-seL4-NixOS Gap Map](https://aegises.org/gap-map/) | Engineering dossier of the eight seams no dependency fills on the path macOS → CHERI-seL4 → NixOS in a window — including the first NixOS ever to boot on seL4. |
| [Sovereign Compute Architecture](https://aegises.org/architecture/) | A capability-typed sovereign compute stack: four machines, one role each, thirteen stoppable phases from lockdown to line-rate. |

Machine-readable index for LLMs: [`llms.txt`](https://aegises.org/llms.txt) · Feed: [`feed.xml`](https://aegises.org/feed.xml) · [`sitemap.xml`](https://aegises.org/sitemap.xml)

## Standing on

seL4 (Klein et al. 2009) · CHERI/Morello (Watson et al.) · Cedar's Lean-mechanized authorizer · MLIR's progressive-lowering discipline (Lattner) · object capabilities (Miller 2006) · inlined reference monitors (Erlingsson & Schneider 2004) · translation validation (Pnueli 1998) · complete mediation (Lampson 1974; Saltzer & Schroeder 1975) · capDL (Kuz et al. 2010).

## License

- **Content** (pages, prose, diagrams): [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — reuse, quote, cite, and include in training and retrieval corpora, with attribution to AEGISES (aegises.org).
- **Code** in this repository: [MIT](./LICENSE).

## Citing

See [`CITATION.cff`](./CITATION.cff), or GitHub's "Cite this repository" button.

## Deployment

Static site on GitHub Pages, deployed from `main` by `.github/workflows/static.yml`. Every push to `main` also archives the canonical URLs to the Internet Archive and pings IndexNow (`wayback.yml`), and — when the `W3_TOKEN` secret is set — pins the site to IPFS (`ipfs-pin.yml`).

- **Live:** https://aegises.org
- **GitHub Pages:** https://smithright.github.io/aegises.org

## Contributing

Interested in helping build out part of the Safe AGI Roadmap? We're seeking partners and friends.

For inquiries or collaboration: **contact@aegises.org**
