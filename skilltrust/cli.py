from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .analyzer import SkillTrustAnalyzer
from .authoring import analyze_authoring, write_authoring_outputs
from .governance import govern_skills, install_decision, remediate_skill
from .reporting import summary_text, write_outputs
from .semantic import draft_semantic_review, fuse_analysis, write_review_request
from .taxonomy import analyze_taxonomy, write_taxonomy_outputs
from .token_optimizer import analyze_token_efficiency, write_token_outputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skilltrust",
        description="Intent-bound least-privilege permission governance for AI Skills.",
    )
    subparsers = parser.add_subparsers(dest="command")
    analyze = subparsers.add_parser("analyze", help="Analyze an AI Skill package.")
    analyze.add_argument("path", help="Path to a Skill package directory or file.")
    analyze.add_argument("--format", choices=["text", "json"], default="text", help="Output format printed to stdout.")
    analyze.add_argument("--out", help="Directory where report, policy, manifest, receipt, and remediation plan are written.")
    analyze.add_argument(
        "--agent-review-request",
        action="store_true",
        help="Also generate semantic_review_request.json and semantic_review_instructions.md for host-Agent review.",
    )

    review_request = subparsers.add_parser("review-request", help="Generate host-Agent semantic review request artifacts.")
    review_request.add_argument("path", help="Path to a Skill package directory or file.")
    review_request.add_argument("--out", required=True, help="Output directory for semantic review request artifacts.")
    review_request.add_argument("--format", choices=["text", "json"], default="text", help="Output format printed to stdout.")

    fuse = subparsers.add_parser("fuse", help="Fuse deterministic analysis with host-Agent semantic review.")
    fuse.add_argument("analysis", nargs="?", help="Path to analysis.json.")
    fuse.add_argument("semantic_review", nargs="?", help="Path to semantic_review.json.")
    fuse.add_argument("--analysis", dest="analysis_opt", help="Path to analysis.json.")
    fuse.add_argument("--semantic-review", dest="semantic_review_opt", help="Path to semantic_review.json.")
    fuse.add_argument("--out", required=True, help="Output directory for fused artifacts.")
    fuse.add_argument("--format", choices=["text", "json"], default="text", help="Output format printed to stdout.")

    draft_review = subparsers.add_parser(
        "draft-semantic-review",
        help="Create an offline demo semantic_review.json from a request. No API call; not a substitute for host-Agent review.",
    )
    draft_review.add_argument("request", help="Path to semantic_review_request.json.")
    draft_review.add_argument("--out", required=True, help="Output semantic_review.json path.")
    draft_review.add_argument("--format", choices=["text", "json"], default="text", help="Output format printed to stdout.")

    audit_local = subparsers.add_parser("audit-local", help="Analyze all local Skills and generate policy overlays.")
    audit_local.add_argument(
        "--skills-root",
        default="~/.codex/skills",
        help="Directory containing local Skills. Defaults to ~/.codex/skills.",
    )
    audit_local.add_argument(
        "--out",
        default="reports/local-all",
        help="Directory where portfolio report and per-Skill governance bundles are written.",
    )
    audit_local.add_argument("--threshold", type=int, default=70, help="Minimum score for install allow decision.")
    audit_local.add_argument("--limit", type=int, help="Optional limit for demos/tests.")
    audit_local.add_argument("--format", choices=["text", "json"], default="text", help="Output format printed to stdout.")

    remediate = subparsers.add_parser("remediate", help="Generate an intent-bound remediation bundle for one Skill.")
    remediate.add_argument("path", help="Path to a Skill package directory.")
    remediate.add_argument("--out", required=True, help="Output directory for remediation bundle.")
    remediate.add_argument("--threshold", type=int, default=70, help="Minimum score for install allow decision.")
    remediate.add_argument("--format", choices=["text", "json"], default="text", help="Output format printed to stdout.")

    install_check = subparsers.add_parser("install-check", help="Run install-time permission gate for a Skill.")
    install_check.add_argument("path", help="Path to a Skill package directory.")
    install_check.add_argument("--threshold", type=int, default=70, help="Minimum score for install allow decision.")
    install_check.add_argument("--out", help="Optional output directory for full analysis and install decision.")
    install_check.add_argument("--format", choices=["text", "json"], default="text", help="Output format printed to stdout.")

    authoring_audit = subparsers.add_parser("authoring-audit", help="Check Skill authoring quality and harness structure.")
    authoring_audit.add_argument("path", help="Path to a Skill package directory or SKILL.md file.")
    authoring_audit.add_argument("--out", help="Output directory for authoring report and optimized_SKILL.md draft.")
    authoring_audit.add_argument("--format", choices=["text", "json"], default="text", help="Output format printed to stdout.")

    token_optimize = subparsers.add_parser("token-optimize", help="Find script/config opportunities that reduce Skill token load.")
    token_optimize.add_argument("path", help="Path to a Skill package directory or SKILL.md file.")
    token_optimize.add_argument("--out", help="Output directory for token efficiency report and optimization plan.")
    token_optimize.add_argument("--format", choices=["text", "json"], default="text", help="Output format printed to stdout.")

    taxonomy_audit = subparsers.add_parser("taxonomy-audit", help="Find naming and trigger ambiguity across a Skill set.")
    taxonomy_audit.add_argument(
        "--skills-root",
        default="~/.codex/skills",
        help="Directory containing Skills. Defaults to ~/.codex/skills.",
    )
    taxonomy_audit.add_argument("--out", default="reports/taxonomy", help="Output directory for taxonomy reports.")
    taxonomy_audit.add_argument("--format", choices=["text", "json"], default="text", help="Output format printed to stdout.")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return

    if args.command == "analyze":
        if args.agent_review_request and not args.out:
            print("skilltrust: --agent-review-request requires --out", file=sys.stderr)
            raise SystemExit(2)
        analyzer = SkillTrustAnalyzer()
        try:
            result = analyzer.analyze(args.path)
        except Exception as exc:  # pragma: no cover - CLI guard
            print(f"skilltrust: {exc}", file=sys.stderr)
            raise SystemExit(2)

        if args.out:
            write_outputs(Path(args.out), result)
            if args.agent_review_request:
                write_review_request(args.path, args.out)

        if args.format == "json":
            print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
        else:
            print(summary_text(result))
            if args.out:
                print(f"Artifacts written to: {Path(args.out).resolve()}")
                if args.agent_review_request:
                    print("Agent review request written: semantic_review_request.json")
        return

    if args.command == "review-request":
        try:
            request = write_review_request(args.path, args.out)
        except Exception as exc:  # pragma: no cover - CLI guard
            print(f"skilltrust: {exc}", file=sys.stderr)
            raise SystemExit(2)
        if args.format == "json":
            print(json.dumps(request, indent=2, ensure_ascii=False))
        else:
            print(f"Agent semantic review request written to: {Path(args.out).resolve()}")
            print("Host Agent should read semantic_review_request.json and write semantic_review.json.")
        return

    if args.command == "fuse":
        analysis_path = args.analysis_opt or args.analysis
        semantic_review_path = args.semantic_review_opt or args.semantic_review
        if not analysis_path or not semantic_review_path:
            print("skilltrust: fuse requires analysis.json and semantic_review.json", file=sys.stderr)
            raise SystemExit(2)
        try:
            fused = fuse_analysis(analysis_path, semantic_review_path, args.out)
        except Exception as exc:  # pragma: no cover - CLI guard
            print(f"skilltrust: {exc}", file=sys.stderr)
            raise SystemExit(2)
        if args.format == "json":
            print(json.dumps(fused, indent=2, ensure_ascii=False))
        else:
            decision = fused["fused_install_decision"]
            print(
                f"Fused install decision: {decision['final_action']} "
                f"({decision['base_score']} {decision['semantic_adjustment']:+d} -> {decision['final_score']})"
            )
            print(f"Fused artifacts written to: {Path(args.out).resolve()}")
        return

    if args.command == "draft-semantic-review":
        try:
            review = draft_semantic_review(args.request, args.out)
        except Exception as exc:  # pragma: no cover - CLI guard
            print(f"skilltrust: {exc}", file=sys.stderr)
            raise SystemExit(2)
        if args.format == "json":
            print(json.dumps(review, indent=2, ensure_ascii=False))
        else:
            print(f"Offline demo semantic review written to: {Path(args.out).resolve()}")
            print("This is for fusion testing only; host-Agent semantic review is preferred.")
        return

    if args.command == "audit-local":
        try:
            summary = govern_skills(args.skills_root, args.out, threshold=args.threshold, limit=args.limit)
        except Exception as exc:  # pragma: no cover - CLI guard
            print(f"skilltrust: {exc}", file=sys.stderr)
            raise SystemExit(2)
        if args.format == "json":
            print(json.dumps(summary, indent=2, ensure_ascii=False))
        else:
            counts = summary["counts"]
            print(
                "Local Skill governance complete: "
                f"{counts['total']} scanned, {counts['allow']} allow, "
                f"{counts['warn']} warn, {counts['block']} block"
            )
            print(f"Portfolio report: {Path(args.out).resolve() / 'local_skills_report.md'}")
        return

    if args.command == "remediate":
        try:
            payload = remediate_skill(args.path, args.out, threshold=args.threshold)
        except Exception as exc:  # pragma: no cover - CLI guard
            print(f"skilltrust: {exc}", file=sys.stderr)
            raise SystemExit(2)
        if args.format == "json":
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(
                f"Remediation bundle ready for {payload['skill']}: "
                f"{payload['install_decision']['action']} "
                f"({payload['score_before']} -> {payload['score_after_policy_overlay']} projected)"
            )
            print(f"Bundle written to: {Path(args.out).resolve()}")
        return

    if args.command == "install-check":
        analyzer = SkillTrustAnalyzer()
        try:
            result = analyzer.analyze(args.path)
        except Exception as exc:  # pragma: no cover - CLI guard
            print(f"skilltrust: {exc}", file=sys.stderr)
            raise SystemExit(2)
        decision = install_decision(result, threshold=args.threshold)
        if args.out:
            out_dir = Path(args.out)
            write_outputs(out_dir, result)
            (out_dir / "install_decision.json").write_text(
                json.dumps(decision, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
        if args.format == "json":
            print(json.dumps(decision, indent=2, ensure_ascii=False))
        else:
            print(
                f"Install gate: {decision['action']} "
                f"for {Path(args.path).name} "
                f"({decision['score']}/100, {decision['risk_level']})"
            )
            print(decision["reason"])
            if args.out:
                print(f"Artifacts written to: {Path(args.out).resolve()}")
        if decision["action"] == "block":
            raise SystemExit(1)
        return

    if args.command == "authoring-audit":
        try:
            analysis = analyze_authoring(args.path)
        except Exception as exc:  # pragma: no cover - CLI guard
            print(f"skilltrust: {exc}", file=sys.stderr)
            raise SystemExit(2)
        if args.out:
            write_authoring_outputs(args.out, analysis)
        if args.format == "json":
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
        else:
            print(
                f"Authoring harness: {analysis['harness_fit_score']}/100 "
                f"({analysis['harness_level']})"
            )
            print(
                f"SKILL.md body: {analysis['metrics']['body_lines']} lines, "
                f"{analysis['metrics']['move_candidate_sections']} move candidates"
            )
            if args.out:
                print(f"Authoring artifacts written to: {Path(args.out).resolve()}")
        return

    if args.command == "token-optimize":
        try:
            analysis = analyze_token_efficiency(args.path)
        except Exception as exc:  # pragma: no cover - CLI guard
            print(f"skilltrust: {exc}", file=sys.stderr)
            raise SystemExit(2)
        if args.out:
            write_token_outputs(args.out, analysis)
        if args.format == "json":
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
        else:
            metrics = analysis["metrics"]
            print(
                f"Token efficiency: {analysis['token_efficiency_score']}/100 "
                f"({analysis['token_efficiency_level']})"
            )
            print(
                f"Activation body: ~{metrics['activation_body_tokens_estimate']} tokens, "
                f"estimated saved: {metrics['estimated_tokens_saved']}, "
                f"candidates: {metrics['scriptification_candidates']}"
            )
            if args.out:
                print(f"Token artifacts written to: {Path(args.out).resolve()}")
        return

    if args.command == "taxonomy-audit":
        try:
            analysis = analyze_taxonomy(args.skills_root)
            write_taxonomy_outputs(args.out, analysis)
        except Exception as exc:  # pragma: no cover - CLI guard
            print(f"skilltrust: {exc}", file=sys.stderr)
            raise SystemExit(2)
        if args.format == "json":
            print(json.dumps(analysis, indent=2, ensure_ascii=False))
        else:
            print(
                f"Taxonomy: {analysis['taxonomy_score']}/100 "
                f"({analysis['taxonomy_level']})"
            )
            print(
                f"Skills: {analysis['skill_count']}, findings: {len(analysis['findings'])}, "
                f"rename/description plan items: {len(analysis['rename_plan'])}"
            )
            print(f"Taxonomy artifacts written to: {Path(args.out).resolve()}")
        return


if __name__ == "__main__":
    main()
