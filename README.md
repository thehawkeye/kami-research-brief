# Kami Research Brief Theme

**Version:** 2.0 — "Professional & Classy"
**Design system:** Kami (github.com/tw93/Kami)
**Author:** Adapted for research briefs, academic documents, and publication-quality one-pagers

---

## Theme Philosophy

This theme refines the Kami design system for the highest typographic drama and editorial authority. It is built around four principles:

1. **Focal pull quote** — bleeds past the body column, full width minus margins, ivory background with a 3pt ink-blue left bar. The most important idea on the page commands the most visual space.
2. **Ink-blue accent discipline** — never more than 5% of surface. Every branded element (metric top-borders, section left-bars, logo, pull quote bar) uses the same `#1B365D` value.
3. **Hierarchy through contrast** — display at 32pt+, body at 9pt, dense at 8.5pt. If title and body compete for attention, neither wins.
4. **Print-first** — A4 page model, page number top-right, centered footer, hairline rules at 0.3pt. Documents should feel more like a paper journal than a web page.

---

## Files

| File | Purpose |
|------|---------|
| `kami-research-brief.css` | Complete CSS — all Kami tokens + component styles |
| `kami-research-brief.template.html` | HTML wrapper — injects CSS and content |
| `render_kami_research_brief.py` | Markdown → HTML → PDF renderer |
| `example/` | Sample source markdown + rendered outputs |

---

## Quick Start

### 1. Render a document

```bash
python3 render_kami_research_brief.py \
  --input example/example.md \
  --output-prefix output/my-research-brief \
  --meta "Platform Strategy · Research Brief · April 2026"
```

Outputs:
- `output/my-research-brief.cleaned.md` — cleaned markdown
- `output/my-research-brief.html` — styled HTML (open in browser)
- `output/my-research-brief.pdf` — print-ready PDF

### 2. Use in Claude Code / AI agents

```bash
# With Kami skill installed:
make a one-pager research brief about [topic]

# The agent will use this theme automatically if you reference it.
```

### 3. Use as a standalone HTML template

Drop this into your pipeline:
```python
css      = Path("kami-research-brief.css").read_text()
template = Path("kami-research-brief.template.html").read_text()
html = (
    template
    .replace("{{DOC_TITLE}}", "My Document")
    .replace("{{CSS}}", css)
    .replace("{{META_LINE}}", "Research Brief · 2026")
    .replace("{{CONTENT_HTML}}", pandoc_output)
)
Path("output.html").write_text(html)
```

---

## Design Tokens

### Color

| Token | Hex | Use |
|-------|-----|-----|
| `--parchment` | `#f5f4ed` | Page background — never pure white |
| `--ivory` | `#faf9f5` | Cards, callouts, pull quote background |
| `--warm-sand` | `#e8e6dc` | Button / interactive surface |
| `--brand` | `#1B365D` | **Ink blue — the only chromatic color** |
| `--near-black` | `#141413` | Primary text — warm olive undertone |
| `--dark-warm` | `#3d3d3a` | Secondary text, links |
| `--charcoal` | `#4d4c48` | Body dense, button text |
| `--olive` | `#5e5d59` | Subtext, descriptions |
| `--stone` | `#87867f` | Tertiary, metadata, page number |
| `--border-cream` | `#e8e5da` | Default card border |
| `--border-warm` | `#e0ddd2` | Section divider, hairline |
| `--border-soft` | `#e5e3d8` | Dotted divider, timeline |

### Typography

| Element | Font | Size | Weight | Line-height |
|---------|------|------|--------|-------------|
| Display title | Newsreader | 32pt | 500 | 1.08 |
| Section title | Newsreader | 10.5pt | 500 | — |
| Body lead | Newsreader | 9.5pt | 400 | 1.58 |
| Body | Newsreader | 9pt | 400 | 1.50 |
| Body dense | Newsreader | 8.5pt | 400 | 1.44 |
| Caption / meta | Inter | 7–8pt | 400/600 | 1.35–1.40 |
| Label | Inter | 6.5pt | 600 | — |

