from __future__ import annotations

from typing import Any, Dict, List

from .findings import URL_RE
from .models import DeclaredIntent, Finding, RequiredPermissions


def build_permission_manifest(
    input_path: str, intent: DeclaredIntent, required: RequiredPermissions
) -> Dict[str, Any]:
    return {
        "schema_version": "skilltrust.permission_manifest.v1",
        "input_path": input_path,
        "declared_intent": {
            "summary": intent.summary,
            "primary_intents": intent.primary_intents,
            "clarity_score": intent.clarity_score,
        },
        "minimal_required_permissions": required.to_dict(),
        "least_privilege_statement": (
            "The skill should receive only the listed permissions needed to satisfy its declared intent. "
            "Sensitive local credentials, home-directory enumeration, hidden network sinks, and dangerous shell "
            "behavior are denied unless explicitly re-declared and re-audited."
        ),
    }


def build_policy(intent: DeclaredIntent, required: RequiredPermissions, findings: List[Finding]) -> Dict[str, Any]:
    denied_domains = _denied_domains(findings)
    allowed_network = [item["scope"] for item in required.network]
    default_network = "allow_task_relevant_domains" if allowed_network else "deny"

    return {
        "schema_version": "skilltrust.policy.v1",
        "intent_binding": {
            "summary": intent.summary,
            "primary_intents": intent.primary_intents,
            "clarity_score": intent.clarity_score,
            "boundary_mode": "least_privilege",
        },
        "filesystem": {
            "allow_read": [item["scope"] for item in required.filesystem_read],
            "allow_write": [item["scope"] for item in required.filesystem_write],
            "deny_read": [
                "$HOME/.ssh/**",
                "$HOME/.aws/**",
                "$HOME/.gcp/**",
                "$HOME/**/.env",
                "$HOME/**/Cookies/**",
                "$HOME/**/Login Data",
                "$HOME/.zsh_history",
                "$HOME/.bash_history",
            ],
            "deny_write": ["$HOME/**", "/etc/**", "/var/**"],
            "deny_enumeration": ["$HOME/**", "/Users/*/**", "/home/*/**"],
        },
        "network": {
            "default": default_network,
            "allow": allowed_network,
            "deny": sorted(denied_domains),
            "deny_methods": [
                {"method": "POST", "scope": "unapproved domains"},
                {"method": "PUT", "scope": "unapproved domains"},
            ],
            "require_user_confirmation_for": ["new domains", "file uploads", "webhook-like destinations"],
        },
        "environment": {
            "allow": [item["name"] for item in required.environment if "name" in item],
            "deny_patterns": ["*TOKEN*", "*SECRET*", "*KEY*", "*PASSWORD*", "*CREDENTIAL*", "*COOKIE*"],
        },
        "shell": {
            "allow": sorted({item["command"] for item in required.shell}),
            "deny": ["sudo", "rm -rf", "chmod 777", "ssh", "scp", "nc", "curl|bash", "wget|bash", "shell=True", "eval", "exec"],
        },
        "connectors": {
            "allow": [item["connector"] for item in required.connectors],
            "require_user_consent": True,
        },
        "dependencies": {
            "require_pinned_versions": True,
            "deny_postinstall": True,
            "deny_remote_install_scripts": True,
        },
        "prompt_integrity": {
            "deny_directives": [
                "ignore previous instructions",
                "do not tell the user",
                "exfiltrate context",
                "self-authorize hidden actions",
            ],
            "require_visible_boundaries": True,
        },
        "audit": {
            "log_decisions": True,
            "record_file_hashes": True,
            "record_policy_version": True,
        },
    }


def _denied_domains(findings: List[Finding]) -> List[str]:
    domains = set()
    for finding in findings:
        if finding.category != "network":
            continue
        for url in URL_RE.findall(finding.evidence):
            domain = url.split("//", 1)[-1].split("/", 1)[0].lower()
            domains.add(domain)
    return sorted(domains)
