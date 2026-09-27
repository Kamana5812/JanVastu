import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { Card } from '../../design-system/Card';
import { Button } from '../../design-system/Button';
import { CheckCircle, AlertCircle, Clock } from 'lucide-react';

export default function PlannerDashboard({ level }) {
  const [stats, setStats] = useState(null);
  const [needs, setNeeds] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const token = localStorage.getItem('token');
        const headers = { 'Authorization': `Bearer ${token}` };
        
        const [statsRes, needsRes] = await Promise.all([
          fetch('http://localhost:8000/api/v1/planner/stats', { headers }),
          fetch('http://localhost:8000/api/v1/planner/needs', { headers })
        ]);
        
        if (statsRes.ok && needsRes.ok) {
          setStats(await statsRes.json());
          setNeeds(await needsRes.json());
        }
      } catch (err) {
        console.error("Error fetching planner data", err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [level]);

  const handleUpdateStatus = async (id, newStatus) => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8000/api/v1/planner/needs/${id}/status`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ status: newStatus })
      });
      if (res.ok) {
        // Optimistic update
        setNeeds(needs.map(n => n.id === id ? { ...n, status: newStatus } : n));
      }
    } catch (err) {
      alert("Update failed");
    }
  };

  const chartData = stats ? [
    { name: 'Reported', value: stats.by_status?.reported || 0 },
    { name: 'Verified', value: stats.by_status?.verified || 0 },
    { name: 'Planned', value: stats.by_status?.planned || 0 },
    { name: 'Resolved', value: stats.by_status?.resolved || 0 },
    { name: 'Rejected', value: stats.by_status?.rejected || 0 }
  ] : [];

  return (
    <div style={{ padding: 'var(--space-6)', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ marginBottom: 'var(--space-6)' }}>
        <h1 style={{ fontSize: 'var(--text-display)', textTransform: 'capitalize' }}>{level} Dashboard</h1>
        <p style={{ color: 'var(--color-text-muted)' }}>Overview of verified infrastructure needs requiring planning and budget allocation.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: 'var(--space-6)', marginBottom: 'var(--space-8)' }}>
        <Card style={{ padding: 'var(--space-5)', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
          <h2 style={{ fontSize: 'var(--text-h2)', color: 'var(--color-text-muted)' }}>Total Needs Tracked</h2>
          <span style={{ fontSize: '64px', fontWeight: 800, color: 'var(--color-primary)' }}>{stats?.total || 0}</span>
        </Card>
        
        <Card style={{ padding: 'var(--space-5)', height: '300px' }}>
          <h3 style={{ marginBottom: 'var(--space-4)' }}>Needs by Status</h3>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="var(--color-primary)" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </Card>
      </div>

      <h2 style={{ fontSize: 'var(--text-h2)', marginBottom: 'var(--space-4)' }}>Actionable Needs</h2>
      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: 'var(--color-bg)', borderBottom: '2px solid var(--border-color)', textAlign: 'left' }}>
              <th style={{ padding: 'var(--space-3)' }}>Category</th>
              <th style={{ padding: 'var(--space-3)' }}>Location</th>
              <th style={{ padding: 'var(--space-3)' }}>Affected</th>
              <th style={{ padding: 'var(--space-3)' }}>Status</th>
              <th style={{ padding: 'var(--space-3)' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {needs.map(need => (
              <tr key={need.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                <td style={{ padding: 'var(--space-3)', textTransform: 'capitalize', fontWeight: 600 }}>{need.category}</td>
                <td style={{ padding: 'var(--space-3)' }}>{need.district}, {need.state}</td>
                <td style={{ padding: 'var(--space-3)' }}>{need.affected_people || 'N/A'}</td>
                <td style={{ padding: 'var(--space-3)' }}>
                  <span style={{
                    padding: '2px 8px', borderRadius: '12px', fontSize: '12px', fontWeight: 600,
                    backgroundColor: need.status === 'verified' ? 'var(--color-success)' : 'var(--color-bg)',
                    color: need.status === 'verified' ? '#fff' : 'var(--color-text)'
                  }}>
                    {need.status}
                  </span>
                </td>
                <td style={{ padding: 'var(--space-3)' }}>
                  {need.status === 'verified' && (
                    <Button variant="outline" onClick={() => handleUpdateStatus(need.id, 'planned')}>
                      Mark Planned
                    </Button>
                  )}
                  {need.status === 'planned' && (
                    <Button variant="primary" onClick={() => handleUpdateStatus(need.id, 'resolved')}>
                      Mark Resolved
                    </Button>
                  )}
                </td>
              </tr>
            ))}
            {needs.length === 0 && (
              <tr>
                <td colSpan="5" style={{ padding: 'var(--space-6)', textAlign: 'center', color: 'var(--color-text-muted)' }}>
                  No needs found for your jurisdiction.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
