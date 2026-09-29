import React from 'react';
import {Navigate, useLocation} from 'react-router-dom';
import {useAuth} from './useAuth';

export default function ProtectedRoute({ children, allowedRoles }) {
  const { user } = useAuth();
  const location = useLocation();

  if (!user) {
    return <Navigate to={'/auth/login?next='+encodeURIComponent(location.pathname+location.search)} replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" replace />;
  }

  return children;
}
