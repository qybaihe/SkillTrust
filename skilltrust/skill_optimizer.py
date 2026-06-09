from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .analyzer import SkillTrustAnalyzer
from .authoring import analyze_authoring
from .governance import (
    authoring_actions,
    install_decision,
    token_actions,
)
from .taxonomy import analyze_taxonomy
from .token_optimizer import analyze_token_efficiency


SKILL_DESIGN_GUIDES: List[Dict[str, str]] = [
    {
        "id": "G-001",
        "dimension": "token_efficiency",
        "title": "Compact activation harness",
        "rule": (
            "Keep SKILL.md focused on trigger, scope, safety boundary, core workflow, and reference navigation. "
            "Move long examples, detailed variants, and domain background into lazily loaded references."
        ),
        "ai_optimization_hint": (
            "Rewrite the entry harness so the Agent can decide when to use the Skill without loading every detail."
        ),
    },
    {
        "id": "G-002",
        "dimension": "execution_efficiency",
        "title": "Code deterministic work",
        "rule": (
            "Convert deterministic parsing, validation, rendering, exporting, routing, and repeated command sequences "
            "into scripts, schemas, or config instead of asking the model to simulate them in prose."
        ),
        "ai_optimization_hint": (
            "Look for checklist-like or procedure-heavy sections and propose a helper script or JSON Schema."
        ),
    },
    {
        "id": "G-003",
        "dimension": "selection_accuracy",
        "title": "Trigger-precise metadata",
        "rule": (
            "Use a short, domain-specific name and a description that says when to use the Skill, what inputs it expects, "
            "and which neighboring tasks are out of scope."
        ),
        "ai_optimization_hint": (
            "Tighten frontmatter and the first heading so similar Skills do not compete for the same user request."
        ),
    },
    {
        "id": "G-004",
        "dimension": "permission_governance",
        "title": "Least-privilege policy overlay",
        "rule": (
            "State required filesystem, network, shell, environment, connector, and dependency permissions explicitly. "
            "Deny sensitive paths, secrets, credential stores, and unrelated network sinks by default."
        ),
        "ai_optimization_hint": (
            "Generate a reviewable policy overlay and keep unsafe behavior behind a confirmation or deny gate."
        ),
    },
    {
        "id": "G-005",
        "dimension": "selection_accuracy",
        "title": "Reference navigation over reference dumping",
        "rule": (
            "Every reference should be directly linked from SKILL.md with a read-when-needed condition. "
            "Avoid nested reference mazes that force the Agent to search blindly."
        ),
        "ai_optimization_hint": (
            "Add a small reference map and remove irrelevant context from the activation path."
        ),
    },
    {
        "id": "G-006",
        "dimension": "execution_efficiency",
        "title": "Machine-checkable outputs",
        "rule": (
            "When outputs have required fields or structure, express the contract as JSON Schema, typed config, "
            "or a validator script so errors are caught deterministically."
        ),
        "ai_optimization_hint": (
            "Replace format prose with a schema plus one validation command that emits concise errors."
        ),
    },
]


