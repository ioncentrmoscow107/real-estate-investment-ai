export type CollectorStatus = {
  sources: string[];
  scheduler_running: boolean;
  interval_minutes: number;
};

export type Listing = {
  id: number;
  source: string;
  external_id: string;
  title: string;
  url: string;
  address: string | null;
  price_rub: string;
  floor: number;
  building_year: number;
  property_type: string;
  area_sqm: string | null;
  tenant: string | null;
  ai_summary: string | null;
  investment_score: number | null;
  created_at: string;
  updated_at: string;
};

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

async function fetchJson<T>(path: string): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export function getCollectorStatus() {
  return fetchJson<CollectorStatus>("/api/v1/collectors/status");
}

export function getListings() {
  return fetchJson<Listing[]>("/api/v1/listings");
}

