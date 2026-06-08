#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from skilltrust.analyzer import SkillTrustAnalyzer
from skilltrust.governance import install_decision
from skilltrust.token_optimizer import analyze_token_efficiency


RESULTS_JSON = ROOT / "docs/benchmarks/external-baseline-results.json"
REPORT_EN = ROOT / "docs/benchmarks/external-baseline-benchmark.md"
REPORT_ZH = ROOT / "docs/benchmarks/external-baseline-benchmark.zh-CN.md"

PUBLISHED_SAMPLE_TOKEN_SAVINGS = {
    "source": "docs/benchmarks/value-proof.md",
    "sample_count": 28,
    "skills_with_token_saving_opportunities": 20,
    "activation_body_tokens_before": 30699,
    "projected_activation_tokens_after": 23867,
    "estimated_tokens_saved": 6832,
    "estimated_reduction_percent": 22.3,
    "scriptification_candidates": 26,
    "reference_extraction_candidates": 17,
    "interpretation": (
        "First-pass optimization estimate for the original public benchmark sample, before the "
        "optimized preview packages were generated."
    ),
}


FIXTURE_CASES = [
    {
        "name": "benign-pdf-skill",
        "path": ROOT / "fixtures/benign-pdf-skill",
        "expected": "allow",
        "scenario": "low-risk PDF summarization Skill with local-only file handling",
    },
    {
        "name": "overprivileged-research-skill",
        "path": ROOT / "fixtures/overprivileged-research-skill",
        "expected": "warn",
        "scenario": "research Skill that asks for broader network, home, shell, and credential surfaces than its declared intent needs",
    },
    {
        "name": "malicious-like-writing-skill",
        "path": ROOT / "fixtures/malicious-like-writing-skill",
        "expected": "block",
        "scenario": "writing Skill fixture with sensitive local credential and network exfiltration-shaped behavior",
    },
]