def analyze_skill_optimization(skill_path: str | Path, threshold: int = 70) -> Dict[str, Any]:
    root = Path(skill_path).expanduser().resolve()
    skill_file = root / "SKILL.md" if root.is_dir() else root
    if not skill_file.exists():
        raise FileNotFoundError(f"SKILL.md not found: {skill_file}")

    skill_dir = skill_file.parent
    deterministic = SkillTrustAnalyzer().analyze(skill_dir)
    authoring = analyze_authoring(skill_dir)
    token = analyze_token_efficiency(skill_dir)
    taxonomy = _single_skill_taxonomy(skill_dir)

    dimensions = {
        "token_efficiency": _token_dimension(token),
        "execution_efficiency": _execution_dimension(authoring, token, deterministic.to_dict()),
        "selection_accuracy": _selection_dimension(authoring, taxonomy, deterministic.to_dict()),
        "permission_governance": _permission_dimension(deterministic.to_dict(), threshold),
    }
    actions = _optimization_actions(authoring, token, taxonomy, deterministic.to_dict(), threshold)
    current_score = _average_dimension_score(dimensions)
    projected_score = min(100, current_score + _projected_lift(actions))

    current_decision = install_decision(deterministic, threshold=threshold)
    projected_action = current_decision["action"]
    if not deterministic.findings and projected_score >= threshold and deterministic.score.risk_level != "Critical Risk":
        projected_action = "allow"

    plan = {
        "schema_version": "skilltrust.skill_optimization.v1",
        "skill_path": str(skill_dir),
        "skill_file": str(skill_file),
        "product_goal": (
            "Upload one AI Skill and produce an optimized preview Skill that is more intent-bound, "
            "token-efficient, execution-efficient, and selection-accurate."
        ),
        "target_outcomes": [
            "reduce activation tokens without removing necessary safety boundaries",
            "improve execution efficiency by moving deterministic work into code, schemas, or config",
            "improve Agent selection accuracy through clearer names, descriptions, triggers, and boundaries",
            "preserve deterministic permission evidence and least-privilege policy controls",
        ],
        "current_install_decision": current_decision,
        "projected_install_decision": {
            "action": projected_action,
            "score": projected_score,
            "note": (
                "Projected score assumes the preview package applies the generated policy overlay and optimization plan. "
                "Critical data-flow evidence remains block-level until removed or gated."
            ),
        },
        "deterministic_analysis": deterministic.to_dict(),
        "authoring_analysis": authoring,
        "token_efficiency_analysis": token,
        "taxonomy_analysis": taxonomy,
        "dimensions": dimensions,
        "optimization_score": current_score,
        "projected_optimization_score": projected_score,
        "optimization_actions": actions,
        "skill_design_guides": SKILL_DESIGN_GUIDES,
        "optimized_skill_package_blueprint": _package_blueprint(authoring, deterministic.to_dict(), token, actions),
        "agent_assist_prompt": _agent_assist_prompt(),
    }
    return plan


