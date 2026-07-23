# Operations

## Local Development

Start everything:

```bash
docker compose up --build
```

Before the backend starts, the `db-migrate` service applies every SQL file from
`database/migrations` in filename order. The migrations are idempotent, so this
also updates an existing local PostgreSQL volume without deleting its data.

Backend health:

```bash
curl http://localhost:8000/health
```

Collector status:

```bash
curl http://localhost:8000/api/v1/collectors/status
```

## Environment

Keep secrets in `.env`. Do not commit real OpenAI API keys or production database credentials.

## Production Notes

- Replace development reload commands with fixed production start commands.
- Run migrations with a managed migration process.
- Add persistent logs and job metrics before enabling real scraping.
- Confirm legal and contractual access rules for each listing source.

