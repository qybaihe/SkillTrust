from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


TARGET_ACTIVATION_TOKENS = 1800


@dataclass
class TokenCandidate:
    id: str
    kind: str
    section: str
    file: str
    line: int
    current_tokens: int
    estimated_tokens_saved: int
    proposed_artifact: str
    reason: str
    conversion_strategy: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "section": self.section,
            "file": self.file,
            "line": self.line,
            "current_tokens": self.current_tokens,
            "estimated_tokens_saved": self.estimated_tokens_saved,
            "proposed_artifact": self.proposed_artifact,
            "reason": self.reason,
            "conversion_strategy": self.conversion_strategy,
        }


def estimate_tokens(text: str) -> int:
    # Practical deterministic estimate: English averages ~4 chars/token; CJK is denser.
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    non_cjk = max(0, len(text) - cjk)
    return max(1, int(non_cjk / 4 + cjk / 1.8))


def analyze_token_efficiency(skill_path: str | Path) -> Dict[str, Any]:
    root = Path(skill_path).expanduser().resolve()
    skill_file = root / "SKILL.md" if root.is_dir() else root
    if not skill_file.exists():
        raise FileNotFoundError(f"SKILL.md not found: {skill_file}")

    text = skill_file.read_text(encoding="utf-8", errors="replace")
    frontmatter, body, body_start = _split_frontmatter(text.splitlines())
    sections = _sections(body.splitlines(), body_start)
    candidates = _scriptification_candidates(sections)

    activation_tokens = estimate_tokens(body)
    frontmatter_tokens = estimate_tokens("\n".join(frontmatter)) if frontmatter else 0
    reference_tokens = _directory_tokens(root / "references")
    script_files = _script_files(root / "scripts")
    total_savings = sum(item.estimated_tokens_saved for item in candidates)
    projected_activation_tokens = max(250, activation_tokens - total_savings)
    score = _score(activation_tokens, candidates)

    return {
        "schema_version": "skilltrust.token_efficiency.v1",
        "skill_path": str(root),
        "skill_file": str(skill_file),
        "metrics": {
            "frontmatter_tokens_estimate": frontmatter_tokens,
            "activation_body_tokens_estimate": activation_tokens,
            "target_activation_tokens": TARGET_ACTIVATION_TOKENS,
            "projected_activation_tokens": projected_activation_tokens,
            "reference_tokens_deferred": reference_tokens,
            "script_files": len(script_files),
            "scriptification_candidates": len(candidates),
            "estimated_tokens_saved": total_savings,
        },
        "token_efficiency_score": score,
        "token_efficiency_level": _level(score),
        "scriptification_candidates": [item.to_dict() for item in candidates],
        "optimization_principles": [
            "Keep judgment, ambiguity, and user-facing tradeoffs in SKILL.md.",
            "Move deterministic transforms, validators, routing tables, schemas, and fixed command sequences into scripts or config.",
            "Use references for knowledge that may be needed, but scripts for logic that should not be re-interpreted.",
            "Prefer a short instruction that calls a bundled tool over a long instruction block that asks the model to simulate that tool.",
        ],
    }


def write_token_outputs(out_dir: str | Path, analysis: Dict[str, Any]) -> None:
    out = Path(out_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "token_optimization_plan.json").write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "token_efficiency_report.md").write_text(render_token_report(analysis), encoding="utf-8")


