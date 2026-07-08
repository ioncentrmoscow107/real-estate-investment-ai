"use client";

import { Filter, RefreshCw, Search } from "lucide-react";
import { useMemo, useState } from "react";
import type {
  DashboardProperty,
  IntakeFunnel,
  ProfileFilterDefaults,
  Recommendation,
  SearchProfile,
} from "../lib/api";

const recommendationLabels: Record<Recommendation, string> = {
  BUY: "Покупать",
  WATCH: "Изучить подробнее",
  AVOID: "Не рекомендую",
};

const marketSupportLabels: Record<string, string> = {
  any: "Любая",
  strong: "Сильная",
  moderate: "Умеренная",
  neutral: "Нейтральная",
  weak: "Слабая",
};

type FilterKey = keyof ProfileFilterDefaults;

function numberOrNull(value: string) {
  return value === "" ? null : Number(value);
}

function toInputValue(value: number | null) {
  return value === null ? "" : String(value);
}

function formatRubShort(value: number | null) {
  if (value === null) {
    return "нет данных";
  }
  if (value >= 1_000_000) {
    return `${(value / 1_000_000).toLocaleString("ru-RU", { maximumFractionDigits: 1 })} млн ₽`;
  }
  return `${value.toLocaleString("ru-RU")} ₽`;
}

function formatDateTime(value: string | null) {
  if (!value) {
    return "не запланировано";
  }
  return new Intl.DateTimeFormat("ru-RU", {
    day: "2-digit",
    month: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
  }).format(new Date(value));
}

function matchesRange(value: number | null, min: number | null, max: number | null) {
  if (value === null) {
    return min === null && max === null;
  }
  if (min !== null && value < min) {
    return false;
  }
  if (max !== null && value > max) {
    return false;
  }
  return true;
}

function profileProperties(properties: DashboardProperty[], profileId: string) {
  return properties.filter((property) => property.search_profile_ids.includes(profileId));
}

function applyFilters(properties: DashboardProperty[], filters: ProfileFilterDefaults) {
  const locationQuery = filters.location_query.trim().toLocaleLowerCase("ru-RU");

  return properties.filter((property) => {
    if (!matchesRange(property.price_rub, filters.price_min, filters.price_max)) return false;
    if (!matchesRange(property.price_per_sqm, filters.price_per_sqm_min, filters.price_per_sqm_max)) return false;
    if (!matchesRange(property.area_sqm, filters.area_min, filters.area_max)) return false;
    if (!matchesRange(property.floor, filters.floor_min, filters.floor_max)) return false;
    if (filters.first_floor_only && property.floor !== 1) return false;
    if (locationQuery) {
      const haystack = [property.address, property.district, property.metro].filter(Boolean).join(" ").toLocaleLowerCase("ru-RU");
      if (!haystack.includes(locationQuery)) return false;
    }
    if (filters.source !== "any" && property.source !== filters.source) return false;
    if (filters.property_category !== "any" && property.property_category !== filters.property_category) return false;
    if (filters.deal_type !== "any" && property.deal_type !== filters.deal_type) return false;
    if (filters.recommendation !== "any" && property.recommendation !== filters.recommendation) return false;
    if (property.investment_score < filters.investment_score_min) return false;
    if (property.risk_score > filters.risk_max) return false;
    if (property.data_quality_score < filters.data_quality_min) return false;
    if (filters.tenant_exists && !property.tenant_exists) return false;
    if (filters.federal_tenant_only && !property.has_federal_tenant) return false;
    if (filters.rent_yield_min !== null && (property.rent_yield_percent === null || property.rent_yield_percent < filters.rent_yield_min)) return false;
    if (filters.electric_power_min !== null && (property.electric_power_kw === null || property.electric_power_kw < filters.electric_power_min)) return false;
    if (filters.building_year_min !== null && (property.building_year === null || property.building_year < filters.building_year_min)) return false;
    if (filters.only_with_photos && property.photos.length === 0) return false;
    if (filters.only_with_missing_information && property.missing_information.length === 0) return false;
    if (filters.market_support_level !== "any" && property.market_support_level !== filters.market_support_level) return false;
    return true;
  });
}

function breakdownEntries(items: Record<string, number>) {
  return Object.entries(items).sort((a, b) => b[1] - a[1]);
}

