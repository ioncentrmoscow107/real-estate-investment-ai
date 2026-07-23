import { NextRequest, NextResponse } from "next/server";

const BACKEND_API_BASE_URL =
  process.env.API_BASE_URL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000";

async function passThrough(response: Response) {
  return new NextResponse(await response.text(), {
    status: response.status,
    headers: {
      "content-type": response.headers.get("content-type") ?? "application/json",
    },
  });
}

function unavailableResponse() {
  return NextResponse.json(
    { detail: "Manual intake service is unavailable" },
    { status: 503 },
  );
}

export async function GET() {
  try {
    const response = await fetch(
      `${BACKEND_API_BASE_URL}/api/v1/manual-intake/batches`,
      { cache: "no-store" },
    );
    return passThrough(response);
  } catch {
    return unavailableResponse();
  }
}

export async function POST(request: NextRequest) {
  try {
    const response = await fetch(
      `${BACKEND_API_BASE_URL}/api/v1/manual-intake/batches`,
      {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: await request.text(),
        cache: "no-store",
      },
    );
    return passThrough(response);
  } catch {
    return unavailableResponse();
  }
}
