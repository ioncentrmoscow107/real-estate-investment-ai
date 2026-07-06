import {
  AlertTriangle,
  BarChart3,
  Building2,
  CheckCircle2,
  ChevronDown,
  CircleHelp,
  ClipboardCheck,
  ShieldAlert,
  XCircle,
} from "lucide-react";
import type { ReactNode } from "react";
import { getDashboardProperties } from "../lib/api";
import type { DashboardProperty, Recommendation } from "../lib/api";

const recommendationLabels: Record<Recommendation, string> = {
  BUY: "Покупать",
  WATCH: "Изучить подробнее",
  AVOID: "Не рекомендую",
};

const scoreLabels = [
  ["investment_score", "Инвестиционный рейтинг"],
  ["liquidity_score", "Ликвидность"],
  ["tenant_score", "Арендатор"],
  ["building_score", "Здание"],
  ["location_score", "Локация"],
  ["risk_score", "Риск"],
  ["fake_score", "Риск фейка"],
  ["data_quality_score", "Качество данных"],
] as const;

function formatRub(value: number) {
  return `${formatNumber(value)} ₽`;
}

function formatArea(value: number) {
  return `${formatNumber(value)} м²`;
}

function formatPricePerSqm(value: number) {
  return `${formatNumber(value)} ₽/м²`;
}

function formatNumber(value: number) {
  return new Intl.NumberFormat("ru-RU", {
    maximumFractionDigits: 0,
  }).format(value);
}

