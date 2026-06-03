from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .analyzer import SkillTrustAnalyzer
from .authoring import analyze_authoring, write_authoring_outputs
from .models import AnalysisResult, SEVERITY_WEIGHTS
from .reporting import write_outputs
from .taxonomy import analyze_taxonomy, write_taxonomy_outputs
from .token_optimizer import analyze_token_efficiency, write_token_outputs


BLOCK_LEVELS = {"Critical Risk"}
WARN_LEVELS = {"Needs Review", "Overprivileged"}


@dataclass
class SkillGovernanceRecord:
    name: str
    path: str
    report_dir: str
    score: int
    risk_level: str
    decision: str
    findings_count: int
    optimized_controls: List[str]
    authoring_score: int
    authoring_level: str
    authoring_actions: List[str]
    token_score: int
    token_level: str
    estimated_tokens_saved: int
    token_actions: List[str]
    top_findings: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "path": self.path,
            "report_dir": self.report_dir,
            "score": self.score,
            "risk_level": self.risk_level,
            "decision": self.decision,
            "findings_count": self.findings_count,
            "optimized_controls": self.optimized_controls,
            "authoring_score": self.authoring_score,
            "authoring_level": self.authoring_level,
            "authoring_actions": self.authoring_actions,
            "token_score": self.token_score,
            "token_level": self.token_level,
            "estimated_tokens_saved": self.estimated_tokens_saved,
            "token_actions": self.token_actions,
            "top_findings": self.top_findings,
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


def install_decision(result: AnalysisResult, threshold: int = 70) -> Dict[str, Any]:
    if result.score.risk_level in BLOCK_LEVELS:
        action = "block"
        reason = "Critical permission overreach or sensitive data-flow evidence requires remediation before install."
    elif result.score.trust_fit_score < threshold or result.score.risk_level in WARN_LEVELS:
        action = "warn"
        reason = "The Skill can be installed only with the generated policy overlay and human review."
    else:
        action = "allow"
        reason = "Declared intent and observed permissions fit the generated least-privilege policy."

    return {
        "action": action,
        "threshold": threshold,
        "score": result.score.trust_fit_score,
        "risk_level": result.score.risk_level,
        "reason": reason,
        "required_policy": result.policy,
        "permission_manifest": result.permission_manifest,
    }


def optimized_controls(result: AnalysisResult) -> List[str]:
    controls = set()
    categories = {finding.category for finding in result.findings}

    if "filesystem" in categories:
        controls.add("Constrained filesystem reads to skill/workspace/user-selected paths.")
        controls.add("Denied home-directory enumeration and sensitive local credential paths.")
    if "environment" in categories:
        controls.add("Blocked secret-bearing environment variable patterns.")
    if "network" in categories or "data_flow" in categories:
        controls.add("Denied unapproved POST/webhook sinks and unrelated outbound domains.")
    if "shell" in categories:
        controls.add("Restricted shell execution to explicit helper command allowlists.")
    if "install" in categories or "dependency" in categories:
        controls.add("Required pinned dependencies and denied postinstall/remote setup scripts.")
    if "prompt" in categories:
        controls.add("Blocked hidden prompt directives and self-authorization language.")
    if not controls:
        controls.add("Preserved generated least-privilege policy; no material remediation needed.")

    return sorted(controls)


def authoring_actions(authoring: Dict[str, Any]) -> List[str]:
    actions = []
    metrics = authoring["metrics"]
    if metrics["body_lines"] > 180:
        actions.append("Slim SKILL.md into a compact harness and move details into references/.")
    if authoring["reference_extraction_plan"]:
        actions.append(
            f"Extract {len(authoring['reference_extraction_plan'])} detail sections into one-level reference files."
        )
    if any(item["category"] == "unlinked-reference" for item in authoring["findings"]):
        actions.append("Link existing reference files directly from SKILL.md with read-when-needed guidance.")
    if any(item["category"] == "reference-navigation" for item in authoring["findings"]):
        actions.append("Add table of contents to long reference files.")
    if not actions:
        actions.append("Harness already compact; preserve current progressive disclosure structure.")
    return actions