def render_token_report(analysis: Dict[str, Any]) -> str:
    metrics = analysis["metrics"]
    lines = [
        "# SkillTrust Token Efficiency Report",
        "",
        f"Skill: `{analysis['skill_path']}`",
        f"Token Efficiency Score: {analysis['token_efficiency_score']}/100 ({analysis['token_efficiency_level']})",
        "",
        "## Token Budget",
        "",
        f"- Frontmatter tokens estimate: {metrics['frontmatter_tokens_estimate']}",
        f"- Activation body tokens estimate: {metrics['activation_body_tokens_estimate']}",
        f"- Target activation body tokens: {metrics['target_activation_tokens']}",
        f"- Projected activation tokens after optimizations: {metrics['projected_activation_tokens']}",
        f"- Deferred reference tokens estimate: {metrics['reference_tokens_deferred']}",
        f"- Existing script files: {metrics['script_files']}",
        f"- Scriptification candidates: {metrics['scriptification_candidates']}",
        f"- Estimated activation tokens saved: {metrics['estimated_tokens_saved']}",
        "",
        "## Scriptification Candidates",
        "",
    ]
    candidates = analysis["scriptification_candidates"]
    if candidates:
        lines.append("| ID | Kind | Location | Saved | Proposed Artifact |")
        lines.append("| --- | --- | --- | ---: | --- |")
        for item in candidates:
            lines.append(
                f"| {item['id']} | {item['kind']} | `{item['file']}:{item['line']}` | "
                f"{item['estimated_tokens_saved']} | `{item['proposed_artifact']}` |"
            )
        lines.append("")
        for item in candidates:
            lines.extend(
                [
                    f"### {item['id']} - {item['kind']}",
                    "",
                    f"- Section: {item['section']}",
                    f"- Current tokens: {item['current_tokens']}",
                    f"- Estimated saved: {item['estimated_tokens_saved']}",
                    f"- Reason: {item['reason']}",
                    f"- Conversion strategy: {item['conversion_strategy']}",
                    "",
                ]
            )
    else:
        lines.append("- No high-value scriptification candidates detected.")

    lines.extend(["", "## Principles", ""])
    for item in analysis["optimization_principles"]:
        lines.append(f"- {item}")
    return "\n".join(lines) + "\n"


def _split_frontmatter(lines: List[str]) -> Tuple[List[str], str, int]:
    if lines and lines[0].strip() == "---":
        for index in range(1, len(lines)):
            if lines[index].strip() == "---":
                return lines[: index + 1], "\n".join(lines[index + 1 :]), index + 2
    return [], "\n".join(lines), 1


def _sections(lines: List[str], body_start: int) -> List[Dict[str, Any]]:
    headings = []
    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,4})\s+(.+?)\s*$", line)
        if match:
            headings.append({"level": len(match.group(1)), "title": match.group(2), "index": index})
    if not headings:
        return [{"title": "SKILL.md body", "line": body_start, "text": "\n".join(lines)}]

    sections = []
    for pos, heading in enumerate(headings):
        next_index = headings[pos + 1]["index"] if pos + 1 < len(headings) else len(lines)
        text = "\n".join(lines[heading["index"] : next_index])
        sections.append({"title": heading["title"], "line": body_start + heading["index"], "text": text})
    return sections


def _scriptification_candidates(sections: Iterable[Dict[str, Any]]) -> List[TokenCandidate]:
    candidates: List[TokenCandidate] = []
    counter = 1
    for section in sections:
        text = section["text"]
        tokens = estimate_tokens(text)
        lowered = text.lower()
        kind, reason, strategy, artifact = _classify_section(section["title"], lowered, text)
        if not kind:
            continue
        if tokens < 180 and kind not in {"validator-script", "command-wrapper"}:
            continue
        saved = _estimated_savings(tokens, kind)
        candidates.append(
            TokenCandidate(
                id=f"TO-{counter:03d}",
                kind=kind,
                section=section["title"],
                file="SKILL.md",
                line=section["line"],
                current_tokens=tokens,
                estimated_tokens_saved=saved,
                proposed_artifact=artifact,
                reason=reason,
                conversion_strategy=strategy,
            )
        )
        counter += 1
    return sorted(candidates, key=lambda item: item.estimated_tokens_saved, reverse=True)[:20]


