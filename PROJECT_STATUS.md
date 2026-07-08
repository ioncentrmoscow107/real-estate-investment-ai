# Project Status

This file is the project control panel. Keep it updated after each meaningful sprint, feature, fix, or architectural change.

## Current Version

0.1.0

Current milestone: TASK-009 Editable Property Data, Manual Overrides & Deal Workflow v1.

## Completed Sprints

- Initial project scaffold.
- Data Acquisition Pipeline v1.
- Investment Scoring v1.
- Property Intelligence Engine v1.
- Dashboard v1.
- TASK-005: Russian Investor Dashboard UX v2.
- TASK-006: Property & Market Intelligence v1.
- TASK-007: Local Dev Environment Stabilization.
- TASK-007A: Local Run Scripts Bootstrap Hotfix.
- Manual Listing Intake / Manual Analysis Batch concept.
- TASK-008B: Flexible Search Profiles and Dashboard Filters.
- TASK-009: Editable Property Data, Manual Overrides & Deal Workflow v1.

## Current Sprint

TASK-009: Editable Property Data, Manual Overrides & Deal Workflow v1.

Focus:

- Add sample manual overrides and correction history.
- Add deal workflow status and next action to every sample property.
- Add requested document checklist examples.
- Keep the task sample/UI-only without persistence or real editing.

## Completed Features

- FastAPI backend application with health, listings, collectors, and dashboard routes.
- PostgreSQL schema for persisted listings.
- Docker Compose runtime for database, backend, and frontend.
- APScheduler-based collection interval service.
- Collector registry with source placeholders for CIAN, Avito, Domclick, and Yandex Realty.
- Safe source adapter contract for raw collection and normalization.
- CIAN adapter stub with mock/sample payload normalization.
- Normalized listing model for commercial real estate objects.
- MVP investment filters:
  - price from 100,000,000 RUB to 400,000,000 RUB;
  - first floor;
  - building year 2016 or newer;
  - supported property types or federal tenant signal.
- Text extraction for electric power, repair condition, and federal tenant signals.
- Conservative deduplication confidence service.
- Rule-based investment scoring without OpenAI API calls.
- Deterministic Property Intelligence Engine with editable JSON rules.
- Dashboard sample data service.
- Investor dashboard in Next.js showing summary metrics, scores, recommendations, risks, missing information, and due diligence items.
- Russian investor-facing dashboard UX with localized recommendation labels:
  - `BUY` -> `Покупать`;
  - `WATCH` -> `Изучить подробнее`;
  - `AVOID` -> `Не рекомендую`.
- Compact investment memo cards with key facts, strengths, risks, all score groups, missing information, and due diligence checklist.
- Russian sample analyzed properties for realistic Moscow commercial real estate scenarios.
- Dashboard API response includes average risk and full score set for investor details.
- Property & Market Intelligence v1 sample data:
  - explainable score factors;
  - photo placeholders;
  - building and premises context;
  - surroundings context;
  - traffic context;
  - competition context;
  - nearby sale comparables;
  - nearby rental rates;
  - district commercial market trends;
  - residential new-development and resale context;
  - market support conclusion.
- Dashboard v3 expanded investor dossier sections for property and market intelligence.
- Documentation in `docs/` for architecture, operations, data acquisition, source adapters, investment scoring, property intelligence, and dashboard.
- Windows local development scripts:
  - `scripts/start_backend.ps1`;
  - `scripts/start_frontend.ps1`;
  - `scripts/check_env.ps1`;
  - `scripts/git_status.ps1`.
- Russian local run guide in `docs/local-run.md`.
- README local development section with backend/frontend commands and URLs.
- `.gitignore` coverage for Python caches, pytest cache, frontend build/runtime folders, local env files, and OS metadata.
- TASK-007A hotfix for local run scripts:
  - backend script bootstraps missing `.venv` and backend dependencies;
  - frontend script bootstraps missing `frontend/node_modules`;
  - environment check reports Python, venv Python, uvicorn, Node, npm.cmd, node_modules, and ports.
- Manual listing intake concept:
  - sample `manual_intake_batch` and `manual_listing_url` data;
  - dashboard section for `Ручная подборка`;
  - documentation in `docs/listing-intake-strategy.md`.
- Flexible search profile concept:
  - predefined profiles for commercial 100-400M, small premises under 30M, offices 30-150M, tenant-income properties, and custom filtering;
  - dashboard filter panel with price, price per sqm, area, floor, location, source, category, deal type, recommendation, score, risk, data quality, tenant, yield, power, building year, photo, missing-info, and market-support controls;
  - filter result summary and profile-specific intake funnel.
- Property workflow and manual overrides concept:
  - manual overrides for corrected/verified property fields;
  - correction history for audit-style change display;
  - workflow status and next action for every sample property;
  - requested document checklist in expanded property cards.

## Known Issues