def token_actions(token_analysis: Dict[str, Any]) -> List[str]:
    candidates = token_analysis["scriptification_candidates"]
    actions = []
    kinds = {item["kind"] for item in candidates}
    if "validator-script" in kinds:
        actions.append("Compile deterministic checklists and red lines into validator scripts.")
    if "command-wrapper" in kinds or "deterministic-transform-script" in kinds:
        actions.append("Replace repeated command/procedure text with parameterized helper scripts.")
    if "routing-config" in kinds:
        actions.append("Move routing tables into config plus a deterministic resolver.")
    if "schema-config" in kinds:
        actions.append("Move output format rules into JSON Schema/config and validate with code.")
    if "reference-or-asset" in kinds or "reference-deferral" in kinds:
        actions.append("Defer examples/style libraries into references or assets.")
    if not actions:
        actions.append("No high-value scriptification candidates; keep the current token path.")
    return actions


def build_record(
    name: str,
    path: Path,
    report_dir: Path,
    result: AnalysisResult,
    threshold: int,
    authoring: Dict[str, Any],
    token_analysis: Dict[str, Any],
) -> SkillGovernanceRecord:
    decision = install_decision(result, threshold=threshold)["action"]
    top = sorted(result.findings, key=lambda item: SEVERITY_WEIGHTS.get(item.severity, 0), reverse=True)[:5]
    return SkillGovernanceRecord(
        name=name,
        path=str(path),
        report_dir=str(report_dir),
        score=result.score.trust_fit_score,
        risk_level=result.score.risk_level,
        decision=decision,
        findings_count=len(result.findings),
        optimized_controls=optimized_controls(result),
        authoring_score=authoring["harness_fit_score"],
        authoring_level=authoring["harness_level"],
        authoring_actions=authoring_actions(authoring),
        token_score=token_analysis["token_efficiency_score"],
        token_level=token_analysis["token_efficiency_level"],
        estimated_tokens_saved=token_analysis["metrics"]["estimated_tokens_saved"],
        token_actions=token_actions(token_analysis),
        top_findings=[
            {
                "id": finding.id,
                "severity": finding.severity,
                "category": finding.category,
                "location": f"{finding.file}:{finding.line}",
                "recommendation": finding.recommendation,
            }
            for finding in top
        ],
    )


