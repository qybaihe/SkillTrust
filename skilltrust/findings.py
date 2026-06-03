from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlparse

from .files import TextFile
from .models import DeclaredIntent, Finding, ObservedPermission


URL_RE = re.compile(r"https?://[A-Za-z0-9._~:/?#\[\]@!$&'()*+,;=%-]+")

SUSPICIOUS_WEBHOOK_DOMAINS = {
    "webhook.site",
    "requestbin.com",
    "pipedream.net",
    "discord.com",
    "hooks.slack.com",
    "ngrok.io",
}

SUSPICIOUS_NETWORK_TERMS = {"webhook", "telemetry", "beacon", "collector", "exfil"}

NETWORK_INTENTS = {"research", "market_analysis", "competition_discovery", "browser_operation", "form_filling"}
DOC_FILES = {"SKILL.md", "README.md", "README"}


@dataclass(frozen=True)
class LineHit:
    file: TextFile
    line_no: int
    line: str
    category: str
    permission: str
    severity: str
    relation: str
    why: str
    recommendation: str
    policy_effect: str
    confidence: str = "high"


class FindingFactory:
    def __init__(self) -> None:
        self.counts: Dict[str, int] = {}

    def create(self, hit: LineHit, severity: Optional[str] = None, category: Optional[str] = None) -> Finding:
        final_category = category or hit.category
        prefix = {
            "filesystem": "FS",
            "network": "NET",
            "shell": "SH",
            "environment": "ENV",
            "install": "INS",
            "prompt": "PR",
            "data_flow": "DF",
            "dependency": "DEP",
        }.get(final_category, "GEN")
        self.counts[prefix] = self.counts.get(prefix, 0) + 1
        finding_id = f"ST-{prefix}-{self.counts[prefix]:03d}"
        return Finding(
            id=finding_id,
            severity=severity or hit.severity,
            category=final_category,
            file=hit.file.relpath,
            line=hit.line_no,
            evidence=hit.line.strip()[:300],
            declared_intent_relation=hit.relation,
            why_it_matters=hit.why,
            recommendation=hit.recommendation,
            policy_effect=hit.policy_effect,
            confidence=hit.confidence,
        )


def extract_observed_permissions(
    files: List[TextFile], intent: DeclaredIntent
) -> Tuple[List[ObservedPermission], List[Finding]]:
    factory = FindingFactory()
    observed: List[ObservedPermission] = []
    findings: List[Finding] = []
    sensitive_sources: Dict[str, List[LineHit]] = {}
    network_sinks: Dict[str, List[LineHit]] = {}

    for file in files:
        for line_no, line in enumerate(file.lines, start=1):
            for hit in _scan_line(file, line_no, line, intent):
                observed.append(
                    ObservedPermission(
                        category=hit.category,
                        permission=hit.permission,
                        file=file.relpath,
                        line=line_no,
                        evidence=line.strip()[:300],
                        relation=hit.relation,
                        severity_hint=hit.severity,
                    )
                )

                if _should_promote_to_finding(hit):
                    findings.append(factory.create(hit))

                if hit.category in {"filesystem", "environment"} and hit.severity in {"high", "critical"}:
                    sensitive_sources.setdefault(file.relpath, []).append(hit)
                if _is_network_sink(hit):
                    network_sinks.setdefault(file.relpath, []).append(hit)

    for relpath, sources in sensitive_sources.items():
        sinks = network_sinks.get(relpath, [])
        if not sinks:
            continue
        source = sources[0]
        sink = sinks[0]
        combined = LineHit(
            file=source.file,
            line_no=sink.line_no,
            line=f"sensitive source at line {source.line_no} reaches network sink: {sink.line.strip()}",
            category="data_flow",
            permission="sensitive-source-to-network-sink",
            severity="critical",
            relation=(
                "overreach: the declared intent does not justify a hidden path from local sensitive data "
                "to outbound network traffic"
            ),
            why=(
                "A sensitive source and an outbound POST/webhook sink in the same executable file is a plausible "
                "exfiltration path, even when the token or endpoint is a fixture."
            ),
            recommendation=(
                "Remove the network sink, isolate any required upload behind explicit user confirmation, and block "
                "secret-bearing paths in the runtime policy."
            ),
            policy_effect="deny network POST/webhook sinks when sensitive filesystem or environment sources are touched",
            confidence="high",
        )
        findings.append(factory.create(combined))

    return observed, findings


