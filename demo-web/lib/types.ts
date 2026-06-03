export type Action = "allow" | "warn" | "block";

export type DemoStep =
  | "unpack"
  | "deterministic"
  | "semantic"
  | "fusion"
  | "package"
  | "complete";

export type StatusState = "queued" | "running" | "completed" | "failed";

export type Finding = {
  id: string;
  severity: string;
  category: string;
  file: string;
  line: number;
  evidence: string;
  declared_intent_relation: string;
  why_it_matters: string;
  recommendation: string;
  policy_effect: string;
  confidence: string;
};

export type ObservedPermission = {
  category: string;
  permission: string;
  file: string;
  line: number;
  evidence: string;
  relation: string;
  severity_hint: string;
};

export type SemanticAssessment = {
  finding_id: string;
  semantic_fit: string;
  rationale: string;
  recommended_policy_change: string;
  confidence: string;
};

export type DemoSummary = {
  run_id: string;
  status: StatusState;
  step: DemoStep;
  created_at: string;
  completed_at?: string;
  input: {
    name: string;
    kind: "fixture" | "zip" | "skill-md";
    skill_path: string;
  };
  agent_review: {
    mode: "mimo" | "deterministic-fallback";
    model?: string;
    base_url?: string;
    fallback_reason?: string;
  };
  decision: {
    final_action: Action;
    deterministic_action: Action;
    semantic_recommendation: Action;
    trust_fit_score: number;
    final_score: number;
    risk_level: string;
    conservative_reason: string;
    critical_dataflow_protected: boolean;
  };
  declared_intent: {
    summary: string;
    primary_intents: string[];
    clarity_score: number;
    boundaries: string[];
  };
  required_permissions: Record<string, Array<Record<string, string>> | string[]>;
  observed_permissions: ObservedPermission[];
  permission_overreach: Finding[];
  deterministic_findings: Finding[];
  semantic_review: {
    declared_boundary_summary: string;
    reading_summary: string;
    recommendation_reason: string;
    task_boundary: {
      in_scope: string[];
      out_of_scope: string[];
      requires_user_confirmation: string[];
    };
    finding_assessments: SemanticAssessment[];
    likely_false_positives: SemanticAssessment[];
    policy_refinements: Array<Record<string, string>>;
  };
  critical_data_flow: Finding[];
  policy_overlay: Record<string, unknown>;
  remediation_suggestions: string[];
  downloads: {
    optimized_skill_zip: string;
    artifacts_zip: string;
    trust_report: string;
    permission_manifest: string;
    policy_overlay: string;
    audit_receipt: string;
    remediation_plan: string;
  };
};
