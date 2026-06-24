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

## Project Structure

```text
backend/      FastAPI app, API routes, database models, scheduler, collectors
frontend/     Next.js dashboard
database/     PostgreSQL schema and seed files
ai/           AI prompt templates and analysis contract
docs/         Engineering notes
docker/       Dockerfiles
```