**Never use italic.** Serif weight is always locked at 500.

### Spacing (4pt base)

| Tier | Value | Use |
|------|-------|-----|
| xs | 2–3pt | Inline |
| sm | 4–5pt | Tag padding |
| md | 8–10pt | Component interior |
| lg | 16–20pt | Between components |
| xl | 18–24pt | Section-title margin |
| 2xl | 40–60pt | Between major sections |

---

## Component Reference

### Logo mark
```html
<div class="logo-mark">
  <div class="logo-icon"><span>K</span></div>
  <div class="logo-name">Your Brand<span class="logo-ver">v2.0</span></div>
</div>
```

### Eyebrow label
Always sans, uppercase, 7pt, stone color, letter-spacing 1.4px.

### Section title (signature Kami left-bar)
```html
<div class="section-title">Section Title</div>
```
Border-left: 2.5pt ink-blue, padding-left 7pt, border-radius 1.5pt.

### Metric card
```html
<div class="metric">
  <div class="metric-value">73%</div>
  <div class="metric-label">Switching cost premium</div>
  <div class="metric-sublabel">vs. perceived benefit</div>
</div>
```
Top border: 2pt ink-blue — the branded accent on each card.

### Pull quote (focal element)
```html
<div class="pullquote">
  <p>"The quote text — larger, italic, near-black."</p>
  <cite>Source · Attribution</cite>
</div>
```
Margin: bleeds slightly past body column. Ivory background, branded left bar, generous vertical padding.

### Two-column list
```html
<div class="two-col">
  <div class="col-section">
    <div class="col-label">Column Label</div>
    <div class="col-item">
      <div class="col-bullet"></div>
      <div class="col-text"><strong>Bold term:</strong> Description.</div>
    </div>
  </div>
</div>
```

### Timeline
```html
<div class="timeline-item">
  <div class="timeline-date">Apr 2026</div>
  <div class="timeline-content">
    <div class="timeline-title">Event title</div>
    <div class="timeline-desc">Description text.</div>
  </div>
</div>
```

### Callout box
```html
<div class="callout">
  <div class="callout-label">Label</div>
  <p>Callout body text.</p>
</div>
```
Border-left: 2.5pt ink-blue, ivory background.

### Tags
```html
<span class="tag">Tag Label</span>
```
Solid hex background — never rgba (WeasyPrint double-rectangle bug).

### Hairline divider
```html
<hr class="hairline">
```
0.3pt solid `--border-warm`. Used between major sections — not decorative borders.

### Centered footer
```html
<div class="doc-footer">
  <div class="footer-org">Organisation · <span class="footer-brand">Brand</span></div>
  <div class="footer-confidential">Confidential · Do Not Distribute</div>
</div>
```

---

## Kami Nine Invariants

This theme inherits all nine Kami invariants. Do not violate these:

1. Page background `#f5f4ed` (parchment), never pure white
2. Single accent: ink-blue `#1B365D`
3. All grays warm-toned (yellow-brown undertone), no cool blue-gray
4. English: serif for headlines and body. Sans for UI elements only.
5. Serif weight locked at 500, no bold
6. Line-height: 1.1–1.58 max. **Never 1.6+**
7. Tag backgrounds must be solid hex, no rgba
8. Depth via ring / whisper shadow, no hard drop shadows
9. **No italic anywhere** (exception: pull quote quote text only)

---

## Requirements

- `pandoc` — Markdown to HTML conversion
- Google Chrome (for PDF output via `--print-to-pdf`)

Install pandoc: `brew install pandoc`

Chrome is assumed at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. Edit the `chrome` path in `render_kami_research_brief.py` for Linux/Windows.

---

## License

MIT — use freely. The Kami design system (github.com/tw93/Kami) is MIT licensed. Newsreader and Inter fonts are OFL open source.
