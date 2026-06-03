import fs from "node:fs/promises";
import path from "node:path";
import { NextResponse } from "next/server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  const cwd = path.join(/* turbopackIgnore: true */ process.cwd());
  const root = path.basename(cwd) === "demo-web" ? path.join(cwd, "..") : cwd;
  const coverPath = path.join(root, "docs", "assets", "skilltrust-cover.png");
  const image = await fs.readFile(coverPath);
  return new NextResponse(image, {
    headers: {
      "Content-Type": "image/png",
      "Cache-Control": "public, max-age=3600"
    }
  });
}
