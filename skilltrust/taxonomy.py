from __future__ import annotations

import json
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

GENERIC_NAME_TOKENS = {
    "agent",
    "assistant",
    "automation",
    "browser",
    "builder",
    "cli",
    "content",
    "data",
    "design",
    "doc",
    "docs",
    "generator",
    "helper",
    "image",
    "manager",
    "market",
    "post",
    "publisher",
    "report",
    "skill",
    "tool",
    "web",
}

STOPWORDS = {
    "a",
    "an",
    "and",
    "as",
    "for",
    "from",
    "in",
    "into",
    "of",
    "on",
    "or",
    "the",
    "to",
    "use",
    "using",
    "when",
    "with",
    "skill",
    "skills",
    "user",
    "users",
    "codex",
    "agent",
    "assistant",
    "help",
    "helps",
    "task",
    "tasks",
    "involve",
    "involves",
    "request",
    "requests",
    "file",
    "files",
    "especially",
    "prefer",
}


@dataclass
class SkillIdentity:
    directory_name: str
    declared_name: str
    path: str
    description: str
    body_heading: str

    def display_name(self) -> str:
        return self.declared_name or self.directory_name

    def normalized_name(self) -> str:
        return normalize_name(self.display_name())

    def name_tokens(self) -> Set[str]:
        return set(tokenize(self.display_name()))

    def trigger_tokens(self) -> Set[str]:
        return set(tokenize(f"{self.display_name()} {self.description} {self.body_heading}"))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "directory_name": self.directory_name,
            "declared_name": self.declared_name,
            "path": self.path,
            "description": self.description,
            "body_heading": self.body_heading,
        }


def analyze_taxonomy(skills_root: str | Path) -> Dict[str, Any]:
    root = Path(skills_root).expanduser().resolve()
    identities = [load_skill_identity(path) for path in discover_skill_dirs(root)]
    findings: List[Dict[str, Any]] = []
    rename_plan: List[Dict[str, Any]] = []

    _add_identity_findings(identities, findings, rename_plan)
    _add_pairwise_findings(identities, findings, rename_plan)

    score = _score(findings)
    return {
        "schema_version": "skilltrust.taxonomy.v1",
        "skills_root": str(root),
        "skill_count": len(identities),
        "taxonomy_score": score,
        "taxonomy_level": _level(score),
        "skills": [identity.to_dict() for identity in identities],
        "findings": findings,
        "rename_plan": _dedupe_plan(rename_plan),
        "approval_required": True,
        "approval_note": (
            "SkillTrust does not rename or edit local Skills automatically. Apply this plan only after explicit user approval, "
            "with backups and a review of references, docs, and any caller configuration that names these Skills."
        ),
        "naming_standards": {
            "principles": [
                "Use short, domain-specific, hyphen-case names.",
                "Prefer verb-domain or domain-action names over generic names.",
                "Keep related Skills namespaced consistently, such as `xhs-auth`, `xhs-publish`, and `xhs-explore`.",
                "Avoid near-duplicates whose descriptions share the same trigger words without clear differentiators.",
                "Make `description` trigger-oriented: state when to use the Skill and when not to use it.",
            ],
            "description_template": (
                "Use when the user wants <specific task/domain>. Covers <core capabilities>. "
                "Do not use for <neighboring but different tasks>; use <other-skill> instead."
            ),
        },
    }


def discover_skill_dirs(root: str | Path) -> List[Path]:
    base = Path(root).expanduser().resolve()
    if not base.exists():
        raise FileNotFoundError(f"Skills root does not exist: {base}")
    if (base / "SKILL.md").exists():
        return [base]
    dirs = []
    for skill_file in sorted(base.rglob("SKILL.md")):
        parts = set(skill_file.parts)
        if "__pycache__" in parts or ".git" in parts or "reports" in parts:
            continue
        dirs.append(skill_file.parent)
    return dirs


