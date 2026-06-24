# Architecture

The backend owns listing collection, filtering, persistence, and AI analysis orchestration.

The frontend is a Next.js dashboard that reads from the backend API.

PostgreSQL stores normalized listings and AI outputs. Source-specific scraping code should live behind collector adapters in `backend/app/services/collectors`.

## Collection Flow

1. APScheduler triggers every 30 minutes.
2. Collector registry calls each source adapter.
3. Raw listings are filtered by investment criteria.
4. Matching listings are persisted with source and external ID uniqueness.
5. AI analysis can enrich accepted listings.

## Scraping Boundary

Scraping is not implemented in this scaffold. Each source should be added as a concrete collector implementing the `collect()` method. Keep parsing, retries, rate limits, and source-specific authentication isolated inside each adapter.

