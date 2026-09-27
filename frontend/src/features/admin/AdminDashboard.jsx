import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Check, X, ShieldAlert, Users } from 'lucide-react';
import { Card } from '../../design-system/Card';
import { Button } from '../../design-system/Button';
import { EmptyState } from '../../design-system/EmptyState';

export default function AdminDashboard() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('pending'); // pending, active, suspended

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      // Fetch users based on filter
      const res = await fetch(`http://localhost:8000/api/v1/admin/users${filter ? `?status=${filter}` : ''}`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (res.ok) {
        setUsers(await res.json());
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, [filter]);

  const handleUpdateStatus = async (userId, newStatus) => {
    try {
      const token = localStorage.getItem('token');
      const res = await fetch(`http://localhost:8000/api/v1/admin/users/${userId}/status`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ status: newStatus })
      });
      if (res.ok) {
        // Remove from list if we are currently filtering by something else, or just re-fetch
        fetchUsers();
      }
    } catch (err) {
      alert("Failed to update status");
    }
  };

  return (
    <div style={{ padding: 'var(--space-6)', maxWidth: '1200px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 'var(--space-6)' }}>
        <div>
          <h1 style={{ fontSize: 'var(--text-display)' }}>Admin Dashboard</h1>
          <p style={{ color: 'var(--color-text-muted)' }}>Manage user access and system configuration.</p>
        </div>
        <Button variant="outline" onClick={() => navigate('/admin/ai-ops')}>
          AI Ops Center
        </Button>
      </div>

      <div style={{ display: 'flex', gap: 'var(--space-4)', marginBottom: 'var(--space-6)' }}>
        <Button variant={filter === 'pending' ? 'primary' : 'outline'} onClick={() => setFilter('pending')}>
          Pending Requests
        </Button>
        <Button variant={filter === 'active' ? 'primary' : 'outline'} onClick={() => setFilter('active')}>
          Active Users
        </Button>
        <Button variant={filter === 'suspended' ? 'primary' : 'outline'} onClick={() => setFilter('suspended')}>
          Suspended
        </Button>
        <Button variant={filter === '' ? 'primary' : 'outline'} onClick={() => setFilter('')}>
          All Users
        </Button>
      </div>

      <Card style={{ padding: 'var(--space-0)' }}>
        {loading ? (
          <div style={{ padding: 'var(--space-6)', textAlign: 'center' }}>Loading users...</div>
        ) : users.length === 0 ? (
          <div style={{ padding: 'var(--space-8)' }}>
            <EmptyState 
              title="No users found"
              description={`There are no users with status: ${filter || 'any'}.`}
              icon={<Users size={48} color="var(--color-text-muted)" />}
            />
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: 'var(--color-bg)', borderBottom: '2px solid var(--border-color)', textAlign: 'left' }}>
                  <th style={{ padding: 'var(--space-4)' }}>Name</th>
                  <th style={{ padding: 'var(--space-4)' }}>Role</th>
                  <th style={{ padding: 'var(--space-4)' }}>Details</th>
                  <th style={{ padding: 'var(--space-4)' }}>Status</th>
                  <th style={{ padding: 'var(--space-4)' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {users.map(user => (
                  <tr key={user.id} style={{ borderBottom: '1px solid var(--border-color)' }}>
                    <td style={{ padding: 'var(--space-4)' }}>
                      <strong>{user.full_name}</strong>
                      <span style={{ display: 'block', fontSize: 'var(--text-caption)', color: 'var(--color-text-muted)' }}>{user.email}</span>
                    </td>
                    <td style={{ padding: 'var(--space-4)' }}>
                      <span style={{ textTransform: 'capitalize' }}>{user.role.replace('_', ' ')}</span>
                    </td>
                    <td style={{ padding: 'var(--space-4)' }}>
                      {user.department && <span style={{ display: 'block', fontSize: 'var(--text-caption)' }}>Dept: {user.department}</span>}
                      {user.jurisdiction && <span style={{ display: 'block', fontSize: 'var(--text-caption)' }}>Area: {user.jurisdiction}</span>}
                    </td>
                    <td style={{ padding: 'var(--space-4)' }}>
                      <span style={{
                        padding: '2px 8px', borderRadius: '12px', fontSize: '12px', fontWeight: 600,
                        backgroundColor: user.status === 'active' ? 'var(--color-success)' : user.status === 'pending' ? 'var(--color-warning)' : 'var(--color-critical)',
                        color: '#fff'
                      }}>
                        {user.status}
                      </span>
                    </td>
                    <td style={{ padding: 'var(--space-4)' }}>
                      {user.status === 'pending' && (
                        <div style={{ display: 'flex', gap: 'var(--space-2)' }}>
                          <Button variant="primary" style={{ backgroundColor: 'var(--color-success)', borderColor: 'var(--color-success)', padding: '4px 8px' }} onClick={() => handleUpdateStatus(user.id, 'active')}>
                            Approve
                          </Button>
                          <Button variant="outline" style={{ padding: '4px 8px' }} onClick={() => handleUpdateStatus(user.id, 'rejected')}>
                            Reject
                          </Button>
                        </div>
                      )}
                      {user.status === 'active' && user.role !== 'admin' && (
                         <Button variant="outline" style={{ color: 'var(--color-critical)', borderColor: 'var(--color-critical)', padding: '4px 8px' }} onClick={() => handleUpdateStatus(user.id, 'suspended')}>
                           Suspend
                         </Button>
                      )}
                      {user.status === 'suspended' && (
                         <Button variant="outline" style={{ padding: '4px 8px' }} onClick={() => handleUpdateStatus(user.id, 'active')}>
                           Restore
                         </Button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </Card>
    </div>
  );
}
