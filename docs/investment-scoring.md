# Investment Scoring v1

## Назначение

Investment Scoring v1 считает структурный инвестиционный анализ для каждого нормализованного коммерческого объекта без OpenAI API. Это rule-based слой, который должен работать предсказуемо, объяснимо и скептически.

Сервис находится в:

```text
backend/app/services/acquisition/scoring.py
```

## Входные данные

Скоринг принимает `NormalizedListing` из data acquisition pipeline.

Ключевые поля:

- `price_rub`;
- `area_sqm`;
- `price_per_sqm`;
- `floor`;
- `building_year`;
- `electric_power_kw`;
- `electric_power_can_be_increased`;
- `has_federal_tenant`;
- `tenant_name`;
- `repair_condition`;
- `photos`;
- `seller_name`;
- `seller_phone_hash`;
- `raw_payload.exposure_days` или `raw_payload.days_on_market`, если есть.

## Выходные данные

`InvestmentAnalysis` содержит:

- `investment_score` от 0 до 100;
- `liquidity_score` от 0 до 100;
- `risk_score` от 0 до 100;
- `fake_score` от 0 до 100;
- `data_quality_score` от 0 до 100;
- `advantages`;
- `disadvantages`;
- `risks`;
- `recommendation`: `BUY`, `WATCH`, `AVOID`;
- `short_summary`.

## Скептический принцип

Скоринг не должен продавать объект. Он должен искать причины не покупать:

- missing data;
- подозрительно низкая цена;
- слабая или неизвестная tenant story;
- недостаточная электрическая мощность;
- ремонт или shell&core;
- не первый этаж;
- старое здание;
- долгая экспозиция;
- отсутствие продавца, телефона или фото.

## Основные факторы

### Investment Score

Итоговая оценка собирается из:

- price score;
- building score;
- tenant score;
- power score;
- repair score;
- liquidity score;
- data quality score;
- risk penalty;
- fake penalty.

### Liquidity Score

Повышают ликвидность:

- первый этаж;
- федеральный арендатор;
- цена в диапазоне 100-400 млн RUB;
- площадь в ликвидном диапазоне;
- отсутствие долгой экспозиции.

Снижают ликвидность:

- этаж выше первого;
- цена вне диапазона;
- очень крупная площадь;
- экспозиция 90+ дней.

### Risk Score

Повышают риск:

- не первый этаж;
- здание старше 2016 года;
- отсутствует электрическая мощность;
- низкая мощность без возможности увеличения;
- нет федерального арендатора;
- требуется ремонт;
- долгая экспозиция.

### Fake Score

Повышают fake score:

- нет адреса;
- нет фотографий;
- подозрительно низкая цена за м2;
- нет электрической мощности;
- нет продавца и seller phone hash.

Снижает fake score:

- подтвержденный федеральный арендатор.

### Data Quality Score

Снижается при отсутствии:

- цены;
- площади;
- цены за м2;
- адреса;
- этажа;
- года постройки;
- типа помещения;
- электрической мощности;
- фотографий.

## Recommendation

```text
BUY:
  investment_score >= 75
  risk_score <= 45
  fake_score <= 35
  data_quality_score >= 70

AVOID:
  investment_score < 50
  или risk_score >= 70
  или fake_score >= 60
  или data_quality_score < 45

WATCH:
  все промежуточные случаи
```

## Ограничения v1

- Нет OpenAI API.
- Нет рыночной базы comparable sales.
- Подозрительно низкая цена определяется грубым порогом.
- Скоринг не заменяет due diligence.
- Результат должен использоваться как первичная аналитическая сортировка, а не как автоматическое инвестиционное решение.

