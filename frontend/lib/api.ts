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

export type InvestorScoreExplanation = {
  positive_factors: string[];
  negative_factors: string[];
  summary: string;
};

export type PropertyPhoto = {
  url: string | null;
  caption: string;
  type: string;
  is_main: boolean;
};

export type BuildingContext = {
  building_year: number | null;
  building_class: string;
  residential_units: number | null;
  commercial_units: number | null;
  floors_total: number | null;
  parking_type: string;
  facade_condition: string;
  entrance_type: string;
  entrance_visibility: string;
  window_display_quality: string;
  ceiling_height_m: number | null;
  separate_entrance: boolean;
  loading_access: string;
  comments: string;
};

export type SurroundingsContext = {
  radius_m: number;
  residential_density: string;
  office_density: string;
  schools_nearby: number;
  kindergartens_nearby: number;
  medical_centers_nearby: number;
  business_centers_nearby: number;
  shopping_centers_nearby: number;
  public_transport_stops_nearby: number;
  metro_distance_m: number | null;
  parking_availability: string;
  key_anchors: string[];
  comments: string;
};

export type TrafficContext = {
  pedestrian_traffic_level: string;
  car_traffic_level: string;
  target_traffic_level: string;
  transit_traffic_level: string;
  visibility_from_road: string;
  nearest_metro_distance_m: number | null;
  nearest_public_transport_distance_m: number | null;
  main_pedestrian_routes: string[];
  traffic_positive_factors: string[];
  traffic_negative_factors: string[];
  comments: string;
};

export type CompetitionContext = {
  nearby_competitors_count: number;
  vacant_premises_nearby: number;
  saturation_level: string;
  competitor_categories: string[];
  anchor_tenants_nearby: string[];
  risk_of_oversupply: string;
  comments: string;
};

export type SaleComparable = {
  title: string;
  distance_m: number;
  area_sqm: number;
  price_rub: number;
  price_per_sqm: number;
  property_type: string;
  building_year: number | null;
  source: string;
  confidence: string;
};

export type SaleComparablesSummary = {
  avg_price_per_sqm: number;
  min_price_per_sqm: number;
  max_price_per_sqm: number;
  subject_price_vs_market_percent: number;
  conclusion: string;
};

export type RentalRate = {
  title: string;
  distance_m: number;
  property_type: string;
  area_sqm: number;
  rent_rub_per_month: number;
  rent_rub_per_sqm_per_year: number;
  source: string;
  confidence: string;
};

export type RentalRatesSummary = {
  avg_rent_rub_per_sqm_per_year: number;
  min_rent_rub_per_sqm_per_year: number;
  max_rent_rub_per_sqm_per_year: number;
  subject_rent_vs_market_percent: number;
  conclusion: string;
};

export type MarketTrend = {
  period: string;
  trend: string;
  change_percent: number;
  confidence: string;
  explanation: string;
};

export type DistrictMarketTrends = {
  commercial_rent_trend: MarketTrend;
  commercial_sale_price_trend: MarketTrend;
  vacancy_trend: MarketTrend;
};

export type ResidentialMarketContext = {
  new_development: {
    new_buildings_nearby_count: number;
    planned_units: number;
    delivered_units_last_3_years: number;
    projects_under_construction: number;
    avg_new_building_price_per_sqm: number | null;
    price_trend_percent: number;
    comments: string;
  };
  resale_market: {
    avg_resale_price_per_sqm: number | null;
    resale_price_trend_percent: number;
    liquidity_level: string;
    demand_level: string;
    comments: string;
  };
};

export type MarketSupportSummary = {
  support_level: string;
  positive_factors: string[];
  negative_factors: string[];
  conclusion: string;
};

export type ManualIntakeStatus = "draft" | "queued" | "processing" | "analyzed" | "failed";

export type ManualListingUrl = {
  id: string;
  url: string;
  source_detected: string;
  status: ManualIntakeStatus;
  error_message: string | null;
  created_at: string;
  updated_at: string;
};

export type ManualIntakeBatch = {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
  status: ManualIntakeStatus;
  urls: ManualListingUrl[];
  total_urls: number;
  processed_count: number;
  failed_count: number;
  analyzed_count: number;
  source: "manual";
  linked_search_profile_id: string | null;
};

