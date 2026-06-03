from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


RULES_VERSION = "skilltrust-rules-v0.1.0"


SEVERITY_WEIGHTS = {
    "info": 1,
    "low": 3,
    "medium": 7,
    "high": 14,
    "critical": 25,
}


@dataclass(frozen=True)
class EvidenceLocation:
    file: str
    line: int
    text: str


@dataclass
class Finding:
    id: str
    severity: str
    category: str
    file: str
    line: int
    evidence: str
    declared_intent_relation: str
    why_it_matters: str
    recommendation: str
    policy_effect: str
    confidence: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class IntentSignal:
    intent: str
    weight: int
    source: str
    evidence: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class DeclaredIntent:
    summary: str
    primary_intents: List[str]
    clarity_score: int
    signals: List[IntentSignal] = field(default_factory=list)
    boundaries: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["signals"] = [signal.to_dict() for signal in self.signals]
        return data


@dataclass
class RequiredPermissions:
    filesystem_read: List[Dict[str, str]]
    filesystem_write: List[Dict[str, str]]
    network: List[Dict[str, str]]
    environment: List[Dict[str, str]]
    shell: List[Dict[str, str]]
    connectors: List[Dict[str, str]]
    dependencies: List[Dict[str, str]]
    denied_by_default: List[Dict[str, str]]
    rationale: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ObservedPermission:
    category: str
    permission: str
    file: str
    line: int
    evidence: str
    relation: str
    severity_hint: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class ScoreBreakdown:
    trust_fit_score: int
    risk_level: str
    components: Dict[str, int]
    explanation: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AnalysisResult:
    input_path: str
    rules_version: str
    declared_intent: DeclaredIntent
    required_permissions: RequiredPermissions
    observed_permissions: List[ObservedPermission]
    findings: List[Finding]
    score: ScoreBreakdown
    permission_manifest: Dict[str, Any]
    policy: Dict[str, Any]
    audit_receipt: Optional[Dict[str, Any]] = None
    remediation_plan: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "input_path": self.input_path,
            "rules_version": self.rules_version,
            "declared_intent": self.declared_intent.to_dict(),
            "required_permissions": self.required_permissions.to_dict(),
            "observed_permissions": [item.to_dict() for item in self.observed_permissions],
            "findings": [item.to_dict() for item in self.findings],
            "score": self.score.to_dict(),
            "permission_manifest": self.permission_manifest,
            "policy": self.policy,
            "audit_receipt": self.audit_receipt,
            "remediation_plan": self.remediation_plan,
        }
