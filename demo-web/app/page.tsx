"use client";

import {
  AlertTriangle,
  Archive,
  Brain,
  CheckCircle2,
  ChevronRight,
  Download,
  FileArchive,
  FileJson,
  FileText,
  Gauge,
  LockKeyhole,
  PackageCheck,
  Radar,
  RefreshCw,
  ShieldCheck,
  ShieldX,
  Sparkles,
  UploadCloud,
  Zap
} from "lucide-react";
import { ChangeEvent, FormEvent, useEffect, useMemo, useRef, useState } from "react";
import type { Action, DemoSummary, DemoStep, Finding, ObservedPermission, SemanticAssessment } from "../lib/types";

const STEPS: Array<{ id: DemoStep; label: string; icon: typeof UploadCloud }> = [
  { id: "unpack", label: "Unpack Skill", icon: UploadCloud },
  { id: "deterministic", label: "Deterministic Evidence", icon: Radar },
  { id: "semantic", label: "Agent Semantic Review", icon: Brain },
  { id: "fusion", label: "Policy Fusion", icon: ShieldCheck },
  { id: "package", label: "Optimized Package", icon: PackageCheck }
];

const FIXTURES = [
  {
    id: "benign-pdf-skill",
    label: "Try benign PDF Skill",
    expected: "allow",
    detail: "Clean PDF summarization with scoped file access."
  },
  {
    id: "overprivileged-research-skill",
    label: "Try overprivileged research Skill",
    expected: "warn",
    detail: "Good intent, but asks for home, env, and telemetry surfaces."
  },
  {
    id: "malicious-like-writing-skill",
    label: "Try malicious-like writing Skill",
    expected: "block",
    detail: "Hidden prompt bypass plus sensitive data-flow to network sink."
  }
];

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [activeStep, setActiveStep] = useState<DemoStep>("unpack");
  const [summary, setSummary] = useState<DemoSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    if (!isRunning) {
      return;
    }
    let index = 0;
    const timer = window.setInterval(() => {
      index = Math.min(index + 1, STEPS.length - 1);
      setActiveStep(STEPS[index].id);
    }, 1100);
    return () => window.clearInterval(timer);
  }, [isRunning]);

  const actionTone = summary ? toneForAction(summary.decision.final_action) : "neutral";
  const findingsByCategory = useMemo(() => groupByCategory(summary?.deterministic_findings || []), [summary]);

  async function submitAnalyze(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!file) {
      setError("Choose a .zip package or a SKILL.md file first.");
      return;
    }
    const form = new FormData();
    form.append("file", file);
    await startAnalysis(form);
  }

  async function runFixture(fixture: string) {
    const form = new FormData();
    form.append("fixture", fixture);
    await startAnalysis(form);
  }

  async function startAnalysis(form: FormData) {
    setError(null);
    setSummary(null);
    setIsRunning(true);
    setActiveStep("unpack");
    try {
      const response = await fetch("/api/analyze", {
        method: "POST",
        body: form
      });
      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || "Analysis failed.");
      }
      setSummary(payload as DemoSummary);
      setActiveStep("complete");
    } catch (analysisError) {
      setError(analysisError instanceof Error ? analysisError.message : String(analysisError));
    } finally {
      setIsRunning(false);
    }
  }

  function onFileChange(event: ChangeEvent<HTMLInputElement>) {
    setFile(event.target.files?.[0] || null);
    setError(null);
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">
            <ShieldCheck size={18} />
          </span>
          <div>
            <p className="eyebrow">UCWS Singapore Hackathon 2026 · Skill Track</p>
            <h1>SkillTrust Governance Console</h1>
          </div>
        </div>
        <div className="top-actions">
          <a className="ghost-link" href="/api/assets/skilltrust-cover" target="_blank" rel="noreferrer">
            <FileText size={16} />
            Architecture
          </a>
          {summary ? (
            <a className="ghost-link" href={`/api/runs/${summary.run_id}/report`} target="_blank" rel="noreferrer">
              <FileText size={16} />
              Fused Report
            </a>
          ) : null}
        </div>
      </header>

      <section className="console-grid">
        <div className="intake-panel">
          <div className="cover-strip">
            <img src="/api/assets/skilltrust-cover" alt="SkillTrust architecture" />
            <div>
              <p className="eyebrow">Intent-Bound Permission Governance</p>
              <h2>Upload, audit, fuse Agent judgment, then download a governed Skill.</h2>
            </div>
          </div>

          <div className="flow-strip" aria-label="SkillTrust demo workflow">
            {["Upload Skill", "Analyze Intent", "Review Permissions", "Fuse Agent Judgment", "Download Optimized Skill"].map(
              (item, index) => (
                <div className="flow-item" key={item}>
                  <span>{index + 1}</span>
                  <p>{item}</p>
                  {index < 4 ? <ChevronRight size={14} aria-hidden="true" /> : null}
                </div>
              )
            )}
          </div>

          <form className="upload-zone" onSubmit={submitAnalyze}>
            <input
              ref={fileInputRef}
              type="file"
              accept=".zip,.md"
              onChange={onFileChange}
              aria-label="Upload Skill package"
            />
            <button className="drop-target" type="button" onClick={() => fileInputRef.current?.click()}>
              <UploadCloud size={34} />
              <span>{file ? file.name : "Drop in a .zip package or select SKILL.md"}</span>
              <small>Runs inside demo-web/.runs and never installs the uploaded Skill.</small>
            </button>
            <button className="primary-button" type="submit" disabled={isRunning || !file}>
              {isRunning ? <RefreshCw size={18} className="spin" /> : <Zap size={18} />}
              Analyze Skill
            </button>
          </form>

          <div className="fixture-row">
            {FIXTURES.map((fixture) => (
              <button className="fixture-button" key={fixture.id} onClick={() => runFixture(fixture.id)} disabled={isRunning}>
                <span className={`mini-badge ${fixture.expected}`}>{fixture.expected}</span>
                <strong>{fixture.label}</strong>
                <small>{fixture.detail}</small>
              </button>
            ))}
          </div>

          {error ? (
            <div className="error-banner">
              <AlertTriangle size={18} />
              <span>{error}</span>
            </div>
          ) : null}
        </div>

        <aside className="status-panel">
          <div className="panel-title">
            <Sparkles size={18} />
            <h2>Pipeline Status</h2>
          </div>
          <div className="step-stack">
            {STEPS.map((step, index) => {
              const state = stepState(step.id, activeStep, isRunning, Boolean(summary));
              const Icon = step.icon;
              return (
                <div className={`step ${state}`} key={step.id}>
                  <span className="step-icon">
                    <Icon size={17} />
                  </span>
                  <div>
                    <strong>{step.label}</strong>
                    <small>{stepCaption(step.id, summary, state)}</small>
                  </div>
                  <span className="step-number">{index + 1}</span>
                </div>
              );
            })}
          </div>

          <div className="agent-card">
            <div>
              <p className="eyebrow">Agent Runtime</p>
              <h3>Pi-compatible Review Adapter</h3>
            </div>
            <p>
              {summary?.agent_review.mode === "mimo"
                ? `${summary.agent_review.model} via OpenAI-compatible Chat Completions`
                : "MIMO-ready; deterministic fallback is shown when no key is configured or the endpoint is unavailable."}
            </p>
          </div>
        </aside>
      </section>

      {summary ? (
        <section className="results-grid">
          <div className={`decision-panel ${actionTone}`}>
            <div className="decision-main">
              <ActionIcon action={summary.decision.final_action} />
              <div>
                <p className="eyebrow">Final Action</p>
                <h2>{summary.decision.final_action}</h2>
                <p>{summary.decision.conservative_reason}</p>
              </div>
            </div>
            <div className="metrics">
              <Metric label="Trust Fit Score" value={`${summary.decision.trust_fit_score}`} icon={Gauge} />
              <Metric label="Fused Score" value={`${summary.decision.final_score}`} icon={ShieldCheck} />
              <Metric label="Risk Level" value={summary.decision.risk_level} icon={AlertTriangle} />
            </div>
          </div>

          <div className="summary-panel">
            <div className="panel-title">
              <LockKeyhole size={18} />
              <h2>Intent Boundary</h2>
            </div>
            <p className="summary-text">{summary.declared_intent.summary || "No declared intent was detected."}</p>
            <div className="intent-tags">
              {summary.declared_intent.primary_intents.map((intent) => (
                <span key={intent}>{intent}</span>
              ))}
            </div>
            <ul className="compact-list">
              {summary.declared_intent.boundaries.slice(0, 4).map((boundary) => (
                <li key={boundary}>{boundary}</li>
              ))}
            </ul>
          </div>

          <div className="wide-panel">
            <div className="panel-title">
              <Radar size={18} />
              <h2>Permission Overreach</h2>
            </div>
            {summary.permission_overreach.length ? (
              <div className="overreach-grid">
                {summary.permission_overreach.slice(0, 6).map((finding) => (
                  <FindingCard key={finding.id} finding={finding} />
                ))}
              </div>
            ) : (
              <EmptyLine text="No material permission overreach was detected." />
            )}
          </div>

          <div className="wide-panel">
            <div className="panel-title">
              <FileJson size={18} />
              <h2>Required vs Observed Permissions</h2>
            </div>
            <div className="permission-grid">
              <PermissionList title="Required Permissions" data={summary.required_permissions} />
              <ObservedList items={summary.observed_permissions} />
            </div>
          </div>

          <div className="wide-panel">
            <div className="panel-title">
              <Brain size={18} />
              <h2>Agent Semantic Review</h2>
            </div>
            <div className="semantic-grid">
              <div>
                <p className="section-kicker">Declared boundary</p>
                <p>{summary.semantic_review.declared_boundary_summary || summary.semantic_review.reading_summary}</p>
              </div>
              <div>
                <p className="section-kicker">Recommendation</p>
                <p>{summary.semantic_review.recommendation_reason || "Semantic reviewer preserved deterministic evidence."}</p>
              </div>
              <BoundaryColumn title="In scope" values={summary.semantic_review.task_boundary.in_scope} />
              <BoundaryColumn title="Out of scope" values={summary.semantic_review.task_boundary.out_of_scope} />
              <BoundaryColumn
                title="Requires confirmation"
                values={summary.semantic_review.task_boundary.requires_user_confirmation}
              />
            </div>
            <AssessmentTable assessments={summary.semantic_review.finding_assessments} />
          </div>

          <div className="split-panels">
            <div className="summary-panel">
              <div className="panel-title">
                <AlertTriangle size={18} />
                <h2>Critical Data-Flow Protection</h2>
              </div>
              {summary.critical_data_flow.length ? (
                summary.critical_data_flow.map((finding) => <FindingCard key={finding.id} finding={finding} compact />)
              ) : (
                <EmptyLine text="No critical sensitive-source-to-network-sink flow was found." />
              )}
            </div>

            <div className="summary-panel">
              <div className="panel-title">
                <ShieldCheck size={18} />
                <h2>Policy Overlay</h2>
              </div>
              <PolicyOverlay policy={summary.policy_overlay} />
            </div>
          </div>

          <div className="wide-panel">
            <div className="panel-title">
              <Archive size={18} />
              <h2>Optimization Summary & Downloads</h2>
            </div>
            <div className="download-layout">
              <div>
                <ul className="compact-list">
                  {summary.remediation_suggestions.length ? (
                    summary.remediation_suggestions.map((item) => <li key={item}>{item}</li>)
                  ) : (
                    <li>Preserve the generated least-privilege policy; no remediation is required.</li>
                  )}
                </ul>
                <p className="fallback-note">
                  Review mode:{" "}
                  {summary.agent_review.mode === "mimo"
                    ? `${summary.agent_review.model} semantic review`
                    : summary.agent_review.fallback_reason}
                </p>
              </div>
              <div className="download-grid">
                <DownloadButton href={summary.downloads.optimized_skill_zip} label="Optimized Skill zip" icon={PackageCheck} />
                <DownloadButton href={summary.downloads.artifacts_zip} label="All artifacts zip" icon={Archive} />
                <DownloadButton href={summary.downloads.trust_report} label="Trust report" icon={FileText} />
                <DownloadButton href={summary.downloads.permission_manifest} label="Permission manifest" icon={FileJson} />
                <DownloadButton href={summary.downloads.policy_overlay} label="Policy overlay" icon={ShieldCheck} />
                <DownloadButton href={summary.downloads.audit_receipt} label="Audit receipt" icon={CheckCircle2} />
                <DownloadButton href={summary.downloads.remediation_plan} label="Remediation plan" icon={AlertTriangle} />
              </div>
            </div>
          </div>

          <div className="wide-panel">
            <div className="panel-title">
              <FileText size={18} />
              <h2>Deterministic Evidence Table</h2>
            </div>
            {summary.deterministic_findings.length ? (
              <EvidenceTable groups={findingsByCategory} />
            ) : (
              <EmptyLine text="The deterministic scanner produced no findings." />
            )}
          </div>
        </section>
      ) : null}
    </main>
  );
}