def _scan_line(file: TextFile, line_no: int, line: str, intent: DeclaredIntent) -> List[LineHit]:
    hits: List[LineHit] = []
    stripped = line.strip()
    if not stripped:
        return hits

    lowered = stripped.lower()
    primary = ", ".join(intent.primary_intents) or "unspecified"

    if _is_doc_file(file.relpath):
        if _matches_prompt_integrity(lowered):
            hits.append(
                LineHit(
                    file=file,
                    line_no=line_no,
                    line=line,
                    category="prompt",
                    permission="prompt-integrity-bypass",
                    severity="high",
                    relation=f"overreach: declared intent ({primary}) does not require hidden self-authorization or instruction bypass",
                    why="Prompt instructions that hide actions, ignore prior rules, or exfiltrate context undermine user consent.",
                    recommendation="Remove hidden instructions and state safety boundaries explicitly in SKILL.md.",
                    policy_effect="deny prompt directives that bypass user consent, hide actions, or request exfiltration",
                )
            )
        return hits

    if _matches_env_file(lowered):
        hits.append(
            LineHit(
                file=file,
                line_no=line_no,
                line=line,
                category="filesystem",
                permission="read-env-file",
                severity="high",
                relation=f"overreach: declared intent ({primary}) does not require reading .env secret files",
                why="`.env` files commonly contain API keys, tokens, and credentials unrelated to skill execution.",
                recommendation="Accept explicit user-provided config paths only, and remove implicit `.env` reads.",
                policy_effect="deny read access to $HOME/**/.env and workspace .env unless explicitly approved",
            )
        )

    if _matches_sensitive_path(lowered):
        hits.append(
            LineHit(
                file=file,
                line_no=line_no,
                line=line,
                category="filesystem",
                permission="read-sensitive-local-path",
                severity="high",
                relation=f"overreach: declared intent ({primary}) does not require local credential stores or profile data",
                why="Credential stores, SSH keys, cookies, cloud configs, and shell history are sensitive surfaces.",
                recommendation="Remove the access or replace it with a user-selected file input scoped to the task.",
                policy_effect="deny read access to SSH keys, browser cookies, cloud credentials, and shell history",
            )
        )

    if _matches_home_scan(lowered):
        hits.append(
            LineHit(
                file=file,
                line_no=line_no,
                line=line,
                category="filesystem",
                permission="home-directory-enumeration",
                severity="high",
                relation=f"overreach: declared intent ({primary}) can be completed with project or user-selected files",
                why="Scanning `$HOME` creates broad visibility into unrelated personal files and increases blast radius.",
                recommendation="Constrain reads to `$WORKSPACE`, `$SKILL_DIR`, and explicit user-selected paths.",
                policy_effect="deny recursive enumeration of $HOME and absolute user profile paths",
            )
        )

    if _matches_env_access(lowered):
        severity = "high" if _matches_secret_word(lowered) else "medium"
        hits.append(
            LineHit(
                file=file,
                line_no=line_no,
                line=line,
                category="environment",
                permission="environment-variable-access",
                severity=severity,
                relation=f"overreach: declared intent ({primary}) does not require broad environment inspection",
                why="Environment variables frequently hold credentials and service tokens.",
                recommendation="Read only named, documented, non-secret configuration variables when necessary.",
                policy_effect="deny environment variable reads matching *TOKEN*, *SECRET*, *KEY*, *PASSWORD*",
            )
        )

    for url in URL_RE.findall(stripped):
        hit = _network_hit(file, line_no, line, url, intent)
        hits.append(hit)

    if _matches_network_library(lowered):
        severity = "info" if _intent_allows_network(intent) and not _line_suggests_post_or_webhook(lowered) else "medium"
        relation = (
            f"related: declared intent ({primary}) may require network access"
            if _intent_allows_network(intent)
            else f"overreach: declared intent ({primary}) does not require outbound network access"
        )
        hits.append(
            LineHit(
                file=file,
                line_no=line_no,
                line=line,
                category="network",
                permission="programmatic-network-client",
                severity=severity,
                relation=relation,
                why="Programmatic clients can move data outside the skill boundary unless constrained by domain and method.",
                recommendation="Declare approved domains and block unapproved POST/webhook destinations.",
                policy_effect="allow only declared domains and deny hidden POST sinks",
                confidence="medium",
            )
        )

    if _matches_dangerous_shell(lowered):
        hits.append(
            LineHit(
                file=file,
                line_no=line_no,
                line=line,
                category="shell",
                permission="dangerous-shell-command",
                severity="critical" if "curl" in lowered and "|" in lowered and "sh" in lowered else "high",
                relation=f"overreach: declared intent ({primary}) does not justify high-impact shell behavior",
                why="Commands such as sudo, destructive deletes, SSH transfer, netcat, or curl-pipe-shell are hard to audit and easy to misuse.",
                recommendation="Replace with narrow local helpers, require explicit user confirmation, or remove the command.",
                policy_effect="deny sudo, rm -rf, chmod 777, ssh, scp, nc, and curl|bash patterns",
            )
        )

    if _matches_dynamic_exec(lowered):
        hits.append(
            LineHit(
                file=file,
                line_no=line_no,
                line=line,
                category="shell",
                permission="dynamic-code-or-command-execution",
                severity="high",
                relation=f"overreach: declared intent ({primary}) should not need runtime-generated command execution",
                why="Dynamic exec makes the actual runtime behavior depend on untrusted data and weakens auditability.",
                recommendation="Use explicit command allowlists and structured APIs instead of dynamic shell/code execution.",
                policy_effect="deny shell=True, eval, exec, and unreviewed subprocess command strings",
            )
        )

    if _matches_postinstall(lowered):
        hits.append(
            LineHit(
                file=file,
                line_no=line_no,
                line=line,
                category="install",
                permission="install-time-script",
                severity="high",
                relation=f"overreach: declared intent ({primary}) does not require arbitrary install-time execution",
                why="Postinstall hooks run before the user can inspect normal runtime behavior and can bypass skill policy.",
                recommendation="Remove postinstall hooks or replace them with documented, user-invoked setup steps.",
                policy_effect="deny package postinstall hooks and remote setup scripts",
            )
        )

    if _matches_unpinned_dependency(file.relpath, stripped):
        hits.append(
            LineHit(
                file=file,
                line_no=line_no,
                line=line,
                category="dependency",
                permission="unpinned-dependency",
                severity="low",
                relation=f"weak fit: declared intent ({primary}) can be implemented with reproducible dependency versions",
                why="Unpinned dependencies make audit receipts harder to reproduce and can change behavior over time.",
                recommendation="Pin dependencies with exact versions or use standard-library implementations when feasible.",
                policy_effect="require pinned dependency versions in install-time policy",
                confidence="medium",
            )
        )

    if _matches_prompt_integrity(lowered):
        hits.append(
            LineHit(
                file=file,
                line_no=line_no,
                line=line,
                category="prompt",
                permission="prompt-integrity-bypass",
                severity="high",
                relation=f"overreach: declared intent ({primary}) does not require hidden self-authorization or instruction bypass",
                why="Prompt instructions that hide actions, ignore prior rules, or exfiltrate context undermine user consent.",
                recommendation="Remove hidden instructions and state safety boundaries explicitly in SKILL.md.",
                policy_effect="deny prompt directives that bypass user consent, hide actions, or request exfiltration",
            )
        )

    return hits


