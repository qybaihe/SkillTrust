from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


TARGET_BODY_LINES = 180
WARN_BODY_LINES = 300
MAX_BODY_LINES = 500
MAX_BODY_WORDS = 5000


@dataclass
class AuthoringFinding:
    id: str
    severity: str
    category: str
    file: str
    line: int
    evidence: str
    recommendation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "severity": self.severity,
            "category": self.category,
            "file": self.file,
            "line": self.line,
            "evidence": self.evidence,
            "recommendation": self.recommendation,
        }


def analyze_authoring(skill_path: str | Path) -> Dict[str, Any]:
    root = Path(skill_path).expanduser().resolve()
    skill_file = root / "SKILL.md" if root.is_dir() else root
    if not skill_file.exists():
        raise FileNotFoundError(f"SKILL.md not found: {skill_file}")

    text = skill_file.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    frontmatter, body, body_start = _split_frontmatter(lines)
    metadata = _parse_frontmatter(frontmatter)
    body_lines = body.splitlines()
    references_dir = root / "references"
    reference_files = sorted(references_dir.rglob("*.md")) if references_dir.exists() else []
    direct_refs = _direct_reference_links(body)
    headings = _heading_sections(body_lines, body_start)
    move_candidates = _move_candidates(headings)

    findings: List[AuthoringFinding] = []
    counter = 1

    def add(severity: str, category: str, line: int, evidence: str, recommendation: str) -> None:
        nonlocal counter
        findings.append(
            AuthoringFinding(
                id=f"SA-{counter:03d}",
                severity=severity,
                category=category,
                file="SKILL.md",
                line=line,
                evidence=evidence[:260],
                recommendation=recommendation,
            )
        )
        counter += 1

    if "name" not in metadata:
        add("high", "metadata", 1, "Missing `name` in frontmatter.", "Add a short hyphen-case `name` field.")
    if "description" not in metadata:
        add(
            "high",
            "metadata",
            1,
            "Missing `description` in frontmatter.",
            "Add a clear trigger-oriented description; this is the field used for skill activation.",
        )
    else:
        description = metadata["description"]
        if len(description) < 60:
            add(
                "medium",
                "metadata",
                1,
                "Description is very short.",
                "Expand the description with concrete trigger scenarios and boundaries.",
            )
        if len(description) > 1200:
            add(
                "medium",
                "metadata",
                1,
                "Description is very long.",
                "Move detailed capability lists into SKILL.md body or references; keep description trigger-focused.",
            )

    body_word_count = _word_count(body)
    if len(body_lines) > MAX_BODY_LINES:
        add(
            "high",
            "monolithic-skill-md",
            body_start,
            f"SKILL.md body has {len(body_lines)} lines.",
            "Split detailed workflows, examples, schemas, and variant-specific guidance into `references/`.",
        )
    elif len(body_lines) > WARN_BODY_LINES:
        add(
            "medium",
            "skill-md-length",
            body_start,
            f"SKILL.md body has {len(body_lines)} lines.",
            "Keep only trigger-critical workflow guidance in SKILL.md; move long sections into references.",
        )
    if body_word_count > MAX_BODY_WORDS:
        add(
            "high",
            "context-budget",
            body_start,
            f"SKILL.md body has about {body_word_count} words.",
            "Reduce context cost by moving deep reference content into lazily loaded files.",
        )

    if len(body_lines) > TARGET_BODY_LINES and not reference_files:
        add(
            "high",
            "missing-references",
            body_start,
            "Long SKILL.md but no `references/` directory.",
            "Create `references/` and link each detailed file directly from SKILL.md.",
        )

    if move_candidates:
        first = move_candidates[0]
        add(
            "medium" if len(body_lines) <= MAX_BODY_LINES else "high",
            "progressive-disclosure",
            first["start_line"],
            f"{len(move_candidates)} sections look suitable for reference extraction.",
            "Keep the main harness short and move advanced/domain-specific sections into one-level reference files.",
        )

    if reference_files:
        referenced_paths = {Path(ref).as_posix() for ref in direct_refs}
        for ref in reference_files:
            rel = ref.relative_to(root).as_posix()
            if rel not in referenced_paths and f"./{rel}" not in referenced_paths:
                findings.append(
                    AuthoringFinding(
                        id=f"SA-{counter:03d}",
                        severity="low",
                        category="unlinked-reference",
                        file=rel,
                        line=1,
                        evidence=f"`{rel}` is not directly linked from SKILL.md.",
                        recommendation="Reference files should be linked from SKILL.md with clear read-when-needed guidance.",
                    )
                )
                counter += 1
            if len(ref.relative_to(references_dir).parts) > 1:
                findings.append(
                    AuthoringFinding(
                        id=f"SA-{counter:03d}",
                        severity="medium",
                        category="nested-reference",
                        file=rel,
                        line=1,
                        evidence=f"`{rel}` is nested below references/.",
                        recommendation="Keep references one level deep unless the hierarchy is absolutely necessary.",
                    )
                )
                counter += 1
            ref_lines = ref.read_text(encoding="utf-8", errors="replace").splitlines()
            if len(ref_lines) > 100 and not _has_toc(ref_lines):
                findings.append(
                    AuthoringFinding(
                        id=f"SA-{counter:03d}",
                        severity="low",
                        category="reference-navigation",
                        file=rel,
                        line=1,
                        evidence=f"`{rel}` has {len(ref_lines)} lines and no obvious table of contents.",
                        recommendation="Add a short table of contents near the top of long reference files.",
                    )
                )
                counter += 1

    score = _score(findings)
    level = _level(score)
    return {
        "schema_version": "skilltrust.authoring.v1",
        "skill_path": str(root),
        "skill_file": str(skill_file),
        "metadata": metadata,
        "metrics": {
            "skill_md_lines": len(lines),
            "body_lines": len(body_lines),
            "body_words_estimate": body_word_count,
            "references_count": len(reference_files),
            "direct_reference_links": len(direct_refs),
            "move_candidate_sections": len(move_candidates),
        },
        "harness_fit_score": score,
        "harness_level": level,
        "findings": [finding.to_dict() for finding in findings],
        "move_candidates": move_candidates,
        "optimized_skill_md_draft": _optimized_skill_md(frontmatter, body_lines, metadata, move_candidates),
        "reference_extraction_plan": _reference_plan(move_candidates),
        "standards": {
            "target_body_lines": TARGET_BODY_LINES,
            "warn_body_lines": WARN_BODY_LINES,
            "max_body_lines": MAX_BODY_LINES,
            "max_body_words": MAX_BODY_WORDS,
            "principles": [
                "Keep SKILL.md as the harness: trigger, boundaries, core workflow, and reference navigation.",
                "Move detailed workflows, schemas, long examples, variants, troubleshooting, and style libraries into references/.",
                "Link reference files directly from SKILL.md and state when to read each one.",
                "Keep references one level deep and add a table of contents for long files.",
            ],
        },
    }


