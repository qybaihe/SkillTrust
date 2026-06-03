"use client";

import {
  AlertTriangle,
  Archive,
  Brain,
  CheckCircle2,
  ChevronRight,
  Download,
  FileJson,
  FileText,
  FolderUp,
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

type Lang = "en" | "zh";
type Copy = (typeof COPY)["en"] | (typeof COPY)["zh"];

const COPY = {
  en: {
    language: "Language",
    hackathon: "UCWS Singapore Hackathon 2026 · Skill Track",
    title: "SkillTrust Governance Console",
    architecture: "Architecture",
    fusedReport: "Fused Report",
    heroEyebrow: "Intent-Bound Permission Governance",
    heroTitle: "Upload, audit, fuse Agent judgment, then download a governed Skill.",
    workflowLabel: "SkillTrust demo workflow",
    flow: ["Upload Skill", "Analyze Intent", "Review Permissions", "Fuse Agent Judgment", "Download Optimized Skill"],
    uploadAria: "Upload Skill package",
    folderAria: "Upload Skill folder",
    uploadPrompt: "Drop in a .zip package or select SKILL.md",
    folderPrompt: "Upload Folder",
    uploadNote: "Runs inside demo-web/.runs and never installs the uploaded Skill.",
    analyzeSkill: "Analyze Skill",
    analyzingFolder: "Analyzing folder...",
    chooseFileError: "Choose a .zip package or a SKILL.md file first.",
    pipelineStatus: "Pipeline Status",
    agentRuntime: "Agent Runtime",
    agentAdapter: "Pi-compatible Review Adapter",
    agentFallback: "Semantic review is server-side optional; deterministic fallback keeps the demo flow complete.",
    agentMimo: "via OpenAI-compatible Chat Completions",
    finalAction: "Final Action",
    trustFitScore: "Trust Fit Score",
    fusedScore: "Fused Score",
    riskLevel: "Risk Level",
    intentBoundary: "Intent Boundary",
    noDeclaredIntent: "No declared intent was detected.",
    permissionOverreach: "Permission Overreach",
    noOverreach: "No material permission overreach was detected.",
    requiredObserved: "Required vs Observed Permissions",
    requiredPermissions: "Required Permissions",
    observedPermissions: "Observed / Requested Permissions",
    noRequiredPermissions: "No required permission rows were generated.",
    noObservedPermissions: "No observed permission requests were found.",
    agentSemanticReview: "Agent Semantic Review",
    declaredBoundary: "Declared boundary",
    recommendation: "Recommendation",
    semanticEvidencePreserved: "Semantic reviewer preserved deterministic evidence.",
    inScope: "In scope",
    outOfScope: "Out of scope",
    requiresConfirmation: "Requires confirmation",
    noneSpecified: "None specified.",
    noSemanticAssessments: "No semantic finding assessments were returned.",
    finding: "Finding",
    semanticFit: "Semantic Fit",
    confidence: "Confidence",
    rationale: "Rationale",
    criticalDataFlow: "Critical Data-Flow Protection",
    noCriticalDataFlow: "No critical sensitive-source-to-network-sink flow was found.",
    policyOverlay: "Policy Overlay",
    optimizationDownloads: "Optimization Summary & Downloads",
    noRemediation: "Preserve the generated least-privilege policy; no remediation is required.",
    reviewMode: "Review mode",
    semanticReview: "semantic review",
    downloads: {
      optimized: "Optimized Skill zip",
      artifacts: "All artifacts zip",
      trustReport: "Trust report",
      manifest: "Permission manifest",
      policy: "Policy overlay",
      receipt: "Audit receipt",
      remediation: "Remediation plan"
    },
    deterministicEvidence: "Deterministic Evidence Table",
    noFindings: "The deterministic scanner produced no findings.",
    table: {
      id: "ID",
      severity: "Severity",
      location: "Location",
      evidence: "Evidence",
      policyEffect: "Policy Effect"
    },
    policyLabels: {
      fsAllow: "Filesystem read allow",
      fsDeny: "Filesystem read deny",
      networkDefault: "Network default",
      networkDeny: "Network deny",
      shellAllow: "Shell allow",
      shellDeny: "Shell deny",
      none: "None",
      notSpecified: "not specified"
    },
    steps: {
      unpack: "Unpack Skill",
      deterministic: "Deterministic Evidence",
      semantic: "Agent Semantic Review",
      fusion: "Policy Fusion",
      package: "Optimized Package",
      complete: "Complete"
    },
    stepCaptions: {
      waiting: "Waiting.",
      running: "Running now.",
      completed: "Completed.",
      fallbackCompleted: "Fallback review completed.",
      mimoCompleted: "MIMO semantic reviewer completed."
    },
    fixtures: {
      benign: {
        label: "Try benign PDF Skill",
        detail: "Clean PDF summarization with scoped file access."
      },
      overprivileged: {
        label: "Try overprivileged research Skill",
        detail: "Good intent, but asks for home, env, and telemetry surfaces."
      },
      malicious: {
        label: "Try malicious-like writing Skill",
        detail: "Hidden prompt bypass plus sensitive data-flow to network sink."
      }
    }
  },
  zh: {
    language: "语言",
    hackathon: "UCWS Singapore Hackathon 2026 · Skill 赛道",
    title: "SkillTrust 治理控制台",
    architecture: "架构图",
    fusedReport: "融合报告",
    heroEyebrow: "意图绑定权限治理",
    heroTitle: "上传、审计、融合 Agent 判断，并下载受治理的 Skill。",
    workflowLabel: "SkillTrust 演示流程",
    flow: ["上传 Skill", "分析意图", "审查权限", "融合 Agent 判断", "下载优化版 Skill"],
    uploadAria: "上传 Skill package",
    folderAria: "上传 Skill 文件夹",
    uploadPrompt: "选择 .zip package 或 SKILL.md",
    folderPrompt: "上传文件夹",
    uploadNote: "只在 demo-web/.runs 内处理，不会安装上传的 Skill。",
    analyzeSkill: "开始分析",
    analyzingFolder: "正在分析文件夹...",
    chooseFileError: "请先选择 .zip package 或 SKILL.md 文件。",
    pipelineStatus: "流程状态",
    agentRuntime: "Agent 运行时",
    agentAdapter: "Pi-compatible 审查适配器",
    agentFallback: "语义审查由服务端可选启用；fallback 也能跑完整演示流程。",
    agentMimo: "通过 OpenAI-compatible Chat Completions",
    finalAction: "最终动作",
    trustFitScore: "Trust Fit 分数",
    fusedScore: "融合分数",
    riskLevel: "风险等级",
    intentBoundary: "意图边界",
    noDeclaredIntent: "没有检测到明确意图。",
    permissionOverreach: "权限越界",
    noOverreach: "没有检测到实质性权限越界。",
    requiredObserved: "所需权限 vs 观测权限",
    requiredPermissions: "所需权限",
    observedPermissions: "观测 / 请求权限",
    noRequiredPermissions: "没有生成所需权限条目。",
    noObservedPermissions: "没有发现观测权限请求。",
    agentSemanticReview: "Agent 语义审查",
    declaredBoundary: "声明边界",
    recommendation: "审查建议",
    semanticEvidencePreserved: "语义审查已保留 deterministic evidence。",
    inScope: "范围内",
    outOfScope: "范围外",
    requiresConfirmation: "需要用户确认",
    noneSpecified: "未指定。",
    noSemanticAssessments: "没有返回语义 finding 评估。",
    finding: "Finding",
    semanticFit: "语义匹配",
    confidence: "置信度",
    rationale: "理由",
    criticalDataFlow: "关键数据流保护",
    noCriticalDataFlow: "没有发现关键敏感源到网络出口的数据流。",
    policyOverlay: "策略覆盖层",
    optimizationDownloads: "优化摘要与下载",
    noRemediation: "保留生成的最小权限策略；无需 remediation。",
    reviewMode: "审查模式",
    semanticReview: "语义审查",
    downloads: {
      optimized: "优化版 Skill zip",
      artifacts: "全部 artifacts zip",
      trustReport: "Trust report",
      manifest: "权限 manifest",
      policy: "策略 overlay",
      receipt: "审计 receipt",
      remediation: "Remediation plan"
    },
    deterministicEvidence: "Deterministic Evidence 表",
    noFindings: "deterministic scanner 没有产生 finding。",
    table: {
      id: "ID",
      severity: "严重性",
      location: "位置",
      evidence: "证据",
      policyEffect: "策略效果"
    },
    policyLabels: {
      fsAllow: "文件读取允许",
      fsDeny: "文件读取拒绝",
      networkDefault: "网络默认策略",
      networkDeny: "网络拒绝",
      shellAllow: "Shell 允许",
      shellDeny: "Shell 拒绝",
      none: "无",
      notSpecified: "未指定"
    },
    steps: {
      unpack: "解包 Skill",
      deterministic: "确定性证据",
      semantic: "Agent 语义审查",
      fusion: "策略融合",
      package: "优化包",
      complete: "完成"
    },
    stepCaptions: {
      waiting: "等待中。",
      running: "运行中。",
      completed: "已完成。",
      fallbackCompleted: "Fallback 审查已完成。",
      mimoCompleted: "MIMO 语义审查已完成。"
    },
    fixtures: {
      benign: {
        label: "试用良性 PDF Skill",
        detail: "干净的 PDF 总结，只使用限定文件访问。"
      },
      overprivileged: {
        label: "试用越权 Research Skill",
        detail: "意图合理，但请求 home、env 和遥测面。"
      },
      malicious: {
        label: "试用恶意特征 Writing Skill",
        detail: "包含隐藏 prompt bypass 和敏感数据流。"
      }
    }
  }
} as const;

const STEPS: Array<{ id: DemoStep; icon: typeof UploadCloud }> = [
  { id: "unpack", icon: UploadCloud },
  { id: "deterministic", icon: Radar },
  { id: "semantic", icon: Brain },
  { id: "fusion", icon: ShieldCheck },
  { id: "package", icon: PackageCheck }
];

const FIXTURES = [
  {
    id: "benign-pdf-skill",
    copyKey: "benign",
    expected: "allow",
  },
  {
    id: "overprivileged-research-skill",
    copyKey: "overprivileged",
    expected: "warn",
  },
  {
    id: "malicious-like-writing-skill",
    copyKey: "malicious",
    expected: "block",
  }
] as const;

export default function Home() {
  const [lang, setLang] = useState<Lang>("en");
  const [file, setFile] = useState<File | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [activeStep, setActiveStep] = useState<DemoStep>("unpack");
  const [summary, setSummary] = useState<DemoSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const folderInputRef = useRef<HTMLInputElement | null>(null);
  const t = COPY[lang];

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
      setError(t.chooseFileError);
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

  async function onFolderChange(event: ChangeEvent<HTMLInputElement>) {
    const files = Array.from(event.target.files || []);
    event.target.value = "";
    if (!files.length) {
      return;
    }
    setFile(null);
    setError(null);
    const form = new FormData();
    for (const item of files) {
      form.append("files[]", item);
      form.append("paths[]", item.webkitRelativePath || item.name);
    }
    await startAnalysis(form);
  }

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand">
          <span className="brand-mark" aria-hidden="true">
            <ShieldCheck size={18} />
          </span>
          <div>
            <p className="eyebrow">{t.hackathon}</p>
            <h1>{t.title}</h1>
          </div>
        </div>
        <div className="top-actions">
          <div className="language-toggle" aria-label={t.language}>
            <button className={lang === "en" ? "active" : ""} type="button" onClick={() => setLang("en")}>
              EN
            </button>
            <button className={lang === "zh" ? "active" : ""} type="button" onClick={() => setLang("zh")}>
              中文
            </button>
          </div>
          <a className="ghost-link" href="/api/assets/skilltrust-cover" target="_blank" rel="noreferrer">
            <FileText size={16} />
            {t.architecture}
          </a>
          {summary ? (
            <a className="ghost-link" href={`/api/runs/${summary.run_id}/report`} target="_blank" rel="noreferrer">
              <FileText size={16} />
              {t.fusedReport}
            </a>
          ) : null}
        </div>
      </header>

      <section className="console-grid">
        <div className="intake-panel">
          <div className="cover-strip">
            <img src="/api/assets/skilltrust-cover" alt="SkillTrust architecture" />
            <div>
              <p className="eyebrow">{t.heroEyebrow}</p>
              <h2>{t.heroTitle}</h2>
            </div>
          </div>

          <div className="flow-strip" aria-label={t.workflowLabel}>
            {t.flow.map((item, index) => (
                <div className="flow-item" key={item}>
                  <span>{index + 1}</span>
                  <p>{item}</p>
                  {index < 4 ? <ChevronRight size={14} aria-hidden="true" /> : null}
                </div>
              ))}
          </div>

          <form className="upload-zone" onSubmit={submitAnalyze}>
            <input
              ref={fileInputRef}
              type="file"
              accept=".zip,.md"
              onChange={onFileChange}
              aria-label={t.uploadAria}
            />
            <input
              ref={folderInputRef}
              className="folder-input"
              type="file"
              multiple
              onChange={onFolderChange}
              aria-label={t.folderAria}
              {...{ webkitdirectory: "", directory: "" }}
            />
            <button className="drop-target" type="button" onClick={() => fileInputRef.current?.click()}>
              <UploadCloud size={34} />
              <span>{file ? file.name : t.uploadPrompt}</span>
              <small>{t.uploadNote}</small>
            </button>
            <div className="upload-actions">
              <button className="primary-button" type="submit" disabled={isRunning || !file}>
                {isRunning ? <RefreshCw size={18} className="spin" /> : <Zap size={18} />}
                {t.analyzeSkill}
              </button>
              <button className="secondary-button" type="button" disabled={isRunning} onClick={() => folderInputRef.current?.click()}>
                <FolderUp size={18} />
                {isRunning ? t.analyzingFolder : t.folderPrompt}
              </button>
            </div>
          </form>

          <div className="fixture-row">
            {FIXTURES.map((fixture) => (
              <button className="fixture-button" key={fixture.id} onClick={() => runFixture(fixture.id)} disabled={isRunning}>
                <span className={`mini-badge ${fixture.expected}`}>{fixture.expected}</span>
                <strong>{t.fixtures[fixture.copyKey].label}</strong>
                <small>{t.fixtures[fixture.copyKey].detail}</small>
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
            <h2>{t.pipelineStatus}</h2>
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
                    <strong>{t.steps[step.id]}</strong>
                    <small>{stepCaption(step.id, summary, state, t)}</small>
                  </div>
                  <span className="step-number">{index + 1}</span>
                </div>
              );
            })}
          </div>

          <div className="agent-card">
            <div>
              <p className="eyebrow">{t.agentRuntime}</p>
              <h3>{t.agentAdapter}</h3>
            </div>
            <p>
              {summary?.agent_review.mode === "mimo"
                ? `${summary.agent_review.model} ${t.agentMimo}`
                : t.agentFallback}
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
                <p className="eyebrow">{t.finalAction}</p>
                <h2>{summary.decision.final_action}</h2>
                <p>{summary.decision.conservative_reason}</p>
              </div>
            </div>
            <div className="metrics">
              <Metric label={t.trustFitScore} value={`${summary.decision.trust_fit_score}`} icon={Gauge} />
              <Metric label={t.fusedScore} value={`${summary.decision.final_score}`} icon={ShieldCheck} />
              <Metric label={t.riskLevel} value={summary.decision.risk_level} icon={AlertTriangle} />
            </div>
          </div>

          <div className="summary-panel">
            <div className="panel-title">
              <LockKeyhole size={18} />
              <h2>{t.intentBoundary}</h2>
            </div>
            <p className="summary-text">{summary.declared_intent.summary || t.noDeclaredIntent}</p>
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
              <h2>{t.permissionOverreach}</h2>
            </div>
            {summary.permission_overreach.length ? (
              <div className="overreach-grid">
                {summary.permission_overreach.slice(0, 6).map((finding) => (
                  <FindingCard key={finding.id} finding={finding} />
                ))}
              </div>
            ) : (
              <EmptyLine text={t.noOverreach} />
            )}
          </div>

          <div className="wide-panel">
            <div className="panel-title">
              <FileJson size={18} />
              <h2>{t.requiredObserved}</h2>
            </div>
            <div className="permission-grid">
              <PermissionList title={t.requiredPermissions} data={summary.required_permissions} emptyText={t.noRequiredPermissions} />
              <ObservedList title={t.observedPermissions} items={summary.observed_permissions} emptyText={t.noObservedPermissions} />
            </div>
          </div>

          <div className="wide-panel">
            <div className="panel-title">
              <Brain size={18} />
              <h2>{t.agentSemanticReview}</h2>
            </div>
            <div className="semantic-grid">
              <div>
                <p className="section-kicker">{t.declaredBoundary}</p>
                <p>{summary.semantic_review.declared_boundary_summary || summary.semantic_review.reading_summary}</p>
              </div>
              <div>
                <p className="section-kicker">{t.recommendation}</p>
                <p>{summary.semantic_review.recommendation_reason || t.semanticEvidencePreserved}</p>
              </div>
              <BoundaryColumn title={t.inScope} values={summary.semantic_review.task_boundary.in_scope} noneText={t.noneSpecified} />
              <BoundaryColumn title={t.outOfScope} values={summary.semantic_review.task_boundary.out_of_scope} noneText={t.noneSpecified} />
              <BoundaryColumn
                title={t.requiresConfirmation}
                values={summary.semantic_review.task_boundary.requires_user_confirmation}
                noneText={t.noneSpecified}
              />
            </div>
            <AssessmentTable assessments={summary.semantic_review.finding_assessments} copy={t} />
          </div>

          <div className="split-panels">
            <div className="summary-panel">
              <div className="panel-title">
                <AlertTriangle size={18} />
                <h2>{t.criticalDataFlow}</h2>
              </div>
              {summary.critical_data_flow.length ? (
                summary.critical_data_flow.map((finding) => <FindingCard key={finding.id} finding={finding} compact />)
              ) : (
                <EmptyLine text={t.noCriticalDataFlow} />
              )}
            </div>

            <div className="summary-panel">
              <div className="panel-title">
                <ShieldCheck size={18} />
                <h2>{t.policyOverlay}</h2>
              </div>
              <PolicyOverlay policy={summary.policy_overlay} copy={t} />
            </div>
          </div>

          <div className="wide-panel">
            <div className="panel-title">
              <Archive size={18} />
              <h2>{t.optimizationDownloads}</h2>
            </div>
            <div className="download-layout">
              <div>
                <ul className="compact-list">
                  {summary.remediation_suggestions.length ? (
                    summary.remediation_suggestions.map((item) => <li key={item}>{item}</li>)
                  ) : (
                    <li>{t.noRemediation}</li>
                  )}
                </ul>
                <p className="fallback-note">
                  {t.reviewMode}:{" "}
                  {summary.agent_review.mode === "mimo"
                    ? `${summary.agent_review.model} ${t.semanticReview}`
                    : summary.agent_review.fallback_reason}
                </p>
              </div>
              <div className="download-grid">
                <DownloadButton href={summary.downloads.optimized_skill_zip} label={t.downloads.optimized} icon={PackageCheck} />
                <DownloadButton href={summary.downloads.artifacts_zip} label={t.downloads.artifacts} icon={Archive} />
                <DownloadButton href={summary.downloads.trust_report} label={t.downloads.trustReport} icon={FileText} />
                <DownloadButton href={summary.downloads.permission_manifest} label={t.downloads.manifest} icon={FileJson} />
                <DownloadButton href={summary.downloads.policy_overlay} label={t.downloads.policy} icon={ShieldCheck} />
                <DownloadButton href={summary.downloads.audit_receipt} label={t.downloads.receipt} icon={CheckCircle2} />
                <DownloadButton href={summary.downloads.remediation_plan} label={t.downloads.remediation} icon={AlertTriangle} />
              </div>
            </div>
          </div>

          <div className="wide-panel">
            <div className="panel-title">
              <FileText size={18} />
              <h2>{t.deterministicEvidence}</h2>
            </div>
            {summary.deterministic_findings.length ? (
              <EvidenceTable groups={findingsByCategory} copy={t} />
            ) : (
              <EmptyLine text={t.noFindings} />
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

function PermissionList({
  title,
  data,
  emptyText
}: {
  title: string;
  data: DemoSummary["required_permissions"];
  emptyText: string;
}) {
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
        <EmptyLine text={emptyText} />
      )}
    </div>
  );
}

