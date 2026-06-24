CREATE TABLE IF NOT EXISTS listings (
    id BIGSERIAL PRIMARY KEY,
    source VARCHAR(40) NOT NULL,
    external_id VARCHAR(128) NOT NULL,
    title VARCHAR(500) NOT NULL,
    url TEXT NOT NULL,
    address VARCHAR(500),
    price_rub NUMERIC(14, 2) NOT NULL,
    floor INTEGER NOT NULL,
    building_year INTEGER NOT NULL,
    property_type VARCHAR(80) NOT NULL,
    area_sqm NUMERIC(10, 2),
    tenant VARCHAR(255),
    ai_summary TEXT,
    investment_score INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_listing_source_external_id UNIQUE (source, external_id)
);

CREATE INDEX IF NOT EXISTS ix_listings_source ON listings (source);
CREATE INDEX IF NOT EXISTS ix_listings_price_rub ON listings (price_rub);
CREATE INDEX IF NOT EXISTS ix_listings_floor ON listings (floor);
CREATE INDEX IF NOT EXISTS ix_listings_building_year ON listings (building_year);
CREATE INDEX IF NOT EXISTS ix_listings_property_type ON listings (property_type);
CREATE INDEX IF NOT EXISTS ix_listings_created_at ON listings (created_at DESC);