def write_taxonomy_outputs(out_dir: str | Path, analysis: Dict[str, Any]) -> None:
    out = Path(out_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "skill_taxonomy_report.md").write_text(render_taxonomy_report(analysis), encoding="utf-8")
    (out / "skill_taxonomy_plan.json").write_text(
        json.dumps(analysis, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "rename_approval_plan.md").write_text(render_approval_plan(analysis), encoding="utf-8")


def render_taxonomy_report(analysis: Dict[str, Any]) -> str:
    lines = [
        "# SkillTrust Taxonomy Optimization Report",
        "",
        f"Skills root: `{analysis['skills_root']}`",
        f"Skill count: {analysis['skill_count']}",
        f"Taxonomy Score: {analysis['taxonomy_score']}/100 ({analysis['taxonomy_level']})",
        f"Approval required: {analysis['approval_required']}",
        "",
        "## Summary",
        "",
        f"- Findings: {len(analysis['findings'])}",
        f"- Rename/description plan items: {len(analysis['rename_plan'])}",
        "",
        "## Findings",
        "",
    ]
    if analysis["findings"]:
        lines.append("| ID | Severity | Category | Skill(s) | Recommendation |")
        lines.append("| --- | --- | --- | --- | --- |")
        for finding in analysis["findings"]:
            lines.append(
                f"| {finding['id']} | {finding['severity']} | {finding['category']} | "
                f"`{finding['skills']}` | {finding['recommendation']} |"
            )
    else:
        lines.append("- No naming or trigger ambiguity findings detected.")

    lines.extend(["", "## Proposed Rename / Description Plan", ""])
    if analysis["rename_plan"]:
        lines.append("| Action | Skill | Proposed Name | Description Change | Approval |")
        lines.append("| --- | --- | --- | --- | --- |")
        for item in analysis["rename_plan"]:
            lines.append(
                f"| {item['action']} | `{item['current_name']}` | `{item['proposed_name']}` | "
                f"{item['description_strategy']} | required |"
            )
    else:
        lines.append("- No rename or description update proposed.")

    lines.extend(
        [
            "",
            "## Naming Standards",
            "",
        ]
    )
    for principle in analysis["naming_standards"]["principles"]:
        lines.append(f"- {principle}")
    lines.extend(
        [
            "",
            "## Approval Boundary",
            "",
            analysis["approval_note"],
        ]
    )
    return "\n".join(lines) + "\n"


def render_approval_plan(analysis: Dict[str, Any]) -> str:
    lines = [
        "# SkillTrust Rename Approval Plan",
        "",
        "This file is intentionally a plan, not an applied migration.",
        "",
        "## Approval Required",
        "",
        analysis["approval_note"],
        "",
        "## Proposed Changes",
        "",
    ]
    if not analysis["rename_plan"]:
        lines.append("- No changes proposed.")
        return "\n".join(lines) + "\n"
    for index, item in enumerate(analysis["rename_plan"], start=1):
        lines.extend(
            [
                f"### {index}. {item['current_name']}",
                "",
                f"- Action: {item['action']}",
                f"- Current path: `{item['path']}`",
                f"- Proposed name: `{item['proposed_name']}`",
                f"- Rationale: {item['rationale']}",
                f"- Description strategy: {item['description_strategy']}",
                f"- Apply status: `pending-user-approval`",
                "",
            ]
        )
    return "\n".join(lines)


def load_skill_identity(skill_dir: Path) -> SkillIdentity:
    skill_file = skill_dir / "SKILL.md"
    text = skill_file.read_text(encoding="utf-8", errors="replace")
    frontmatter = _frontmatter(text)
    heading = _first_heading(text)
    return SkillIdentity(
        directory_name=skill_dir.name,
        declared_name=frontmatter.get("name", ""),
        path=str(skill_dir),
        description=frontmatter.get("description", ""),
        body_heading=heading,
    )


def normalize_name(name: str) -> str:
    lowered = name.strip().lower()
    lowered = re.sub(r"[_\s]+", "-", lowered)
    lowered = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "", lowered)
    lowered = re.sub(r"-+", "-", lowered).strip("-")
    return lowered


def tokenize(value: str) -> List[str]:
    raw = re.findall(r"[A-Za-z0-9]+|[\u4e00-\u9fff]{2,}", value.lower())
    return [token for token in raw if token not in STOPWORDS and len(token) > 1]