function Metric({ label, value, icon: Icon }: { label: string; value: string; icon: typeof Gauge }) {
  return (
    <div className="metric">
      <Icon size={17} />
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function ActionIcon({ action }: { action: Action }) {
  if (action === "allow") {
    return <ShieldCheck className="action-icon allow" size={52} />;
  }
  if (action === "block") {
    return <ShieldX className="action-icon block" size={52} />;
  }
  return <AlertTriangle className="action-icon warn" size={52} />;
}

function FindingCard({ finding, compact = false }: { finding: Finding; compact?: boolean }) {
  return (
    <article className={`finding-card ${compact ? "compact" : ""}`}>
      <div className="finding-head">
        <span className={`severity ${finding.severity}`}>{finding.severity}</span>
        <strong>{finding.id}</strong>
      </div>
      <p>{finding.recommendation}</p>
      <code>
        {finding.file}:{finding.line}
      </code>
    </article>
  );
}

function PermissionList({ title, data }: { title: string; data: DemoSummary["required_permissions"] }) {
  const rows = Object.entries(data || {}).flatMap(([category, items]) =>
    Array.isArray(items)
      ? items.map((item, index) => ({
          key: `${category}-${index}`,
          category,
          label:
            typeof item === "string"
              ? item
              : item.scope || item.command || item.constraint || item.reason || JSON.stringify(item),
          reason: typeof item === "string" ? "" : item.reason || ""
        }))
      : []
  );
  return (
    <div className="permission-column">
      <h3>{title}</h3>
      {rows.length ? (
        rows.slice(0, 12).map((row) => (
          <div className="permission-row" key={row.key}>
            <span>{row.category}</span>
            <strong>{row.label}</strong>
            {row.reason ? <small>{row.reason}</small> : null}
          </div>
        ))
      ) : (
        <EmptyLine text="No required permission rows were generated." />
      )}
    </div>
  );
}

function ObservedList({ items }: { items: ObservedPermission[] }) {
  return (
    <div className="permission-column">
      <h3>Observed / Requested Permissions</h3>
      {items.length ? (
        items.slice(0, 12).map((item, index) => (
          <div className="permission-row observed" key={`${item.permission}-${index}`}>
            <span>{item.category}</span>
            <strong>{item.permission}</strong>
            <small>
              {item.file}:{item.line} · {item.relation}
            </small>
          </div>
        ))
      ) : (
        <EmptyLine text="No observed permission requests were found." />
      )}
    </div>
  );
}

function BoundaryColumn({ title, values }: { title: string; values: string[] }) {
  return (
    <div className="boundary-column">
      <p className="section-kicker">{title}</p>
      <ul>
        {(values || []).slice(0, 4).map((value) => (
          <li key={value}>{value}</li>
        ))}
        {!values?.length ? <li>None specified.</li> : null}
      </ul>
    </div>
  );
}

function AssessmentTable({ assessments }: { assessments: SemanticAssessment[] }) {
  if (!assessments.length) {
    return <EmptyLine text="No semantic finding assessments were returned." />;
  }
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Finding</th>
            <th>Semantic Fit</th>
            <th>Confidence</th>
            <th>Rationale</th>
          </tr>
        </thead>
        <tbody>
          {assessments.map((assessment) => (
            <tr key={assessment.finding_id}>
              <td>{assessment.finding_id}</td>
              <td>{assessment.semantic_fit}</td>
              <td>{assessment.confidence}</td>
              <td>{assessment.rationale}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function PolicyOverlay({ policy }: { policy: Record<string, unknown> }) {
  const filesystem = policy.filesystem as Record<string, string[]> | undefined;
  const network = policy.network as Record<string, unknown> | undefined;
  const shell = policy.shell as Record<string, string[]> | undefined;
  return (
    <div className="policy-stack">
      <PolicyLine label="Filesystem read allow" values={filesystem?.allow_read} />
      <PolicyLine label="Filesystem read deny" values={filesystem?.deny_read} />
      <PolicyLine label="Network default" values={[String(network?.default || "not specified")]} />
      <PolicyLine label="Network deny" values={network?.deny as string[] | undefined} />
      <PolicyLine label="Shell allow" values={shell?.allow} />
      <PolicyLine label="Shell deny" values={shell?.deny} />
    </div>
  );
}

function PolicyLine({ label, values }: { label: string; values?: string[] }) {
  return (
    <div className="policy-line">
      <span>{label}</span>
      <strong>{values?.slice(0, 4).join(", ") || "None"}</strong>
    </div>
  );
}

function DownloadButton({ href, label, icon: Icon }: { href: string; label: string; icon: typeof Download }) {
  return (
    <a className="download-button" href={href}>
      <Icon size={17} />
      {label}
    </a>
  );
}

function EvidenceTable({ groups }: { groups: Record<string, Finding[]> }) {
  return (
    <div className="evidence-groups">
      {Object.entries(groups).map(([category, findings]) => (
        <div className="evidence-group" key={category}>
          <h3>{category}</h3>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Severity</th>
                  <th>Location</th>
                  <th>Evidence</th>
                  <th>Policy Effect</th>
                </tr>
              </thead>
              <tbody>
                {findings.map((finding) => (
                  <tr key={finding.id}>
                    <td>{finding.id}</td>
                    <td>{finding.severity}</td>
                    <td>
                      {finding.file}:{finding.line}
                    </td>
                    <td>{finding.evidence}</td>
                    <td>{finding.policy_effect}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      ))}
    </div>
  );
}

function EmptyLine({ text }: { text: string }) {
  return <p className="empty-line">{text}</p>;
}

function stepState(step: DemoStep, active: DemoStep, isRunning: boolean, hasSummary: boolean) {
  if (hasSummary) {
    return "done";
  }
  if (!isRunning) {
    return "idle";
  }
  const activeIndex = STEPS.findIndex((item) => item.id === active);
  const stepIndex = STEPS.findIndex((item) => item.id === step);
  if (stepIndex < activeIndex) {
    return "done";
  }
  if (stepIndex === activeIndex) {
    return "active";
  }
  return "idle";
}

function stepCaption(step: DemoStep, summary: DemoSummary | null, state: string) {
  if (summary) {
    if (step === "semantic") {
      return summary.agent_review.mode === "mimo" ? "MIMO semantic reviewer completed." : "Fallback review completed.";
    }
    return "Completed.";
  }
  if (state === "active") {
    return "Running now.";
  }
  if (state === "done") {
    return "Completed.";
  }
  return "Waiting.";
}

function toneForAction(action: Action) {
  if (action === "allow") {
    return "allow";
  }
  if (action === "block") {
    return "block";
  }
  return "warn";
}

function groupByCategory(findings: Finding[]) {
  return findings.reduce<Record<string, Finding[]>>((groups, finding) => {
    groups[finding.category] ||= [];
    groups[finding.category].push(finding);
    return groups;
  }, {});
}
