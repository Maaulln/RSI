'use client';

import { useState, useEffect } from 'react';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export default function Home() {
  const [overview, setOverview] = useState<any>(null);
  const [health, setHealth] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [overviewRes, healthRes] = await Promise.all([
          fetch(`${API_URL}/api/admin/overview`),
          fetch(`${API_URL}/api/admin/system-health`),
        ]);

        if (!overviewRes.ok) throw new Error('Failed to fetch overview');
        setOverview(await overviewRes.json());
        if (healthRes.ok) {
          setHealth(await healthRes.json());
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <h1>DARSI Admin Dashboard</h1>
        <p>RSI A. Yani Surabaya — System Monitoring</p>
      </header>

      {loading && <p className="status">Loading...</p>}
      {error && <p className="error">Error: {error}. Pastikan backend berjalan di http://localhost:8000 dan coba refresh halaman.</p>}

      {overview && (
        <section className="cards">
          <div className="card">
            <h3>Total Nodes</h3>
            <p className="value">{overview.total_nodes}</p>
          </div>
          <div className="card online">
            <h3>Online</h3>
            <p className="value">{overview.online_nodes}</p>
          </div>
          <div className="card offline">
            <h3>Offline</h3>
            <p className="value">{overview.offline_nodes}</p>
          </div>
          <div className="card">
            <h3>Today Sessions</h3>
            <p className="value">{overview.today_sessions}</p>
          </div>
          <div className="card">
            <h3>Pharmacy Queue</h3>
            <p className="value">{overview.pending_pharmacy_queue}</p>
          </div>
        </section>
      )}

      {health && (
        <section className="health">
          <h2>System Health</h2>
          <p>
            Status: <strong>{health.overall_status}</strong> — Uptime{' '}
            {health.uptime_percentage}%
          </p>
          <p>Database: {health.database_status}</p>
        </section>
      )}

      <section className="links">
        <h2>Quick Links</h2>
        <ul>
          <li>
            <a href={`${API_URL}/docs`} target="_blank" rel="noreferrer">
              API Documentation (Swagger)
            </a>
          </li>
          <li>
            <a href="http://localhost:3000" target="_blank" rel="noreferrer">
              Kiosk UI
            </a>
          </li>
        </ul>
      </section>
    </div>
  );
}
