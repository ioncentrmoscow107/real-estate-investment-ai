import { Building2, Clock3, Database, RefreshCw } from "lucide-react";
import { getCollectorStatus, getListings } from "../lib/api";

function formatRub(value: string) {
  return new Intl.NumberFormat("ru-RU", {
    style: "currency",
    currency: "RUB",
    maximumFractionDigits: 0,
  }).format(Number(value));
}

export default async function Dashboard() {
  const [status, listings] = await Promise.all([getCollectorStatus(), getListings()]);

  return (
    <div className="page">
      <header className="topbar">
        <div className="topbar-inner">
          <div className="brand">
            <strong>CRE Investment AI</strong>
            <span>Commercial real estate acquisition intelligence</span>
          </div>
          <span className={status.scheduler_running ? "status-ok" : "status-warn"}>
            {status.scheduler_running ? "Collector running" : "Collector stopped"}
          </span>
        </div>
      </header>

      <main className="main">
        <section className="summary-grid">
          <div className="card metric">
            <Building2 size={20} />
            <span className="metric-label">Listings</span>
            <span className="metric-value">{listings.length}</span>
          </div>
          <div className="card metric">
            <Database size={20} />
            <span className="metric-label">Sources</span>
            <span className="metric-value">{status.sources.length}</span>
          </div>
          <div className="card metric">
            <Clock3 size={20} />
            <span className="metric-label">Collection interval</span>
            <span className="metric-value">{status.interval_minutes} min</span>
          </div>
          <div className="card metric">
            <RefreshCw size={20} />
            <span className="metric-label">Price filter</span>
            <span className="metric-value">100-400M</span>
          </div>
        </section>

        <section className="card">
          <div className="toolbar">
            <div>
              <h1>Qualified Listings</h1>
              <p>First-floor assets built from 2016 onward, filtered for target property types.</p>
            </div>
            <button className="button" type="button">
              <RefreshCw size={16} />
              Refresh
            </button>
          </div>

          <div className="table-wrap">
            {listings.length === 0 ? (
              <div className="empty">No listings yet. Scraping adapters are ready but not implemented.</div>
            ) : (
              <table>
                <thead>
                  <tr>
                    <th>Asset</th>
                    <th>Source</th>
                    <th>Price</th>
                    <th>Floor</th>
                    <th>Year</th>
                    <th>Type</th>
                    <th>Score</th>
                  </tr>
                </thead>
                <tbody>
                  {listings.map((listing) => (
                    <tr key={listing.id}>
                      <td>
                        <a href={listing.url} rel="noreferrer" target="_blank">
                          {listing.title}
                        </a>
                        <div>{listing.address}</div>
                      </td>
                      <td>{listing.source}</td>
                      <td>{formatRub(listing.price_rub)}</td>
                      <td>{listing.floor}</td>
                      <td>{listing.building_year}</td>
                      <td>
                        <span className="pill">{listing.property_type}</span>
                      </td>
                      <td>{listing.investment_score ?? "-"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

