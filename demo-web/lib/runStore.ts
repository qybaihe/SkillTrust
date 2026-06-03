import fs from "node:fs/promises";
import path from "node:path";

type RunStatus = {
  run_id: string;
  status: string;
  step: string;
  created_at: string;
  completed_at?: string;
  error?: string;
  summary?: unknown;
};

export function demoRoot(): string {
  const cwd = path.join(/* turbopackIgnore: true */ process.cwd());
  return path.basename(cwd) === "demo-web" ? cwd : path.join(cwd, "demo-web");
}

export function runsRoot(): string {
  return path.join(demoRoot(), ".runs");
}

export async function readRun(runId: string): Promise<RunStatus | null> {
  if (!isSafeRunId(runId)) {
    return null;
  }
  const statusPath = path.join(runsRoot(), runId, "status.json");
  try {
    return JSON.parse(await fs.readFile(statusPath, "utf-8")) as RunStatus;
  } catch {
    return null;
  }
}

export function runPath(runId: string, ...segments: string[]): string | null {
  if (!isSafeRunId(runId)) {
    return null;
  }
  const root = path.join(runsRoot(), runId);
  const resolved = path.resolve(root, ...segments);
  if (!resolved.startsWith(path.resolve(root))) {
    return null;
  }
  return resolved;
}

function isSafeRunId(runId: string): boolean {
  return /^[a-zA-Z0-9_-]+$/.test(runId);
}
