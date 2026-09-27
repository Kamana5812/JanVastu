import React from 'react';

export function Badge({ children, status = 'info', className = '', ...props }) {
  const colors = {
    success: 'var(--color-success)',
    warning: 'var(--color-warning)',
    critical: 'var(--color-critical)',
    info: 'var(--color-info)'
  };

  return (
    <span
      className={`badge ${className}`}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        padding: 'var(--space-1) var(--space-2)',
        borderRadius: 'var(--radius-sm)',
        fontSize: 'var(--text-caption)',
        fontWeight: 600,
        backgroundColor: colors[status],
        color: 'white'
      }}
      {...props}
    >
      {children}
    </span>
  );
}