def write_authoring_outputs(out_dir: str | Path, analysis: Dict[str, Any]) -> None:
    out = Path(out_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "authoring_analysis.json").write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "authoring_report.md").write_text(render_authoring_report(analysis), encoding="utf-8")
    (out / "optimized_SKILL.md").write_text(analysis["optimized_skill_md_draft"], encoding="utf-8")
    (out / "reference_extraction_plan.json").write_text(
        json.dumps(analysis["reference_extraction_plan"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def render_authoring_report(analysis: Dict[str, Any]) -> str:
    metrics = analysis["metrics"]
    lines = [
        "# SkillTrust Authoring Optimization Report",
        "",
        f"Skill: `{analysis['skill_path']}`",
        f"Harness Fit Score: {analysis['harness_fit_score']}/100 ({analysis['harness_level']})",
        "",
        "## Metrics",
        "",
        f"- SKILL.md lines: {metrics['skill_md_lines']}",
        f"- Body lines: {metrics['body_lines']}",
        f"- Body words estimate: {metrics['body_words_estimate']}",
        f"- Reference files: {metrics['references_count']}",
        f"- Direct reference links: {metrics['direct_reference_links']}",
        f"- Move candidate sections: {metrics['move_candidate_sections']}",
        "",
        "## Harness Standard",
        "",
        "- Keep `SKILL.md` short: trigger, boundaries, core workflow, and reference navigation.",
        "- Put detailed steps, examples, schemas, variants, and troubleshooting in `references/`.",
        "- Link every reference directly from `SKILL.md` with read-when-needed guidance.",
        "- Keep references one level deep; long references should include a table of contents.",
        "",
        "## Findings",
        "",
    ]
    if analysis["findings"]:
        lines.append("| ID | Severity | Category | Location | Recommendation |")
        lines.append("| --- | --- | --- | --- | --- |")
        for finding in analysis["findings"]:
            lines.append(
                f"| {finding['id']} | {finding['severity']} | {finding['category']} | "
                f"`{finding['file']}:{finding['line']}` | {finding['recommendation']} |"
            )
    else:
        lines.append("- No authoring structure findings. The Skill harness is already compact and navigable.")

    lines.extend(["", "## Proposed Reference Extraction", ""])
    if analysis["reference_extraction_plan"]:
        for item in analysis["reference_extraction_plan"]:
            lines.append(f"- Move `{item['heading']}` to `{item['target_reference']}` ({item['reason']}).")
    else:
        lines.append("- No section extraction needed.")

    lines.extend(
        [
            "",
            "## Generated Draft",
            "",
            "See `optimized_SKILL.md` for a compact harness draft. Source files were not modified.",
        ]
    )
    return "\n".join(lines) + "\n"


def _split_frontmatter(lines: List[str]) -> Tuple[List[str], str, int]:
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                return lines[: index + 1], "\n".join(lines[index + 1 :]), index + 2
    return [], "\n".join(lines), 1


def _parse_frontmatter(lines: List[str]) -> Dict[str, str]:
    metadata: Dict[str, str] = {}
    if not lines:
        return metadata
    for line in lines[1:-1]:
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata


def _word_count(text: str) -> int:
    latin = re.findall(r"[A-Za-z0-9_]+", text)
    cjk = re.findall(r"[\u4e00-\u9fff]", text)
    return len(latin) + max(1, len(cjk) // 2)


def _direct_reference_links(body: str) -> List[str]:
    refs = set()
    for match in re.finditer(r"(?:\(|`)(references/[^)`\s]+\.md)(?:\)|`)", body):
        refs.add(match.group(1))
    return sorted(refs)


def _heading_sections(lines: List[str], body_start: int) -> List[Dict[str, Any]]:
    headings = []
    for index, line in enumerate(lines):
        match = re.match(r"^(#{2,4})\s+(.+?)\s*$", line)
        if match:
            headings.append({"level": len(match.group(1)), "title": match.group(2), "index": index})
    sections = []
    for pos, heading in enumerate(headings):
        next_index = headings[pos + 1]["index"] if pos + 1 < len(headings) else len(lines)
        section_lines = lines[heading["index"] : next_index]
        sections.append(
            {
                "heading": heading["title"],
                "level": heading["level"],
                "start_line": body_start + heading["index"],
                "line_count": len(section_lines),
                "content_preview": "\n".join(section_lines[:8])[:500],
            }
        )
    return sections


def _move_candidates(sections: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    candidates = []
    keywords = [
        "advanced",
        "examples",
        "reference",
        "schema",
        "troubleshooting",
        "详细",
        "完整",
        "示例",
        "模板",
        "组件",
        "风格",
        "api",
        "commands",
        "checklist",
    ]
    for section in sections:
        title = section["heading"].lower()
        reason_parts = []
        if section["line_count"] >= 45:
            reason_parts.append(f"long section ({section['line_count']} lines)")
        if any(keyword in title for keyword in keywords):
            reason_parts.append("detail/reference-oriented heading")
        if reason_parts:
            target = f"references/{_slug(section['heading'])}.md"
            candidates.append(
                {
                    "heading": section["heading"],
                    "start_line": section["start_line"],
                    "line_count": section["line_count"],
                    "target_reference": target,
                    "reason": "; ".join(reason_parts),
                    "preview": section["content_preview"],
                }
            )
    return candidates[:20]


def _reference_plan(candidates: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        {
            "heading": item["heading"],
            "source_line": item["start_line"],
            "target_reference": item["target_reference"],
            "reason": item["reason"],
            "skill_md_replacement": f"- For {item['heading']}, read `{item['target_reference']}` when the task needs those details.",
        }
        for item in candidates
    ]


def _optimized_skill_md(
    frontmatter: List[str],
    body_lines: List[str],
    metadata: Dict[str, str],
    candidates: List[Dict[str, Any]],
) -> str:
    title = metadata.get("name") or _first_title(body_lines) or "optimized-skill"
    kept = _compact_core_lines(body_lines, candidates)
    result = []
    if frontmatter:
        result.extend(frontmatter)
        result.append("")
    result.append(f"# {title}")
    result.append("")
    result.append("## Core Harness")
    result.append("")
    result.append("Use this compact harness for trigger-critical workflow, safety boundaries, and reference navigation.")
    result.append("")
    if kept:
        result.extend(kept[:120])
    else:
        result.append("- Follow the declared workflow for this Skill.")
        result.append("- Load references only when the current task needs them.")
    if candidates:
        result.extend(["", "## References", ""])
        for item in candidates:
            result.append(f"- `{item['target_reference']}`: {item['heading']} ({item['reason']}).")
    result.append("")
    result.append("<!-- Generated by SkillTrust Authoring Optimizer. Review before applying. -->")
    return "\n".join(result).strip() + "\n"


def _compact_core_lines(body_lines: List[str], candidates: List[Dict[str, Any]]) -> List[str]:
    candidate_headings = {item["heading"] for item in candidates}
    output: List[str] = []
    skip_until_next_heading = False
    for line in body_lines:
        is_heading = re.match(r"^#{2,4}\s+(.+?)\s*$", line)
        if is_heading:
            skip_until_next_heading = is_heading.group(1) in candidate_headings
            if skip_until_next_heading:
                continue
        if not skip_until_next_heading:
            output.append(line)
    return _trim_blank_runs(output)


def _trim_blank_runs(lines: List[str]) -> List[str]:
    result = []
    blanks = 0
    for line in lines:
        if line.strip():
            blanks = 0
            result.append(line)
        else:
            blanks += 1
            if blanks <= 1:
                result.append(line)
    return result


def _first_title(lines: Iterable[str]) -> str | None:
    for line in lines:
        match = re.match(r"^#\s+(.+)", line)
        if match:
            return match.group(1).strip()
    return None


def _has_toc(lines: List[str]) -> bool:
    preview = "\n".join(lines[:25]).lower()
    return "table of contents" in preview or "目录" in preview or "- [" in preview


def _score(findings: Iterable[AuthoringFinding]) -> int:
    weights = {"low": 3, "medium": 8, "high": 18, "critical": 30}
    penalty = sum(weights.get(finding.severity, 0) for finding in findings)
    return max(0, min(100, 100 - penalty))


def _level(score: int) -> str:
    if score >= 90:
        return "Harness Ready"
    if score >= 75:
        return "Good"
    if score >= 50:
        return "Needs Split"
    return "Monolithic"


def _slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    value = value.strip("-")
    return value[:60] or "reference"