export type ProfileFilterDefaults = {
  price_min: number | null;
  price_max: number | null;
  price_per_sqm_min: number | null;
  price_per_sqm_max: number | null;
  area_min: number | null;
  area_max: number | null;
  floor_min: number | null;
  floor_max: number | null;
  first_floor_only: boolean;
  location_query: string;
  source: string;
  property_category: string;
  deal_type: string;
  recommendation: Recommendation | "any";
  investment_score_min: number;
  risk_max: number;
  data_quality_min: number;
  tenant_exists: boolean;
  federal_tenant_only: boolean;
  rent_yield_min: number | null;
  electric_power_min: number | null;
  building_year_min: number | null;
  only_with_photos: boolean;
  only_with_missing_information: boolean;
  market_support_level: string;
};

export type SearchProfile = {
  id: string;
  name: string;
  description: string;
  is_custom: boolean;
  default_filters: ProfileFilterDefaults;
};

export type IntakeFunnel = {
  active_profile_id: string;
  last_run: string | null;
  next_run: string | null;
  refresh_interval_minutes: number;
  max_listings_per_source: number;
  source_breakdown: Record<string, number>;
  location_breakdown: Record<string, number>;
};

export type ManualOverride = {
  label: string;
  original_value: string;
  override_value: string;
  source: string;
  comment: string;
  updated_at: string;
};

export type CorrectionHistoryItem = {
  field: string;
  label: string;
  old_value: string;
  new_value: string;
  source: string;
  comment: string;
  changed_at: string;
};

export type PropertyWorkflowStatus =
  | "new"
  | "interesting"
  | "in_review"
  | "documents_requested"
  | "egrn_check"
  | "negotiation"
  | "price_negotiation"
  | "rejected"
  | "archived"
  | "deal_pipeline";

export type RequestedDocument = {
  title: string;
  status: "received" | "requested" | "missing" | "not_required";
  status_label: string;
  comment: string;
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
  floor: number | null;
  building_year: number | null;
  property_type: string;
  search_profile_ids: string[];
  district: string | null;
  metro: string | null;
  property_category: string;
  deal_type: string;
  tenant_exists: boolean;
  rent_yield_percent: number | null;
  market_support_level: string;
  manual_overrides?: Record<string, ManualOverride>;
  correction_history?: CorrectionHistoryItem[];
  property_workflow_status?: PropertyWorkflowStatus;
  property_workflow_status_label?: string;
  workflow_next_action?: string;
  requested_documents?: RequestedDocument[];
  electric_power_kw: number | null;
  electric_power_increase_to_kw: number | null;
  repair_condition: string | null;
  has_federal_tenant: boolean;
  last_updated: string;
  investment_score: number;
  liquidity_score: number;
  tenant_score: number;
  building_score: number;
  location_score: number;
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
  market_signal: string;
  score_explanations: Record<string, InvestorScoreExplanation>;
  photos: PropertyPhoto[];
  building_context: BuildingContext;
  surroundings_context: SurroundingsContext;
  traffic_context: TrafficContext;
  competition_context: CompetitionContext;
  nearby_sale_comparables: SaleComparable[];
  sale_comparables_summary: SaleComparablesSummary;
  nearby_rental_rates: RentalRate[];
  rental_rates_summary: RentalRatesSummary;
  district_market_trends: DistrictMarketTrends;
  residential_market_context: ResidentialMarketContext;
  market_support_summary: MarketSupportSummary;
  explanations: Record<string, ScoreExplanation>;
};

export type DashboardResponse = {
  summary: {
    total_properties: number;
    average_investment_score: number;
    average_risk_score: number;
    recommendations: Record<Recommendation, number>;
  };
  properties: DashboardProperty[];
  manual_intake_batches: ManualIntakeBatch[];
  search_profiles: SearchProfile[];
  intake_funnels: Record<string, IntakeFunnel>;
};

const API_BASE_URL =
  process.env.API_BASE_URL ??
  process.env.NEXT_PUBLIC_API_BASE_URL ??
  "http://localhost:8000";

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
