# Kami One-Pager Template — Universal

**Theme:** Kami One-Pager
**Version:** 1.0
**Design system:** [github.com/tw93/Kami](https://github.com/tw93/Kami)
**License:** MIT

A single, versatile A4 one-pager template that works for any context. Research briefs, book proposals, partnership decks, teaching overviews, conference notes — one template, any subject.

---

## The Four Use Cases

| File | Context | What's Inside |
|------|---------|--------------|
| `01-jams-research.html` | JAMS paper / academic research | Core argument, 6-mechanism architecture, research programme timeline |
| `02-agent-economy-book.html` | "Hermes Unbound" book | Core thesis, key constructs, chapter status, Book Council feedback |
| `03-latticed-iifr.html` | LatticeEd × IIFR partnership | Revenue model, programme areas, launch milestone |
| `04-isl-teaching.html` | ISB executive teaching | Pedagogical approach, core modules, practitioner cases |

All four render from the same template — swap content, keep the design.

---

## Design Philosophy

**Warm parchment canvas, ink-blue accent, serif carries authority.**

One page. One impression. The pull quote is the focal point — it gets the most visual space. Everything else serves it.

- Page number top-right (01) — publication convention
- Centered footer — academic, not corporate
- 0.75pt ink-blue hairline anchors the header
- Section titles carry a 2.5pt left-bar — the signature Kami move
- No gradients, no drop shadows, no cool grays

---

## Components Available

| Component | When to Use |
|-----------|-------------|
| **Header** | Title, subtitle, eyebrow, author meta, tags |
| **Pull quote** | The one thing the reader should remember |
| **Two-column list** | Frameworks, mechanisms, programme areas |
| **Metrics row** | Numbers with interpretation (3 cards, brand top-border) |
| **Timeline** | Programme roadmap, phased plans |
| **Callout** | Key constraint, deadline, or action item |
| **Key points** | Numbered list — chapter status, action items |
| **Table** | Structured comparisons, data |

---

## Quick Start

### Edit the HTML directly
Each `.html` file is self-contained — edit content in the `<body>`. Print to PDF from browser.

### Use the Python renderer

```bash
python3 render_kami_research_brief.py \
  --input your-document.md \
  --output-prefix output/your-file \
  --title "Your Document Title" \
  --meta "Category · Subcategory · Date" \
  --footer-org "Your Organisation" \
  --footer-confidential "Confidential"
```

Requires: `pandoc` (`brew install pandoc`) + Google Chrome for PDF output.

---

## Design Tokens

| Token | Hex | Use |
|-------|-----|-----|
| `--parchment` | `#f5f4ed` | Page background |
| `--brand` | `#1B365D` | Ink blue accent — ≤5% of surface |
| `--near-black` | `#141413` | Primary text |
| `--charcoal` | `#4d4c48` | Body text |
| `--olive` | `#5e5d59` | Subtext |
| `--stone` | `#87867f` | Metadata, page number |

---

## Kami Nine Invariants

1. `#f5f4ed` parchment — never pure white
2. Single accent: `#1B365D` ink blue
3. All grays warm-toned (yellow-brown undertone)
4. Serif for body and headlines; sans for UI only
5. Serif weight locked at 500 — no bold
6. Line-height never exceeds 1.58
7. Tag backgrounds solid hex — no rgba
8. Depth via ring shadow only — no drop shadows
9. **No italic anywhere** (pull quote text excepted)
