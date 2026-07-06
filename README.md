# CRE Investment AI Platform

Production-oriented starter project for commercial real estate investment analysis.

The platform is designed to collect listings every 30 minutes from CIAN, Avito, Domclick, and Yandex Realty, normalize them into PostgreSQL, and prepare them for OpenAI-powered investment analysis.

Scraping is intentionally not implemented yet. Source adapters exist as explicit interfaces so scraping can be added safely without changing the rest of the system.

## Stack

- Backend: Python, FastAPI, SQLAlchemy, APScheduler
- Database: PostgreSQL
- Frontend: Next.js
- AI: OpenAI API
- Runtime: Docker Compose

## Current Filters

- Price: 100-400 million RUB
- Floor: 1st floor only
- Building year: 2016+
- Property types: street retail, retail, free use, federal tenant

## Quick Start

1. Copy `.env.example` to `.env`.
2. Add `OPENAI_API_KEY` when AI analysis is needed.
3. Start the stack:

```bash
docker compose up --build
```

Services:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Backend docs: http://localhost:8000/docs
- PostgreSQL: localhost:5432

## Useful Endpoints

- `GET /health`
- `GET /api/v1/listings`
- `GET /api/v1/collectors/status`
- `POST /api/v1/collectors/run`

## Data Acquisition Pipeline v1

The v1 acquisition foundation lives in `backend/app/services/acquisition`.
It includes the source adapter contract, a safe CIAN adapter stub, normalized
listing fields, business filtering, conservative deduplication, and text
extraction helpers for electric power, repair condition, and federal tenants.

Run backend tests in development mode:

```bash
PYTHONPATH=backend pytest backend/tests
```

The CIAN adapter does not perform production scraping. It is intentionally a
stub that supports mock/sample payload normalization until a compliant public,
import, or API-compatible data path is approved.

## Investment Scoring v1

Rule-based investment scoring lives in `backend/app/services/acquisition/scoring.py`.
It calculates investment, liquidity, risk, fake, and data quality scores without
calling OpenAI. The scorer is intentionally skeptical: missing data, weak power,
no federal tenant, suspicious pricing, repair needs, and long exposure are all
surfaced as explicit disadvantages or risks.

## Property Intelligence Engine v1

Deterministic property intelligence lives in
`backend/app/services/acquisition/property_intelligence.py`. Editable investment
knowledge rules are stored separately in
`backend/app/services/acquisition/rules/property_intelligence_rules.json`.

The engine returns independent investment, liquidity, tenant, building,
location, risk, fake, and data quality scores with explanations for every score,
plus advantages, disadvantages, risks, missing information, due diligence
checklist, recommendation, and summary.

## Dashboard v1

The investor dashboard consumes sample analyzed properties from
`GET /api/v1/dashboard/properties`. It shows total properties, average
investment score, BUY / WATCH / AVOID counts, and a compact expandable list of
all analyzed properties. Real scraping is not implemented in this dashboard
task.

## Project Structure

```text
backend/      FastAPI app, API routes, database models, scheduler, collectors
frontend/     Next.js dashboard
database/     PostgreSQL schema and seed files
ai/           AI prompt templates and analysis contract
docs/         Engineering notes
docker/       Dockerfiles
```
