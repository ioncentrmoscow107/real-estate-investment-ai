# Dashboard v1

## Назначение

Dashboard v1 показывает инвестору все проанализированные объекты в компактном виде. Это не витрина лучших предложений: на экране есть BUY, WATCH и AVOID, чтобы инвестор видел как сильные объекты, так и причины отказаться от слабых.

## Источник данных

В v1 dashboard использует mock/sample analyzed properties. Реальный scraping не реализован и не запускается.

Backend endpoint:

```text
GET /api/v1/dashboard/properties
```

## Summary metrics

Верхняя панель показывает:

- total properties;
- average investment score;
- количество BUY / WATCH / AVOID;
- текущий режим анализа.

## Property list

Каждая строка показывает компактный набор:

- title/address;
- price_rub;
- area_sqm;
- price_per_sqm;
- investment_score;
- liquidity_score;
- risk_score;
- fake_score;
- data_quality_score;
- recommendation.

## Expandable details

Детали раскрываются по объекту и содержат:

- short_summary;
- advantages;
- disadvantages;
- risks;
- missing information;
- due diligence checklist.

Главный список намеренно остается компактным, чтобы не перегружать инвестора.

## Ограничения v1

- Используются sample objects.
- Нет real scraping.
- Нет live database query для analyzed properties.
- Нет сортировки и фильтров на frontend.
- Нет отдельной страницы full analysis.

Эти ограничения осознанные: цель v1 — показать investor-facing workflow и структуру данных для будущего production dashboard.