def govern_skills(
    skills_root: str | Path,
    out_dir: str | Path,
    threshold: int = 70,
    limit: int | None = None,
) -> Dict[str, Any]:
    out = Path(out_dir).expanduser().resolve()
    analyzer = SkillTrustAnalyzer()
    skill_dirs = discover_skill_dirs(skills_root)
    if limit is not None:
        skill_dirs = skill_dirs[:limit]

    records: List[SkillGovernanceRecord] = []
    for skill_dir in skill_dirs:
        name = _safe_name(skill_dir.name)
        report_dir = out / "skills" / name
        result = analyzer.analyze(skill_dir)
        write_outputs(report_dir, result)
        authoring = analyze_authoring(skill_dir)
        write_authoring_outputs(report_dir, authoring)
        token_analysis = analyze_token_efficiency(skill_dir)
        write_token_outputs(report_dir, token_analysis)
        _write_install_gate_artifacts(report_dir, result, threshold)
        _write_optimization_summary(report_dir, skill_dir, result, threshold, authoring, token_analysis)
        records.append(build_record(name, skill_dir, report_dir, result, threshold, authoring, token_analysis))

    taxonomy = analyze_taxonomy(skills_root)
    write_taxonomy_outputs(out, taxonomy)
    summary = build_governance_summary(skills_root, out, threshold, records, taxonomy)
    out.mkdir(parents=True, exist_ok=True)
    (out / "local_skills_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "local_skills_report.md").write_text(render_governance_report(summary), encoding="utf-8")
    return summary


def remediate_skill(
    skill_path: str | Path,
    out_dir: str | Path,
    threshold: int = 70,
) -> Dict[str, Any]:
    root = Path(skill_path).expanduser().resolve()
    out = Path(out_dir).expanduser().resolve()
    result = SkillTrustAnalyzer().analyze(root)
    write_outputs(out, result)
    authoring = analyze_authoring(root)
    write_authoring_outputs(out, authoring)
    token_analysis = analyze_token_efficiency(root)
    write_token_outputs(out, token_analysis)
    _write_install_gate_artifacts(out, result, threshold)
    _write_optimization_summary(out, root, result, threshold, authoring, token_analysis)

    payload = {
        "skill": root.name,
        "path": str(root),
        "report_dir": str(out),
        "install_decision": install_decision(result, threshold),
        "optimized_controls": optimized_controls(result),
        "score_before": result.score.trust_fit_score,
        "score_after_policy_overlay": projected_score_after_policy(result),
        "authoring_score": authoring["harness_fit_score"],
        "authoring_level": authoring["harness_level"],
        "authoring_actions": authoring_actions(authoring),
        "token_efficiency_score": token_analysis["token_efficiency_score"],
        "token_efficiency_level": token_analysis["token_efficiency_level"],
        "estimated_tokens_saved": token_analysis["metrics"]["estimated_tokens_saved"],
        "token_actions": token_actions(token_analysis),
        "mode": "policy-overlay",
        "note": (
            "SkillTrust does not edit source files by default. The generated policy overlay and remediation plan "
            "constrain the Skill to intent-bound permissions for review or installation."
        ),
    }
    (out / "remediation_bundle.json").write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return payload


def projected_score_after_policy(result: AnalysisResult) -> int:
    if result.score.risk_level == "Critical Risk":
        return min(84, max(result.score.trust_fit_score, 70))
    if result.score.risk_level in {"Overprivileged", "Needs Review"}:
        return min(89, max(result.score.trust_fit_score + 25, 70))
    return result.score.trust_fit_score


def build_governance_summary(
    skills_root: str | Path,
    out_dir: Path,
    threshold: int,
    records: Iterable[SkillGovernanceRecord],
    taxonomy: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    items = [record.to_dict() for record in records]
    counts = {
        "total": len(items),
        "allow": sum(1 for item in items if item["decision"] == "allow"),
        "warn": sum(1 for item in items if item["decision"] == "warn"),
        "block": sum(1 for item in items if item["decision"] == "block"),
        "remediation_bundles": len(items),
        "authoring_needs_split": sum(1 for item in items if item["authoring_level"] in {"Needs Split", "Monolithic"}),
        "token_heavy": sum(1 for item in items if item["token_level"] in {"Can Save Tokens", "Token Heavy"}),
        "estimated_tokens_saved": sum(item["estimated_tokens_saved"] for item in items),
        "taxonomy_findings": len(taxonomy["findings"]) if taxonomy else 0,
        "rename_plan_items": len(taxonomy["rename_plan"]) if taxonomy else 0,
    }
    return {
        "schema_version": "skilltrust.local_governance.v1",
        "skills_root": str(Path(skills_root).expanduser().resolve()),
        "out_dir": str(out_dir),
        "threshold": threshold,
        "counts": counts,
        "records": items,
        "taxonomy": taxonomy,
    }


def render_governance_report(summary: Dict[str, Any]) -> str:
    counts = summary["counts"]
    lines = [
        "# SkillTrust Local Skills Governance Report",
        "",
        f"Skills root: `{summary['skills_root']}`",
        f"Output directory: `{summary['out_dir']}`",
        f"Install threshold: {summary['threshold']}",
        "",
        "## Portfolio Summary",
        "",
        f"- Total Skills scanned: {counts['total']}",
        f"- Allow: {counts['allow']}",
        f"- Warn / policy overlay required: {counts['warn']}",
        f"- Block until remediation: {counts['block']}",
        f"- Remediation bundles generated: {counts['remediation_bundles']}",
        f"- Authoring needs split: {counts['authoring_needs_split']}",
        f"- Token-heavy Skills: {counts['token_heavy']}",
        f"- Estimated activation tokens saved: {counts['estimated_tokens_saved']}",
        f"- Taxonomy findings: {counts['taxonomy_findings']}",
        f"- Rename/description plan items: {counts['rename_plan_items']}",
        "",
        "## Skill Results",
        "",
        "| Skill | Score | Risk | Install Gate | Harness | Token | Saved | Findings | Report |",
        "| --- | ---: | --- | --- | --- | --- | ---: | ---: | --- |",
    ]
    for item in summary["records"]:
        lines.append(
            f"| `{item['name']}` | {item['score']} | {item['risk_level']} | {item['decision']} | "
            f"{item['authoring_score']} {item['authoring_level']} | "
            f"{item['token_score']} {item['token_level']} | {item['estimated_tokens_saved']} | "
            f"{item['findings_count']} | `{item['report_dir']}` |"
        )

    taxonomy = summary.get("taxonomy")
    if taxonomy:
        lines.extend(
            [
                "",
                "## Taxonomy / Skill Selection Accuracy",
                "",
                f"- Taxonomy Score: {taxonomy['taxonomy_score']}/100 ({taxonomy['taxonomy_level']})",
                f"- Findings: {len(taxonomy['findings'])}",
                f"- Rename/description plan items: {len(taxonomy['rename_plan'])}",
                "- Approval required before any rename or description edit.",
                "",
            ]
        )
        if taxonomy["findings"]:
            lines.append("| ID | Severity | Category | Skills | Recommendation |")
            lines.append("| --- | --- | --- | --- | --- |")
            for finding in taxonomy["findings"][:20]:
                lines.append(
                    f"| {finding['id']} | {finding['severity']} | {finding['category']} | "
                    f"`{finding['skills']}` | {finding['recommendation']} |"
                )

    lines.extend(["", "## Optimizations Applied As Policy Overlays", ""])
    for item in summary["records"]:
        lines.append(f"### {item['name']}")
        lines.append(f"- Decision: {item['decision']}")
        lines.append(f"- Score: {item['score']} ({item['risk_level']})")
        lines.append("- Controls:")
        for control in item["optimized_controls"]:
            lines.append(f"  - {control}")
        lines.append("- Authoring optimization:")
        for action in item["authoring_actions"]:
            lines.append(f"  - {action}")
        lines.append("- Token optimization:")
        for action in item["token_actions"]:
            lines.append(f"  - {action}")
        if item["top_findings"]:
            lines.append("- Top findings:")
            for finding in item["top_findings"]:
                lines.append(
                    f"  - `{finding['id']}` {finding['severity']} {finding['category']} "
                    f"at `{finding['location']}`: {finding['recommendation']}"
                )
        lines.append("")
    return "\n".join(lines) + "\n"


def _write_install_gate_artifacts(out_dir: Path, result: AnalysisResult, threshold: int) -> None:
    decision = install_decision(result, threshold)
    (out_dir / "install_decision.json").write_text(
        json.dumps(decision, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def _write_optimization_summary(
    out_dir: Path,
    skill_dir: Path,
    result: AnalysisResult,
    threshold: int,
    authoring: Dict[str, Any] | None = None,
    token_analysis: Dict[str, Any] | None = None,
) -> None:
    decision = install_decision(result, threshold)
    controls = optimized_controls(result)
    lines = [
        "# SkillTrust Optimization Summary",
        "",
        f"Skill: `{skill_dir.name}`",
        f"Path: `{skill_dir}`",
        f"Install decision: `{decision['action']}`",
        f"Trust Fit Score: {result.score.trust_fit_score}/100 ({result.score.risk_level})",
        f"Projected score with policy overlay: {projected_score_after_policy(result)}/100",
        (
            f"Harness Fit Score: {authoring['harness_fit_score']}/100 ({authoring['harness_level']})"
            if authoring
            else "Harness Fit Score: not evaluated"
        ),
        (
            f"Token Efficiency Score: {token_analysis['token_efficiency_score']}/100 "
            f"({token_analysis['token_efficiency_level']})"
            if token_analysis
            else "Token Efficiency Score: not evaluated"
        ),
        "",
        "## What SkillTrust Optimized",
        "",
    ]
    for control in controls:
        lines.append(f"- {control}")
    lines.extend(
        [
            "",
            "## Authoring Optimization",
            "",
        ]
    )
    if authoring:
        for action in authoring_actions(authoring):
            lines.append(f"- {action}")
    else:
        lines.append("- Not evaluated.")
    lines.extend(["", "## Token Optimization", ""])
    if token_analysis:
        for action in token_actions(token_analysis):
            lines.append(f"- {action}")
        lines.append(f"- Estimated activation tokens saved: {token_analysis['metrics']['estimated_tokens_saved']}")
    else:
        lines.append("- Not evaluated.")
    lines.extend(
        [
            "",
            "## Generated Governance Files",
            "",
            "- `permission_manifest.json`",
            "- `skilltrust-policy.json`",
            "- `trust_report.md`",
            "- `audit_receipt.json`",
            "- `remediation_plan.md`",
            "- `install_decision.json`",
            "- `authoring_report.md`",
            "- `optimized_SKILL.md`",
            "- `reference_extraction_plan.json`",
            "- `token_efficiency_report.md`",
            "- `token_optimization_plan.json`",
            "",
            "Source files were not changed. This bundle is a reviewable permission overlay for install-time enforcement.",
        ]
    )
    (out_dir / "optimization_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _safe_name(name: str) -> str:
    cleaned = "".join(char if char.isalnum() or char in "-_." else "-" for char in name.strip())
    return cleaned or "skill"
