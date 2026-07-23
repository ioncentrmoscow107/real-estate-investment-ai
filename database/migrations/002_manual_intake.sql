CREATE TABLE IF NOT EXISTS manual_intake_batches (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(32) NOT NULL,
    source VARCHAR(40) NOT NULL DEFAULT 'manual',
    linked_search_profile_id VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS manual_listing_urls (
    id VARCHAR(36) PRIMARY KEY,
    batch_id VARCHAR(36) NOT NULL
        REFERENCES manual_intake_batches(id) ON DELETE CASCADE,
    url TEXT NOT NULL,
    source_detected VARCHAR(40) NOT NULL,
    status VARCHAR(32) NOT NULL,
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_manual_listing_url_batch_url UNIQUE (batch_id, url)
);

CREATE INDEX IF NOT EXISTS ix_manual_intake_batches_status
    ON manual_intake_batches (status);
CREATE INDEX IF NOT EXISTS ix_manual_intake_batches_created_at
    ON manual_intake_batches (created_at DESC);
CREATE INDEX IF NOT EXISTS ix_manual_listing_urls_batch_id
    ON manual_listing_urls (batch_id);
CREATE INDEX IF NOT EXISTS ix_manual_listing_urls_source_detected
    ON manual_listing_urls (source_detected);
CREATE INDEX IF NOT EXISTS ix_manual_listing_urls_status
    ON manual_listing_urls (status);
