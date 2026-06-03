from __future__ import annotations

from pathlib import Path

from .files import load_text_files
from .findings import extract_observed_permissions
from .intent import extract_declared_intent
from .models import AnalysisResult, RULES_VERSION
from .permissions import infer_required_permissions
from .policy import build_permission_manifest, build_policy
from .receipt import build_audit_receipt
from .reporting import render_remediation_plan
from .scoring import compute_score


class SkillTrustAnalyzer:
    def analyze(self, input_path: str | Path) -> AnalysisResult:
        root = Path(input_path).expanduser().resolve()
        if not root.exists():
            raise FileNotFoundError(f"Input path does not exist: {root}")

        files = load_text_files(root)
        declared_intent = extract_declared_intent(files)
        required_permissions = infer_required_permissions(declared_intent)
        observed_permissions, findings = extract_observed_permissions(files, declared_intent)
        policy = build_policy(declared_intent, required_permissions, findings)
        score = compute_score(declared_intent, findings, policy)
        manifest = build_permission_manifest(str(root), declared_intent, required_permissions)

        result = AnalysisResult(
            input_path=str(root),
            rules_version=RULES_VERSION,
            declared_intent=declared_intent,
            required_permissions=required_permissions,
            observed_permissions=observed_permissions,
            findings=findings,
            score=score,
            permission_manifest=manifest,
            policy=policy,
        )
        result.remediation_plan = render_remediation_plan(result)
        result.audit_receipt = build_audit_receipt(root, result)
        return result
