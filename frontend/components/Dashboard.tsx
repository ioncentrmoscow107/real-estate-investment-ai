import {
  AlertTriangle,
  BadgeCheck,
  BarChart3,
  Building2,
  ClipboardCheck,
  ShieldAlert,
} from "lucide-react";
import { getDashboardProperties } from "../lib/api";
import type { DashboardProperty } from "../lib/api";

function formatRub(value: number) {
  return new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
    maximumFractionDigits: 0,
  }).format(value);
}

function formatNumber(value: number) {
  return new Intl.NumberFormat("ru-RU", {
    maximumFractionDigits: 0,
  }).format(value);
}

function RecommendationBadge({ value }: { value: DashboardProperty["recommendation"] }) {
  return <span className={`recommendation recommendation-${value.toLowerCase()}`}>{value}</span>;
}

function ScorePill({ label, value }: { label: string; value: number }) {
  return (
    <span className="score-pill">
      <span>{label}</span>
      <strong>{value}</strong>
    </span>
  );
}

function CompactList({ title, items }: { title: string; items: string[] }) {
  if (items.length === 0) {
    return (
      <div className="detail-block">
        <h3>{title}</h3>
        <p className="muted">No items.</p>
      </div>
    );
  }

  return (
    <div className="detail-block">
      <h3>{title}</h3>
      <ul>
        {items.slice(0, 4).map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function PropertyRow({ property }: { property: DashboardProperty }) {
  return (
    <details className="property-row">
      <summary>
        <div className="property-main">
          <div className="property-title">
            <a href={property.source_url} rel="noreferrer" target="_blank">
              {property.title}
            </a>
            <span>{property.address ?? "Address hidden"}</span>
          </div>
          <div className="property-price">
            <strong>{formatRub(property.price_rub)}</strong>
            <span>
              {formatNumber(property.area_sqm)} m2 · {formatRub(property.price_per_sqm)}/m2
            </span>
          </div>
          <div className="property-scores">
            <ScorePill label="Inv" value={property.investment_score} />
            <ScorePill label="Liq" value={property.liquidity_score} />
            <ScorePill label="Risk" value={property.risk_score} />
            <ScorePill label="Fake" value={property.fake_score} />
            <ScorePill label="Data" value={property.data_quality_score} />
          </div>
          <RecommendationBadge value={property.recommendation} />
        </div>
      </summary>

      <div className="property-details">
        <p className="summary-text">{property.short_summary}</p>
        <div className="details-grid">
          <CompactList title="Advantages" items={property.advantages} />
          <CompactList title="Disadvantages" items={property.disadvantages} />
          <CompactList title="Risks" items={property.risks} />
          <CompactList title="Missing information" items={property.missing_information} />
          <CompactList title="Due diligence" items={property.due_diligence_checklist} />
        </div>
      </div>
    </details>
  );
}

export default async function Dashboard() {
  const dashboard = await getDashboardProperties();
  const { summary, properties } = dashboard;

  return (
    <div className="page">
      <header className="topbar">
        <div className="topbar-inner">
          <div className="brand">
            <strong>CRE Investment AI</strong>
            <span>Investor dashboard for commercial real estate decisions</span>
          </div>
          <span className="status-ok">Sample analyzed properties</span>
        </div>
      </header>

      <main className="main">
        <section className="summary-grid">
          <div className="card metric">
            <Building2 size={20} />
            <span className="metric-label">Total properties</span>
            <span className="metric-value">{summary.total_properties}</span>
          </div>
          <div className="card metric">
            <BarChart3 size={20} />
            <span className="metric-label">Average score</span>
            <span className="metric-value">{summary.average_investment_score}</span>
          </div>
          <div className="card metric recommendation-counts">
            <BadgeCheck size={20} />
            <span className="metric-label">BUY / WATCH / AVOID</span>
            <span className="metric-value">
              {summary.recommendations.BUY} / {summary.recommendations.WATCH} /{" "}
              {summary.recommendations.AVOID}
            </span>
          </div>
          <div className="card metric">
            <ShieldAlert size={20} />
            <span className="metric-label">Review mode</span>
            <span className="metric-value">Skeptical</span>
          </div>
        </section>

        <section className="card dashboard-panel">
          <div className="toolbar">
            <div>
              <h1>Analyzed Properties</h1>
              <p>Compact list of all properties. Open a row for risks and due diligence.</p>
            </div>
            <div className="toolbar-note">
              <AlertTriangle size={16} />
              Mock data only
            </div>
          </div>

          <div className="property-list">
            {properties.map((property) => (
              <PropertyRow key={property.id} property={property} />
            ))}
          </div>

          <div className="footer-note">
            <ClipboardCheck size={16} />
            No scraping is running here. This dashboard consumes sample analyzed properties from the API.
          </div>
        </section>
      </main>
    </div>
  );
}
