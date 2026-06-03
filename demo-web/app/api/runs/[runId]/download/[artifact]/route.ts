import fs from "node:fs/promises";
import path from "node:path";
import { NextResponse } from "next/server";
import { runPath } from "../../../../../../lib/runStore";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const ARTIFACTS: Record<string, { path: string[]; type: string }> = {
  "optimized-skill.zip": { path: ["packages", "optimized-skill.zip"], type: "application/zip" },
  "artifacts.zip": { path: ["packages", "artifacts.zip"], type: "application/zip" },
  "trust_report.md": { path: ["outputs", "trust_report.md"], type: "text/markdown; charset=utf-8" },
  "permission_manifest.json": { path: ["outputs", "permission_manifest.json"], type: "application/json; charset=utf-8" },
  "skilltrust-policy.json": { path: ["fused", "skilltrust-policy.json"], type: "application/json; charset=utf-8" },
  "audit_receipt.json": { path: ["outputs", "audit_receipt.json"], type: "application/json; charset=utf-8" },
  "remediation_plan.md": { path: ["outputs", "remediation_plan.md"], type: "text/markdown; charset=utf-8" }
};

export async function GET(_: Request, { params }: { params: Promise<{ runId: string; artifact: string }> }) {
  const { runId, artifact } = await params;
  const item = ARTIFACTS[artifact];
  if (!item) {
    return NextResponse.json({ error: "Unknown artifact." }, { status: 404 });
  }
  const filePath = runPath(runId, ...item.path);
  if (!filePath) {
    return NextResponse.json({ error: "Run not found." }, { status: 404 });
  }
  try {
    const data = await fs.readFile(filePath);
    return new NextResponse(data, {
      headers: {
        "Content-Type": item.type,
        "Content-Disposition": `attachment; filename="${path.basename(artifact)}"`
      }
    });
  } catch {
    return NextResponse.json({ error: "Artifact not found." }, { status: 404 });
  }
}