function formatScore(value: number) {
  return `${value} / 100`;
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function repairLabel(value: DashboardProperty["repair_condition"]) {
  if (value === "quality_repair" || value === "has_repair") {
    return "Готовое состояние";
  }
  if (value === "shell_core") {
    return "Shell&core";
  }
  if (value === "none" || value === "no_repair" || value === "needs_repair") {
    return "Требуется ремонт";
  }
  return "Нет данных";
}

function powerLabel(property: DashboardProperty) {
  if (!property.electric_power_kw) {
    return "Нет данных";
  }

  const base = `${formatNumber(property.electric_power_kw)} кВт`;
  if (!property.electric_power_increase_to_kw) {
    return base;
  }

  return `${base}, увеличение до ${formatNumber(property.electric_power_increase_to_kw)} кВт`;
}

function RecommendationBadge({ value }: { value: Recommendation }) {
  return (
    <span className={`recommendation recommendation-${value.toLowerCase()}`}>
      {recommendationLabels[value]}
    </span>
  );
}

function KpiCard({
  icon,
  label,
  value,
  tone,
}: {
  icon: ReactNode;
  label: string;
  value: string | number;
  tone?: "buy" | "watch" | "avoid";
}) {
  return (
    <div className={`metric ${tone ? `metric-${tone}` : ""}`}>
      {icon}
      <span className="metric-label">{label}</span>
      <span className="metric-value">{value}</span>
    </div>
  );
}

function ScoreTile({ label, value }: { label: string; value: number }) {
  return (
    <div className="score-tile">
      <span>{label}</span>
      <strong>{formatScore(value)}</strong>
    </div>
  );
}

function PreviewList({
  icon,
  title,
  items,
}: {
  icon: ReactNode;
  title: string;
  items: string[];
}) {
  return (
    <div className="preview-list">
      <div className="preview-title">
        {icon}
        <span>{title}</span>
      </div>
      <ul>
        {items.slice(0, 3).map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function DetailList({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="detail-block">
      <h3>{title}</h3>
      {items.length === 0 ? (
        <p className="muted">Нет данных.</p>
      ) : (
        <ul>
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

function PropertyCard({ property }: { property: DashboardProperty }) {
  return (
    <details className={`property-card property-card-${property.recommendation.toLowerCase()}`}>
      <summary>
        <div className="memo-header">
          <RecommendationBadge value={property.recommendation} />
          <div className="memo-score">
            <span>Инвестиционный рейтинг</span>
            <strong>{formatScore(property.investment_score)}</strong>
          </div>
        </div>

        <div className="memo-title">
          <h2>{property.title}</h2>
          <p>{property.address ?? "Адрес не раскрыт"}</p>
        </div>

        <div className="memo-facts">
          <span>
            <strong>Цена</strong>
            {formatRub(property.price_rub)}
          </span>
          <span>
            <strong>Площадь</strong>
            {formatArea(property.area_sqm)}
          </span>
          <span>
            <strong>Цена за м²</strong>
            {formatPricePerSqm(property.price_per_sqm)}
          </span>
          <span>
            <strong>Риск</strong>
            {formatScore(property.risk_score)}
          </span>
          <span>
            <strong>Риск фейка</strong>
            {formatScore(property.fake_score)}
          </span>
          <span>
            <strong>Качество данных</strong>
            {formatScore(property.data_quality_score)}
          </span>
        </div>

        <div className="memo-preview">
          <PreviewList
            icon={<CheckCircle2 size={16} />}
            title="Ключевые преимущества"
            items={property.advantages}
          />
          <PreviewList
            icon={<AlertTriangle size={16} />}
            title="Ключевые риски"
            items={property.risks}
          />
        </div>

        <span className="details-action">
          <span className="details-open">Подробнее</span>
          <span className="details-close">Свернуть</span>
          <ChevronDown size={16} />
        </span>
      </summary>

      <div className="property-details">
        <div className="conclusion">
          <h3>Инвестиционный вывод</h3>
          <p>{property.short_summary}</p>
        </div>

        <div className="score-grid">
          {scoreLabels.map(([key, label]) => (
            <ScoreTile key={key} label={label} value={property[key]} />
          ))}
        </div>

        <div className="object-meta">
          <span>
            <strong>Электрическая мощность</strong>
            {powerLabel(property)}
          </span>
          <span>
            <strong>Состояние ремонта</strong>
            {repairLabel(property.repair_condition)}
          </span>
          <span>
            <strong>Федеральный арендатор</strong>
            {property.has_federal_tenant ? "Да" : "Нет"}
          </span>
          <span>
            <strong>Последнее обновление</strong>
            {formatDate(property.last_updated)}
          </span>
        </div>

        <div className="details-grid">
          <DetailList title="Преимущества" items={property.advantages} />
          <DetailList title="Недостатки" items={property.disadvantages} />
          <DetailList title="Риски" items={property.risks} />
          <DetailList title="Недостающие данные" items={property.missing_information} />
          <DetailList title="Что проверить" items={property.due_diligence_checklist} />
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
            <strong>AI-инвестиционный анализ коммерческой недвижимости</strong>
            <span>Объекты 100–400 млн ₽ · 1 этаж · дома от 2016 года · стрит-ритейл / ПСН / торговые помещения</span>
          </div>
          <span className="status-ok">Демо-данные без реального сбора объявлений</span>
        </div>
      </header>

      <main className="main">
        <section className="summary-grid" aria-label="Ключевые показатели">
          <KpiCard icon={<Building2 size={20} />} label="Всего объектов" value={summary.total_properties} />
          <KpiCard
            icon={<CheckCircle2 size={20} />}
            label="Покупать"
            value={summary.recommendations.BUY}
            tone="buy"
          />
          <KpiCard
            icon={<CircleHelp size={20} />}
            label="Изучить подробнее"
            value={summary.recommendations.WATCH}
            tone="watch"
          />
          <KpiCard
            icon={<XCircle size={20} />}
            label="Не рекомендую"
            value={summary.recommendations.AVOID}
            tone="avoid"
          />
          <KpiCard
            icon={<BarChart3 size={20} />}
            label="Средний инвестиционный рейтинг"
            value={formatScore(summary.average_investment_score)}
          />
          <KpiCard
            icon={<ShieldAlert size={20} />}
            label="Средний риск"
            value={formatScore(summary.average_risk_score)}
          />
        </section>

        <section className="dashboard-panel">
          <div className="toolbar">
            <div>
              <h1>Инвестиционные объекты</h1>
              <p>Каждая карточка показывает решение, сильные стороны, риски и список проверок перед сделкой.</p>
            </div>
            <div className="toolbar-note">
              <ClipboardCheck size={16} />
              Анализ всех подходящих объектов
            </div>
          </div>

          <div className="property-list">
            {properties.map((property) => (
              <PropertyCard key={property.id} property={property} />
            ))}
          </div>

          <div className="footer-note">
            <AlertTriangle size={16} />
            Реальный scraping не включен. Данные на экране используются для демонстрации инвесторского workflow.
          </div>
        </section>
      </main>
    </div>
  );
}