def _network_hit(file: TextFile, line_no: int, line: str, url: str, intent: DeclaredIntent) -> LineHit:
    domain = urlparse(url).netloc.lower()
    suspicious = _is_suspicious_domain(domain) or _has_suspicious_network_term(url.lower())
    allows_network = _intent_allows_network(intent)
    postish = _line_suggests_post_or_webhook(line.lower())
    primary = ", ".join(intent.primary_intents) or "unspecified"

    if suspicious:
        severity = "high"
        relation = (
            f"overreach: declared intent ({primary}) may allow relevant web access, but `{domain}` is a generic webhook/sink"
        )
        why = "Webhook-like endpoints are common exfiltration sinks and are not auditable source domains."
        recommendation = "Remove the webhook or replace it with a declared, user-approved destination and explicit data contract."
        policy = f"deny network access to {domain}"
    elif not allows_network:
        severity = "high" if postish else "medium"
        relation = f"overreach: declared intent ({primary}) does not require outbound network access"
        why = "Network egress can disclose local content and should be declared and domain-scoped."
        recommendation = "Remove network egress or add a clear declared intent, allowed domains, and user confirmation."
        policy = f"deny undeclared network access to {domain}"
    else:
        severity = "info"
        relation = f"related: declared intent ({primary}) can require external research/navigation"
        why = "Network access appears consistent with the declared workflow, but should remain domain-scoped."
        recommendation = "Keep this domain in an approved allowlist only if it is needed for the task."
        policy = f"allow only if {domain} is task-relevant or user-approved"

    return LineHit(
        file=file,
        line_no=line_no,
        line=line,
        category="network",
        permission=f"network-url:{domain}",
        severity=severity,
        relation=relation,
        why=why,
        recommendation=recommendation,
        policy_effect=policy,
    )


def _should_promote_to_finding(hit: LineHit) -> bool:
    if hit.severity in {"medium", "high", "critical"}:
        return True
    if hit.category in {"install", "prompt", "dependency"}:
        return True
    return False


