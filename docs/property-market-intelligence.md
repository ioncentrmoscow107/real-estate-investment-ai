# Property & Market Intelligence v1

## Назначение

Property & Market Intelligence v1 расширяет dashboard от оценки самого объекта к объяснимому инвестиционному досье: фото, физический контекст помещения, окружение, трафик, конкуренты, аналоги продаж и аренды, локальные тренды и вывод о поддержке рынка.

В этой версии используются только sample/mock данные. Реальные источники, scraping, карты, геокодинг и внешние market-data API не подключаются.

## Data model

Каждый dashboard property сохраняет существующие поля:

- базовые параметры объекта;
- score-поля;
- рекомендацию `BUY`, `WATCH`, `AVOID`;
- преимущества;
- недостатки;
- риски;
- недостающие данные;
- due diligence checklist.

Дополнительно добавлены блоки:

- `score_explanations`;
- `photos`;
- `building_context`;
- `surroundings_context`;
- `traffic_context`;
- `competition_context`;
- `nearby_sale_comparables`;
- `sale_comparables_summary`;
- `nearby_rental_rates`;
- `rental_rates_summary`;
- `district_market_trends`;
- `residential_market_context`;
- `market_support_summary`;
- `market_signal`.

## Explainable scores

`score_explanations` содержит объяснение по каждому score:

- `positive_factors`;
- `negative_factors`;
- `summary`.

Этот блок нужен, потому что инвесторы не доверяют необъясненным оценкам. Для риска и риска фейка UI отдельно поясняет, что высокий score хуже.

В будущей версии эти объяснения могут формироваться из rule engine, LLM-аналитика или комбинированной модели, но сейчас они заданы как русские sample-text для проверки UX.

## Photos

`photos` содержит:

- `url`;
- `caption`;
- `type`;
- `is_main`.

Если реального изображения нет, frontend показывает CSS-заглушку. Это позволяет проверить layout без нестабильных remote images и без подключения внешних источников.

В будущем реальные фото могут приходить из разрешенных импортов, партнерских feed-ов или официальных API.

## Building context

`building_context` описывает дом и физическое помещение:

- год постройки;
- класс / тип дома;
- количество квартир;
- коммерческие помещения;
- этажность;
- паркинг;
- фасад;
- вход;
- витрины;
- высоту потолков;
- отдельный вход;
- разгрузку;
- комментарий.

В будущем этот блок должен влиять на `building_score`, `liquidity_score`, `risk_score` и `data_quality_score`.

## Surroundings context

`surroundings_context` описывает спрос вокруг объекта:

- жилую плотность;
- офисную плотность;
- школы;
- детские сады;
- медцентры;
- бизнес-центры;
- торговые центры;
- транспорт;
- метро;
- парковки;
- якорные точки спроса.

В будущем этот блок должен влиять на `location_score`, `liquidity_score` и market support conclusion.

## Traffic context

`traffic_context` описывает пешеходный, автомобильный, целевой и транзитный трафик, видимость с дороги, расстояние до метро и остановок, основные маршруты, усиливающие и ослабляющие факторы.

В будущем этот блок должен влиять на `location_score`, `liquidity_score`, `tenant_score` и `risk_score`.

## Competition context

`competition_context` показывает:

- количество конкурентов;
- вакантные помещения;
- насыщенность;
- категории конкурентов;
- якорных арендаторов;
- риск перенасыщения;
- комментарий AI.

В будущем этот блок должен снижать ликвидность и повышать риск при высокой вакансии или перенасыщении, а также помогать выбирать подходящий tenant mix.

## Commercial sale comparables

`nearby_sale_comparables` хранит аналоги продаж:

- название;
- расстояние;
- площадь;
- цену;
- цену за м²;
- тип помещения;
- год здания;
- источник;
- уверенность.

`sale_comparables_summary` хранит средний, минимальный и максимальный уровень цены за м², отклонение объекта от рынка и вывод.

В будущем этот блок должен влиять на `investment_score`, `risk_score`, `fake_score` и `data_quality_score`.

## Rental comparables

`nearby_rental_rates` хранит аналоги аренды:

- название;
- расстояние;
- тип;
- площадь;
- аренду в месяц;
- ставку ₽/м²/год;
- источник;
- уверенность.

`rental_rates_summary` показывает рыночный диапазон и вывод о реалистичности арендной ставки.

В будущем этот блок должен влиять на `investment_score`, `tenant_score`, `liquidity_score` и `risk_score`.

## District market trends

`district_market_trends` содержит:

- тренд коммерческой аренды;
- тренд коммерческих продаж;
- тренд вакантности.

Для каждого тренда хранится период, направление, изменение в процентах, уверенность и объяснение.

В будущем тренды должны усиливать или ослаблять market support conclusion и корректировать risk score.

## Residential market context

`residential_market_context` делится на:

- `new_development`;
- `resale_market`.

Новостройки показывают будущий локальный спрос. Вторичный рынок показывает платежеспособность, ликвидность района и устойчивость спроса.

В будущем этот блок должен влиять на `location_score`, `liquidity_score` и long-term market support.

## Market support conclusion

`market_support_summary` отвечает на вопрос: поддерживает ли локальный рынок покупку.

Уровни:

- сильная поддержка рынка;
- умеренная поддержка рынка;
- нейтрально;
- слабая поддержка рынка;
- данных недостаточно.

Вывод включает positive и negative factors, чтобы инвестор видел не только итог, но и причины.

## What can be mocked now

В v1 можно безопасно mock-ать:

- фото через CSS placeholders;
- score explanations;
- building context;
- surroundings context;
- traffic levels;
- competition context;
- sale/rent comparables;
- district trends;
- residential market context;
- market support conclusion.

Mock-данные нужны для проверки продукта, UI, API shape и будущих тестов.

## Possible real sources later

Будущие источники должны подключаться только легальным и устойчивым способом:

- официальные API, если доступны;
- партнерские фиды;
- разрешенные выгрузки;
- ручные или полуавтоматические импорты;
- внутренние базы сделок и аренды;
- проверенные отчеты брокеров;
- разрешенные справочники зданий и районов.

Запрещено подключать aggressive scraping, обход логина, captcha bypass, anti-bot bypass или маскировку под пользователя для обхода правил площадки.

## Limitations

- Данные рынка сейчас sample/mock, не реальные.
- Аналоги продаж и аренды не являются доказательством рыночной стоимости.
- Тренды района не подтверждены внешними источниками.
- Фото являются placeholder-ами.
- Вывод по рынку демонстрирует продуктовую логику, а не заменяет due diligence.
- Перед сделкой все параметры должны подтверждаться документами, натурной проверкой и независимой оценкой.