def write_skill_optimization_outputs(out_dir: str | Path, plan: Dict[str, Any]) -> None:
    out = Path(out_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "skill_optimization_plan.json").write_text(
        json.dumps(plan, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "skill_optimization_report.md").write_text(render_skill_optimization_report(plan), encoding="utf-8")
    (out / "optimized_SKILL.md").write_text(
        plan["authoring_analysis"]["optimized_skill_md_draft"], encoding="utf-8"
    )
    (out / "skill_design_guidelines.md").write_text(render_skill_design_guidelines(plan), encoding="utf-8")


def render_skill_optimization_report(plan: Dict[str, Any]) -> str:
    metrics = plan["token_efficiency_analysis"]["metrics"]
    dimensions = plan["dimensions"]
    lines = [
        "# SkillTrust Skill Optimization Report",
        "",
        f"Skill: `{plan['skill_path']}`",
        "",
        "## Product Goal",
        "",
        plan["product_goal"],
        "",
        "## Optimization Score",
        "",
        f"- Current optimization score: {plan['optimization_score']}/100",
        f"- Projected optimization score: {plan['projected_optimization_score']}/100",
        f"- Current install action: `{plan['current_install_decision']['action']}`",
        f"- Projected install action: `{plan['projected_install_decision']['action']}`",
        "",
        "## Outcome Dimensions",
        "",
        "| Dimension | Score | Level | Summary |",
        "| --- | ---: | --- | --- |",
    ]
    for key in ["token_efficiency", "execution_efficiency", "selection_accuracy", "permission_governance"]:
        item = dimensions[key]
        lines.append(f"| {key} | {item['score']} | {item['level']} | {item['summary']} |")

    lines.extend(
        [
            "",
            "## Token Savings",
            "",
            f"- Current activation body tokens: {metrics['activation_body_tokens_estimate']}",
            f"- Projected activation body tokens: {metrics['projected_activation_tokens']}",
            f"- Estimated activation tokens saved: {metrics['estimated_tokens_saved']}",
            f"- Scriptification candidates: {metrics['scriptification_candidates']}",
            "",
            "## Optimization Actions",
            "",
        ]
    )
    if plan["optimization_actions"]:
        lines.append("| Priority | Dimension | Action | Expected Benefit | Implementation |")
        lines.append("| ---: | --- | --- | --- | --- |")
        for action in plan["optimization_actions"]:
            lines.append(
                f"| {action['priority']} | {action['dimension']} | {action['title']} | "
                f"{action['expected_benefit']} | {action['implementation']} |"
            )
    else:
        lines.append("- No material optimization actions detected.")

    lines.extend(
        [
            "",
            "## Optimized Preview Package Blueprint",
            "",
        ]
    )
    for item in plan["optimized_skill_package_blueprint"]["files"]:
        lines.append(f"- `{item['path']}`: {item['purpose']}")

    lines.extend(
        [
            "",
            "## Agent Assist Prompt",
            "",
            "```text",
            plan["agent_assist_prompt"],
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def render_skill_design_guidelines(plan: Dict[str, Any]) -> str:
    lines = [
        "# SkillTrust Skill Design Guidelines",
        "",
        "Use these guidelines when a host Agent or AI reviewer converts an uploaded Skill into an optimized preview package.",
        "",
    ]
    for guide in plan["skill_design_guides"]:
        lines.extend(
            [
                f"## {guide['id']} - {guide['title']}",
                "",
                f"- Dimension: `{guide['dimension']}`",
                f"- Rule: {guide['rule']}",
                f"- AI optimization hint: {guide['ai_optimization_hint']}",
                "",
            ]
        )
    return "\n".join(lines)


def _single_skill_taxonomy(skill_dir: Path) -> Dict[str, Any]:
    try:
        return analyze_taxonomy(skill_dir)
    except Exception as exc:  # pragma: no cover - defensive fallback for unusual package shapes
        return {
            "schema_version": "skilltrust.taxonomy.v1",
            "skills_root": str(skill_dir),
            "skill_count": 1,
            "taxonomy_score": 70,
            "taxonomy_level": "Unknown",
            "skills": [],
            "findings": [
                {
                    "id": "TX-FALLBACK",
                    "severity": "low",
                    "category": "taxonomy-unavailable",
                    "skills": skill_dir.name,
                    "recommendation": f"Could not run taxonomy analysis: {exc}",
                }
            ],
            "rename_plan": [],
            "approval_required": True,
        }


def _token_dimension(token: Dict[str, Any]) -> Dict[str, Any]:
    metrics = token["metrics"]
    return {
        "score": token["token_efficiency_score"],
        "level": token["token_efficiency_level"],
        "summary": (
            f"~{metrics['activation_body_tokens_estimate']} activation tokens now; "
            f"{metrics['estimated_tokens_saved']} estimated tokens can be saved."
        ),
        "evidence": {
            "activation_body_tokens_estimate": metrics["activation_body_tokens_estimate"],
            "projected_activation_tokens": metrics["projected_activation_tokens"],
            "estimated_tokens_saved": metrics["estimated_tokens_saved"],
            "scriptification_candidates": metrics["scriptification_candidates"],
        },
        "guides": _guide_ids("token_efficiency"),
    }


def _execution_dimension(
    authoring: Dict[str, Any],
    token: Dict[str, Any],
    deterministic: Dict[str, Any],
) -> Dict[str, Any]:
    script_candidates = [
        item
        for item in token["scriptification_candidates"]
        if item["kind"]
        in {
            "validator-script",
            "command-wrapper",
            "routing-config",
            "schema-config",
            "deterministic-transform-script",
        }
    ]
    observed_count = len(deterministic["observed_permissions"])
    penalty = min(40, len(script_candidates) * 8)
    penalty += min(20, max(0, authoring["metrics"]["body_lines"] - 180) // 15)
    penalty += min(15, observed_count // 4)
    score = max(0, 100 - penalty)
    return {
        "score": score,
        "level": _level(score, "Execution Lean", "Efficient", "Needs Automation", "Manual Heavy"),
        "summary": (
            f"{len(script_candidates)} deterministic sections can become scripts, schemas, or config; "
            f"{observed_count} observed permission surfaces should stay policy-gated."
        ),
        "evidence": {
            "script_or_schema_candidates": len(script_candidates),
            "body_lines": authoring["metrics"]["body_lines"],
            "observed_permission_surfaces": observed_count,
        },
        "guides": _guide_ids("execution_efficiency"),
    }


def _selection_dimension(
    authoring: Dict[str, Any],
    taxonomy: Dict[str, Any],
    deterministic: Dict[str, Any],
) -> Dict[str, Any]:
    score = min(
        100,
        max(
            0,
            round(
                (
                    authoring["harness_fit_score"]
                    + taxonomy.get("taxonomy_score", 70)
                    + deterministic["declared_intent"]["clarity_score"]
                )
                / 3
            ),
        ),
    )
    metadata = authoring.get("metadata", {})
    missing = [key for key in ["name", "description"] if not metadata.get(key)]
    return {
        "score": score,
        "level": _level(score, "Selection Precise", "Clear", "Ambiguous", "Hard To Route"),
        "summary": (
            f"Intent clarity is {deterministic['declared_intent']['clarity_score']}/100; "
            f"taxonomy findings: {len(taxonomy.get('findings', []))}; missing metadata: {', '.join(missing) or 'none'}."
        ),
        "evidence": {
            "intent_clarity_score": deterministic["declared_intent"]["clarity_score"],
            "harness_fit_score": authoring["harness_fit_score"],
            "taxonomy_score": taxonomy.get("taxonomy_score", 70),
            "missing_metadata": missing,
        },
        "guides": _guide_ids("selection_accuracy"),
    }


def _permission_dimension(deterministic: Dict[str, Any], threshold: int) -> Dict[str, Any]:
    score = deterministic["score"]["trust_fit_score"]
    return {
        "score": score,
        "level": deterministic["score"]["risk_level"],
        "summary": (
            f"Install gate is `{install_decision_from_dict(deterministic, threshold)['action']}` with "
            f"{len(deterministic['findings'])} deterministic findings."
        ),
        "evidence": {
            "trust_fit_score": score,
            "risk_level": deterministic["score"]["risk_level"],
            "findings_count": len(deterministic["findings"]),
            "observed_permissions": len(deterministic["observed_permissions"]),
        },
        "guides": _guide_ids("permission_governance"),
    }


def install_decision_from_dict(deterministic: Dict[str, Any], threshold: int) -> Dict[str, Any]:
    risk_level = deterministic["score"]["risk_level"]
    score = deterministic["score"]["trust_fit_score"]
    if risk_level == "Critical Risk":
        action = "block"
    elif score < threshold or risk_level in {"Needs Review", "Overprivileged"}:
        action = "warn"
    else:
        action = "allow"
    return {"action": action, "score": score, "threshold": threshold, "risk_level": risk_level}


def _optimization_actions(
    authoring: Dict[str, Any],
    token: Dict[str, Any],
    taxonomy: Dict[str, Any],
    deterministic: Dict[str, Any],
    threshold: int,
) -> List[Dict[str, Any]]:
    actions: List[Dict[str, Any]] = []
    priority = 1

    def add(
        dimension: str,
        title: str,
        expected_benefit: str,
        implementation: str,
        evidence: str,
        guide_ids: Iterable[str],
    ) -> None:
        nonlocal priority
        actions.append(
            {
                "priority": priority,
                "dimension": dimension,
                "title": title,
                "expected_benefit": expected_benefit,
                "implementation": implementation,
                "evidence": evidence,
                "guide_ids": list(guide_ids),
            }
        )
        priority += 1

    for item in token_actions(token):
        add(
            "token_efficiency",
            item,
            "lower activation-token load and cheaper repeated invocations",
            "Apply the scriptification/reference-deferral candidates from token_optimization_plan.json.",
            f"{token['metrics']['estimated_tokens_saved']} estimated tokens saved.",
            _guide_ids("token_efficiency"),
        )

    for item in authoring_actions(authoring):
        add(
            "selection_accuracy",
            item,
            "clearer Agent routing and less irrelevant context at activation time",
            "Use optimized_SKILL.md as the compact harness draft and review reference_extraction_plan.json.",
            f"Harness score {authoring['harness_fit_score']}/100 with {authoring['metrics']['move_candidate_sections']} move candidates.",
            _guide_ids("selection_accuracy"),
        )

    deterministic_candidate_count = sum(
        1
        for item in token["scriptification_candidates"]
        if item["kind"]
        in {
            "validator-script",
            "command-wrapper",
            "schema-config",
            "routing-config",
            "deterministic-transform-script",
        }
    )
    if deterministic_candidate_count:
        add(
            "execution_efficiency",
            "Turn deterministic prose into helper scripts, schemas, or config.",
            "faster execution, fewer model decisions, and more reproducible outputs",
            "Create the proposed artifacts listed in token_optimization_plan.json and call them from the compact harness.",
            f"{deterministic_candidate_count} script/schema/config candidates found.",
            _guide_ids("execution_efficiency"),
        )

    if taxonomy.get("findings") or taxonomy.get("rename_plan"):
        add(
            "selection_accuracy",
            "Tighten Skill name, description, and trigger boundaries.",
            "higher selection precision when multiple Skills could match the same user request",
            "Apply rename_approval_plan.md only after user approval; otherwise update description wording in the preview package.",
            f"{len(taxonomy.get('findings', []))} taxonomy findings and {len(taxonomy.get('rename_plan', []))} plan items.",
            _guide_ids("selection_accuracy"),
        )

    if deterministic["findings"] or install_decision_from_dict(deterministic, threshold)["action"] != "allow":
        add(
            "permission_governance",
            "Preserve least-privilege policy gates in the optimized package.",
            "safer install path without hiding deterministic evidence",
            "Include skilltrust/permission_manifest.json and skilltrust/skilltrust-policy.json in the preview package.",
            f"{len(deterministic['findings'])} findings; projected policy score {projected_score_from_dict(deterministic)}.",
            _guide_ids("permission_governance"),
        )

    return _dedupe_actions(actions)


def projected_score_from_dict(deterministic: Dict[str, Any]) -> int:
    risk_level = deterministic["score"]["risk_level"]
    score = deterministic["score"]["trust_fit_score"]
    if risk_level == "Critical Risk":
        return min(84, max(score, 70))
    if risk_level in {"Overprivileged", "Needs Review"}:
        return min(89, max(score + 25, 70))
    return score


def _package_blueprint(
    authoring: Dict[str, Any],
    deterministic: Dict[str, Any],
    token: Dict[str, Any],
    actions: List[Dict[str, Any]],
) -> Dict[str, Any]:
    return {
        "package_name": "optimized-skill.zip",
        "mode": "preview-only",
        "does_not_auto_install": True,
        "files": [
            {
                "path": "SKILL.md",
                "purpose": "compact optimized harness draft generated from authoring analysis",
            },
            {
                "path": "skilltrust/permission_manifest.json",
                "purpose": "least-privilege permission contract inferred from declared intent",
            },
            {
                "path": "skilltrust/skilltrust-policy.json",
                "purpose": "runtime policy overlay for filesystem, network, shell, environment, dependency, and prompt gates",
            },
            {
                "path": "skilltrust/optimization_summary.md",
                "purpose": "human review summary covering token savings, execution efficiency, selection accuracy, and policy changes",
            },
            {
                "path": "skilltrust/skill_optimization_plan.json",
                "purpose": "machine-readable optimization plan for an Agent or CI gate",
            },
        ],
        "draft_skill_md": authoring["optimized_skill_md_draft"],
        "permission_manifest": deterministic["permission_manifest"],
        "policy_overlay": deterministic["policy"],
        "estimated_tokens_saved": token["metrics"]["estimated_tokens_saved"],
        "actions_count": len(actions),
    }


def _agent_assist_prompt() -> str:
    return (
        "Use SkillTrust to optimize this uploaded Skill into a preview package. "
        "Read skill_optimization_plan.json, skill_design_guidelines.md, permission_manifest.json, "
        "and skilltrust-policy.json. Preserve deterministic findings and do not claim unsafe findings are removed "
        "unless the source behavior is actually removed or policy-gated. Optimize for three measurable outcomes: "
        "fewer activation tokens, more deterministic execution through code/schema/config, and clearer Agent selection. "
        "Generate only a reviewable preview package; do not install it automatically."
    )


def _guide_ids(dimension: str) -> List[str]:
    return [guide["id"] for guide in SKILL_DESIGN_GUIDES if guide["dimension"] == dimension]


def _average_dimension_score(dimensions: Dict[str, Dict[str, Any]]) -> int:
    return round(sum(item["score"] for item in dimensions.values()) / max(1, len(dimensions)))


def _projected_lift(actions: List[Dict[str, Any]]) -> int:
    dimensions = {action["dimension"] for action in actions}
    return min(24, len(actions) * 3 + len(dimensions) * 2)


def _level(score: int, high: str, good: str, mid: str, low: str) -> str:
    if score >= 90:
        return high
    if score >= 75:
        return good
    if score >= 50:
        return mid
    return low


def _dedupe_actions(actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    result = []
    for action in actions:
        key = (action["dimension"], action["title"])
        if key in seen:
            continue
        seen.add(key)
        action["priority"] = len(result) + 1
        result.append(action)
    return result