def _frontmatter(text: str) -> Dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}
    data: Dict[str, str] = {}
    current_key = ""
    for line in lines[1:end]:
        if re.match(r"^\w[\w-]*\s*:", line):
            key, value = line.split(":", 1)
            current_key = key.strip()
            data[current_key] = value.strip().strip('"')
        elif current_key and line.startswith(" "):
            data[current_key] = f"{data[current_key]} {line.strip()}".strip()
    return data


def _first_heading(text: str) -> str:
    for line in text.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return match.group(1)
    return ""


def _add_identity_findings(
    identities: List[SkillIdentity], findings: List[Dict[str, Any]], rename_plan: List[Dict[str, Any]]
) -> None:
    seen: Dict[str, List[SkillIdentity]] = {}
    for identity in identities:
        seen.setdefault(identity.normalized_name(), []).append(identity)

        if identity.declared_name and normalize_name(identity.declared_name) != normalize_name(identity.directory_name):
            _finding(
                findings,
                "medium",
                "name-directory-mismatch",
                identity.display_name(),
                f"`name` is `{identity.declared_name}` but directory is `{identity.directory_name}`.",
                "Align declared name and directory name, or document why the alias is intentional.",
            )
            _plan(rename_plan, identity, normalize_name(identity.directory_name), "update-name", "Align frontmatter name with installed directory name.")

        if not identity.description:
            _finding(
                findings,
                "high",
                "missing-description",
                identity.display_name(),
                "Missing description.",
                "Add a trigger-oriented description with positive and negative use cases.",
            )
            _plan(rename_plan, identity, identity.normalized_name(), "update-description", "Add trigger-oriented description.")
        elif len(identity.description) < 80:
            _finding(
                findings,
                "medium",
                "weak-description",
                identity.display_name(),
                "Description is too short to disambiguate neighboring Skills.",
                "Expand description with specific trigger scenarios, capabilities, and exclusions.",
            )
            _plan(rename_plan, identity, identity.normalized_name(), "update-description", "Expand trigger-oriented description.")

        tokens = identity.name_tokens()
        if _is_generic_name(identity):
            suggested = _suggest_name(identity)
            _finding(
                findings,
                "medium",
                "generic-name",
                identity.display_name(),
                f"Name tokens `{', '.join(sorted(tokens))}` are generic.",
                f"Use a more domain-specific name such as `{suggested}`.",
            )
            _plan(rename_plan, identity, suggested, "rename", "Generic name weakens model-side Skill selection.")

    for normalized, group in seen.items():
        if normalized and len(group) > 1:
            names = ", ".join(item.display_name() for item in group)
            _finding(
                findings,
                "high",
                "duplicate-name",
                names,
                f"{len(group)} Skills normalize to `{normalized}`.",
                "Rename or namespace duplicate Skills so the model has one unambiguous target.",
            )


def _add_pairwise_findings(
    identities: List[SkillIdentity], findings: List[Dict[str, Any]], rename_plan: List[Dict[str, Any]]
) -> None:
    counter_pairs = set()
    for index, left in enumerate(identities):
        for right in identities[index + 1 :]:
            pair_key = tuple(sorted([left.path, right.path]))
            if pair_key in counter_pairs:
                continue
            counter_pairs.add(pair_key)

            name_similarity = SequenceMatcher(None, left.normalized_name(), right.normalized_name()).ratio()
            trigger_similarity = _jaccard(left.trigger_tokens(), right.trigger_tokens())
            shared_name_tokens = left.name_tokens() & right.name_tokens()
            same_prefix = _prefix(left.normalized_name()) and _prefix(left.normalized_name()) == _prefix(right.normalized_name())

            if name_similarity >= 0.82 or (shared_name_tokens and trigger_similarity >= 0.42):
                severity = "high" if trigger_similarity >= 0.55 else "medium"
                skills = f"{left.display_name()} <-> {right.display_name()}"
                _finding(
                    findings,
                    severity,
                    "trigger-overlap",
                    skills,
                    f"name_similarity={name_similarity:.2f}, trigger_similarity={trigger_similarity:.2f}",
                    "Add naming or description differentiators so the model can choose the intended Skill.",
                )
                for identity, other in [(left, right), (right, left)]:
                    _plan(
                        rename_plan,
                        identity,
                        identity.normalized_name(),
                        "update-description",
                        f"Disambiguate from `{other.display_name()}` with explicit when-to-use and when-not-to-use wording.",
                    )
            elif same_prefix and trigger_similarity < 0.18:
                # Namespaced families are useful, but descriptions should mention the differentiating verb.
                for identity, other in [(left, right), (right, left)]:
                    if len(identity.description) < 140:
                        _finding(
                            findings,
                            "low",
                            "namespace-needs-differentiator",
                            f"{identity.display_name()} / {other.display_name()}",
                            "Names share a namespace but description is short.",
                            "Keep the namespace, but make each description say exactly when to use this member of the family.",
                        )