function ObservedList({ title, items, emptyText }: { title: string; items: ObservedPermission[]; emptyText: string }) {
  return (
    <div className="permission-column">
      <h3>{title}</h3>
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
        <EmptyLine text={emptyText} />
      )}
    </div>
  );
}

function BoundaryColumn({ title, values, noneText }: { title: string; values: string[]; noneText: string }) {
  return (
    <div className="boundary-column">
      <p className="section-kicker">{title}</p>
      <ul>
        {(values || []).slice(0, 4).map((value) => (
          <li key={value}>{value}</li>
        ))}
        {!values?.length ? <li>{noneText}</li> : null}
      </ul>
    </div>
  );
}

function AssessmentTable({ assessments, copy }: { assessments: SemanticAssessment[]; copy: Copy }) {
  if (!assessments.length) {
    return <EmptyLine text={copy.noSemanticAssessments} />;
  }
  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            <th>{copy.finding}</th>
            <th>{copy.semanticFit}</th>
            <th>{copy.confidence}</th>
            <th>{copy.rationale}</th>
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

function PolicyOverlay({ policy, copy }: { policy: Record<string, unknown>; copy: Copy }) {
  const filesystem = policy.filesystem as Record<string, string[]> | undefined;
  const network = policy.network as Record<string, unknown> | undefined;
  const shell = policy.shell as Record<string, string[]> | undefined;
  return (
    <div className="policy-stack">
      <PolicyLine label={copy.policyLabels.fsAllow} values={filesystem?.allow_read} noneText={copy.policyLabels.none} />
      <PolicyLine label={copy.policyLabels.fsDeny} values={filesystem?.deny_read} noneText={copy.policyLabels.none} />
      <PolicyLine
        label={copy.policyLabels.networkDefault}
        values={[String(network?.default || copy.policyLabels.notSpecified)]}
        noneText={copy.policyLabels.none}
      />
      <PolicyLine
        label={copy.policyLabels.networkDeny}
        values={network?.deny as string[] | undefined}
        noneText={copy.policyLabels.none}
      />
      <PolicyLine label={copy.policyLabels.shellAllow} values={shell?.allow} noneText={copy.policyLabels.none} />
      <PolicyLine label={copy.policyLabels.shellDeny} values={shell?.deny} noneText={copy.policyLabels.none} />
    </div>
  );
}

function PolicyLine({ label, values, noneText }: { label: string; values?: string[]; noneText: string }) {
  return (
    <div className="policy-line">
      <span>{label}</span>
      <strong>{values?.slice(0, 4).join(", ") || noneText}</strong>
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

function EvidenceTable({ groups, copy }: { groups: Record<string, Finding[]>; copy: Copy }) {
  return (
    <div className="evidence-groups">
      {Object.entries(groups).map(([category, findings]) => (
        <div className="evidence-group" key={category}>
          <h3>{category}</h3>
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>{copy.table.id}</th>
                  <th>{copy.table.severity}</th>
                  <th>{copy.table.location}</th>
                  <th>{copy.table.evidence}</th>
                  <th>{copy.table.policyEffect}</th>
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

function stepCaption(step: DemoStep, summary: DemoSummary | null, state: string, copy: Copy) {
  if (summary) {
    if (step === "semantic") {
      return summary.agent_review.mode === "mimo" ? copy.stepCaptions.mimoCompleted : copy.stepCaptions.fallbackCompleted;
    }
    return copy.stepCaptions.completed;
  }
  if (state === "active") {
    return copy.stepCaptions.running;
  }
  if (state === "done") {
    return copy.stepCaptions.completed;
  }
  return copy.stepCaptions.waiting;
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
