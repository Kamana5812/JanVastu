import React from 'react';

export function Card({ children, className = '', style = {}, ...props }) {
  return (
    <div 
      className={`card ${className}`}
      style={{
        backgroundColor: 'white',
        borderRadius: 'var(--radius-lg)',
        boxShadow: 'var(--shadow-subtle)',
        padding: 'var(--space-5)',
        border: '1px solid var(--border-color)',
        ...style
      }}
      {...props}
    >
      {children}
    </div>
  );
}