def _finding(
    findings: List[Dict[str, Any]],
    severity: str,
    category: str,
    skills: str,
    evidence: str,
    recommendation: str,
) -> None:
    findings.append(
        {
            "id": f"TX-{len(findings) + 1:03d}",
            "severity": severity,
            "category": category,
            "skills": skills,
            "evidence": evidence,
            "recommendation": recommendation,
        }
    )


def _plan(
    rename_plan: List[Dict[str, Any]],
    identity: SkillIdentity,
    proposed_name: str,
    action: str,
    rationale: str,
) -> None:
    rename_plan.append(
        {
            "action": action,
            "current_name": identity.display_name(),
            "directory_name": identity.directory_name,
            "declared_name": identity.declared_name,
            "proposed_name": proposed_name,
            "path": identity.path,
            "rationale": rationale,
            "description_strategy": (
                "Rewrite description to include positive triggers, exclusions, and nearby Skill alternatives."
            ),
            "requires_user_approval": True,
        }
    )


def _dedupe_plan(items: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result = []
    for item in items:
        key = (item["path"], item["action"], item["proposed_name"])
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result


def _suggest_name(identity: SkillIdentity, avoid: SkillIdentity | None = None) -> str:
    special = {
        "doc": "docx-documents",
        "pdf": "pdf-processing",
        "browser": "browser-automation",
        "design": "frontend-design",
    }
    normalized_dir = normalize_name(identity.directory_name)
    if normalized_dir in special:
        return special[normalized_dir]
    tokens = [token for token in tokenize(identity.description) if token not in GENERIC_NAME_TOKENS]
    name_tokens = [token for token in tokenize(identity.display_name()) if token not in GENERIC_NAME_TOKENS]
    chosen = []
    for token in name_tokens + tokens:
        if token not in chosen:
            chosen.append(token)
        if len(chosen) >= 3:
            break
    if avoid:
        avoid_tokens = avoid.name_tokens()
        chosen = [token for token in chosen if token not in avoid_tokens] or chosen
    if not chosen:
        chosen = [normalize_name(identity.directory_name)]
    return "-".join(chosen[:3])


def _is_generic_name(identity: SkillIdentity) -> bool:
    tokens = identity.name_tokens()
    normalized = identity.normalized_name()
    if not tokens:
        return True
    if len(tokens) == 1 and next(iter(tokens)) in GENERIC_NAME_TOKENS:
        return True
    if len(normalized) <= 3 and normalized in GENERIC_NAME_TOKENS:
        return True
    return False


def _jaccard(left: Set[str], right: Set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _prefix(name: str) -> str:
    parts = name.split("-")
    return parts[0] if len(parts) > 1 else ""


def _score(findings: List[Dict[str, Any]]) -> int:
    weights = {"low": 2, "medium": 8, "high": 18, "critical": 30}
    penalty = sum(weights.get(item["severity"], 0) for item in findings)
    return max(0, min(100, 100 - penalty))


def _level(score: int) -> str:
    if score >= 90:
        return "Clear Taxonomy"
    if score >= 75:
        return "Mostly Clear"
    if score >= 50:
        return "Ambiguous"
    return "Needs Reshuffle"
