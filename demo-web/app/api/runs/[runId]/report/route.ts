import fs from "node:fs/promises";
import { NextResponse } from "next/server";
import { runPath } from "../../../../../lib/runStore";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(_: Request, { params }: { params: Promise<{ runId: string }> }) {
  const { runId } = await params;
  const fusedReport = runPath(runId, "fused", "fused_trust_report.md");
  const deterministicReport = runPath(runId, "outputs", "trust_report.md");
  const reportPath = fusedReport && (await exists(fusedReport)) ? fusedReport : deterministicReport;
  if (!reportPath || !(await exists(reportPath))) {
    return NextResponse.json({ error: "Report not found." }, { status: 404 });
  }
  const report = await fs.readFile(reportPath, "utf-8");
  return new NextResponse(report, {
    headers: {
      "Content-Type": "text/markdown; charset=utf-8"
    }
  });
}

async function exists(filePath: string): Promise<boolean> {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}
