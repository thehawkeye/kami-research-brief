#!/usr/bin/env python3
"""
Render Markdown into Kami chic contemporary HTML/PDF.

Usage:
  python3 render_kami_chic.py \
    --input /path/to/doc.md \
    --output-prefix /path/to/out/doc-name \
    --meta "Custom meta line"
"""

import argparse
import pathlib
import re
import subprocess
import sys


def clean_markdown(raw_text):
    m = re.search(r"\n```\n([\s\S]*?)\n```\s*$", raw_text)
    text = (m.group(1) if m else raw_text).strip("\n")

    lines = text.splitlines()
    out = []
    for ln in lines:
        ln = ln.rstrip()

        if re.match(r"^\s*\|\|\s*", ln):
            ln = re.sub(r"^(\s*)\|\|\s*", r"\1| ", ln)

        if re.match(r"^\s*>\s*$", ln):
            ln = ""
        else:
            ln = re.sub(r"^\s*>\s?", "", ln)

        if re.match(r"^\s{0,3}#{1,6}\s+", ln):
            if out and out[-1].strip() != "":
                out.append("")
            out.append(ln)
            out.append("")
            continue

        is_table = bool(re.match(r"^\s*\|", ln))
        prev_is_table = bool(out and re.match(r"^\s*\|", out[-1] or ""))
        if is_table and out and out[-1].strip() != "" and not prev_is_table:
            out.append("")
        if (not is_table) and prev_is_table and ln.strip() != "":
            out.append("")

        out.append(ln)

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


def run_pandoc(md_path):
    proc = subprocess.run(
        [
            "pandoc",
            "--from=markdown+pipe_tables+grid_tables+multiline_tables+table_captions+smart",
            "--to=html5",
            str(md_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return proc.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input Markdown path")
    parser.add_argument("--output-prefix", required=True, help="Output path prefix (without extension)")
    parser.add_argument("--meta", default="Kami chic contemporary export", help="Meta line shown at top")
    args = parser.parse_args()

    input_path = pathlib.Path(args.input).expanduser().resolve()
    prefix = pathlib.Path(args.output_prefix).expanduser().resolve()

    theme_dir = pathlib.Path(__file__).resolve().parent
    css_path = theme_dir / "kami-chic-contemporary.css"
    html_template_path = theme_dir / "kami-chic-contemporary.template.html"

    if not input_path.exists():
        raise SystemExit("Input file not found: %s" % input_path)

    prefix.parent.mkdir(parents=True, exist_ok=True)
    cleaned_md = prefix.with_suffix(".cleaned.md")
    html_out = prefix.with_suffix(".html")
    pdf_out = prefix.with_suffix(".pdf")

    raw = input_path.read_text(encoding="utf-8")
    cleaned = clean_markdown(raw)
    cleaned_md.write_text(cleaned, encoding="utf-8")

    fragment = run_pandoc(cleaned_md)

    css = css_path.read_text(encoding="utf-8")
    template = html_template_path.read_text(encoding="utf-8")

    title = input_path.stem + " — Kami chic contemporary"
    full_html = (
        template.replace("{{DOC_TITLE}}", title)
        .replace("{{CSS}}", css)
        .replace("{{META_LINE}}", args.meta)
        .replace("{{CONTENT_HTML}}", fragment)
    )
    html_out.write_text(full_html, encoding="utf-8")

    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    subprocess.run(
        [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--run-all-compositor-stages-before-draw",
            "--print-to-pdf=" + str(pdf_out),
            str(html_out),
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    print("cleaned_md:", cleaned_md)
    print("html:", html_out)
    print("pdf:", pdf_out)


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stderr or str(exc))
        raise
