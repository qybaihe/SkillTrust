from __future__ import annotations

import json
from pathlib import Path

from skilltrust import SkillTrustAnalyzer
from skilltrust.authoring import analyze_authoring, write_authoring_outputs
from skilltrust.governance import govern_skills, install_decision, remediate_skill
from skilltrust.reporting import write_outputs
from skilltrust.semantic import draft_semantic_review, fuse_analysis, write_review_request
from skilltrust.taxonomy import analyze_taxonomy, write_taxonomy_outputs
from skilltrust.token_optimizer import analyze_token_efficiency, write_token_outputs


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures"


def analyze_fixture(name: str):
    return SkillTrustAnalyzer().analyze(FIXTURES / name)


def test_benign_pdf_skill_is_trusted() -> None:
    result = analyze_fixture("benign-pdf-skill")

    assert result.score.risk_level == "Trusted"
    assert result.score.trust_fit_score >= 85
    assert result.findings == []
    assert "pdf_summarization" in result.declared_intent.primary_intents
    assert result.policy["network"]["default"] == "deny"


def test_overprivileged_research_skill_is_overprivileged() -> None:
    result = analyze_fixture("overprivileged-research-skill")

    assert result.score.risk_level == "Overprivileged"
    assert 30 <= result.score.trust_fit_score <= 49
    assert {finding.category for finding in result.findings} >= {"filesystem", "environment", "network"}
    assert not any(finding.category == "data_flow" for finding in result.findings)
    assert any(".env" in finding.evidence for finding in result.findings)
    assert any("telemetry.unrelated.example.invalid" in finding.evidence for finding in result.findings)


def test_malicious_like_writing_skill_is_critical() -> None:
    result = analyze_fixture("malicious-like-writing-skill")

    assert result.score.risk_level == "Critical Risk"
    assert result.score.trust_fit_score <= 29
    assert any(finding.category == "data_flow" and finding.severity == "critical" for finding in result.findings)
    assert any(finding.category == "prompt" for finding in result.findings)
    assert any("webhook.site" in finding.evidence for finding in result.findings)


def test_findings_have_required_fields() -> None:
    result = analyze_fixture("malicious-like-writing-skill")

    required = [
        "id",
        "severity",
        "category",
        "file",
        "line",
        "evidence",
        "declared_intent_relation",
        "why_it_matters",
        "recommendation",
        "policy_effect",
        "confidence",
    ]
    for finding in result.findings:
        data = finding.to_dict()
        for key in required:
            assert data[key] not in ("", None)


def test_output_artifacts_are_generated(tmp_path: Path) -> None:
    result = analyze_fixture("overprivileged-research-skill")
    write_outputs(tmp_path, result)

    expected = {
        "permission_manifest.json",
        "skilltrust-policy.json",
        "trust_report.md",
        "audit_receipt.json",
        "remediation_plan.md",
        "analysis.json",
    }
    assert expected <= {path.name for path in tmp_path.iterdir()}

    receipt = json.loads((tmp_path / "audit_receipt.json").read_text(encoding="utf-8"))
    assert receipt["rules_version"] == "skilltrust-rules-v0.1.0"
    assert receipt["result_hash"]
    assert receipt["evidence_chain_summary"]

    report = (tmp_path / "trust_report.md").read_text(encoding="utf-8")
    assert "Permission Overreach Findings" in report
    assert "Trust Fit Score" in report


def test_install_gate_decisions() -> None:
    analyzer = SkillTrustAnalyzer()

    benign = analyzer.analyze(FIXTURES / "benign-pdf-skill")
    overprivileged = analyzer.analyze(FIXTURES / "overprivileged-research-skill")
    malicious = analyzer.analyze(FIXTURES / "malicious-like-writing-skill")

    assert install_decision(benign)["action"] == "allow"
    assert install_decision(overprivileged)["action"] == "warn"
    assert install_decision(malicious)["action"] == "block"


def test_govern_skills_generates_portfolio(tmp_path: Path) -> None:
    summary = govern_skills(FIXTURES, tmp_path)

    assert summary["counts"]["total"] == 3
    assert summary["counts"]["allow"] == 1
    assert summary["counts"]["warn"] == 1
    assert summary["counts"]["block"] == 1
    assert "taxonomy_findings" in summary["counts"]
    assert "rename_plan_items" in summary["counts"]
    assert (tmp_path / "local_skills_summary.json").exists()
    assert (tmp_path / "local_skills_report.md").exists()
    assert (tmp_path / "skill_taxonomy_report.md").exists()

    for record in summary["records"]:
        report_dir = Path(record["report_dir"])
        assert (report_dir / "install_decision.json").exists()
        assert (report_dir / "optimization_summary.md").exists()
        assert record["optimized_controls"]


def test_remediate_skill_generates_policy_overlay_bundle(tmp_path: Path) -> None:
    payload = remediate_skill(FIXTURES / "overprivileged-research-skill", tmp_path)

    assert payload["mode"] == "policy-overlay"
    assert payload["install_decision"]["action"] == "warn"
    assert payload["score_after_policy_overlay"] >= 70
    assert payload["authoring_score"] >= 0
    assert payload["authoring_actions"]
    assert payload["token_efficiency_score"] >= 0
    assert payload["token_actions"]
    assert (tmp_path / "remediation_bundle.json").exists()
    assert (tmp_path / "skilltrust-policy.json").exists()
    assert (tmp_path / "optimization_summary.md").exists()
    assert (tmp_path / "authoring_report.md").exists()
    assert (tmp_path / "optimized_SKILL.md").exists()
    assert (tmp_path / "token_efficiency_report.md").exists()