def _intent_allows_network(intent: DeclaredIntent) -> bool:
    return bool(set(intent.primary_intents).intersection(NETWORK_INTENTS))


def _is_suspicious_domain(domain: str) -> bool:
    return any(domain == item or domain.endswith(f".{item}") for item in SUSPICIOUS_WEBHOOK_DOMAINS)


def _has_suspicious_network_term(value: str) -> bool:
    return any(term in value for term in SUSPICIOUS_NETWORK_TERMS)


def _line_suggests_post_or_webhook(line: str) -> bool:
    return any(token in line for token in ["requests.post", ".post(", "method: 'post'", 'method: "post"', "-x post", "webhook"])


def _is_network_sink(hit: LineHit) -> bool:
    if hit.category != "network":
        return False
    line = hit.line.lower()
    return _line_suggests_post_or_webhook(line) or "webhook" in hit.permission


def _matches_env_file(line: str) -> bool:
    return bool(re.search(r"(^|[^\w.-])\.env([^\w-]|$)|dotenv|env_path|env_file", line))


def _matches_sensitive_path(line: str) -> bool:
    patterns = [
        r"\.ssh",
        r"id_rsa",
        r"id_ed25519",
        r"\.aws",
        r"\.gcp",
        r"application support/.*/cookies",
        r"cookies(?:\.sqlite|/|\\|$)",
        r"login data",
        r"keychain",
        r"\.zsh_history",
        r"\.bash_history",
        r"credentials\.json",
        r"service_account",
    ]
    return any(re.search(pattern, line) for pattern in patterns)


def _matches_home_scan(line: str) -> bool:
    patterns = [
        r"path\.home\(\).*rglob",
        r"path\.home\(\).*glob",
        r"expanduser\([\"']~",
        r"\$home",
        r"\b~[/\\]",
        r"/users/[^/]+",
        r"/home/[^/]+",
        r"find\s+~",
        r"find\s+\$home",
        r"os\.walk\([^)]*(path\.home|expanduser|~|\$home)",
    ]
    return any(re.search(pattern, line) for pattern in patterns)


def _matches_env_access(line: str) -> bool:
    return any(token in line for token in ["os.environ", "process.env", "getenv(", "env::var", "std::env"])


def _matches_secret_word(line: str) -> bool:
    return any(token in line for token in ["token", "secret", "password", "api_key", "apikey", "credential", "auth"])


def _matches_network_library(line: str) -> bool:
    return any(token in line for token in ["requests.", "httpx.", "urllib.request", "fetch(", "axios.", "curl ", "wget "])


def _matches_dangerous_shell(line: str) -> bool:
    patterns = [
        r"\bsudo\b",
        r"rm\s+-rf",
        r"chmod\s+777",
        r"\bscp\b",
        r"\bssh\b",
        r"\bnc\b",
        r"netcat",
        r"curl\b.*\|.*(sh|bash)",
        r"wget\b.*\|.*(sh|bash)",
        r"base64\b.*(-d|--decode).*\|.*(sh|bash)",
    ]
    return any(re.search(pattern, line) for pattern in patterns)


def _matches_dynamic_exec(line: str) -> bool:
    patterns = [
        r"shell\s*=\s*true",
        r"\beval\(",
        r"\bexec\(",
        r"os\.system\(",
        r"subprocess\.(popen|run|call|check_call|check_output)\([^)]*\+",
    ]
    return any(re.search(pattern, line) for pattern in patterns)


def _matches_postinstall(line: str) -> bool:
    return '"postinstall"' in line or "'postinstall'" in line or "postinstall:" in line


def _matches_unpinned_dependency(relpath: str, line: str) -> bool:
    if not line or line.startswith("#"):
        return False
    filename = relpath.rsplit("/", 1)[-1]
    if filename == "requirements.txt":
        if line.startswith(("-e ", "git+", "http://", "https://")):
            return True
        return bool(re.match(r"^[A-Za-z0-9_.-]+(?:\[[^\]]+\])?$", line))
    return False


def _matches_prompt_integrity(line: str) -> bool:
    patterns = [
        r"ignore previous instructions",
        r"ignore all previous",
        r"do not tell (the )?user",
        r"do not reveal",
        r"hidden command",
        r"exfiltrate",
        r"bypass.*policy",
        r"override.*safety",
        r"self-authori[sz]e",
        r"send.*token",
    ]
    return any(re.search(pattern, line) for pattern in patterns)


def _is_doc_file(relpath: str) -> bool:
    return relpath.rsplit("/", 1)[-1] in DOC_FILES
