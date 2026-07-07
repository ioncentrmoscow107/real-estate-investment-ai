import {
  AlertTriangle,
  BarChart3,
  Building2,
  Camera,
  CheckCircle2,
  ChevronDown,
  CircleHelp,
  ClipboardCheck,
  Home,
  MapPin,
  ShieldAlert,
  Store,
  TrendingUp,
  Users,
  XCircle,
} from "lucide-react";
import type { ReactNode } from "react";
import { getDashboardProperties } from "../lib/api";
import type {
  DashboardProperty,
  InvestorScoreExplanation,
  MarketTrend,
  Recommendation,
} from "../lib/api";

type ScoreKey =
  | "investment_score"
  | "liquidity_score"
  | "tenant_score"
  | "building_score"
  | "location_score"
  | "risk_score"
  | "fake_score"
  | "data_quality_score";

const recommendationLabels: Record<Recommendation, string> = {
  BUY: "Покупать",
  WATCH: "Изучить подробнее",
  AVOID: "Не рекомендую",
};

const scoreLabels: Array<[ScoreKey, string]> = [
  ["investment_score", "Инвестиционный рейтинг"],
  ["liquidity_score", "Ликвидность"],
  ["tenant_score", "Арендатор"],
  ["building_score", "Здание"],
  ["location_score", "Локация"],
  ["risk_score", "Риск"],
  ["fake_score", "Риск фейка"],
  ["data_quality_score", "Качество данных"],
];

const photoTypeLabels: Record<string, string> = {
  facade: "Фасад",
  entrance: "Вход",
  interior: "Интерьер",
  window_display: "Витрины",
  street_view: "Улица",
  surroundings: "Окружение",
  floor_plan: "Планировка",
  engineering: "Инженерия",
};

function formatRub(value: number | null) {
  if (value === null) {
    return "нет данных";
  }
  return `${formatNumber(value)} ₽`;
}

function formatArea(value: number | null) {
  if (value === null) {
    return "нет данных";
  }
  return `${formatNumber(value)} м²`;
}

function formatPricePerSqm(value: number | null) {
  if (value === null) {
    return "нет данных";
  }
  return `${formatNumber(value)} ₽/м²`;
}

function formatNumber(value: number) {
  return new Intl.NumberFormat("ru-RU", {
    maximumFractionDigits: 0,
  }).format(value);
}

