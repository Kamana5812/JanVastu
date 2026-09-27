import React from 'react';
import { AlertCircle } from 'lucide-react';
import { Button } from './Button';

export function ErrorState({ title = 'Error', message = 'Something went wrong.', onRetry }) {
  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      padding: 'var(--space-6)',
      textAlign: 'center'
    }}>
      <AlertCircle size={48} color="var(--color-critical)" />
      <h3 style={{ marginTop: 'var(--space-4)', color: 'var(--color-critical)' }}>{title}</h3>
      <p style={{ marginTop: 'var(--space-2)', color: 'var(--color-text-muted)', marginBottom: 'var(--space-4)' }}>{message}</p>
      {onRetry && <Button variant="secondary" onClick={onRetry}>Retry</Button>}
    </div>
  );
}
