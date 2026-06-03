from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from .files import file_hashes
from .models import AnalysisResult, RULES_VERSION


def build_audit_receipt(root: Path, result: AnalysisResult) -> Dict[str, Any]:
    result_payload = result.to_dict()
    result_payload["audit_receipt"] = None
    canonical = json.dumps(result_payload, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    result_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    hashes = file_hashes(root)

    evidence_summary = []
    for finding in result.findings:
        evidence_hash = hashlib.sha256(finding.evidence.encode("utf-8")).hexdigest()
        evidence_summary.append(
            {
                "id": finding.id,
                "category": finding.category,
                "severity": finding.severity,
                "file": finding.file,
                "line": finding.line,
                "evidence_hash": evidence_hash,
            }
        )

    return {
        "schema_version": "skilltrust.audit_receipt.v1",
        "scan_time_utc": datetime.now(timezone.utc).isoformat(),
        "input_path": str(root.resolve()),
        "rules_version": RULES_VERSION,
        "file_count": len(hashes),
        "file_hashes": hashes,
        "result_hash": result_hash,
        "evidence_chain_summary": evidence_summary,
        "reproducibility": {
            "instructions": "Run `skilltrust analyze <input_path> --format json` with the same rules version and file tree.",
            "hash_algorithm": "sha256",
        },
    }
