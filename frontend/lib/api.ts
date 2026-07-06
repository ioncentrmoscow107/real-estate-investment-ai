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

export type Recommendation = "BUY" | "WATCH" | "AVOID";

export type ScoreExplanation = {
  score: number;
  explanations: string[];
  applied_rules: string[];
};

export type DashboardProperty = {
  id: string;
  source: string;
  source_url: string;
  title: string;
  address: string | null;
  price_rub: number;
  area_sqm: number;
  price_per_sqm: number;
  investment_score: number;
  liquidity_score: number;
  risk_score: number;
  fake_score: number;
  data_quality_score: number;
  recommendation: Recommendation;
  advantages: string[];
  disadvantages: string[];
  risks: string[];
  missing_information: string[];
  due_diligence_checklist: string[];
  short_summary: string;
  explanations: Record<string, ScoreExplanation>;
};

export type DashboardResponse = {
  summary: {
    total_properties: number;
    average_investment_score: number;
    recommendations: Record<Recommendation, number>;
  };
  properties: DashboardProperty[];
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

export function getDashboardProperties() {
  return fetchJson<DashboardResponse>("/api/v1/dashboard/properties");
}