function formatPercent(value: number) {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toLocaleString("ru-RU", { maximumFractionDigits: 1 })}%`;
}

function formatScore(value: number) {
  return `${value} / 100`;
}

function formatDistance(value: number | null) {
  if (value === null) {
    return "нет данных";
  }
  return value >= 1000 ? `${(value / 1000).toLocaleString("ru-RU", { maximumFractionDigits: 1 })} км` : `${value} м`;
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

function yesNo(value: boolean) {
  return value ? "Да" : "Нет";
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

function trendLabel(trend: MarketTrend) {
  const arrow = trend.change_percent > 0 ? "↑" : trend.change_percent < 0 ? "↓" : "→";
  return `${arrow} ${formatPercent(trend.change_percent)} за ${trend.period}`;
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

function Section({
  title,
  icon,
  children,
}: {
  title: string;
  icon: ReactNode;
  children: ReactNode;
}) {
  return (
    <section className="intelligence-section">
      <h3>
        {icon}
        {title}
      </h3>
      {children}
    </section>
  );
}

function FactGrid({ items }: { items: Array<[string, ReactNode]> }) {
  return (
    <div className="fact-grid">
      {items.map(([label, value]) => (
        <span key={label}>
          <strong>{label}</strong>
          {value}
        </span>
      ))}
    </div>
  );
}

function TextList({ items }: { items: string[] }) {
  if (items.length === 0) {
    return <p className="muted">Нет данных.</p>;
  }

  return (
    <ul>
      {items.map((item) => (
        <li key={item}>{item}</li>
      ))}
    </ul>
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
      <TextList items={items.slice(0, 3)} />
    </div>
  );
}

function PhotoPlaceholder({ caption, large = false }: { caption: string; large?: boolean }) {
  return (
    <div className={`photo-placeholder ${large ? "photo-placeholder-large" : ""}`}>
      <Camera size={large ? 28 : 20} />
      <span>{caption}</span>
    </div>
  );
}

function PhotoView({ property }: { property: DashboardProperty }) {
  const mainPhoto = property.photos.find((photo) => photo.is_main) ?? property.photos[0];
  return (
    <div className="photo-strip">
      <div className="main-photo">
        {mainPhoto?.url ? (
          <img alt={mainPhoto.caption} src={mainPhoto.url} />
        ) : (
          <PhotoPlaceholder caption={mainPhoto?.caption ?? "Фото объекта"} large />
        )}
      </div>
      <div className="photo-thumbs">
        {property.photos.map((photo) => (
          <div className="photo-thumb" key={`${photo.type}-${photo.caption}`}>
            {photo.url ? <img alt={photo.caption} src={photo.url} /> : <PhotoPlaceholder caption={photoTypeLabels[photo.type] ?? "Фото"} />}
            <span>{photo.caption}</span>
          </div>
        ))}
      </div>
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

function ScoreExplanationBlock({
  label,
  scoreKey,
  score,
  explanation,
}: {
  label: string;
  scoreKey: ScoreKey;
  score: number;
  explanation: InvestorScoreExplanation;
}) {
  const isRisk = scoreKey === "risk_score";
  const isFake = scoreKey === "fake_score";
  const positiveTitle = isRisk || isFake ? "Что снижает риск" : "Что повысило оценку";
  const negativeTitle = isRisk ? "Что усиливает риск" : isFake ? "Почему AI сомневается" : "Что снизило оценку";

  return (
    <div className="score-explanation">
      <div className="score-explanation-head">
        <span>{label}</span>
        <strong>{formatScore(score)}</strong>
      </div>
      <p>{explanation.summary}</p>
      <div className="explanation-columns">
        <div>
          <h4>{positiveTitle}</h4>
          <TextList items={explanation.positive_factors} />
        </div>
        <div>
          <h4>{negativeTitle}</h4>
          <TextList items={explanation.negative_factors} />
        </div>
      </div>
    </div>
  );
}

function ComparablesTable({
  type,
  property,
}: {
  type: "sale" | "rent";
  property: DashboardProperty;
}) {
  if (type === "sale") {
    return (
      <div className="table-like">
        {property.nearby_sale_comparables.map((item) => (
          <div className="comparable-row" key={item.title}>
            <strong>{item.title}</strong>
            <span>{formatDistance(item.distance_m)}</span>
            <span>{formatArea(item.area_sqm)}</span>
            <span>{formatRub(item.price_rub)}</span>
            <span>{formatPricePerSqm(item.price_per_sqm)}</span>
            <span>{item.confidence}</span>
          </div>
        ))}
      </div>
    );
  }

  return (
    <div className="table-like">
      {property.nearby_rental_rates.map((item) => (
        <div className="comparable-row" key={item.title}>
          <strong>{item.title}</strong>
          <span>{formatDistance(item.distance_m)}</span>
          <span>{formatArea(item.area_sqm)}</span>
          <span>{formatRub(item.rent_rub_per_month)} / мес.</span>
          <span>{formatPricePerSqm(item.rent_rub_per_sqm_per_year)} / год</span>
          <span>{item.confidence}</span>
        </div>
      ))}
    </div>
  );
}

function PropertyCard({ property }: { property: DashboardProperty }) {
  const mainPhoto = property.photos.find((photo) => photo.is_main) ?? property.photos[0];

  return (
    <details className={`property-card property-card-${property.recommendation.toLowerCase()}`}>
      <summary>
        <div className="compact-card">
          <div className="compact-photo">
            {mainPhoto?.url ? (
              <img alt={mainPhoto.caption} src={mainPhoto.url} />
            ) : (
              <PhotoPlaceholder caption={mainPhoto?.caption ?? "Фото объекта"} large />
            )}
          </div>

          <div className="compact-content">
            <div className="memo-header">
              <RecommendationBadge value={property.recommendation} />
              <span className="market-signal">{property.market_signal}</span>
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
            </div>
          </div>
        </div>

        <div className="memo-preview">
          <PreviewList icon={<CheckCircle2 size={16} />} title="Ключевые преимущества" items={property.advantages} />
          <PreviewList icon={<AlertTriangle size={16} />} title="Ключевые риски" items={property.risks} />
        </div>

        <span className="details-action">
          <span className="details-open">Подробнее</span>
          <span className="details-close">Свернуть</span>
          <ChevronDown size={16} />
        </span>
      </summary>

      <div className="property-details">
        <Section title="Инвестиционное заключение" icon={<ClipboardCheck size={18} />}>
          <div className="conclusion">
            <p>{property.short_summary}</p>
          </div>
          <div className="score-grid">
            {scoreLabels.map(([key, label]) => (
              <ScoreTile key={key} label={label} value={property[key]} />
            ))}
          </div>
          <p className="score-note">
            Для инвестиционного рейтинга, ликвидности, арендатора, здания, локации и качества данных выше — лучше.
            Для риска и риска фейка выше — хуже.
          </p>
        </Section>

        <Section title="Фото объекта" icon={<Camera size={18} />}>
          <PhotoView property={property} />
        </Section>

        <Section title="Почему такие рейтинги" icon={<BarChart3 size={18} />}>
          <div className="score-explanations">
            {scoreLabels.map(([key, label]) => (
              <ScoreExplanationBlock
                key={key}
                label={label}
                scoreKey={key}
                score={property[key]}
                explanation={property.score_explanations[key]}
              />
            ))}
          </div>
        </Section>

        <Section title="Дом и помещение" icon={<Home size={18} />}>
          <FactGrid
            items={[
              ["Год постройки", property.building_context.building_year ?? "нет данных"],
              ["Класс / тип дома", property.building_context.building_class],
              ["Количество квартир", property.building_context.residential_units ?? "нет данных"],
              ["Коммерческие помещения", property.building_context.commercial_units ?? "нет данных"],
              ["Паркинг", property.building_context.parking_type],
              ["Отдельный вход", yesNo(property.building_context.separate_entrance)],
              ["Видимость входа", property.building_context.entrance_visibility],
              ["Витринность", property.building_context.window_display_quality],
              ["Высота потолков", property.building_context.ceiling_height_m ? `${property.building_context.ceiling_height_m} м` : "нет данных"],
              ["Состояние фасада", property.building_context.facade_condition],
              ["Зона разгрузки", property.building_context.loading_access],
              ["Последнее обновление", formatDate(property.last_updated)],
            ]}
          />
          <p className="section-comment">{property.building_context.comments}</p>
        </Section>

        <Section title="Окружение" icon={<MapPin size={18} />}>
          <FactGrid
            items={[
              ["Радиус анализа", formatDistance(property.surroundings_context.radius_m)],
              ["Жилые дома", property.surroundings_context.residential_density],
              ["Офисы", property.surroundings_context.office_density],
              ["Школы", property.surroundings_context.schools_nearby],
              ["Детские сады", property.surroundings_context.kindergartens_nearby],
              ["Медцентры", property.surroundings_context.medical_centers_nearby],
              ["Бизнес-центры", property.surroundings_context.business_centers_nearby],
              ["Торговые центры", property.surroundings_context.shopping_centers_nearby],
              ["Метро / МЦК / МЦД", formatDistance(property.surroundings_context.metro_distance_m)],
              ["Остановки транспорта", property.surroundings_context.public_transport_stops_nearby],
              ["Парковки", property.surroundings_context.parking_availability],
              ["Якорные точки спроса", property.surroundings_context.key_anchors.join(", ")],
            ]}
          />
          <p className="section-comment">{property.surroundings_context.comments}</p>
        </Section>

        <Section title="Трафик" icon={<Users size={18} />}>
          <FactGrid
            items={[
              ["Пешеходный трафик", property.traffic_context.pedestrian_traffic_level],
              ["Автомобильный трафик", property.traffic_context.car_traffic_level],
              ["Целевой трафик", property.traffic_context.target_traffic_level],
              ["Транзитный трафик", property.traffic_context.transit_traffic_level],
              ["Видимость с дороги", property.traffic_context.visibility_from_road],
              ["До метро", formatDistance(property.traffic_context.nearest_metro_distance_m)],
              ["До остановки", formatDistance(property.traffic_context.nearest_public_transport_distance_m)],
              ["Основные маршруты", property.traffic_context.main_pedestrian_routes.join(", ")],
            ]}
          />
          <div className="two-columns">
            <div>
              <h4>Что усиливает трафик</h4>
              <TextList items={property.traffic_context.traffic_positive_factors} />
            </div>
            <div>
              <h4>Что ослабляет трафик</h4>
              <TextList items={property.traffic_context.traffic_negative_factors} />
            </div>
          </div>
          <p className="section-comment">{property.traffic_context.comments}</p>
        </Section>

        <Section title="Конкуренты" icon={<Store size={18} />}>
          <FactGrid
            items={[
              ["Количество конкурентов рядом", property.competition_context.nearby_competitors_count],
              ["Вакантные помещения рядом", property.competition_context.vacant_premises_nearby],
              ["Уровень насыщения", property.competition_context.saturation_level],
              ["Категории конкурентов", property.competition_context.competitor_categories.join(", ")],
              ["Якорные арендаторы рядом", property.competition_context.anchor_tenants_nearby.join(", ")],
              ["Риск перенасыщения", property.competition_context.risk_of_oversupply],
            ]}
          />
          <p className="section-comment">{property.competition_context.comments}</p>
        </Section>

        <Section title="Продажи рядом" icon={<Building2 size={18} />}>
          <ComparablesTable type="sale" property={property} />
          <FactGrid
            items={[
              ["Средняя цена за м²", formatPricePerSqm(property.sale_comparables_summary.avg_price_per_sqm)],
              ["Минимум", formatPricePerSqm(property.sale_comparables_summary.min_price_per_sqm)],
              ["Максимум", formatPricePerSqm(property.sale_comparables_summary.max_price_per_sqm)],
              ["Объект к рынку", formatPercent(property.sale_comparables_summary.subject_price_vs_market_percent)],
            ]}
          />
          <p className="section-comment">{property.sale_comparables_summary.conclusion}</p>
        </Section>

        <Section title="Арендные ставки рядом" icon={<Store size={18} />}>
          <ComparablesTable type="rent" property={property} />
          <FactGrid
            items={[
              ["Средняя ставка", `${formatPricePerSqm(property.rental_rates_summary.avg_rent_rub_per_sqm_per_year)} / год`],
              ["Минимум", `${formatPricePerSqm(property.rental_rates_summary.min_rent_rub_per_sqm_per_year)} / год`],
              ["Максимум", `${formatPricePerSqm(property.rental_rates_summary.max_rent_rub_per_sqm_per_year)} / год`],
              ["Объект к рынку", formatPercent(property.rental_rates_summary.subject_rent_vs_market_percent)],
            ]}
          />
          <p className="section-comment">{property.rental_rates_summary.conclusion}</p>
        </Section>

        <Section title="Тенденции рынка" icon={<TrendingUp size={18} />}>
          <div className="trend-grid">
            {[
              ["Аренда коммерции", property.district_market_trends.commercial_rent_trend],
              ["Продажа коммерции", property.district_market_trends.commercial_sale_price_trend],
              ["Вакантность", property.district_market_trends.vacancy_trend],
            ].map(([label, trend]) => (
              <div className="trend-card" key={label as string}>
                <strong>{label as string}</strong>
                <span>{(trend as MarketTrend).trend}: {trendLabel(trend as MarketTrend)}</span>
                <small>Уверенность: {(trend as MarketTrend).confidence}</small>
                <p>{(trend as MarketTrend).explanation}</p>
              </div>
            ))}
          </div>
        </Section>

        <Section title="Жилой рынок округа" icon={<Home size={18} />}>
          <FactGrid
            items={[
              ["Новостройки рядом", property.residential_market_context.new_development.new_buildings_nearby_count],
              ["Планируемые квартиры", property.residential_market_context.new_development.planned_units],
              ["Введено за 3 года", property.residential_market_context.new_development.delivered_units_last_3_years],
              ["Проекты в строительстве", property.residential_market_context.new_development.projects_under_construction],
              ["Средняя цена новостроек", formatPricePerSqm(property.residential_market_context.new_development.avg_new_building_price_per_sqm)],
              ["Тренд цен новостроек", formatPercent(property.residential_market_context.new_development.price_trend_percent)],
              ["Средняя цена вторички", formatPricePerSqm(property.residential_market_context.resale_market.avg_resale_price_per_sqm)],
              ["Тренд цен вторички", formatPercent(property.residential_market_context.resale_market.resale_price_trend_percent)],
              ["Ликвидность вторички", property.residential_market_context.resale_market.liquidity_level],
              ["Спрос на вторичку", property.residential_market_context.resale_market.demand_level],
            ]}
          />
          <p className="section-comment">{property.residential_market_context.new_development.comments}</p>
          <p className="section-comment">{property.residential_market_context.resale_market.comments}</p>
        </Section>

        <Section title="Вывод по рынку" icon={<ShieldAlert size={18} />}>
          <div className="market-conclusion">
            <strong>{property.market_support_summary.support_level}</strong>
            <p>{property.market_support_summary.conclusion}</p>
          </div>
          <div className="two-columns">
            <div>
              <h4>Что поддерживает покупку</h4>
              <TextList items={property.market_support_summary.positive_factors} />
            </div>
            <div>
              <h4>Что ослабляет решение</h4>
              <TextList items={property.market_support_summary.negative_factors} />
            </div>
          </div>
        </Section>

        <Section title="Что проверить" icon={<ClipboardCheck size={18} />}>
          <div className="two-columns">
            <div>
              <h4>Список проверок</h4>
              <TextList items={property.due_diligence_checklist} />
            </div>
            <div>
              <h4>Недостающие данные</h4>
              <TextList items={property.missing_information} />
            </div>
          </div>
        </Section>
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
          <KpiCard icon={<CheckCircle2 size={20} />} label="Покупать" value={summary.recommendations.BUY} tone="buy" />
          <KpiCard icon={<CircleHelp size={20} />} label="Изучить подробнее" value={summary.recommendations.WATCH} tone="watch" />
          <KpiCard icon={<XCircle size={20} />} label="Не рекомендую" value={summary.recommendations.AVOID} tone="avoid" />
          <KpiCard icon={<BarChart3 size={20} />} label="Средний инвестиционный рейтинг" value={formatScore(summary.average_investment_score)} />
          <KpiCard icon={<ShieldAlert size={20} />} label="Средний риск" value={formatScore(summary.average_risk_score)} />
        </section>

        <section className="dashboard-panel">
          <div className="toolbar">
            <div>
              <h1>Инвестиционные объекты</h1>
              <p>Карточка показывает решение, фото, сильные стороны, риски и короткий рыночный сигнал. Детали раскрывают логику рейтингов и рынок вокруг объекта.</p>
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
            Реальные источники рынка пока не подключены. Данные демонстрационные и нужны для проверки продукта и UX.
          </div>
        </section>
      </main>
    </div>
  );
}
