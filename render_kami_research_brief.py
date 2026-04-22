#!/usr/bin/env python3
"""
Render Markdown into Kami Research Brief HTML/PDF.

Usage:
  python3 render_kami_research_brief.py \\
    --input /path/to/doc.md \\
    --output-prefix /path/to/output/doc-name \\
    --title "Document Title" \\
    --meta "Platform Strategy · Research Brief · April 2026" \\
    --footer-org "Prepared for EFPM Research Programme · ISB" \\
    --footer-confidential "Confidential · Do Not Distribute"

Outputs:
  <output-prefix>.cleaned.md
  <output-prefix>.html       (styled, open in browser)
  <output-prefix>.pdf        (print-ready via Chrome headless)
"""

import argparse
import pathlib
import re
import subprocess
import sys


# ---------------------------------------------------------------------------
# Markdown pre-processor
# ---------------------------------------------------------------------------

def clean_markdown(raw_text: str) -> str:
    """
    Normalise Pandoc-flavoured Markdown before conversion.
    - Strips HTML comment blocks and page-break hints
    - Fixes bare || table guards
    - Removes blockquote markers (converts to plain text or styled divs)
    - Adds spacing around headings
    """
    text = raw_text.strip("\n")

    # Remove <!-- comments --> anywhere
    text = re.sub(r"<!--[\s\S]*?-->", "", text)

    # Remove page-break hints
    text = re.sub(r"^\s*\[PAGE\].*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*\\newpage\s*$", "", text, flags=re.MULTILINE)

    lines = text.splitlines()
    out = []

    for ln in lines:
        ln = ln.rstrip()

        # Fix || guards at line start (not inside cells)
        if re.match(r"^\s*\|\|\s*", ln):
            ln = re.sub(r"^(\s*)\|\|\s*", r"\1| ", ln)

        # Strip blockquote markers — convert to styled paragraphs
        if re.match(r"^\s*>\s*$", ln):
            ln = ""
        else:
            ln = re.sub(r"^\s*>\s?", "", ln)

        # Space around headings
        if re.match(r"^\s{0,3}#{1,6}\s+", ln):
            if out and out[-1].strip() != "":
                out.append("")
            out.append(ln)
            out.append("")
            continue

        # Detect and space tables
        is_table = bool(re.match(r"^\s*\|", ln))
        prev_is_table = bool(out and re.match(r"^\s*\|", out[-1] or ""))
        if is_table and out and out[-1].strip() != "" and not prev_is_table:
            out.append("")
        if (not is_table) and prev_is_table and ln.strip() != "":
            out.append("")

        out.append(ln)

    # Collapse multiple blanks (max 2 consecutive)
    clean_lines = []
    blank = 0
    for ln in out:
        if ln.strip() == "":
            blank += 1
        else:
            blank = 0
        if blank <= 2:
            clean_lines.append(ln)

    return "\n".join(clean_lines).strip() + "\n"


# ---------------------------------------------------------------------------
# Pandoc conversion
# ---------------------------------------------------------------------------

def run_pandoc(md_path: pathlib.Path) -> str:
    cmd = [
        "pandoc",
        "--from=markdown+pipe_tables+grid_tables+multiline_tables"
        "+table_captions+auto_identifiers+header_attributes",
        "--to=html5",
        "--standalone",
        str(md_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return result.stdout


def wrap_html(fragment: str, css: str, title: str,
              meta: str, footer_org: str, footer_confidential: str) -> str:
    """Wrap Pandoc HTML fragment inside the Kami Research Brief template."""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<style>
{css}
</style>
</head>
<body>
<div class="page">
  <div class="page-number">01</div>
  {fragment}
  <div class="doc-footer">
    <div class="footer-org">{footer_org}</div>
    <div class="footer-confidential">{footer_confidential}</div>
    <div class="print-page-num">01</div>
  </div>
</div>
</body>
</html>"""


def html_to_pdf(html_path: pathlib.Path, pdf_path: pathlib.Path) -> None:
    """
    Print HTML to PDF using Chrome headless.
    Adjust the chrome path for your OS:
      macOS:   /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
      Linux:   google-chrome  (or /usr/bin/google-chrome)
      Windows: "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    """
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            f"--print-to-pdf={pdf_path}",
            str(html_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render Markdown → Kami Research Brief HTML + PDF"
    )
    parser.add_argument("--input",   required=True,
                        help="Input Markdown file path")
    parser.add_argument("--output-prefix", required=True,
                        help="Output path prefix (without extension)")
    parser.add_argument("--title",   default="Kami Research Brief",
                        help="Document title")
    parser.add_argument("--meta",    default="Research Brief",
                        help="Meta eyebrow line shown below logo")
    parser.add_argument("--footer-org",         default="",
                        help="Footer organisation line")
    parser.add_argument("--footer-confidential", default="Confidential",
                        help="Footer confidentiality notice")
    args = parser.parse_args()

    theme_dir = pathlib.Path(__file__).resolve().parent
    css_path  = theme_dir / "kami-onepager.css"

    if not css_path.exists():
        sys.stderr.write(
            f"ERROR: kami-onepager.css not found in {theme_dir}\n"
        )
        sys.exit(1)

    input_path  = pathlib.Path(args.input).expanduser().resolve()
    prefix      = pathlib.Path(args.output_prefix).expanduser().resolve()
    prefix.parent.mkdir(parents=True, exist_ok=True)

    if not input_path.exists():
        sys.stderr.write(f"ERROR: Input file not found: {input_path}\n")
        sys.exit(1)

    # 1. Clean markdown
    raw = input_path.read_text(encoding="utf-8")
    cleaned = clean_markdown(raw)
    cleaned_md = prefix.with_suffix(".cleaned.md")
    cleaned_md.write_text(cleaned, encoding="utf-8")
    print(f"✓ cleaned markdown: {cleaned_md}")

    # 2. Pandoc → HTML fragment
    fragment = run_pandoc(cleaned_md)
    css = css_path.read_text(encoding="utf-8")

    # 3. Wrap in template
    full_html = wrap_html(
        fragment             =fragment,
        css                  =css,
        title                =args.title,
        meta                 =args.meta,
        footer_org           =args.footer_org,
        footer_confidential  =args.footer_confidential,
    )
    html_out = prefix.with_suffix(".html")
    html_out.write_text(full_html, encoding="utf-8")
    print(f"✓ HTML: {html_out}")

    # 4. Chrome → PDF
    pdf_out = prefix.with_suffix(".pdf")
    try:
        html_to_pdf(html_out, pdf_out)
        print(f"✓ PDF:  {pdf_out}")
    except FileNotFoundError:
        sys.stderr.write(
            "WARNING: Chrome not found at the expected path.\n"
            "Install Chrome or edit the `chrome` variable in this script "
            "to point at your Chrome binary.\n"
            f"HTML output is still available: {html_out}\n"
        )


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr or str(exc))
        raise