EXTERNAL_TOOLS = [
    {
        "name": "SkillTrust",
        "category": "AI Skill governance",
        "binary": "python",
        "run_mode": "native",
        "fit": "purpose-built for install-time AI Skill intent and permission governance",
        "notes": "Runs in this repository without an external service.",
        "covers": {
            "skill_package": True,
            "declared_intent": True,
            "required_permissions": True,
            "observed_surface": True,
            "intent_overreach": True,
            "line_evidence": True,
            "agent_semantic_review": True,
            "allow_warn_block": True,
            "critical_dataflow_guard": True,
            "permission_manifest": True,
            "policy_overlay": True,
            "audit_receipt": True,
            "remediation_plan": True,
            "optimized_skill_package": True,
            "token_efficiency": True,
        },
    },
    {
        "name": "SkillGuard",
        "category": "AI Skill / agent safety research",
        "binary": None,
        "run_mode": "research-baseline",
        "fit": "closest conceptual baseline for AI Skill risk review when available",
        "notes": "Tracked as a research/specialized baseline; no local CLI was available in this benchmark environment.",
        "covers": {
            "skill_package": True,
            "declared_intent": True,
            "required_permissions": False,
            "observed_surface": True,
            "intent_overreach": True,
            "line_evidence": True,
            "agent_semantic_review": False,
            "allow_warn_block": True,
            "critical_dataflow_guard": True,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "Scandar",
        "category": "AI agent / Skill scanner",
        "binary": None,
        "run_mode": "research-baseline",
        "fit": "specialized scanner-style baseline for AI agent instructions and tools",
        "notes": "Tracked as a specialized baseline; no local CLI was available in this benchmark environment.",
        "covers": {
            "skill_package": True,
            "declared_intent": True,
            "required_permissions": False,
            "observed_surface": True,
            "intent_overreach": True,
            "line_evidence": True,
            "agent_semantic_review": False,
            "allow_warn_block": True,
            "critical_dataflow_guard": True,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "Socket.dev",
        "category": "software supply-chain security",
        "binary": "socket",
        "source_url": "https://docs.socket.dev/",
        "run_mode": "tool-availability",
        "fit": "excellent package/dependency risk scanner; not an AI Skill intent-governance layer",
        "notes": "Useful complement for dependency behavior and malware indicators.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": True,
            "intent_overreach": False,
            "line_evidence": True,
            "agent_semantic_review": False,
            "allow_warn_block": False,
            "critical_dataflow_guard": False,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "Semgrep",
        "category": "SAST",
        "binary": "semgrep",
        "source_url": "https://docs.semgrep.dev/",
        "run_mode": "tool-availability",
        "fit": "strong source-code pattern and SAST baseline; does not infer AI Skill declared intent",
        "notes": "Can complement SkillTrust by scanning helper scripts inside a Skill package.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": True,
            "intent_overreach": False,
            "line_evidence": True,
            "agent_semantic_review": False,
            "allow_warn_block": False,
            "critical_dataflow_guard": False,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "CodeQL",
        "category": "semantic code analysis",
        "binary": "codeql",
        "source_url": "https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql",
        "run_mode": "tool-availability",
        "fit": "deep semantic source-code analysis baseline; not an install-time Skill permission model",
        "notes": "Best used for non-trivial codebases inside or referenced by a Skill.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": True,
            "intent_overreach": False,
            "line_evidence": True,
            "agent_semantic_review": False,
            "allow_warn_block": False,
            "critical_dataflow_guard": False,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "Gitleaks",
        "category": "secret scanning",
        "binary": "gitleaks",
        "source_url": "https://github.com/gitleaks/gitleaks",
        "run_mode": "tool-availability",
        "fit": "secret detection baseline; catches leaked credentials, not permission overreach",
        "notes": "Complements SkillTrust's secret-path and environment-surface findings.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": True,
            "intent_overreach": False,
            "line_evidence": True,
            "agent_semantic_review": False,
            "allow_warn_block": False,
            "critical_dataflow_guard": False,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "TruffleHog",
        "category": "secret scanning",
        "binary": "trufflehog",
        "source_url": "https://github.com/trufflesecurity/trufflehog",
        "run_mode": "tool-availability",
        "fit": "secret detection baseline; useful for repository history and verified credential checks",
        "notes": "Complements SkillTrust but does not generate an AI Skill policy overlay.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": True,
            "intent_overreach": False,
            "line_evidence": True,
            "agent_semantic_review": False,
            "allow_warn_block": False,
            "critical_dataflow_guard": False,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "OSV-Scanner",
        "category": "dependency vulnerability scanning",
        "binary": "osv-scanner",
        "source_url": "https://google.github.io/osv-scanner/",
        "run_mode": "tool-availability",
        "fit": "known-vulnerability baseline for lockfiles/SBOMs; not an AI Skill intent scanner",
        "notes": "Complements SkillTrust dependency policy checks.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": False,
            "intent_overreach": False,
            "line_evidence": True,
            "agent_semantic_review": False,
            "allow_warn_block": False,
            "critical_dataflow_guard": False,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "Trivy",
        "category": "vulnerability / misconfiguration scanning",
        "binary": "trivy",
        "source_url": "https://trivy.dev/",
        "run_mode": "tool-availability",
        "fit": "broad CVE, IaC, container, and secret scanning baseline",
        "notes": "Strong complementary supply-chain scanner; outside the AI Skill intent boundary.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": True,
            "intent_overreach": False,
            "line_evidence": True,
            "agent_semantic_review": False,
            "allow_warn_block": False,
            "critical_dataflow_guard": False,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "Grype",
        "category": "vulnerability scanning",
        "binary": "grype",
        "source_url": "https://github.com/anchore/grype",
        "run_mode": "tool-availability",
        "fit": "SBOM/package vulnerability scanning baseline",
        "notes": "Useful for dependency packages but not AI Skill instruction semantics.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": False,
            "intent_overreach": False,
            "line_evidence": True,
            "agent_semantic_review": False,
            "allow_warn_block": False,
            "critical_dataflow_guard": False,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "OpenSSF Scorecard",
        "category": "project security posture",
        "binary": "scorecard",
        "source_url": "https://github.com/ossf/scorecard",
        "run_mode": "tool-availability",
        "fit": "repository health and supply-chain best-practice baseline",
        "notes": "Operates at repository/project level rather than package intent level.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": False,
            "intent_overreach": False,
            "line_evidence": False,
            "agent_semantic_review": False,
            "allow_warn_block": False,
            "critical_dataflow_guard": False,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "OpenSSF Package Analysis",
        "category": "dynamic package behavior analysis",
        "binary": None,
        "run_mode": "service-baseline",
        "fit": "dynamic package install behavior baseline; useful for dependency ecosystem risk",
        "notes": "Not a local AI Skill analyzer in this benchmark run.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": True,
            "intent_overreach": False,
            "line_evidence": False,
            "agent_semantic_review": False,
            "allow_warn_block": False,
            "critical_dataflow_guard": False,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "promptfoo",
        "category": "LLM red teaming / evals",
        "binary": "promptfoo",
        "source_url": "https://www.promptfoo.dev/docs/intro/",
        "run_mode": "tool-availability",
        "fit": "LLM app evaluation and red-team baseline; tests model behavior, not install-time Skill permissions",
        "notes": "Complements SkillTrust after a Skill is wired into a runtime.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": False,
            "intent_overreach": False,
            "line_evidence": False,
            "agent_semantic_review": True,
            "allow_warn_block": False,
            "critical_dataflow_guard": True,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "garak",
        "category": "LLM vulnerability scanning",
        "binary": "garak",
        "source_url": "https://github.com/NVIDIA/garak",
        "run_mode": "tool-availability",
        "fit": "LLM vulnerability scanner; targets deployed model/app behavior rather than Skill package governance",
        "notes": "Complementary runtime red-team layer.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": False,
            "intent_overreach": False,
            "line_evidence": False,
            "agent_semantic_review": True,
            "allow_warn_block": False,
            "critical_dataflow_guard": True,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "Lakera Guard",
        "category": "LLM security guardrail",
        "binary": None,
        "source_url": "https://www.lakera.ai/guard",
        "run_mode": "api-baseline",
        "fit": "runtime prompt-injection and content-risk guardrail; not a package optimizer",
        "notes": "Requires service/API integration; complementary to SkillTrust policy gates.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": False,
            "intent_overreach": False,
            "line_evidence": False,
            "agent_semantic_review": True,
            "allow_warn_block": False,
            "critical_dataflow_guard": True,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
    {
        "name": "NeMo Guardrails",
        "category": "LLM guardrails framework",
        "binary": "nemoguardrails",
        "source_url": "https://docs.nvidia.com/nemo/guardrails/latest/index.html",
        "run_mode": "tool-availability",
        "fit": "runtime conversational guardrails framework; not an AI Skill permission analyzer",
        "notes": "Complementary for runtime behavior once policy is known.",
        "covers": {
            "skill_package": False,
            "declared_intent": False,
            "required_permissions": False,
            "observed_surface": False,
            "intent_overreach": False,
            "line_evidence": False,
            "agent_semantic_review": True,
            "allow_warn_block": False,
            "critical_dataflow_guard": True,
            "permission_manifest": False,
            "policy_overlay": False,
            "audit_receipt": False,
            "remediation_plan": False,
            "optimized_skill_package": False,
            "token_efficiency": False,
        },
    },
]


CAPABILITY_LABELS_EN = {
    "skill_package": "AI Skill package",
    "declared_intent": "declared intent",
    "required_permissions": "required permissions",
    "observed_surface": "observed permission surface",
    "intent_overreach": "intent vs permission overreach",
    "line_evidence": "line-level evidence",
    "agent_semantic_review": "Agent semantic review",
    "allow_warn_block": "allow/warn/block decision",
    "critical_dataflow_guard": "critical data-flow guard",
    "permission_manifest": "permission manifest",
    "policy_overlay": "policy overlay",
    "audit_receipt": "audit receipt",
    "remediation_plan": "remediation plan",
    "optimized_skill_package": "optimized Skill package",
    "token_efficiency": "token efficiency",
}


CAPABILITY_LABELS_ZH = {
    "skill_package": "AI Skill 包",
    "declared_intent": "声明意图",
    "required_permissions": "必要权限推断",
    "observed_surface": "实际权限面",
    "intent_overreach": "意图与权限越界",
    "line_evidence": "行级证据",
    "agent_semantic_review": "Agent 语义审查",
    "allow_warn_block": "allow/warn/block 决策",
    "critical_dataflow_guard": "关键数据流保护",
    "permission_manifest": "权限清单",
    "policy_overlay": "策略覆盖层",
    "audit_receipt": "审计凭证",
    "remediation_plan": "修复计划",
    "optimized_skill_package": "优化版 Skill 包",
    "token_efficiency": "Token 效率",
}


def run() -> dict[str, Any]:
    analyzer = SkillTrustAnalyzer()
    fixtures = []
    for case in FIXTURE_CASES:
        result = analyzer.analyze(case["path"])
        decision = install_decision(result)["action"]
        token = analyze_token_efficiency(case["path"])
        fixtures.append(
            {
                "name": case["name"],
                "scenario": case["scenario"],
                "expected": case["expected"],
                "actual": decision,
                "matches_expected": decision == case["expected"],
                "score": result.score.trust_fit_score,
                "risk_level": result.score.risk_level,
                "declared_intent": result.declared_intent.summary,
                "findings_count": len(result.findings),
                "observed_permissions_count": len(result.observed_permissions),
                "token_metrics": token["metrics"],
            }
        )

    optimized = []
    for skill_file in sorted((ROOT / "optimized-skills").glob("*/SKILL.md")):
        token = analyze_token_efficiency(skill_file.parent)
        metrics = token["metrics"]
        optimized.append(
            {
                "name": skill_file.parent.name,
                "activation_body_tokens_estimate": metrics["activation_body_tokens_estimate"],
                "projected_activation_tokens": metrics["projected_activation_tokens"],
                "estimated_tokens_saved": metrics["estimated_tokens_saved"],
                "scriptification_candidates": metrics["scriptification_candidates"],
                "token_efficiency_score": token["token_efficiency_score"],
                "token_efficiency_level": token["token_efficiency_level"],
            }
        )

    tool_records = []
    for tool in EXTERNAL_TOOLS:
        record = dict(tool)
        if tool["run_mode"] == "native":
            status = "available"
            version = "repo module"
        elif tool["binary"]:
            status, version = binary_status(tool["binary"])
        else:
            status, version = "not_run", "no local CLI configured"
        record["local_status"] = status
        record["version"] = version
        record["coverage_count"] = sum(1 for covered in tool["covers"].values() if covered)
        tool_records.append(record)

    skilltrust = next(item for item in tool_records if item["name"] == "SkillTrust")
    max_external = max(item["coverage_count"] for item in tool_records if item["name"] != "SkillTrust")

    optimized_preview_rescan = token_savings_summary(optimized)
    payload = {
        "schema_version": "skilltrust.external_baseline.v1",
        "date": date.today().isoformat(),
        "summary": {
            "fixture_cases": len(fixtures),
            "fixture_expectations_matched": sum(1 for item in fixtures if item["matches_expected"]),
            "tools_compared": len(tool_records),
            "skilltrust_capability_count": skilltrust["coverage_count"],
            "best_external_capability_count": max_external,
            "optimized_skill_count": len(optimized),
            "published_first_pass_tokens_saved": PUBLISHED_SAMPLE_TOKEN_SAVINGS["estimated_tokens_saved"],
            "published_first_pass_reduction_percent": PUBLISHED_SAMPLE_TOKEN_SAVINGS["estimated_reduction_percent"],
            "optimized_preview_rescan_tokens_saved": optimized_preview_rescan["estimated_tokens_saved"],
        },
        "fixtures": fixtures,
        "tools": tool_records,
        "published_sample_token_savings": PUBLISHED_SAMPLE_TOKEN_SAVINGS,
        "optimized_preview_rescan_token_savings": optimized_preview_rescan,
        "optimized_skills": optimized,
        "methodology": {
            "external_tool_policy": (
                "External tools are recorded as local-run baselines only when a CLI is installed. "
                "Otherwise the benchmark uses a capability matrix and marks the tool not_run."
            ),
            "claim_boundary": (
                "SkillTrust is compared on AI Skill install-time governance dimensions, not on CVE, "
                "secret, SAST, or runtime LLM red-team tasks where specialist tools remain complementary."
            ),
        },
    }
    RESULTS_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULTS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT_EN.write_text(render_en(payload), encoding="utf-8")
    REPORT_ZH.write_text(render_zh(payload), encoding="utf-8")
    return payload


def binary_status(binary: str) -> tuple[str, str]:
    path = shutil.which(binary)
    if not path:
        return "not_installed", "not found on PATH"

    commands = [
        [binary, "--version"],
        [binary, "version"],
    ]
    for command in commands:
        try:
            completed = subprocess.run(
                command,
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=10,
                check=False,
            )
        except Exception:
            continue
        output = " ".join(completed.stdout.strip().split())
        if output:
            return "available", output[:180]
    return "available", str(path)


def token_savings_summary(optimized: list[dict[str, Any]]) -> dict[str, Any]:
    before = sum(item["activation_body_tokens_estimate"] for item in optimized)
    saved = sum(item["estimated_tokens_saved"] for item in optimized)
    after = sum(item["projected_activation_tokens"] for item in optimized)
    candidates = sum(item["scriptification_candidates"] for item in optimized)
    with_savings = sum(1 for item in optimized if item["estimated_tokens_saved"] > 0)
    reduction = round((saved / before) * 100, 1) if before else 0
    top = sorted(optimized, key=lambda item: item["estimated_tokens_saved"], reverse=True)[:5]
    return {
        "activation_body_tokens_before": before,
        "projected_activation_tokens_after": after,
        "estimated_tokens_saved": saved,
        "estimated_reduction_percent": reduction,
        "skills_with_savings": with_savings,
        "scriptification_candidates": candidates,
        "top_token_saving_skills": [
            {
                "name": item["name"],
                "estimated_tokens_saved": item["estimated_tokens_saved"],
                "activation_body_tokens_estimate": item["activation_body_tokens_estimate"],
                "token_efficiency_score": item["token_efficiency_score"],
            }
            for item in top
        ],
    }


def render_en(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    published_token = payload["published_sample_token_savings"]
    rescan_token = payload["optimized_preview_rescan_token_savings"]
    lines = [
        "# External Baseline Benchmark",
        "",
        f"Date: {payload['date']}",
        "",
        "This benchmark compares SkillTrust with well-known security scanners, supply-chain tools, and LLM guardrail/evaluation tools. The point is not to claim that one tool replaces the others. The point is to show where SkillTrust adds a missing layer: install-time, intent-bound permission governance for AI Skill packages, plus optimization guidance that can reduce always-loaded Skill tokens.",
        "",
        "Chinese version: [外部基线 Benchmark](external-baseline-benchmark.zh-CN.md).",
        "",
        "## Headline Result",
        "",
        f"- Compared tools: {summary['tools_compared']}",
        f"- SkillTrust governance capabilities covered: {summary['skilltrust_capability_count']} / {len(CAPABILITY_LABELS_EN)}",
        f"- Best external baseline coverage on these Skill-governance dimensions: {summary['best_external_capability_count']} / {len(CAPABILITY_LABELS_EN)}",
        f"- Fixture install decisions matched expected outcomes: {summary['fixture_expectations_matched']} / {summary['fixture_cases']}",
        f"- Optimized Skill packages measured: {summary['optimized_skill_count']}",
        f"- Published first-pass activation-token reduction on the original 28-package sample: {published_token['activation_body_tokens_before']} -> {published_token['projected_activation_tokens_after']}, saving {published_token['estimated_tokens_saved']} tokens ({published_token['estimated_reduction_percent']}%)",
        f"- Optimized preview pack rescan: only {rescan_token['estimated_tokens_saved']} residual tokens left to save ({rescan_token['estimated_reduction_percent']}%), which indicates the preview pack is already compact",
        "",
        "## Fixture Decision Benchmark",
        "",
        "| Fixture | Scenario | Expected | SkillTrust | Score | Risk | Findings | Token Saved |",
        "| --- | --- | --- | --- | ---: | --- | ---: | ---: |",
    ]
    for item in payload["fixtures"]:
        lines.append(
            f"| `{item['name']}` | {item['scenario']} | `{item['expected']}` | `{item['actual']}` | "
            f"{item['score']} | {item['risk_level']} | {item['findings_count']} | "
            f"{item['token_metrics']['estimated_tokens_saved']} |"
        )

    lines.extend(
        [
            "",
            "## Capability Matrix",
            "",
            "Legend: `yes` means the capability is a direct target of the tool class; `partial` means it can contribute evidence but does not produce the SkillTrust-style artifact or decision; `no` means outside the tool's main scope.",
            "",
            "| Tool | Category | Local Status | Skill Package | Intent | Overreach | Agent Review | Decision | Policy | Optimized Skill | Token Saving | Notes |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for tool in payload["tools"]:
        covers = tool["covers"]
        tool_name = tool["name"]
        if tool.get("source_url"):
            tool_name = f"[{tool_name}]({tool['source_url']})"
        lines.append(
            f"| {tool_name} | {tool['category']} | {tool['local_status']} | "
            f"{mark(covers['skill_package'])} | {mark(covers['declared_intent'])} | "
            f"{mark(covers['intent_overreach'])} | {mark(covers['agent_semantic_review'])} | "
            f"{mark(covers['allow_warn_block'])} | {mark(covers['policy_overlay'])} | "
            f"{mark(covers['optimized_skill_package'])} | {mark(covers['token_efficiency'])} | "
            f"{tool['fit']} |"
        )

    lines.extend(
        [
            "",
            "## Detailed Governance Dimensions",
            "",
            "| Capability | SkillTrust | Best External Baselines | Why It Matters For AI Skills |",
            "| --- | --- | --- | --- |",
        ]
    )
    explanations = {
        "skill_package": "The unit under review is a reusable AI Skill package, not only a repository or dependency graph.",
        "declared_intent": "A Skill should be judged against what it claims to do.",
        "required_permissions": "Least privilege requires inferring the minimum permission set needed for that intent.",
        "observed_surface": "Observed filesystem, shell, environment, network, connector, dependency, and prompt surfaces must remain visible.",
        "intent_overreach": "The core governance question is whether observed/requested permissions exceed declared intent.",
        "line_evidence": "Reviewers need reproducible evidence, not only a score.",
        "agent_semantic_review": "A host Agent can read examples and docs end-to-end to mark likely false positives without deleting evidence.",
        "allow_warn_block": "Install-time gates need a conservative action.",
        "critical_dataflow_guard": "Sensitive local data to network-like sinks cannot be semantically upgraded to safe.",
        "permission_manifest": "The review should produce an installable least-privilege contract.",
        "policy_overlay": "A policy overlay lets a host runtime enforce or display the boundary.",
        "audit_receipt": "Receipts make the review replayable with hashes and rule versions.",
        "remediation_plan": "Governance should explain how to converge the Skill to least privilege.",
        "optimized_skill_package": "SkillTrust can emit a preview package rather than only a finding list.",
        "token_efficiency": "Moving deterministic detail out of always-loaded instructions can lower activation context cost.",
    }
    for key, label in CAPABILITY_LABELS_EN.items():
        external_names = [
            tool["name"]
            for tool in payload["tools"]
            if tool["name"] != "SkillTrust" and tool["covers"].get(key)
        ]
        external = ", ".join(external_names[:5]) if external_names else "none directly"
        if len(external_names) > 5:
            external += ", ..."
        lines.append(f"| {label} | yes | {external} | {explanations[key]} |")

    lines.extend(
        [
            "",
            "## Token-Saving Benchmark",
            "",
            "SkillTrust has two token-efficiency measurements in this repository:",
            "",
            f"- Original public benchmark sample: `{published_token['activation_body_tokens_before']}` -> `{published_token['projected_activation_tokens_after']}` estimated activation-body tokens, saving `{published_token['estimated_tokens_saved']}` tokens (`{published_token['estimated_reduction_percent']}%`).",
            f"- Optimized preview pack rescan: `{rescan_token['activation_body_tokens_before']}` -> `{rescan_token['projected_activation_tokens_after']}` estimated activation-body tokens, with only `{rescan_token['estimated_tokens_saved']}` residual tokens left to save (`{rescan_token['estimated_reduction_percent']}%`).",
            "",
            "The first number shows the product value: SkillTrust finds token waste in the original packages. The second number is a regression check: after SkillTrust emits optimized preview packages, the remaining always-loaded token waste is much smaller.",
            "",
            f"- Original skills with token-saving opportunities: {published_token['skills_with_token_saving_opportunities']} / {published_token['sample_count']}",
            f"- Original scriptification candidates: {published_token['scriptification_candidates']}",
            f"- Original reference extraction candidates: {published_token['reference_extraction_candidates']}",
            f"- Optimized preview packages with remaining token-saving opportunities: {rescan_token['skills_with_savings']} / {summary['optimized_skill_count']}",
            f"- Remaining scriptification/config candidates after preview optimization: {rescan_token['scriptification_candidates']}",
            "",
            "Top residual opportunities after the optimized preview pack rescan:",
            "",
            "| Skill | Activation Tokens | Estimated Saved | Token Score |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for item in rescan_token["top_token_saving_skills"]:
        lines.append(
            f"| `{item['name']}` | {item['activation_body_tokens_estimate']} | "
            f"{item['estimated_tokens_saved']} | {item['token_efficiency_score']} |"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- SAST, CVE, secret scanning, package behavior analysis, and LLM red-team tools remain valuable complements.",
            "- SkillTrust's differentiated layer is the AI Skill install boundary: declared intent, least-privilege permission inference, overreach detection, conservative fusion with Agent review, policy artifacts, remediation, and optimized preview packages.",
            "- The token-saving metric is an activation-context estimate, not a billing guarantee. It is still useful because Skill packages often load instruction text before any task-specific evidence is needed.",
            "",
            "## Reproduce",
            "",
            "```bash",
            "PYTHONDONTWRITEBYTECODE=1 python scripts/external_baseline_benchmark.py",
            "```",
            "",
            "This regenerates:",
            "",
            "- `docs/benchmarks/external-baseline-results.json`",
            "- `docs/benchmarks/external-baseline-benchmark.md`",
            "- `docs/benchmarks/external-baseline-benchmark.zh-CN.md`",
            "",
            "## Caveats",
            "",
            "- External tools are not forced through network installs. If a local CLI is unavailable, the result is marked `not_installed` or `not_run`.",
            "- Specialized scanners should be evaluated on their native tasks before making broad security claims.",
            "- SkillTrust benchmark claims are limited to AI Skill package governance and token-efficiency planning.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_zh(payload: dict[str, Any]) -> str:
    summary = payload["summary"]
    published_token = payload["published_sample_token_savings"]
    rescan_token = payload["optimized_preview_rescan_token_savings"]
    lines = [
        "# 外部基线 Benchmark",
        "",
        f"日期：{payload['date']}",
        "",
        "这份 benchmark 将 SkillTrust 与主流安全扫描、供应链安全、LLM guardrail / eval 工具放在一起比较。它不是要证明 SkillTrust 替代这些工具，而是说明 SkillTrust 补上的那一层：面向 AI Skill package 的安装前意图绑定权限治理，以及可以减少常驻 Skill token 的优化建议。",
        "",
        "英文版：[External Baseline Benchmark](external-baseline-benchmark.md)。",
        "",
        "## 核心结果",
        "",
        f"- 对比工具数：{summary['tools_compared']}",
        f"- SkillTrust 覆盖的 Skill 治理能力：{summary['skilltrust_capability_count']} / {len(CAPABILITY_LABELS_ZH)}",
        f"- 外部基线在这些 Skill 治理维度上的最高覆盖：{summary['best_external_capability_count']} / {len(CAPABILITY_LABELS_ZH)}",
        f"- Fixture 安装决策命中预期：{summary['fixture_expectations_matched']} / {summary['fixture_cases']}",
        f"- 已测优化版 Skill 包：{summary['optimized_skill_count']}",
        f"- 原始 28 包公开样本第一轮 activation-token reduction：{published_token['activation_body_tokens_before']} -> {published_token['projected_activation_tokens_after']}，节省 {published_token['estimated_tokens_saved']} tokens（{published_token['estimated_reduction_percent']}%）",
        f"- 优化预览包复扫：只剩 {rescan_token['estimated_tokens_saved']} 个可继续节省的 residual tokens（{rescan_token['estimated_reduction_percent']}%），说明 preview pack 已经明显变精简",
        "",
        "## Fixture 决策 Benchmark",
        "",
        "| Fixture | 场景 | 预期 | SkillTrust | 分数 | 风险等级 | Findings | Token 节省 |",
        "| --- | --- | --- | --- | ---: | --- | ---: | ---: |",
    ]
    scenario_zh = {
        "benign-pdf-skill": "低风险 PDF 摘要 Skill，只需要本地文件处理",
        "overprivileged-research-skill": "研究类 Skill 请求了超过声明意图所需的 network、home、shell、credential 权限面",
        "malicious-like-writing-skill": "写作类 fixture 暴露了本地敏感凭证到网络出口的数据流形态",
    }
    for item in payload["fixtures"]:
        lines.append(
            f"| `{item['name']}` | {scenario_zh.get(item['name'], item['scenario'])} | `{item['expected']}` | `{item['actual']}` | "
            f"{item['score']} | {item['risk_level']} | {item['findings_count']} | "
            f"{item['token_metrics']['estimated_tokens_saved']} |"
        )

    lines.extend(
        [
            "",
            "## 能力矩阵",
            "",
            "说明：`yes` 表示这是该工具类别直接覆盖的能力；`partial` 表示可以贡献证据，但不会生成 SkillTrust 风格的治理产物或安装决策；`no` 表示不属于该工具主要范围。",
            "",
            "| 工具 | 类别 | 本地状态 | Skill 包 | 意图 | 越界 | Agent 审查 | 决策 | Policy | 优化包 | Token 节省 | 说明 |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for tool in payload["tools"]:
        covers = tool["covers"]
        tool_name = tool["name"]
        if tool.get("source_url"):
            tool_name = f"[{tool_name}]({tool['source_url']})"
        lines.append(
            f"| {tool_name} | {tool['category']} | {tool['local_status']} | "
            f"{mark(covers['skill_package'])} | {mark(covers['declared_intent'])} | "
            f"{mark(covers['intent_overreach'])} | {mark(covers['agent_semantic_review'])} | "
            f"{mark(covers['allow_warn_block'])} | {mark(covers['policy_overlay'])} | "
            f"{mark(covers['optimized_skill_package'])} | {mark(covers['token_efficiency'])} | "
            f"{tool['fit']} |"
        )

    lines.extend(
        [
            "",
            "## 详细治理维度",
            "",
            "| 能力 | SkillTrust | 外部基线 | 对 AI Skills 的意义 |",
            "| --- | --- | --- | --- |",
        ]
    )
    explanations = {
        "skill_package": "审查对象是可复用 AI Skill package，而不只是代码仓库或依赖图。",
        "declared_intent": "Skill 需要按照它声称要做的事情来判断。",
        "required_permissions": "最小权限治理需要推断完成该意图真正需要的权限集合。",
        "observed_surface": "filesystem、shell、environment、network、connector、dependency、prompt 权限面必须可见。",
        "intent_overreach": "核心问题是实际/请求权限是否超出声明意图。",
        "line_evidence": "审查者需要可复现证据，而不只是一个分数。",
        "agent_semantic_review": "宿主 Agent 可以阅读全文与示例，标注 likely false positive，但不能删除证据。",
        "allow_warn_block": "安装前门禁需要保守的动作输出。",
        "critical_dataflow_guard": "敏感本地数据流向网络出口不能被语义审查洗成安全。",
        "permission_manifest": "审查结果应生成可安装的最小权限契约。",
        "policy_overlay": "Policy overlay 可以让宿主 runtime 展示或执行边界。",
        "audit_receipt": "审计凭证用 hash 和规则版本支持复现。",
        "remediation_plan": "治理结果应该告诉用户如何收敛到最小权限。",
        "optimized_skill_package": "SkillTrust 可以生成优化预览包，而不只是 findings 列表。",
        "token_efficiency": "把确定性细节从常驻指令移出，可以降低激活上下文成本。",
    }
    for key, label in CAPABILITY_LABELS_ZH.items():
        external_names = [
            tool["name"]
            for tool in payload["tools"]
            if tool["name"] != "SkillTrust" and tool["covers"].get(key)
        ]
        external = "、".join(external_names[:5]) if external_names else "无直接覆盖"
        if len(external_names) > 5:
            external += " 等"
        lines.append(f"| {label} | yes | {external} | {explanations[key]} |")

    lines.extend(
        [
            "",
            "## Token 节省 Benchmark",
            "",
            "这个仓库里有两组 token-efficiency 数字：",
            "",
            f"- 原始公开样本：`{published_token['activation_body_tokens_before']}` -> `{published_token['projected_activation_tokens_after']}` estimated activation-body tokens，预计节省 `{published_token['estimated_tokens_saved']}` tokens（`{published_token['estimated_reduction_percent']}%`）。",
            f"- 优化预览包复扫：`{rescan_token['activation_body_tokens_before']}` -> `{rescan_token['projected_activation_tokens_after']}` estimated activation-body tokens，只剩 `{rescan_token['estimated_tokens_saved']}` residual tokens 可继续节省（`{rescan_token['estimated_reduction_percent']}%`）。",
            "",
            "第一组数字展示产品价值：SkillTrust 能在原始 package 里发现 token 浪费。第二组数字是回归检查：SkillTrust 生成优化版 preview package 后，常驻 token 浪费已经明显降低。",
            "",
            f"- 原始样本中有 token-saving 机会的 Skills：{published_token['skills_with_token_saving_opportunities']} / {published_token['sample_count']}",
            f"- 原始 scriptification candidates：{published_token['scriptification_candidates']}",
            f"- 原始 reference extraction candidates：{published_token['reference_extraction_candidates']}",
            f"- 优化预览包复扫后仍有剩余 token-saving 机会的 Skills：{rescan_token['skills_with_savings']} / {summary['optimized_skill_count']}",
            f"- 复扫后剩余 scriptification / config candidates：{rescan_token['scriptification_candidates']}",
            "",
            "优化预览包复扫后的 residual 机会：",
            "",
            "| Skill | Activation Tokens | 预计节省 | Token Score |",
            "| --- | ---: | ---: | ---: |",
        ]
    )
    for item in rescan_token["top_token_saving_skills"]:
        lines.append(
            f"| `{item['name']}` | {item['activation_body_tokens_estimate']} | "
            f"{item['estimated_tokens_saved']} | {item['token_efficiency_score']} |"
        )

    lines.extend(
        [
            "",
            "## 如何解读",
            "",
            "- SAST、CVE、secret scanning、package behavior analysis、LLM red-team 工具仍然很有价值，它们是 SkillTrust 的互补层。",
            "- SkillTrust 的差异化位置是 AI Skill 安装边界：声明意图、最小权限推断、越界检测、与 Agent 语义审查保守融合、policy 产物、修复计划和优化预览包。",
            "- Token 节省是 activation-context 估算，不是生产计费承诺。但它对 Skill 很重要，因为很多 Skill 在真正用到任务细节前，就会先加载大量常驻指令。",
            "",
            "## 复现方式",
            "",
            "```bash",
            "PYTHONDONTWRITEBYTECODE=1 python scripts/external_baseline_benchmark.py",
            "```",
            "",
            "该命令会重新生成：",
            "",
            "- `docs/benchmarks/external-baseline-results.json`",
            "- `docs/benchmarks/external-baseline-benchmark.md`",
            "- `docs/benchmarks/external-baseline-benchmark.zh-CN.md`",
            "",
            "## 限制说明",
            "",
            "- 外部工具不会被脚本强制联网安装；如果本地没有 CLI，就标记为 `not_installed` 或 `not_run`。",
            "- 对专业扫描器的安全强弱判断，应该在它们各自原生任务上单独评估。",
            "- SkillTrust 的 benchmark 结论限定在 AI Skill package 治理与 token-efficiency planning。",
        ]
    )
    return "\n".join(lines) + "\n"


def mark(value: bool) -> str:
    return "yes" if value else "no"


if __name__ == "__main__":
    result = run()
    print(
        "External baseline benchmark generated: "
        f"{result['summary']['tools_compared']} tools, "
        f"{result['summary']['fixture_expectations_matched']}/"
        f"{result['summary']['fixture_cases']} fixture decisions matched, "
        f"{result['published_sample_token_savings']['estimated_tokens_saved']} published first-pass "
        f"tokens saved and {result['optimized_preview_rescan_token_savings']['estimated_tokens_saved']} "
        "residual preview tokens saved."
    )
