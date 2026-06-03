from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable, List

from .files import TextFile
from .models import DeclaredIntent, IntentSignal


INTENT_PATTERNS = {
    "pdf_summarization": [
        r"\bpdf\b",
        r"extract text",
        r"pdftotext",
    ],
    "research": [
        r"\bresearch\b",
        r"market research",
        r"资料调研",
        r"online search",
        r"web research",
        r"competitor",
    ],
    "market_analysis": [
        r"market data",
        r"market sizing",
        r"competitor mapping",
        r"demand validation",
    ],
    "competition_discovery": [
        r"competition",
        r"hackathon",
        r"竞赛",
        r"比赛",
    ],
    "gmail_management": [
        r"gmail",
        r"inbox",
        r"email",
        r"mailbox",
    ],
    "form_filling": [
        r"signup",
        r"\bforms?\b",
        r"\bfill\b",
        r"registration",
    ],
    "browser_operation": [
        r"browser automation",
        r"open.*browser",
        r"chrome",
        r"playwright",
        r"localhost",
    ],
    "presentation_generation": [
        r"presentation",
        r"slide",
        r"ppt",
        r"deck",
    ],
    "writing_assistant": [
        r"writing",
        r"draft",
        r"article",
        r"copywriting",
        r"rewrite",
    ],
    "document_generation": [
        r"document",
        r"docx",
        r"report",
        r"markdown",
    ],
}

BOUNDARY_PATTERNS = [
    r"do not read ([^.。\n]+)",
    r"never access ([^.。\n]+)",
    r"only read ([^.。\n]+)",
    r"requires user confirmation",
    r"user-provided",
    r"least privilege",
    r"no secrets",
    r"安全边界",
]

DOC_NAMES = {"SKILL.md", "README.md", "README", "package.json", "pyproject.toml"}


def _candidate_docs(files: Iterable[TextFile]) -> List[TextFile]:
    docs = [file for file in files if Path(file.relpath).name in DOC_NAMES]
    if docs:
        return docs
    return list(files)


def _line_for_match(content: str, pattern: str) -> int:
    match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
    if not match:
        return 1
    return content[: match.start()].count("\n") + 1


def extract_declared_intent(files: List[TextFile]) -> DeclaredIntent:
    docs = _candidate_docs(files)
    signals: List[IntentSignal] = []
    boundary_hits: List[str] = []

    for file in docs:
        text = file.content
        for intent, patterns in INTENT_PATTERNS.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
                if match:
                    line = _line_for_match(text, pattern)
                    evidence = file.lines[line - 1].strip() if 0 < line <= len(file.lines) else match.group(0)
                    if _is_negative_intent_context(evidence):
                        continue
                    if intent == "pdf_summarization" and not _is_pdf_summary_context(evidence):
                        continue
                    weight = 3 if file.relpath.upper().endswith("SKILL.MD") else 2
                    signals.append(
                        IntentSignal(
                            intent=intent,
                            weight=weight,
                            source=f"{file.relpath}:{line}",
                            evidence=evidence[:220],
                        )
                    )
                    break

        for pattern in BOUNDARY_PATTERNS:
            for match in re.finditer(pattern, text, re.IGNORECASE):
                line = text[: match.start()].count("\n") + 1
                evidence = file.lines[line - 1].strip() if 0 < line <= len(file.lines) else match.group(0)
                boundary_hits.append(f"{file.relpath}:{line} {evidence[:180]}")

    scores = {}
    for signal in signals:
        scores[signal.intent] = scores.get(signal.intent, 0) + signal.weight

    primary = [intent for intent, _score in sorted(scores.items(), key=lambda item: item[1], reverse=True)[:3]]

    if primary:
        summary = ", ".join(intent.replace("_", " ") for intent in primary)
    else:
        summary = "unspecified or weakly declared skill intent"

    has_skill_doc = any(Path(file.relpath).name == "SKILL.md" for file in files)
    has_readme = any(Path(file.relpath).name.upper().startswith("README") for file in files)
    clarity = 35
    clarity += min(35, len(signals) * 8)
    clarity += 15 if has_skill_doc else 0
    clarity += 8 if has_readme else 0
    clarity += min(12, len(boundary_hits) * 4)
    clarity = max(0, min(100, clarity))

    return DeclaredIntent(
        summary=summary,
        primary_intents=primary,
        clarity_score=clarity,
        signals=signals,
        boundaries=boundary_hits[:10],
    )


def _is_negative_intent_context(line: str) -> bool:
    lowered = line.lower()
    markers = [
        "do not",
        "should not",
        "must not",
        "never",
        "no network",
        "not require",
        "not read",
        "not access",
    ]
    return any(marker in lowered for marker in markers)


def _is_pdf_summary_context(line: str) -> bool:
    lowered = line.lower()
    return "pdf skill" in lowered or any(token in lowered for token in ["summar", "extract", "pdftotext", "pdf parser"])
