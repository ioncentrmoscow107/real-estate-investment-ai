# Property Intelligence Engine v1

## Назначение

Property Intelligence Engine v1 превращает нормализованные данные объекта в структурированную инвестиционную аналитику без LLM и без OpenAI API. Engine полностью детерминированный: один и тот же `NormalizedListing` при одних и тех же правилах всегда дает один и тот же результат.

## Где находится реализация

```text
backend/app/services/acquisition/property_intelligence.py
backend/app/services/acquisition/rules/property_intelligence_rules.json
```

Python-код отвечает за применение правил. Инвестиционные правила лежат отдельно в JSON, чтобы менять веса, условия, тексты объяснений и checklist без изменения application code.

## Вход

Engine принимает `NormalizedListing` из acquisition pipeline.

Используемые поля:

- price_rub;
- area_sqm;
- price_per_sqm;
- address;
- latitude;
- longitude;
- floor;
- building_year;
- property_type;
- tenant_name;
- tenant_type;
- has_federal_tenant;
- electric_power_kw;
- electric_power_can_be_increased;
- repair_condition;
- photos;
- seller_name;
- seller_phone_hash;
- raw_payload.exposure_days или raw_payload.days_on_market.

## Выход

Каждый объект получает полный `PropertyIntelligence`:

- Investment Score;
- Liquidity Score;
- Tenant Score;
- Building Score;
- Location Score;
- Risk Score;
- Fake Score;
- Data Quality Score;
- advantages;
- disadvantages;
- risks;
- missing_information;
- due_diligence_checklist;
- explanations по каждому score;
- recommendation: BUY, WATCH, AVOID;
- short_summary;
- rules_version.

## Explanation engine

Для каждого score возвращается:

- финальное значение;
- список текстовых объяснений;
- список примененных rule id.

Даже если score не был изменен конкретным правилом, engine возвращает объяснение:

```text
No specific rule adjusted this score.
```

Это гарантирует, что dashboard и API всегда могут показать причину оценки.

## Принцип скептического аналитика

Engine не продает объект. Он ищет причины не покупать:

- missing data;
- низкая электрическая мощность;
- отсутствие федерального арендатора;
- ремонт или shell/core;
- не первый этаж;
- старое здание;
- подозрительно низкая цена;
- долгая экспозиция;
- отсутствие фото;
- слабая идентификация продавца.

## Примеры правил

```text
IF electric_power_kw < 30
THEN reduce Liquidity Score
```

```text
IF federal tenant
THEN increase Tenant Score
```

```text
IF repair_condition == "none"
THEN reduce Investment Score
```

```text
IF electric_power_can_be_increased == true
THEN increase Liquidity Score
```

```text
IF building_year >= 2020
THEN increase Building Score
```

## Формат правила

```json
{
  "id": "federal_tenant",
  "conditions": [
    {"field": "has_federal_tenant", "operator": "eq", "value": true}
  ],
  "score_adjustments": {
    "tenant_score": 30,
    "liquidity_score": 14,
    "investment_score": 14
  },
  "advantages": ["Federal tenant improves income reliability."],
  "due_diligence": ["Verify lease agreement, tenant entity, rent, indexation, and break options."],
  "explanations": {
    "tenant_score": "Federal tenant materially improves tenant quality."
  }
}
```

## Поддерживаемые операторы

- `missing`;
- `present`;
- `eq`;
- `neq`;
- `lt`;
- `lte`;
- `gt`;
- `gte`;
- `in`;
- `not_between`.

## Recommendation

Пороговые значения лежат в JSON:

```text
BUY:
  investment_score >= 75
  risk_score <= 45
  fake_score <= 35
  data_quality_score >= 70

AVOID:
  investment_score <= 49
  или risk_score >= 70
  или fake_score >= 60
  или data_quality_score <= 44

WATCH:
  все промежуточные случаи
```

## Ограничения v1

- Нет LLM/OpenAI.
- Нет внешней рыночной базы comparable sales.
- Location Score пока использует только наличие адреса/координат и raw context.
- Правила простые и объяснимые, не статистические.
- Engine не заменяет due diligence, а формирует список проверок.

