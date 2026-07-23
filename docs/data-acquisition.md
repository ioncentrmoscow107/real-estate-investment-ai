# Data Acquisition Pipeline v1

## Назначение

Pipeline v1 создает безопасную и расширяемую основу для обработки объявлений коммерческой недвижимости. В этой версии не реализуется production scraping. Система готовит контракты и сервисы, через которые позже можно подключать источники легальным и устойчивым способом.

## Архитектура

```text
Collector -> RawListing -> Normalizer -> Filter -> Matcher -> Property -> Analyzer -> Scorer -> Dashboard
```

В этой задаче реализована foundation-часть:

```text
Collector -> RawListing -> Normalizer -> Filter -> Matcher
```

## Модель RawListing

`RawListing` хранит минимальный исходный пакет от источника:

- `source`;
- `source_listing_id`;
- `source_url`;
- `raw_payload`;
- `collected_at`.

Raw payload сохраняется для аудита, повторной нормализации и будущего анализа изменений.

## Модель NormalizedListing

Единая схема объявления содержит:

- source;
- source_listing_id;
- source_url;
- title;
- description;
- address;
- coordinates;
- price_rub;
- area_sqm;
- price_per_sqm;
- floor;
- total_floors;
- building_year;
- property_type;
- tenant_name;
- tenant_type;
- has_federal_tenant;
- electric_power_kw;
- electric_power_verified;
- electric_power_can_be_increased;
- electric_power_increase_to_kw;
- electric_power_source;
- repair_condition;
- vacant_property_fitout_comment;
- photos;
- seller_name;
- seller_phone_hash;
- published_at;
- first_seen_at;
- last_seen_at;
- raw_payload.

## Бизнес-фильтры MVP

Объект проходит фильтр только если:

- цена от 100,000,000 RUB до 400,000,000 RUB;
- первый этаж;
- здание 2016 года или новее;
- тип объекта входит в допустимые категории или найден федеральный арендатор.

Допустимые типы:

- `street_retail`;
- `retail_premises`;
- `free_use_commercial_premises`;
- `free_use`;
- `federal_tenant`.

## Извлечение полей

Pipeline v1 умеет извлекать из русского текста:

- электрическую мощность в кВт;
- возможность увеличения мощности;
- состояние ремонта;
- федерального арендатора.

Поддерживаемые примеры мощности:

- `электрическая мощность 80 кВт`;
- `мощность 50 кВт, возможно увеличение до 100 кВт`;
- `выделенная мощность 120кВт`.

Поддерживаемые примеры ремонта:

- `без ремонта`;
- `shell&core`;
- `сделан качественный ремонт`;
- `требуется ремонт`.

Поддерживаемые федеральные tenant examples:

- Пятерочка;
- ВкусВилл;
- Магнит;
- Ozon;
- Wildberries;
- Аптека.

## Дедупликация v1

Basic deduplication service возвращает match confidence и причину совпадения. Он пока не мутирует данные и не создает persisted Property. Это намеренно: текущий слой должен быть безопасной основой для будущего `Building -> Property -> Listing`.

Правила:

- `same source + source_listing_id` дает 100 confidence;
- совпадающий адрес дает +40;
- похожая площадь в пределах 3% дает +20;
- тот же этаж дает +10;
- похожая цена в пределах 5% дает +10;
- тот же tenant дает +10;
- тот же seller phone hash дает +10.

## Ограничения

- Нет production scraping.
- Нет обхода логина.
- Нет обхода капчи.
- Нет обхода антибот-защиты.
- Фоновый scheduler запускается вместе с lifecycle FastAPI и вызывает
  зарегистрированные collector adapters с настроенным интервалом. В текущем MVP
  adapters остаются stub-реализациями и не получают реальные объявления.
- Нет записи в PostgreSQL в этой задаче.