def test_authoring_audit_generates_harness_outputs(tmp_path: Path) -> None:
    analysis = analyze_authoring(FIXTURES / "overprivileged-research-skill")
    write_authoring_outputs(tmp_path, analysis)

    assert "harness_fit_score" in analysis
    assert analysis["metrics"]["body_lines"] > 0
    assert analysis["optimized_skill_md_draft"]
    assert (tmp_path / "authoring_report.md").exists()
    assert (tmp_path / "optimized_SKILL.md").exists()
    assert (tmp_path / "reference_extraction_plan.json").exists()


def test_token_optimizer_generates_scriptification_plan(tmp_path: Path) -> None:
    analysis = analyze_token_efficiency(FIXTURES / "overprivileged-research-skill")
    write_token_outputs(tmp_path, analysis)

    assert analysis["metrics"]["activation_body_tokens_estimate"] > 0
    assert "token_efficiency_score" in analysis
    assert analysis["optimization_principles"]
    assert (tmp_path / "token_efficiency_report.md").exists()
    assert (tmp_path / "token_optimization_plan.json").exists()


def test_taxonomy_audit_generates_approval_plan(tmp_path: Path) -> None:
    analysis = analyze_taxonomy(FIXTURES)
    write_taxonomy_outputs(tmp_path, analysis)

    assert analysis["skill_count"] == 3
    assert analysis["approval_required"] is True
    assert "taxonomy_score" in analysis
    assert analysis["findings"]
    assert (tmp_path / "skill_taxonomy_report.md").exists()
    assert (tmp_path / "skill_taxonomy_plan.json").exists()
    assert (tmp_path / "rename_approval_plan.md").exists()


def test_semantic_review_request_is_generated(tmp_path: Path) -> None:
    request = write_review_request(FIXTURES / "overprivileged-research-skill", tmp_path)

    assert (tmp_path / "semantic_review_request.json").exists()
    assert (tmp_path / "semantic_review_instructions.md").exists()
    assert request["schema_version"] == "skilltrust.semantic_review_request.v1"
    assert request["deterministic_findings"]
    assert request["agent_questions"]
    assert request["agent_review_protocol"]
    assert {item["path"] for item in request["core_documents_to_read"]} >= {"SKILL.md", "README.md"}
    assert request["output_schema"]["full_document_reading"]["required"] is True
    assert request["privacy_boundary"]["external_model_api"] is False
    assert request["privacy_boundary"]["api_key_required"] is False


def test_fuse_outputs_warn_for_overprivileged_fixture(tmp_path: Path) -> None:
    request_dir = tmp_path / "request"
    fused_dir = tmp_path / "fused"
    write_review_request(FIXTURES / "overprivileged-research-skill", request_dir)
    draft_semantic_review(request_dir / "semantic_review_request.json", request_dir / "semantic_review.json")

    fused = fuse_analysis(request_dir / "analysis.json", request_dir / "semantic_review.json", fused_dir)

    assert fused["fused_install_decision"]["final_action"] == "warn"
    assert fused["semantic_review"]["full_document_reading"]["documents_read"]
    assert (fused_dir / "fused_analysis.json").exists()
    assert (fused_dir / "fused_trust_report.md").exists()
    assert (fused_dir / "fused_install_decision.json").exists()
    assert (fused_dir / "skilltrust-policy.json").exists()
    assert "agent_semantic_refinements" in fused["fused_policy"]


def test_critical_dataflow_cannot_be_semantically_allowed(tmp_path: Path) -> None:
    request_dir = tmp_path / "request"
    fused_dir = tmp_path / "fused"
    request = write_review_request(FIXTURES / "malicious-like-writing-skill", request_dir)

    semantic_review = request["output_schema"]
    semantic_review["declared_boundary_summary"] = "Writing assistant."
    semantic_review["semantic_install_recommendation"] = {
        "action": "allow",
        "reason": "Test attempts to allow a critical finding.",
        "confidence": "low",
    }
    semantic_review["semantic_score_overlay"] = {
        "base_score": 25,
        "adjustment": 10,
        "final_score": 35,
        "reasons": ["test"],
    }
    for item in semantic_review["finding_assessments"]:
        item["semantic_fit"] = "likely_false_positive"
        item["rationale"] = "Test false positive claim."
    (request_dir / "semantic_review.json").write_text(json.dumps(semantic_review, indent=2), encoding="utf-8")

    fused = fuse_analysis(request_dir / "analysis.json", request_dir / "semantic_review.json", fused_dir)

    assert fused["fused_install_decision"]["final_action"] == "block"
    assert fused["fused_install_decision"]["critical_dataflow_protected"] is True
    assert fused["fused_install_decision"]["final_score"] <= 29
    assert any(item["display_priority"] == "critical_protected" for item in fused["fused_findings"])


def test_likely_false_positive_does_not_delete_finding(tmp_path: Path) -> None:
    request_dir = tmp_path / "request"
    fused_dir = tmp_path / "fused"
    request = write_review_request(FIXTURES / "overprivileged-research-skill", request_dir)

    semantic_review = request["output_schema"]
    semantic_review["semantic_install_recommendation"] = {
        "action": "warn",
        "reason": "Some findings may need human review.",
        "confidence": "medium",
    }
    for item in semantic_review["finding_assessments"]:
        item["semantic_fit"] = "likely_false_positive"
        item["rationale"] = "Test likely false positive."
        item["confidence"] = "low"
    (request_dir / "semantic_review.json").write_text(json.dumps(semantic_review, indent=2), encoding="utf-8")

    fused = fuse_analysis(request_dir / "analysis.json", request_dir / "semantic_review.json", fused_dir)

    deterministic_count = len(json.loads((request_dir / "analysis.json").read_text(encoding="utf-8"))["findings"])
    assert len(fused["fused_findings"]) == deterministic_count
    assert all(item["display_priority"] == "lowered_needs_human_review" for item in fused["fused_findings"])
