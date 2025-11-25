import React from 'react';
import { Navigate } from 'react-router-dom';
import { useStore } from './store/store';

export const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useStore();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return children;
};
