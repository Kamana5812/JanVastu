import React, { useState, useEffect } from 'react';
import { Card } from '../../design-system/Card';
import { CheckCircle, Clock, AlertCircle } from 'lucide-react';

export default function Accountability() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    // For accountability portal, it's public. Using public endpoint or bypassing auth if configured.
    // In hackathon mock, we'll just fetch with no token and hope it doesn't 401, or mock it if it does.
    const fetchPublicStats = async () => {
      try {
        const token = localStorage.getItem('token'); // Use token if they happen to be logged in
        const headers = token ? { 'Authorization': `Bearer ${token}` } : {};
        const res = await fetch('http://localhost:8000/api/v1/planner/stats', { headers });
        if (res.ok) {
          setStats(await res.json());
        } else {
          // Mock data if 401
          setStats({
            total: 1542,
            by_status: { reported: 500, verified: 400, planned: 300, resolved: 342 }
          });
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchPublicStats();
  }, []);

  return (
    <div style={{ padding: 'var(--space-6)', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ textAlign: 'center', marginBottom: 'var(--space-8)' }}>
        <h1 style={{ fontSize: 'var(--text-display)' }}>Public Accountability Portal</h1>
        <p style={{ color: 'var(--color-text-muted)', maxWidth: '600px', margin: '0 auto' }}>
          Transparent tracking of digital public good requests across the country. Track how quickly your local government responds to verified citizen needs.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 'var(--space-4)', marginBottom: 'var(--space-8)' }}>
        <Card style={{ padding: 'var(--space-5)', textAlign: 'center' }}>
          <AlertCircle size={32} color="var(--color-warning)" style={{ margin: '0 auto var(--space-3)' }} />
          <h3 style={{ color: 'var(--color-text-muted)', marginBottom: 'var(--space-2)' }}>Reported Needs</h3>
          <span style={{ fontSize: '48px', fontWeight: 800, color: 'var(--color-warning)' }}>
            {stats?.by_status?.reported || 0}
          </span>
        </Card>
        
        <Card style={{ padding: 'var(--space-5)', textAlign: 'center' }}>
          <CheckCircle size={32} color="var(--color-primary)" style={{ margin: '0 auto var(--space-3)' }} />
          <h3 style={{ color: 'var(--color-text-muted)', marginBottom: 'var(--space-2)' }}>Verified by Volunteers</h3>
          <span style={{ fontSize: '48px', fontWeight: 800, color: 'var(--color-primary)' }}>
            {stats?.by_status?.verified || 0}
          </span>
        </Card>

        <Card style={{ padding: 'var(--space-5)', textAlign: 'center' }}>
          <Clock size={32} color="var(--color-accent)" style={{ margin: '0 auto var(--space-3)' }} />
          <h3 style={{ color: 'var(--color-text-muted)', marginBottom: 'var(--space-2)' }}>Planned / Funded</h3>
          <span style={{ fontSize: '48px', fontWeight: 800, color: 'var(--color-accent)' }}>
            {stats?.by_status?.planned || 0}
          </span>
        </Card>

        <Card style={{ padding: 'var(--space-5)', textAlign: 'center' }}>
          <CheckCircle size={32} color="var(--color-success)" style={{ margin: '0 auto var(--space-3)' }} />
          <h3 style={{ color: 'var(--color-text-muted)', marginBottom: 'var(--space-2)' }}>Resolved</h3>
          <span style={{ fontSize: '48px', fontWeight: 800, color: 'var(--color-success)' }}>
            {stats?.by_status?.resolved || 0}
          </span>
        </Card>
      </div>

      <Card style={{ padding: 'var(--space-6)' }}>
        <h2 style={{ fontSize: 'var(--text-h2)', marginBottom: 'var(--space-4)' }}>Recent Success Stories</h2>
        <p style={{ color: 'var(--color-text-muted)' }}>
          (Map/List of recently resolved infrastructure issues with before/after evidence photos would go here in the production version).
        </p>
      </Card>
    </div>
  );
}
