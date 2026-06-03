from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, List

from .models import AnalysisResult, Finding, SEVERITY_WEIGHTS


def render_report(result: AnalysisResult) -> str:
    score = result.score
    lines: List[str] = [
        "# SkillTrust Trust Report",
        "",
        f"**Input:** `{result.input_path}`",
        f"**Trust Fit Score:** {score.trust_fit_score}/100",
        f"**Risk Level:** {score.risk_level}",
        f"**Rules Version:** `{result.rules_version}`",
        "",
        "## Declared Intent",
        "",
        f"- Summary: {result.declared_intent.summary}",
        f"- Primary intents: {', '.join(result.declared_intent.primary_intents) or 'none detected'}",
        f"- Intent clarity: {result.declared_intent.clarity_score}/100",
    ]
    if result.declared_intent.signals:
        lines.append("- Evidence signals:")
        for signal in result.declared_intent.signals[:8]:
            lines.append(f"  - `{signal.source}` -> {signal.intent}: {signal.evidence}")
    if result.declared_intent.boundaries:
        lines.append("- Declared boundaries:")
        for boundary in result.declared_intent.boundaries[:6]:
            lines.append(f"  - {boundary}")

    lines.extend(
        [
            "",
            "## Inferred Minimum Permissions",
            "",
            _render_permission_list("Filesystem read", result.required_permissions.filesystem_read, "scope"),
            _render_permission_list("Filesystem write", result.required_permissions.filesystem_write, "scope"),
            _render_permission_list("Network", result.required_permissions.network, "scope"),
            _render_permission_list("Shell", result.required_permissions.shell, "command"),
            _render_permission_list("Connectors", result.required_permissions.connectors, "connector"),
            "",
            "## Observed / Requested Permissions",
            "",
        ]
    )

    if result.observed_permissions:
        for item in result.observed_permissions[:30]:
            lines.append(
                f"- `{item.category}` `{item.permission}` at `{item.file}:{item.line}` "
                f"({item.relation}; severity hint: {item.severity_hint})"
            )
        if len(result.observed_permissions) > 30:
            lines.append(f"- ... {len(result.observed_permissions) - 30} more observed permissions omitted from this report view.")
    else:
        lines.append("- No material permission-touching behavior detected in scanned text files.")

    lines.extend(
        [
            "",
            "## Permission Overreach Findings",
            "",
        ]
    )
    if result.findings:
        lines.append("| ID | Severity | Category | Location | Intent Relation |")
        lines.append("| --- | --- | --- | --- | --- |")
        for finding in result.findings:
            relation = finding.declared_intent_relation.replace("\n", " ")[:120]
            lines.append(
                f"| {finding.id} | {finding.severity} | {finding.category} | "
                f"`{finding.file}:{finding.line}` | {relation} |"
            )
        lines.append("")
        for finding in result.findings:
            lines.extend(_render_finding_detail(finding))
    else:
        lines.append("- No permission overreach findings were detected.")

    lines.extend(
        [
            "",
            "## Trust Fit Score Breakdown",
            "",
        ]
    )
    for name, value in result.score.components.items():
        lines.append(f"- {name}: {value}/100")
    lines.append("")
    for item in result.score.explanation:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "## Runtime Policy Effect",
            "",
            "- Filesystem reads are limited to skill/workspace/user-provided inputs and deny sensitive home credential surfaces.",
            "- Network access is denied by default unless the declared intent needs task-relevant domains.",
            "- Shell execution is constrained to explicit local helper commands and denies high-impact patterns.",
            "- Environment secrets, prompt-integrity bypasses, postinstall hooks, and remote setup scripts are blocked.",
            "",
            "## Verification",
            "",
            "This report is paired with `audit_receipt.json`, which records file hashes, rules version, result hash, and evidence hashes.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_remediation_plan(result: AnalysisResult) -> str:
    lines: List[str] = [
        "# SkillTrust Remediation Plan",
        "",
        f"Input: `{result.input_path}`",
        f"Current Trust Fit Score: {result.score.trust_fit_score}/100 ({result.score.risk_level})",
        "",
        "## Goal",
        "",
        "Converge the skill to its declared intent with least-privilege filesystem, network, environment, shell, and install-time permissions.",
        "",
    ]
    if not result.findings:
        lines.extend(
            [
                "## Recommended Actions",
                "",
                "- Keep permissions scoped to the generated `permission_manifest.json`.",
                "- Preserve the generated `skilltrust-policy.json` as an install-time policy contract.",
                "- Re-run SkillTrust after any dependency, connector, or workflow change.",
            ]
        )
        return "\n".join(lines) + "\n"

    grouped = _group_findings(result.findings)
    lines.extend(["## Findings To Fix", ""])
    for category, findings in grouped.items():
        lines.append(f"### {category}")
        for finding in findings:
            lines.append(f"- `{finding.id}` `{finding.file}:{finding.line}`: {finding.recommendation}")
        lines.append("")

    lines.extend(
        [
            "## Policy Convergence Checklist",
            "",
            "- Remove implicit reads of `.env`, SSH keys, browser cookies, cloud credentials, and shell history.",
            "- Replace broad `$HOME` traversal with `$WORKSPACE`, `$SKILL_DIR`, or user-selected input paths.",
            "- Declare every allowed network domain and block generic webhook endpoints.",
            "- Remove hidden POST sinks unless the user explicitly confirms the destination and payload.",
            "- Replace dynamic shell/code execution with explicit allowlisted helper commands.",
            "- Pin dependency versions and remove postinstall hooks or remote install scripts.",
            "- Delete prompt instructions that hide actions, bypass policy, or self-authorize permissions.",
            "",
            "## Re-test",
            "",
            "Run `skilltrust analyze <skill-path> --out reports/<skill-name>-after-remediation` and compare the new audit receipt hash.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(out_dir: Path, result: AnalysisResult) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "permission_manifest.json").write_text(
        json.dumps(result.permission_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out_dir / "skilltrust-policy.json").write_text(
        json.dumps(result.policy, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out_dir / "trust_report.md").write_text(render_report(result), encoding="utf-8")
    (out_dir / "audit_receipt.json").write_text(
        json.dumps(result.audit_receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out_dir / "remediation_plan.md").write_text(result.remediation_plan or render_remediation_plan(result), encoding="utf-8")
    (out_dir / "analysis.json").write_text(
        json.dumps(result.to_dict(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def summary_text(result: AnalysisResult) -> str:
    top = sorted(result.findings, key=lambda item: SEVERITY_WEIGHTS.get(item.severity, 0), reverse=True)[:5]
    lines = [
        f"SkillTrust score: {result.score.trust_fit_score}/100 ({result.score.risk_level})",
        f"Declared intent: {result.declared_intent.summary}",
        f"Findings: {len(result.findings)}",
    ]
    for finding in top:
        lines.append(f"- {finding.id} [{finding.severity}] {finding.category} at {finding.file}:{finding.line}")
    return "\n".join(lines)


def _render_permission_list(title: str, items: Iterable[dict], key: str) -> str:
    values = list(items)
    if not values:
        return f"- {title}: none"
    rendered = "; ".join(f"`{item.get(key, '')}` ({item.get('reason', 'declared')})" for item in values)
    return f"- {title}: {rendered}"


def _render_finding_detail(finding: Finding) -> List[str]:
    return [
        f"### {finding.id} - {finding.category}",
        "",
        f"- Severity: {finding.severity}",
        f"- Location: `{finding.file}:{finding.line}`",
        f"- Evidence: `{finding.evidence}`",
        f"- Declared intent relation: {finding.declared_intent_relation}",
        f"- Why it matters: {finding.why_it_matters}",
        f"- Recommendation: {finding.recommendation}",
        f"- Policy effect: {finding.policy_effect}",
        f"- Confidence: {finding.confidence}",
        "",
    ]


def _group_findings(findings: Iterable[Finding]) -> dict:
    grouped = {}
    for finding in findings:
        grouped.setdefault(finding.category, []).append(finding)
    return grouped
