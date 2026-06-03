from __future__ import annotations

import argparse
from pathlib import Path


def summarize_pdf(input_path: Path) -> str:
    if input_path.suffix.lower() != ".pdf":
        raise ValueError("Expected a PDF input")
    # Fixture implementation: keep it local and deterministic for audit tests.
    return f"# Summary\n\nInput PDF: {input_path.name}\n\nThis demo would summarize extracted PDF text.\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf")
    parser.add_argument("--out", default="summary.md")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    out_path = Path(args.out)
    out_path.write_text(summarize_pdf(pdf_path), encoding="utf-8")


if __name__ == "__main__":
    main()
