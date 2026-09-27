import React, { useState, useEffect } from 'react';
import { Activity, Server, AlertTriangle, Zap, CheckCircle } from 'lucide-react';
import { Card } from '../../design-system/Card';
import { Button } from '../../design-system/Button';
import { useNavigate } from 'react-router-dom';

export default function AIOpsDashboard() {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const token = localStorage.getItem('token');
        const res = await fetch('http://localhost:8000/api/v1/ai-ops/metrics', {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          setMetrics(await res.json());
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchMetrics();
  }, []);

  return (
    <div style={{ padding: 'var(--space-6)', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-6)' }}>
        <div>
          <h1 style={{ fontSize: 'var(--text-display)' }}>AI Operations Center</h1>
          <p style={{ color: 'var(--color-text-muted)' }}>Monitor inference health and model accuracy across the pipeline.</p>
        </div>
        <Button variant="outline" onClick={() => navigate('/admin')}>
          Back to Admin
        </Button>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: 'var(--space-8)' }}>Loading AI Telemetry...</div>
      ) : metrics ? (
        <>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 'var(--space-4)', marginBottom: 'var(--space-6)' }}>
            <Card style={{ padding: 'var(--space-4)', display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
              <div style={{ backgroundColor: 'var(--color-success)', padding: 'var(--space-3)', borderRadius: '50%' }}>
                <Activity color="white" />
              </div>
              <div>
                <span style={{ display: 'block', color: 'var(--color-text-muted)' }}>Pipeline Status</span>
                <strong style={{ fontSize: 'var(--text-h2)' }}>{metrics.pipeline_status}</strong>
              </div>
            </Card>

            <Card style={{ padding: 'var(--space-4)', display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
              <div style={{ backgroundColor: 'var(--color-primary)', padding: 'var(--space-3)', borderRadius: '50%' }}>
                <Server color="white" />
              </div>
              <div>
                <span style={{ display: 'block', color: 'var(--color-text-muted)' }}>Total Reports Processed</span>
                <strong style={{ fontSize: 'var(--text-h2)' }}>{metrics.overall_processed_reports.toLocaleString()}</strong>
              </div>
            </Card>

            <Card style={{ padding: 'var(--space-4)', display: 'flex', alignItems: 'center', gap: 'var(--space-4)' }}>
              <div style={{ backgroundColor: 'var(--color-warning)', padding: 'var(--space-3)', borderRadius: '50%' }}>
                <AlertTriangle color="white" />
              </div>
              <div>
                <span style={{ display: 'block', color: 'var(--color-text-muted)' }}>Anomalies Detected</span>
                <strong style={{ fontSize: 'var(--text-h2)' }}>{metrics.anomalies_detected}</strong>
              </div>
            </Card>
          </div>

          <h2 style={{ fontSize: 'var(--text-h2)', marginBottom: 'var(--space-4)' }}>Active Models</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(350px, 1fr))', gap: 'var(--space-4)' }}>
            {metrics.models.map((model, idx) => (
              <Card key={idx} style={{ padding: 'var(--space-5)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-4)' }}>
                  <h3 style={{ margin: 0 }}>{model.name}</h3>
                  <span style={{ fontSize: 'var(--text-caption)', color: 'var(--color-text-muted)', border: '1px solid var(--border-color)', padding: '2px 6px', borderRadius: '4px' }}>
                    v{model.version}
                  </span>
                </div>
                
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-2)' }}>
                  <span style={{ color: 'var(--color-text-muted)', display: 'flex', alignItems: 'center', gap: 'var(--space-1)' }}>
                    <CheckCircle size={16} color="var(--color-success)" /> Accuracy
                  </span>
                  <strong>{(model.accuracy * 100).toFixed(1)}%</strong>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 'var(--space-2)' }}>
                  <span style={{ color: 'var(--color-text-muted)', display: 'flex', alignItems: 'center', gap: 'var(--space-1)' }}>
                    <Zap size={16} color="var(--color-warning)" /> Avg Latency
                  </span>
                  <strong>{model.latency_ms} ms</strong>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', paddingTop: 'var(--space-3)', marginTop: 'var(--space-3)', borderTop: '1px solid var(--border-color)' }}>
                  <span style={{ color: 'var(--color-text-muted)' }}>Throughput (24h)</span>
                  <strong>{model.processed_last_24h} reqs</strong>
                </div>
              </Card>
            ))}
          </div>
        </>
      ) : null}
    </div>
  );
}
