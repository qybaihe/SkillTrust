from __future__ import annotations

from typing import Dict, List

from .models import DeclaredIntent, RequiredPermissions


def infer_required_permissions(intent: DeclaredIntent) -> RequiredPermissions:
    intents = set(intent.primary_intents)
    fs_read: List[Dict[str, str]] = [
        {"scope": "$SKILL_DIR/**", "reason": "Read the skill package being installed or executed."},
    ]
    fs_write: List[Dict[str, str]] = [
        {"scope": "$WORKSPACE/reports/**", "reason": "Write generated outputs and audit artifacts."},
    ]
    network: List[Dict[str, str]] = []
    environment: List[Dict[str, str]] = []
    shell: List[Dict[str, str]] = [
        {"command": "python", "reason": "Run local analysis or helper scripts when declared by the skill workflow."},
    ]
    connectors: List[Dict[str, str]] = []
    dependencies: List[Dict[str, str]] = [
        {"constraint": "pinned-or-standard-library", "reason": "Install behavior should be reproducible and reviewable."},
    ]
    rationale: List[str] = []

    if "pdf_summarization" in intents:
        fs_read.append({"scope": "user-provided PDF paths", "reason": "PDF summarization needs only the selected input PDFs."})
        fs_write.append({"scope": "user-requested summary output", "reason": "The skill must write the summary requested by the user."})
        shell.append({"command": "pdftotext", "reason": "A local PDF text extractor is a reasonable least-privilege helper."})
        rationale.append("PDF summarization does not require home-directory scanning, secrets, browser cookies, or network egress by default.")

    if intents.intersection({"research", "market_analysis", "competition_discovery"}):
        fs_read.append({"scope": "$WORKSPACE/**", "reason": "Research skills may read user-provided briefs, notes, and source material."})
        fs_write.append({"scope": "$WORKSPACE/**/reports/**", "reason": "Research skills commonly write summaries, tables, and reports."})
        network.extend(
            [
                {"scope": "https://*.google.com/search", "reason": "Web research may use search results when explicitly requested."},
                {"scope": "https://official-or-user-approved-domains/**", "reason": "Follow source links relevant to the declared research topic."},
            ]
        )
        shell.extend(
            [
                {"command": "rg", "reason": "Search within user-provided workspace documents."},
                {"command": "python", "reason": "Parse, transform, and format collected public information."},
            ]
        )
        rationale.append("Research needs public web access and project document reads, but not local credentials or unrelated webhooks.")

    if "gmail_management" in intents:
        connectors.append({"connector": "gmail", "reason": "The declared task requires Gmail messages through the approved connector."})
        rationale.append("Gmail work should use the Gmail connector and should not read local mail caches, SSH keys, or shell history.")

    if intents.intersection({"form_filling", "browser_operation"}):
        connectors.append({"connector": "browser", "reason": "The declared workflow needs browser automation or rendered page state."})
        network.append({"scope": "user-confirmed target URLs", "reason": "Browser tasks should stay on the form or site requested by the user."})
        rationale.append("Browser/form skills require user-confirmed navigation, not arbitrary filesystem or credential access.")

    if "presentation_generation" in intents:
        fs_read.append({"scope": "user-provided source notes and media", "reason": "Deck generation uses the user's source material."})
        fs_write.append({"scope": "presentation output files", "reason": "The skill must write PPTX, PDF, or HTML deck artifacts."})
        rationale.append("Presentation generation can require local render tools, but not secret reads or unrelated network exfiltration.")

    if "writing_assistant" in intents:
        fs_read.append({"scope": "user-provided drafts and references", "reason": "Writing tasks need only selected source text and context."})
        fs_write.append({"scope": "user-requested draft output", "reason": "The skill writes the requested article, document, or report."})
        rationale.append("Writing assistance is content-bound and should not inspect environment secrets or send hidden telemetry.")

    if "document_generation" in intents and "writing_assistant" not in intents:
        fs_read.append({"scope": "user-provided source documents and references", "reason": "Document/report generation uses selected source material."})
        fs_write.append({"scope": "user-requested document output", "reason": "The skill writes the requested report, document, or artifact."})
        rationale.append("Document generation should stay scoped to selected source material and requested output paths.")

    if not intents:
        rationale.append("The skill has weak declared intent, so SkillTrust keeps permissions narrow until a clearer purpose is provided.")

    denied_by_default = [
        {"scope": "$HOME/.ssh/**", "reason": "SSH credentials are never necessary for ordinary skill execution."},
        {"scope": "$HOME/**/.env", "reason": "Environment secret files are outside declared task inputs."},
        {"scope": "$HOME/Library/**/Cookies/**", "reason": "Browser cookies are sensitive profile state."},
        {"scope": "$HOME/.aws/**", "reason": "Cloud credentials are unrelated to the declared task unless explicitly scoped."},
        {"scope": "$HOME/.config/**/tokens*", "reason": "Token stores are sensitive by default."},
        {"scope": "unapproved webhook endpoints", "reason": "Hidden network sinks break auditability and least privilege."},
        {"scope": "shell commands: sudo, rm -rf, chmod 777, nc, ssh, scp, curl|bash", "reason": "High-impact shell behavior requires explicit, narrow justification."},
    ]

    return RequiredPermissions(
        filesystem_read=_dedupe_dicts(fs_read),
        filesystem_write=_dedupe_dicts(fs_write),
        network=_dedupe_dicts(network),
        environment=_dedupe_dicts(environment),
        shell=_dedupe_dicts(shell),
        connectors=_dedupe_dicts(connectors),
        dependencies=_dedupe_dicts(dependencies),
        denied_by_default=denied_by_default,
        rationale=rationale,
    )


def _dedupe_dicts(items: List[Dict[str, str]]) -> List[Dict[str, str]]:
    seen = set()
    result = []
    for item in items:
        key = tuple(sorted(item.items()))
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result
