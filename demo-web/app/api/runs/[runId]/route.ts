import { NextResponse } from "next/server";
import { readRun } from "../../../../lib/runStore";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET(_: Request, { params }: { params: Promise<{ runId: string }> }) {
  const { runId } = await params;
  const status = await readRun(runId);
  if (!status) {
    return NextResponse.json({ error: "Run not found." }, { status: 404 });
  }
  return NextResponse.json(status.summary || status);
}
