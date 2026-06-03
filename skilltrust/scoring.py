from __future__ import annotations

from typing import Dict, List

from .models import DeclaredIntent, Finding, SEVERITY_WEIGHTS, ScoreBreakdown


def risk_level(score: int) -> str:
    if score >= 85:
        return "Trusted"
    if score >= 70:
        return "Mostly Trusted"
    if score >= 50:
        return "Needs Review"
    if score >= 30:
        return "Overprivileged"
    return "Critical Risk"


def compute_score(intent: DeclaredIntent, findings: List[Finding], policy: Dict) -> ScoreBreakdown:
    weighted_overreach = sum(SEVERITY_WEIGHTS.get(item.severity, 0) for item in findings)
    sensitive_tokens = ["env", "ssh", "cookie", "token", "secret", "credential", "home", "key", "password"]
    sensitive_weight = sum(
        SEVERITY_WEIGHTS.get(item.severity, 0)
        for item in findings
        if item.category in {"filesystem", "environment"}
        and any(token in (item.evidence + " " + item.policy_effect).lower() for token in sensitive_tokens)
    )
    data_flow_weight = sum(SEVERITY_WEIGHTS.get(item.severity, 0) for item in findings if item.category == "data_flow")
    install_weight = sum(SEVERITY_WEIGHTS.get(item.severity, 0) for item in findings if item.category in {"install", "dependency"})
    prompt_weight = sum(SEVERITY_WEIGHTS.get(item.severity, 0) for item in findings if item.category == "prompt")

    components = {
        "Intent Clarity": intent.clarity_score,
        "Permission Necessity": max(0, 100 - weighted_overreach * 2),
        "Overreach Ratio": max(0, 100 - weighted_overreach * 2),
        "Sensitive Surface": max(0, 100 - sensitive_weight * 4),
        "Data Flow Safety": max(0, 100 - data_flow_weight * 4),
        "Install-Time Safety": max(0, 100 - install_weight * 5),
        "Prompt Integrity": max(0, 100 - prompt_weight * 5),
        "Enforceability": _enforceability(intent, findings, policy),
        "Auditability": _auditability(findings),
    }

    weights = {
        "Intent Clarity": 0.15,
        "Permission Necessity": 0.20,
        "Overreach Ratio": 0.15,
        "Sensitive Surface": 0.15,
        "Data Flow Safety": 0.15,
        "Install-Time Safety": 0.08,
        "Prompt Integrity": 0.05,
        "Enforceability": 0.04,
        "Auditability": 0.03,
    }
    raw_score = sum(components[name] * weight for name, weight in weights.items())
    score = int(round(max(0, min(100, raw_score))))
    if any(item.category == "data_flow" and item.severity == "critical" for item in findings):
        score = min(score, 25)
    high_or_above = sum(1 for item in findings if SEVERITY_WEIGHTS.get(item.severity, 0) >= SEVERITY_WEIGHTS["high"])
    sensitive_high = sum(
        1
        for item in findings
        if item.category in {"filesystem", "environment"}
        and SEVERITY_WEIGHTS.get(item.severity, 0) >= SEVERITY_WEIGHTS["high"]
    )
    if high_or_above >= 4 and sensitive_high >= 2:
        score = min(score, 45)

    explanation = [
        f"Weighted overreach evidence: {weighted_overreach}",
        f"Sensitive surface evidence: {sensitive_weight}",
        f"Data-flow evidence: {data_flow_weight}",
        "Score compares declared intent, inferred least privilege, observed behavior, and enforceable policy coverage.",
    ]
    if findings:
        top = sorted(findings, key=lambda item: SEVERITY_WEIGHTS.get(item.severity, 0), reverse=True)[:3]
        explanation.append("Highest-impact findings: " + ", ".join(f"{item.id} ({item.severity})" for item in top))
    else:
        explanation.append("No material permission overreach findings were detected.")

    return ScoreBreakdown(
        trust_fit_score=score,
        risk_level=risk_level(score),
        components={name: int(round(value)) for name, value in components.items()},
        explanation=explanation,
    )


def _enforceability(intent: DeclaredIntent, findings: List[Finding], policy: Dict) -> int:
    score = 70 if intent.primary_intents else 45
    if policy.get("filesystem", {}).get("deny_read"):
        score += 10
    if policy.get("network", {}).get("deny"):
        score += 8
    if policy.get("shell", {}).get("deny"):
        score += 6
    if all(item.policy_effect for item in findings):
        score += 6
    return max(0, min(100, score))


def _auditability(findings: List[Finding]) -> int:
    if not findings:
        return 100
    complete = 0
    for item in findings:
        required = [
            item.id,
            item.severity,
            item.category,
            item.file,
            item.line,
            item.evidence,
            item.declared_intent_relation,
            item.why_it_matters,
            item.recommendation,
            item.policy_effect,
            item.confidence,
        ]
        if all(value not in (None, "") for value in required):
            complete += 1
    return int(round((complete / len(findings)) * 100))
