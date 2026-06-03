from __future__ import annotations

import json
import hashlib
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, Iterable, List

from .analyzer import SkillTrustAnalyzer
from .models import RULES_VERSION
from .reporting import write_outputs


SEMANTIC_REVIEW_SCHEMA_VERSION = "skilltrust.agent_semantic_review.v1"
SEMANTIC_REQUEST_SCHEMA_VERSION = "skilltrust.semantic_review_request.v1"
FUSED_SCHEMA_VERSION = "skilltrust.fused_analysis.v1"
CORE_DOCUMENT_NAMES = {"SKILL.md", "README.md", "README"}

ACTION_RANK = {"allow": 0, "warn": 1, "block": 2}
RANK_ACTION = {value: key for key, value in ACTION_RANK.items()}


def write_review_request(skill_path: str | Path, out_dir: str | Path) -> Dict[str, Any]:
    result = SkillTrustAnalyzer().analyze(skill_path)
    out = Path(out_dir).expanduser().resolve()
    write_outputs(out, result)
    request = build_review_request(result.to_dict())
    out.mkdir(parents=True, exist_ok=True)
    (out / "semantic_review_request.json").write_text(
        json.dumps(request, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "semantic_review_instructions.md").write_text(render_review_instructions(request), encoding="utf-8")
    return request


def build_review_request(analysis: Dict[str, Any]) -> Dict[str, Any]:
    findings = analysis.get("findings", [])
    observed = analysis.get("observed_permissions", [])
    core_documents = core_documents_to_read(analysis["input_path"])
    return {
        "schema_version": SEMANTIC_REQUEST_SCHEMA_VERSION,
        "target_path": analysis["input_path"],
        "rules_version": analysis.get("rules_version", RULES_VERSION),
        "agent_review_protocol": [
            "First read each core document in `core_documents_to_read` end-to-end before judging individual findings or score.",
            "Treat deterministic findings as evidence leads with line numbers and hashes, not as the final semantic judgment.",
            "Summarize the declared task boundary from the full documents, not only from finding snippets or keyword matches.",
            "Then reconcile every deterministic finding against that task boundary and the generated least-privilege policy.",
            "Dynamically assess whether the package is under-specified, over-specified, too long, too short, or should split references; do not rely on fixed thresholds alone.",
            "Record the documents read in `full_document_reading.documents_read` in semantic_review.json.",
        ],
        "deterministic_evidence_role": {
            "role": "evidence_pack_not_final_judge",
            "use_for": [
                "line-numbered evidence",
                "hash-backed reproducibility",
                "permission surface discovery",
                "sensitive data-flow leads",
                "initial policy draft",
            ],
            "limitations": [
                "keyword or pattern matches can overstate risk without intent context",
                "length and token thresholds are triage signals, not final quality judgments",
                "only host-Agent full-document reading can decide necessity against declared intent",
            ],
        },
        "dynamic_semantic_judgment_rules": {
            "too_short_signals": [
                "unclear trigger purpose",
                "missing input or output contract",
                "missing permission boundary",
                "missing safety or consent assumptions",
                "insufficient workflow detail for reliable activation",
            ],
            "too_long_signals": [
                "large examples or style libraries loaded at activation",
                "schemas or validators embedded as prose",
                "repeated deterministic command sequences",
                "troubleshooting trees or reference material that should be deferred",
                "workflow variants that should live in references",
            ],
            "judgment_rule": (
                "Long is not automatically bad and short is not automatically good. Judge whether the Agent can "
                "activate, understand, and safely constrain the package without loading irrelevant context."
            ),
        },
        "core_documents_to_read": core_documents,
        "declared_intent": analysis.get("declared_intent", {}),
        "required_permissions": analysis.get("required_permissions", {}),
        "observed_permissions_summary": summarize_observed_permissions(observed),
        "deterministic_findings": findings,
        "base_score": analysis.get("score", {}),
        "generated_policy": analysis.get("policy", {}),
        "permission_manifest": analysis.get("permission_manifest", {}),
        "selected_evidence_snippets": selected_evidence_snippets(findings),
        "privacy_boundary": {
            "mode": "local-only-host-agent-review",
            "external_model_api": False,
            "api_key_required": False,
            "network_required": False,
            "instructions": [
                "Do not execute the target Skill.",
                "Do not access unrelated user directories, secrets, browser profiles, cloud credentials, or personal accounts.",
                "Use the deterministic evidence bundle plus target package SKILL.md/README/workflow files only.",
                "For real local Skills, avoid copying unnecessary personal data into semantic_review.json.",
            ],
        },
        "agent_questions": [
            "After reading the full core documents, what is the Skill's declared task boundary?",
            "Which permissions are task-critical, optional, or unjustified?",
            "For each deterministic finding, is the behavior necessary, acceptable with policy, overreach, likely false positive, or needs human review?",
            "Are any required permissions missing from the declared Skill boundary?",
            "Is the package under-specified, over-specified, too long, too short, or in need of reference splitting?",
            "What policy refinements would make the Skill installable with least privilege?",
            "What install recommendation should the semantic reviewer give: allow, warn, or block?",
            "Should the base score receive a small semantic overlay adjustment between -10 and +10, and why?",
        ],
        "output_schema": semantic_review_schema_template(
            analysis["input_path"], analysis.get("score", {}).get("trust_fit_score", 0), findings, core_documents
        ),
    }


def render_review_instructions(request: Dict[str, Any]) -> str:
    finding_ids = ", ".join(item["id"] for item in request.get("deterministic_findings", [])) or "none"
    core_docs = request.get("core_documents_to_read", [])
    doc_lines = "\n".join(
        f"- `{item['path']}` ({item['role']}, sha256 `{item['sha256']}`)" for item in core_docs
    ) or "- No core documents were found; use the deterministic evidence bundle only."
    return (
        "# SkillTrust Agent Semantic Review Instructions\n\n"
        "You are SkillTrust's host-Agent semantic permission reviewer.\n\n"
        "Do not call an external model API. Do not ask for an API key. You are already the host Agent.\n\n"
        "## Full-Document First Pass\n\n"
        "Before assessing individual findings, read every core document below end-to-end. Use this first pass to understand the Skill's declared task, workflow, boundaries, inputs, and outputs.\n\n"
        f"{doc_lines}\n\n"
        "Record this reading pass in `full_document_reading.documents_read` inside `semantic_review.json`.\n\n"
        "## Deterministic Evidence Role\n\n"
        "The deterministic scanner is an evidence pack, not the final semantic judge. Use its line numbers, hashes, and permission leads to focus review, but decide necessity only after understanding the full declared task boundary.\n\n"
        "Length, token, keyword, path, and dependency matches are triage signals. They can indicate risk, but they do not replace full-document understanding.\n\n"
        "## Review Boundary\n\n"
        "- Read `semantic_review_request.json`.\n"
        "- Read the full core documents listed above before using finding snippets.\n"
        "- You may inspect additional workflow docs and directly relevant package files when the core documents refer to them.\n"
        "- Do not execute the target Skill.\n"
        "- Do not access unrelated user secrets, SSH keys, browser profiles, cloud credentials, or personal accounts.\n"
        "- Do not delete or suppress deterministic findings.\n"
        "- For real local Skills, avoid copying unnecessary personal data into the review.\n\n"
        "## Required Output\n\n"
        "- Write JSON only.\n"
        "- File name: `semantic_review.json`.\n"
        "- Include `full_document_reading` to show which core documents were read and how they informed the boundary.\n"
        f"- Assess every deterministic finding ID: {finding_ids}.\n"
        "- Use schema version `skilltrust.agent_semantic_review.v1`.\n\n"
        "## Allowed Semantic Roles\n\n"
        "- Clarify task boundary.\n"
        "- Mark findings as `necessary`, `acceptable_with_policy`, `overreach`, `likely_false_positive`, or `needs_human_review`.\n"
        "- Recommend policy refinements.\n"
        "- Recommend install action: `allow`, `warn`, or `block`.\n"
        "- Suggest score overlay in the range -10 to +10.\n\n"
        "## Dynamic Authoring And Permission Calibration\n\n"
        "- Decide whether the package is too short, too long, under-specified, over-specified, or should split references.\n"
        "- Do not use a fixed length threshold as the final answer.\n"
        "- Judge whether the Agent can activate the package accurately, understand boundaries, and avoid loading irrelevant context.\n"
        "- For each permission, ask whether the declared task truly needs it, whether it can be narrowed, and whether user confirmation should be required.\n\n"
        "## Conservative Rules\n\n"
        "- Never remove deterministic evidence.\n"
        "- Do not turn critical data-flow evidence into allow.\n"
        "- If you suspect a false positive, mark it `likely_false_positive` or `needs_human_review`; do not delete it.\n\n"
        "## JSON Template\n\n"
        "```json\n"
        f"{json.dumps(request['output_schema'], indent=2, ensure_ascii=False)}\n"
        "```\n"
    )


def semantic_review_schema_template(
    target_path: str, base_score: int, findings: List[Dict[str, Any]], core_documents: List[Dict[str, Any]] | None = None
) -> Dict[str, Any]:
    return {
        "schema_version": SEMANTIC_REVIEW_SCHEMA_VERSION,
        "reviewer": "host-agent",
        "review_mode": "agent-in-the-loop",
        "target_path": target_path,
        "deterministic_evidence_interpretation": {
            "role": "evidence_pack_not_final_judge",
            "how_used": "",
            "limitations_considered": [],
        },
        "full_document_reading": {
            "required": True,
            "documents_read": [
                {
                    "path": item["path"],
                    "sha256": item["sha256"],
                    "read_scope": "full-document",
                    "boundary_notes": "",
                }
                for item in (core_documents or [])
            ],
            "summary": "",
            "uncertainties": [],
        },
        "declared_boundary_summary": "",
        "task_boundary": {
            "in_scope": [],
            "out_of_scope": [],
            "requires_user_confirmation": [],
        },
        "task_critical_permissions": [],
        "dynamic_authoring_assessment": {
            "too_short": False,
            "too_short_reason": "",
            "too_long": False,
            "too_long_reason": "",
            "under_specified": False,
            "over_specified": False,
            "reference_split_recommended": False,
            "script_or_config_extraction_recommended": False,
            "rationale": "",
        },
        "finding_assessments": [
            {
                "finding_id": finding["id"],
                "semantic_fit": "needs_human_review",
                "rationale": "",
                "recommended_policy_change": "",
                "confidence": "medium",
            }
            for finding in findings
        ],
        "missing_permission_declarations": [],
        "policy_refinements": [],
        "semantic_install_recommendation": {
            "action": "warn",
            "reason": "",
            "confidence": "medium",
        },
        "semantic_score_overlay": {
            "base_score": base_score,
            "adjustment": 0,
            "final_score": base_score,
            "reasons": [],
        },
        "privacy_notes": [],
    }


def core_documents_to_read(target_path: str | Path) -> List[Dict[str, Any]]:
    root = Path(target_path).expanduser().resolve()
    if root.is_file():
        candidates = [root] if root.name in CORE_DOCUMENT_NAMES else []
        base = root.parent
    else:
        candidates = [path for path in sorted(root.iterdir()) if path.is_file() and path.name in CORE_DOCUMENT_NAMES]
        base = root

    documents = []
    for path in candidates:
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        try:
            relpath = str(path.resolve().relative_to(base))
        except ValueError:
            relpath = str(path)
        documents.append(
            {
                "path": relpath,
                "absolute_path": str(path.resolve()),
                "role": "primary skill instructions" if path.name == "SKILL.md" else "supporting package readme",
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "read_required": True,
                "read_mode": "full-document-before-finding-review",
            }
        )
    return documents


def summarize_observed_permissions(observed: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    counts: Dict[str, int] = {}
    examples: Dict[str, List[Dict[str, Any]]] = {}
    for item in observed:
        category = item.get("category", "unknown")
        counts[category] = counts.get(category, 0) + 1
        examples.setdefault(category, [])
        if len(examples[category]) < 5:
            examples[category].append(
                {
                    "permission": item.get("permission"),
                    "file": item.get("file"),
                    "line": item.get("line"),
                    "evidence": item.get("evidence", "")[:220],
                    "relation": item.get("relation"),
                }
            )
    return {"counts": counts, "examples": examples}


def selected_evidence_snippets(findings: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    snippets = []
    for finding in findings:
        snippets.append(
            {
                "finding_id": finding["id"],
                "severity": finding["severity"],
                "category": finding["category"],
                "location": f"{finding['file']}:{finding['line']}",
                "evidence_summary": finding.get("evidence", "")[:260],
                "why_it_matters": finding.get("why_it_matters", ""),
                "policy_effect": finding.get("policy_effect", ""),
            }
        )
    return snippets


def draft_semantic_review(request_path: str | Path, out_path: str | Path) -> Dict[str, Any]:
    request = json.loads(Path(request_path).read_text(encoding="utf-8"))
    findings = request.get("deterministic_findings", [])
    base_score = int(request.get("base_score", {}).get("trust_fit_score", 0))
    has_critical_dataflow = any(item.get("category") == "data_flow" and item.get("severity") == "critical" for item in findings)
    has_overreach = bool(findings)
    action = "block" if has_critical_dataflow else "warn" if has_overreach else "allow"
    assessments = []
    for finding in findings:
        semantic_fit = "overreach"
        if finding.get("category") == "dependency" and finding.get("severity") in {"low", "info"}:
            semantic_fit = "acceptable_with_policy"
        assessments.append(
            {
                "finding_id": finding["id"],
                "semantic_fit": semantic_fit,
                "rationale": (
                    "Offline demo draft: this deterministic finding appears outside the declared task boundary."
                    if semantic_fit == "overreach"
                    else "Offline demo draft: acceptable if pinned and enforced by generated policy."
                ),
                "recommended_policy_change": finding.get("policy_effect", "Keep least-privilege policy enforcement."),
                "confidence": "medium",
            }
        )

    review = {
        "schema_version": SEMANTIC_REVIEW_SCHEMA_VERSION,
        "reviewer": "host-agent-demo-draft",
        "review_mode": "offline-draft-for-fusion-testing",
        "target_path": request["target_path"],
        "deterministic_evidence_interpretation": {
            "role": "evidence_pack_not_final_judge",
            "how_used": "Offline draft uses deterministic evidence as triage leads only.",
            "limitations_considered": [
                "A real host-Agent review must read full core documents before final semantic judgment.",
                "Length and keyword matches are not final authoring or permission decisions.",
            ],
        },
        "full_document_reading": {
            "required": True,
            "documents_read": [
                {
                    "path": item["path"],
                    "sha256": item["sha256"],
                    "read_scope": "listed-by-request",
                    "boundary_notes": (
                        "Offline demo draft records the required full-document pass; "
                        "host-Agent review should actually read this document end-to-end."
                    ),
                }
                for item in request.get("core_documents_to_read", [])
            ],
            "summary": (
                "Offline demo draft uses the generated review request. A real host-Agent review should read the full "
                "core documents before judging findings."
            ),
            "uncertainties": ["This draft is for fusion testing only."],
        },
        "declared_boundary_summary": request.get("declared_intent", {}).get("summary", ""),
        "task_boundary": {
            "in_scope": ["Declared workflow and user-provided inputs described by the Skill package."],
            "out_of_scope": ["Unrelated local secrets, hidden exfiltration sinks, and undeclared broad filesystem access."],
            "requires_user_confirmation": ["New network destinations", "file uploads", "access to personal profile paths"],
        },
        "task_critical_permissions": [],
        "dynamic_authoring_assessment": {
            "too_short": False,
            "too_short_reason": "",
            "too_long": False,
            "too_long_reason": "",
            "under_specified": False,
            "over_specified": bool(findings),
            "reference_split_recommended": False,
            "script_or_config_extraction_recommended": False,
            "rationale": "Offline draft does not perform full dynamic authoring review; host-Agent review should assess this after reading core documents.",
        },
        "finding_assessments": assessments,
        "missing_permission_declarations": [],
        "policy_refinements": [
            {
                "area": "filesystem",
                "change": "Keep sensitive local paths denied unless explicitly allowlisted by task and user confirmation.",
                "reason": "Offline demo draft keeps deterministic least-privilege constraints.",
            }
        ],
        "semantic_install_recommendation": {
            "action": action,
            "reason": "Offline demo draft based on deterministic evidence; not a substitute for host-Agent review.",
            "confidence": "medium",
        },
        "semantic_score_overlay": {
            "base_score": base_score,
            "adjustment": 0,
            "final_score": base_score,
            "reasons": ["Offline demo draft does not adjust deterministic score."],
        },
        "privacy_notes": ["Generated locally without API calls or network access."],
    }
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    Path(out_path).write_text(json.dumps(review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return review


def fuse_analysis(analysis_path: str | Path, semantic_review_path: str | Path, out_dir: str | Path) -> Dict[str, Any]:
    analysis = json.loads(Path(analysis_path).read_text(encoding="utf-8"))
    semantic = json.loads(Path(semantic_review_path).read_text(encoding="utf-8"))
    fused = build_fused_analysis(analysis, semantic)
    out = Path(out_dir).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)
    (out / "fused_analysis.json").write_text(json.dumps(fused, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / "fused_trust_report.md").write_text(render_fused_report(fused), encoding="utf-8")
    (out / "fused_install_decision.json").write_text(
        json.dumps(fused["fused_install_decision"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "skilltrust-policy.json").write_text(
        json.dumps(fused["fused_policy"], indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (out / "semantic_review_summary.md").write_text(render_semantic_summary(fused), encoding="utf-8")
    return fused


def build_fused_analysis(analysis: Dict[str, Any], semantic: Dict[str, Any]) -> Dict[str, Any]:
    validate_semantic_review(analysis, semantic)
    deterministic_action = deterministic_install_action(analysis)
    semantic_action = semantic.get("semantic_install_recommendation", {}).get("action", "warn")
    if semantic_action not in ACTION_RANK:
        semantic_action = "warn"

    critical_dataflow = has_critical_dataflow(analysis)
    final_action = fuse_action(deterministic_action, semantic_action, critical_dataflow)
    base_score = int(analysis.get("score", {}).get("trust_fit_score", 0))
    adjustment = clamp(int(semantic.get("semantic_score_overlay", {}).get("adjustment", 0)), -10, 10)
    if critical_dataflow and adjustment > 0:
        adjustment = 0
    final_score = clamp(base_score + adjustment, 0, 100)
    if critical_dataflow:
        final_score = min(final_score, 29)

    assessments = {item["finding_id"]: item for item in semantic.get("finding_assessments", [])}
    fused_findings = []
    for finding in analysis.get("findings", []):
        assessment = assessments.get(
            finding["id"],
            {
                "finding_id": finding["id"],
                "semantic_fit": "needs_human_review",
                "rationale": "No semantic assessment was provided for this deterministic finding.",
                "recommended_policy_change": finding.get("policy_effect", ""),
                "confidence": "low",
            },
        )
        display_priority = "normal"
        if assessment.get("semantic_fit") == "likely_false_positive":
            display_priority = "lowered_needs_human_review"
        if finding.get("category") == "data_flow" and finding.get("severity") == "critical":
            display_priority = "critical_protected"
        fused_findings.append({**finding, "semantic_assessment": assessment, "display_priority": display_priority})

    fused_policy = deepcopy(analysis.get("policy", {}))
    fused_policy["agent_semantic_refinements"] = semantic.get("policy_refinements", [])
    fused_policy["semantic_review_mode"] = semantic.get("review_mode", "agent-in-the-loop")

    return {
        "schema_version": FUSED_SCHEMA_VERSION,
        "analysis_path_input": analysis.get("input_path"),
        "semantic_review_schema_version": semantic.get("schema_version"),
        "deterministic_analysis": analysis,
        "semantic_review": semantic,
        "fused_findings": fused_findings,
        "fused_policy": fused_policy,
        "fused_install_decision": {
            "deterministic_action": deterministic_action,
            "semantic_recommendation": semantic_action,
            "final_action": final_action,
            "base_score": base_score,
            "semantic_adjustment": adjustment,
            "final_score": final_score,
            "critical_dataflow_protected": critical_dataflow,
            "conservative_reason": conservative_reason(deterministic_action, semantic_action, final_action, critical_dataflow),
        },
    }


def validate_semantic_review(analysis: Dict[str, Any], semantic: Dict[str, Any]) -> None:
    if semantic.get("schema_version") != SEMANTIC_REVIEW_SCHEMA_VERSION:
        raise ValueError("semantic_review.json has an unsupported schema_version")
    expected_ids = {finding["id"] for finding in analysis.get("findings", [])}
    provided_ids = {item.get("finding_id") for item in semantic.get("finding_assessments", [])}
    missing = expected_ids - provided_ids
    if missing:
        raise ValueError(f"semantic_review.json is missing finding assessments: {', '.join(sorted(missing))}")


def deterministic_install_action(analysis: Dict[str, Any]) -> str:
    risk = analysis.get("score", {}).get("risk_level", "")
    score = int(analysis.get("score", {}).get("trust_fit_score", 0))
    if risk == "Critical Risk":
        return "block"
    if risk in {"Needs Review", "Overprivileged"} or score < 70:
        return "warn"
    return "allow"


def has_critical_dataflow(analysis: Dict[str, Any]) -> bool:
    return any(
        finding.get("category") == "data_flow" and finding.get("severity") == "critical"
        for finding in analysis.get("findings", [])
    )


def fuse_action(deterministic_action: str, semantic_action: str, critical_dataflow: bool) -> str:
    if critical_dataflow:
        return "block"
    if deterministic_action == "block" and semantic_action == "allow":
        return "warn"
    return RANK_ACTION[max(ACTION_RANK.get(deterministic_action, 1), ACTION_RANK.get(semantic_action, 1))]


def conservative_reason(deterministic_action: str, semantic_action: str, final_action: str, critical_dataflow: bool) -> str:
    if critical_dataflow:
        return "Critical sensitive-source-to-sink evidence is protected and cannot be upgraded by semantic review."
    if deterministic_action == "block" and semantic_action == "allow":
        return "Deterministic block conflicted with semantic allow, so SkillTrust conservatively kept at least warn."
    if ACTION_RANK.get(final_action, 1) >= max(ACTION_RANK.get(deterministic_action, 1), ACTION_RANK.get(semantic_action, 1)):
        return "Final decision keeps the more conservative deterministic or semantic recommendation."
    return "Final decision was conservatively fused from deterministic evidence and semantic review."


def render_fused_report(fused: Dict[str, Any]) -> str:
    decision = fused["fused_install_decision"]
    semantic = fused["semantic_review"]
    lines = [
        "# SkillTrust Fused Trust Report",
        "",
        f"Target: `{fused['analysis_path_input']}`",
        "",
        "## Fused Install Decision",
        "",
        f"- Deterministic action: `{decision['deterministic_action']}`",
        f"- Semantic recommendation: `{decision['semantic_recommendation']}`",
        f"- Final fused action: `{decision['final_action']}`",
        f"- Score before: {decision['base_score']}",
        f"- Semantic adjustment: {decision['semantic_adjustment']}",
        f"- Score after: {decision['final_score']}",
        f"- Conservative reason: {decision['conservative_reason']}",
        "",
        "## Agent Semantic Review",
        "",
        f"- Reviewer: {semantic.get('reviewer')}",
        f"- Review mode: {semantic.get('review_mode')}",
        f"- Declared boundary summary: {semantic.get('declared_boundary_summary', '')}",
        "",
        "## Full Document Reading",
        "",
        f"- Required: `{semantic.get('full_document_reading', {}).get('required', True)}`",
        f"- Summary: {semantic.get('full_document_reading', {}).get('summary', '')}",
    ]
    documents_read = semantic.get("full_document_reading", {}).get("documents_read", [])
    if documents_read:
        for item in documents_read:
            lines.append(
                f"- `{item.get('path')}`: {item.get('read_scope', 'full-document')} "
                f"(sha256 `{item.get('sha256', '')}`)"
            )
    else:
        lines.append("- No full-document reading records were provided.")
    for item in semantic.get("full_document_reading", {}).get("uncertainties", []):
        lines.append(f"- Uncertainty: {item}")
    lines.extend(
        [
            "",
            "## Task Boundary",
            "",
        ]
    )
    boundary = semantic.get("task_boundary", {})
    lines.extend(render_list("In scope", boundary.get("in_scope", [])))
    lines.extend(render_list("Out of scope", boundary.get("out_of_scope", [])))
    lines.extend(render_list("Requires user confirmation", boundary.get("requires_user_confirmation", [])))

    lines.extend(["", "## Finding Semantic Assessment", ""])
    lines.append("| Finding | Severity | Category | Semantic Fit | Priority | Rationale |")
    lines.append("| --- | --- | --- | --- | --- | --- |")
    for finding in fused.get("fused_findings", []):
        assessment = finding["semantic_assessment"]
        rationale = assessment.get("rationale", "").replace("\n", " ")[:140]
        lines.append(
            f"| {finding['id']} | {finding['severity']} | {finding['category']} | "
            f"{assessment.get('semantic_fit')} | {finding['display_priority']} | {rationale} |"
        )

    lines.extend(["", "## Missing Permission Declarations", ""])
    missing = semantic.get("missing_permission_declarations", [])
    if missing:
        for item in missing:
            lines.append(f"- `{item.get('category')}` `{item.get('scope')}`: {item.get('recommended_declaration')}")
    else:
        lines.append("- None declared by semantic reviewer.")

    lines.extend(["", "## Policy Refinements", ""])
    refinements = semantic.get("policy_refinements", [])
    if refinements:
        for item in refinements:
            lines.append(f"- `{item.get('area')}`: {item.get('change')} ({item.get('reason')})")
    else:
        lines.append("- None declared by semantic reviewer.")

    lines.extend(["", "## Evidence Preservation", ""])
    lines.append("- Deterministic findings are preserved in `fused_analysis.json` and cannot be deleted by semantic review.")
    lines.append("- `likely_false_positive` assessments lower display priority only; they do not remove evidence.")
    return "\n".join(lines) + "\n"


def render_semantic_summary(fused: Dict[str, Any]) -> str:
    decision = fused["fused_install_decision"]
    return (
        "# SkillTrust Semantic Review Summary\n\n"
        f"- Deterministic action: `{decision['deterministic_action']}`\n"
        f"- Semantic recommendation: `{decision['semantic_recommendation']}`\n"
        f"- Final fused action: `{decision['final_action']}`\n"
        f"- Final score: {decision['final_score']}\n"
        f"- Reason: {decision['conservative_reason']}\n"
    )


def render_list(title: str, items: List[str]) -> List[str]:
    lines = [f"### {title}", ""]
    if not items:
        lines.append("- None specified.")
    else:
        for item in items:
            lines.append(f"- {item}")
    lines.append("")
    return lines


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))
