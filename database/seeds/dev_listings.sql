INSERT INTO listings (
    source,
    external_id,
    title,
    url,
    address,
    price_rub,
    floor,
    building_year,
    property_type,
    area_sqm,
    tenant,
    ai_summary,
    investment_score
) VALUES
(
    'seed',
    'demo-1',
    'Street retail premises with long lease',
    'https://example.com/demo-1',
    'Moscow, Tverskaya Street',
    180000000,
    1,
    2021,
    'street_retail',
    185.40,
    'Federal tenant',
    'Demo listing for local development.',
    82
)
ON CONFLICT (source, external_id) DO NOTHING;

