# Source Adapters

## Принцип

Каждый источник реализует единый adapter contract:

```python
class BaseSourceAdapter:
    source_name: str

    def collect(self) -> list[RawListing]:
        ...

    def normalize(self, raw_listing: RawListing) -> NormalizedListing:
        ...
```

Цель adapter:

- безопасно получить raw listings разрешенным способом;
- не принимать инвестиционных решений;
- привести source-specific payload к `NormalizedListing`;
- сохранить raw payload для аудита и повторной обработки.

## CIAN Adapter Stub

Реализован `CianAdapter`, но production collection намеренно не включен.

Текущий `collect()` возвращает пустой список и содержит TODO:

- использовать public pages/import/API-compatible access там, где это разрешено;
- проверять robots.txt и условия использования;
- соблюдать rate limits;
- не обходить login, captcha и anti-bot механизмы.

`normalize()` уже работает с mock/sample payload и извлекает:

- цену;
- площадь;
- цену за м2;
- этаж;
- год здания;
- тип объекта;
- адрес;
- координаты;
- федерального арендатора;
- электрическую мощность;
- состояние ремонта;
- фото;
- продавца.

## Planned Sources

Планируемые источники:

- CIAN;
- Avito;
- Domclick;
- Yandex Realty.

В этой версии реализован только универсальный contract и CIAN adapter stub. Остальные adapter должны повторять тот же интерфейс.

## Безопасность и compliance

Запрещено:

- aggressive scraping;
- anti-bot bypass;
- captcha bypass;
- login/session bypass;
- маскировка под обычного пользователя для обхода правил площадки.

Разрешенный будущий подход:

- официальные API, если доступны;
- выгрузки и партнерские фиды;
- публичные страницы при соблюдении robots.txt и условий площадки;
- ручные или полуавтоматические импорты для тестового режима.

