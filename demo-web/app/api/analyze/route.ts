import { NextResponse } from "next/server";
import { runAnalyze } from "../../../lib/demoRunner";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  try {
    const form = await request.formData();
    const fixture = form.get("fixture");
    const file = form.get("file");
    const folderFiles = form.getAll("files[]").filter((item): item is File => item instanceof File);
    const folderPaths = form.getAll("paths[]").map((item) => String(item));
    if (typeof fixture === "string" && fixture.length > 0) {
      const summary = await runAnalyze({ fixture });
      return NextResponse.json(summary);
    }
    if (folderFiles.length > 0) {
      const summary = await runAnalyze({ folderFiles, folderPaths });
      return NextResponse.json(summary);
    }
    if (file instanceof File) {
      const summary = await runAnalyze({ file });
      return NextResponse.json(summary);
    }
    return NextResponse.json({ error: "Upload a .zip, a SKILL.md file, or choose a demo fixture." }, { status: 400 });
  } catch (error) {
    return NextResponse.json({ error: error instanceof Error ? error.message : String(error) }, { status: 500 });
  }
}