def _classify_section(title: str, lowered: str, text: str) -> Tuple[str | None, str, str, str]:
    title_l = title.lower()
    has_code = "```" in text
    command_hits = len(re.findall(r"\b(python|node|npm|npx|bash|sh|ffmpeg|playwright|curl|jq)\b", lowered))
    table_rows = sum(1 for line in text.splitlines() if line.strip().startswith("|"))
    bullet_count = sum(1 for line in text.splitlines() if re.match(r"\s*[-*]\s+", line))

    if any(word in title_l for word in ["check", "verify", "validation", "验收", "检查", "红线"]) or (
        bullet_count >= 10 and any(word in lowered for word in ["must", "禁止", "required", "fail", "error"])
    ):
        return (
            "validator-script",
            "This section describes deterministic checks that can run as code instead of being re-read as judgment rules.",
            "Create `scripts/validate_skill_output.py` or a domain-specific validator. Keep SKILL.md to one line: run the validator and fix failures.",
            "scripts/validate_skill_output.py",
        )

    if has_code and command_hits >= 3:
        return (
            "command-wrapper",
            "Repeated command sequences are better as a wrapper script with arguments than long command instructions.",
            "Create a script that runs the sequence, handles errors, and emits concise status JSON for the model.",
            f"scripts/{_slug(title)}.sh",
        )

    if table_rows >= 8 or any(word in title_l for word in ["route", "routing", "matrix", "decision", "路由", "映射"]):
        return (
            "routing-config",
            "Routing matrices and selection tables can be encoded as JSON/YAML config plus a small resolver.",
            "Move the table into `references/routing.json` or `config/routing.yaml`; add a resolver script for deterministic matching.",
            "config/routing.yaml",
        )

    if any(word in title_l for word in ["schema", "fields", "format", "json", "字段", "结构"]) or re.search(
        r"\{[^{}]{30,}\}", text, re.DOTALL
    ):
        return (
            "schema-config",
            "Structured formats and field rules should be machine-checkable instead of only described in prose.",
            "Move the format into JSON Schema or typed config and validate outputs with a bundled script.",
            "schemas/output.schema.json",
        )

    if any(word in title_l for word in ["example", "examples", "示例", "模板", "style", "风格"]):
        return (
            "reference-or-asset",
            "Large examples and style libraries should be deferred or stored as assets, not loaded on every activation.",
            "Move examples into `references/examples.md` or `assets/`; keep only selection guidance in SKILL.md.",
            f"references/{_slug(title)}.md",
        )

    if any(word in lowered for word in ["convert", "parse", "export", "render", "download", "slice", "generate"]) and (
        has_code or command_hits >= 2
    ):
        return (
            "deterministic-transform-script",
            "Parsing, conversion, rendering, downloading, and slicing are deterministic operations that should be scripts.",
            "Create a parameterized helper script and have SKILL.md call it instead of describing the whole transform.",
            f"scripts/{_slug(title)}.py",
        )

    if len(text.splitlines()) > 80:
        return (
            "reference-deferral",
            "This long section likely exceeds what the model needs on every activation.",
            "Move the section to a direct `references/` file and keep only when-to-read guidance in SKILL.md.",
            f"references/{_slug(title)}.md",
        )

    return None, "", "", ""


def _estimated_savings(tokens: int, kind: str) -> int:
    ratios = {
        "validator-script": 0.82,
        "command-wrapper": 0.78,
        "routing-config": 0.70,
        "schema-config": 0.74,
        "reference-or-asset": 0.65,
        "deterministic-transform-script": 0.80,
        "reference-deferral": 0.68,
    }
    return max(50, int(tokens * ratios.get(kind, 0.6)))


def _directory_tokens(path: Path) -> int:
    if not path.exists():
        return 0
    total = 0
    for file in path.rglob("*.md"):
        try:
            total += estimate_tokens(file.read_text(encoding="utf-8", errors="replace"))
        except OSError:
            continue
    return total


def _script_files(path: Path) -> List[Path]:
    if not path.exists():
        return []
    return [
        file
        for file in path.rglob("*")
        if file.is_file() and file.suffix.lower() in {".py", ".js", ".mjs", ".sh", ".ts", ".rb"}
    ]


def _score(activation_tokens: int, candidates: List[TokenCandidate]) -> int:
    over_budget = max(0, activation_tokens - TARGET_ACTIVATION_TOKENS)
    penalty = min(55, over_budget // 90)
    penalty += min(35, sum(1 for item in candidates if item.kind != "reference-deferral") * 7)
    penalty += min(10, len(candidates) * 2)
    return max(0, min(100, 100 - penalty))


def _level(score: int) -> str:
    if score >= 90:
        return "Token Lean"
    if score >= 75:
        return "Efficient"
    if score >= 50:
        return "Can Save Tokens"
    return "Token Heavy"


def _slug(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", value)
    return value.strip("-")[:60] or "helper"