export function ProfileFilterWorkspace({
  properties,
  profiles,
  intakeFunnels,
}: {
  properties: DashboardProperty[];
  profiles: SearchProfile[];
  intakeFunnels: Record<string, IntakeFunnel>;
}) {
  const [activeProfileId, setActiveProfileId] = useState(profiles[0]?.id ?? "");
  const activeProfile = profiles.find((profile) => profile.id === activeProfileId) ?? profiles[0];
  const [filters, setFilters] = useState<ProfileFilterDefaults>(activeProfile.default_filters);

  const profileScopedProperties = useMemo(() => profileProperties(properties, activeProfile.id), [properties, activeProfile.id]);
  const filteredProperties = useMemo(() => applyFilters(profileScopedProperties, filters), [profileScopedProperties, filters]);
  const funnel = intakeFunnels[activeProfile.id];
  const counts = filteredProperties.reduce(
    (acc, property) => {
      acc[property.recommendation] += 1;
      return acc;
    },
    { BUY: 0, WATCH: 0, AVOID: 0 } as Record<Recommendation, number>,
  );

  function selectProfile(profileId: string) {
    const nextProfile = profiles.find((profile) => profile.id === profileId) ?? profiles[0];
    setActiveProfileId(nextProfile.id);
    setFilters(nextProfile.default_filters);
  }

  function updateFilter<Key extends FilterKey>(key: Key, value: ProfileFilterDefaults[Key]) {
    setFilters((current) => ({ ...current, [key]: value }));
  }

  return (
    <section className="dashboard-panel filter-workspace">
      <div className="toolbar">
        <div>
          <h1>Профиль поиска и фильтры</h1>
          <p>Гибкие фильтры работают по текущим sample-объектам и не запускают сбор данных или парсинг URL.</p>
        </div>
        <div className="toolbar-note">
          <Filter size={16} />
          Активный профиль: {activeProfile.name}
        </div>
      </div>

      <div className="profile-layout">
        <div className="profile-selector">
          <label>
            <span>Профиль поиска</span>
            <select value={activeProfile.id} onChange={(event) => selectProfile(event.target.value)}>
              {profiles.map((profile) => (
                <option key={profile.id} value={profile.id}>
                  {profile.name}
                </option>
              ))}
            </select>
          </label>
          <p>{activeProfile.description}</p>
        </div>

        <div className="funnel-card">
          <h2>Воронка intake</h2>
          <div className="funnel-grid">
            <span><strong>{formatDateTime(funnel?.last_run ?? null)}</strong>последний запуск</span>
            <span><strong>{formatDateTime(funnel?.next_run ?? null)}</strong>следующий запуск</span>
            <span><strong>{funnel?.refresh_interval_minutes ?? 0} мин</strong>интервал</span>
            <span><strong>{funnel?.max_listings_per_source ?? 0}</strong>лимит на источник</span>
          </div>
          <div className="breakdown-grid">
            <div>
              <h3>Источники</h3>
              {breakdownEntries(funnel?.source_breakdown ?? {}).map(([label, value]) => (
                <span key={label}>{label}: {value}</span>
              ))}
            </div>
            <div>
              <h3>Локации</h3>
              {breakdownEntries(funnel?.location_breakdown ?? {}).map(([label, value]) => (
                <span key={label}>{label}: {value}</span>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="filter-grid">
        <label><span>Цена от</span><input type="number" value={toInputValue(filters.price_min)} onChange={(event) => updateFilter("price_min", numberOrNull(event.target.value))} /></label>
        <label><span>Цена до</span><input type="number" value={toInputValue(filters.price_max)} onChange={(event) => updateFilter("price_max", numberOrNull(event.target.value))} /></label>
        <label><span>₽/м² от</span><input type="number" value={toInputValue(filters.price_per_sqm_min)} onChange={(event) => updateFilter("price_per_sqm_min", numberOrNull(event.target.value))} /></label>
        <label><span>₽/м² до</span><input type="number" value={toInputValue(filters.price_per_sqm_max)} onChange={(event) => updateFilter("price_per_sqm_max", numberOrNull(event.target.value))} /></label>
        <label><span>Площадь от</span><input type="number" value={toInputValue(filters.area_min)} onChange={(event) => updateFilter("area_min", numberOrNull(event.target.value))} /></label>
        <label><span>Площадь до</span><input type="number" value={toInputValue(filters.area_max)} onChange={(event) => updateFilter("area_max", numberOrNull(event.target.value))} /></label>
        <label><span>Этаж от</span><input type="number" value={toInputValue(filters.floor_min)} onChange={(event) => updateFilter("floor_min", numberOrNull(event.target.value))} /></label>
        <label><span>Этаж до</span><input type="number" value={toInputValue(filters.floor_max)} onChange={(event) => updateFilter("floor_max", numberOrNull(event.target.value))} /></label>
        <label className="filter-wide"><span>Локация / район / метро</span><input value={filters.location_query} onChange={(event) => updateFilter("location_query", event.target.value)} /></label>
        <label><span>Источник</span><select value={filters.source} onChange={(event) => updateFilter("source", event.target.value)}><option value="any">Любой</option><option value="cian">CIAN</option><option value="manual">Manual</option></select></label>
        <label><span>Категория</span><select value={filters.property_category} onChange={(event) => updateFilter("property_category", event.target.value)}><option value="any">Любая</option><option value="commercial">Коммерция</option><option value="small_commercial">Малые помещения</option><option value="office">Офисы</option></select></label>
        <label><span>Тип сделки</span><select value={filters.deal_type} onChange={(event) => updateFilter("deal_type", event.target.value)}><option value="any">Любой</option><option value="sale">Продажа</option><option value="rent">Аренда</option></select></label>
        <label><span>Рекомендация</span><select value={filters.recommendation} onChange={(event) => updateFilter("recommendation", event.target.value as ProfileFilterDefaults["recommendation"])}><option value="any">Любая</option><option value="BUY">Покупать</option><option value="WATCH">Изучить</option><option value="AVOID">Не рекомендую</option></select></label>
        <label><span>Инвест. рейтинг от</span><input type="number" value={filters.investment_score_min} onChange={(event) => updateFilter("investment_score_min", Number(event.target.value))} /></label>
        <label><span>Риск до</span><input type="number" value={filters.risk_max} onChange={(event) => updateFilter("risk_max", Number(event.target.value))} /></label>
        <label><span>Качество данных от</span><input type="number" value={filters.data_quality_min} onChange={(event) => updateFilter("data_quality_min", Number(event.target.value))} /></label>
        <label><span>Доходность от, %</span><input type="number" value={toInputValue(filters.rent_yield_min)} onChange={(event) => updateFilter("rent_yield_min", numberOrNull(event.target.value))} /></label>
        <label><span>Мощность от, кВт</span><input type="number" value={toInputValue(filters.electric_power_min)} onChange={(event) => updateFilter("electric_power_min", numberOrNull(event.target.value))} /></label>
        <label><span>Год дома от</span><input type="number" value={toInputValue(filters.building_year_min)} onChange={(event) => updateFilter("building_year_min", numberOrNull(event.target.value))} /></label>
        <label><span>Поддержка рынка</span><select value={filters.market_support_level} onChange={(event) => updateFilter("market_support_level", event.target.value)}>{Object.entries(marketSupportLabels).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
      </div>

      <div className="filter-toggles">
        <label><input checked={filters.first_floor_only} type="checkbox" onChange={(event) => updateFilter("first_floor_only", event.target.checked)} /> Только первый этаж</label>
        <label><input checked={filters.tenant_exists} type="checkbox" onChange={(event) => updateFilter("tenant_exists", event.target.checked)} /> Есть арендатор</label>
        <label><input checked={filters.federal_tenant_only} type="checkbox" onChange={(event) => updateFilter("federal_tenant_only", event.target.checked)} /> Только федеральный арендатор</label>
        <label><input checked={filters.only_with_photos} type="checkbox" onChange={(event) => updateFilter("only_with_photos", event.target.checked)} /> Только с фото</label>
        <label><input checked={filters.only_with_missing_information} type="checkbox" onChange={(event) => updateFilter("only_with_missing_information", event.target.checked)} /> Только с недостающими данными</label>
      </div>

      <div className="filter-summary">
        <span><strong>{filteredProperties.length}</strong>показано</span>
        <span><strong>{profileScopedProperties.length}</strong>в профиле</span>
        <span><strong>{profileScopedProperties.length - filteredProperties.length}</strong>скрыто фильтрами</span>
        <span><strong>{counts.BUY}</strong>Покупать</span>
        <span><strong>{counts.WATCH}</strong>Изучить подробнее</span>
        <span><strong>{counts.AVOID}</strong>Не рекомендую</span>
      </div>

      <div className="filtered-list">
        {filteredProperties.map((property) => (
          <article className="filtered-card" key={property.id}>
            <div>
              <h2>{property.title}</h2>
              <p>{property.district ?? "район не раскрыт"} · {property.metro ?? "метро не раскрыто"} · {property.source}</p>
            </div>
            <span className={`recommendation recommendation-${property.recommendation.toLowerCase()}`}>{recommendationLabels[property.recommendation]}</span>
            <div className="filtered-metrics">
              <span>{formatRubShort(property.price_rub)}</span>
              <span>{property.area_sqm} м²</span>
              <span>{property.investment_score}/100</span>
              <span>риск {property.risk_score}/100</span>
              <span>{property.rent_yield_percent ?? "нет"}%</span>
            </div>
          </article>
        ))}
        {filteredProperties.length === 0 && (
          <div className="empty-filter-state">
            <Search size={18} />
            Нет объектов под выбранные фильтры.
          </div>
        )}
      </div>

      <button className="reset-filters" type="button" onClick={() => setFilters(activeProfile.default_filters)}>
        <RefreshCw size={16} />
        Вернуть настройки профиля
      </button>
    </section>
  );
}