- Production scraping is not implemented.
- Collector placeholders currently return no real listings.
- Dashboard v2 uses sample analyzed properties, not live database-backed analyzed properties.
- Property & Market Intelligence v1 uses sample/mock market data, not real external market data.
- Real market data is still sample/mock.
- Real scraping is not implemented.
- Manual URL parsing is not implemented; manual intake is currently sample/mock only.
- Search profiles and filters currently run on sample properties only.
- Property workflow, overrides, and documents are sample/UI-only; no persistence or real editing yet.
- Photos are CSS/sample placeholders, not real listing photos.
- No frontend sorting or filtering in Dashboard v2.
- No full property analysis detail page.
- OpenAI package and prompt assets exist, but current scoring/intelligence is deterministic and does not call OpenAI.
- Property Intelligence rule explanations remain in English internally; the investor-facing dashboard displays Russian sample analysis text.
- `docs/data-acquisition.md` says no background scheduler for that milestone, while the current FastAPI app starts the scheduler service on lifespan. The active collectors are stubs, so this does not currently collect real data.
- Windows PowerShell may block `.venv\Scripts\Activate.ps1`; direct `.venv\Scripts\python.exe` commands are documented.
- Windows PowerShell may block direct `.ps1` execution; use `powershell -ExecutionPolicy Bypass -File ...` as documented.
- Working tree may contain generated/runtime files locally:
  - backend `__pycache__/` directories;
  - `frontend/.next/`;
  - `frontend/node_modules/`.
- `frontend/next-env.d.ts` has a local generated comment change.

## Next Tasks

- After environment stabilization, plan real source ingestion / CIAN adapter / data ingestion validation.
- Decide the next data source path:
  - official API;
  - partner feed;
  - permitted public pages;
  - manual or semi-automatic import.
- Plan validation for real property and market intelligence inputs.
- Decide how to ingest compliant photos, building data, comparables, rent rates, and trend data.
- Connect dashboard to persisted analyzed properties when the backend has a durable analysis store.
- Add dashboard sorting and filtering.
- Add a full property analysis view.
- Localize rule explanation text if those explanations become visible in the UI.
- Add operational logging and job metrics before enabling real collection.
- Clarify scheduler behavior in docs versus runtime.
- Expand tests around dashboard API contracts and frontend data assumptions.

## Last Commit

Pending local commit: `Add property workflow and manual overrides concept`

Branch: `main`

Remote tracking: `origin/main`

## Repository Structure

```text
.
|-- ai/
|   |-- analysis_contract.json
|   `-- prompts/
|-- backend/
|   |-- app/
|   |   |-- api/
|   |   |-- core/
|   |   |-- db/
|   |   |-- models/
|   |   |-- schemas/
|   |   `-- services/
|   |       |-- acquisition/
|   |       |-- ai/
|   |       `-- collectors/
|   `-- tests/
|-- database/
|   |-- migrations/
|   `-- seeds/
|-- docker/
|   |-- backend/
|   `-- frontend/
|-- docs/
|-- frontend/
|   |-- app/
|   |-- components/
|   `-- lib/
|-- docker-compose.yml
|-- requirements.txt
|-- README.md
`-- PROJECT_STATUS.md
```

## Roadmap

### Phase 1: Foundation

Status: complete.

- Backend scaffold.
- Database schema.
- Docker Compose runtime.
- Source adapter boundaries.
- Documentation baseline.

### Phase 2: Acquisition Foundation

Status: complete.

- Raw listing model.
- Normalized listing model.
- CIAN normalization stub.
- MVP business filters.
- Text extraction helpers.
- Deduplication confidence service.

### Phase 3: Deterministic Analysis

Status: complete.

- Rule-based investment scoring.
- Property Intelligence Engine.
- Editable JSON rules.
- Explanations, risks, advantages, missing information, and due diligence output.

### Phase 4: Investor Dashboard

Status: complete for v3 sample-data UX.

- Sample analyzed properties endpoint.
- Summary metrics.
- Compact expandable property list.
- Recommendation display for BUY, WATCH, and AVOID.
- Russian investor-facing labels and sample data.
- Compact investment memo cards.
- Expanded score details and due diligence blocks.
- Property & Market Intelligence sections with photos, score explanations, market context, comparables, trends, residential market context, and market support conclusion.

### Phase 5: Stabilization

Status: current / next.

- Clean generated artifacts from working tree.
- Confirm `.gitignore` coverage.
- Align docs and runtime scheduler behavior.
- Harden API contracts and tests.

### Phase 6: Real Data Path

Status: planned.

- Select compliant source access method.
- Implement one approved source integration.
- Add operational logging, metrics, retries, and rate limiting.
- Persist normalized and analyzed properties.

### Phase 7: Production Dashboard

Status: planned.

- Replace sample dashboard data with live analyzed properties.
- Add sorting, filtering, and full property analysis pages.
- Add user-facing review workflows.
- Add export/reporting if needed.
