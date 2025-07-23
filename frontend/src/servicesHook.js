import { useAuth } from '@clerk/clerk-react';

export const useApi = () => {
  const { getToken } = useAuth();

  const makeRequest = async (endpoint, options = {}) => {
    const token = await getToken();

    if (!token) {
      throw new Error('Unauthorized: No token available');
    }
    const backendUrl = import.meta.env.VITE_BACKEND_URL;

    const response = await fetch(`${backendUrl}/api/${endpoint}`, {
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      ...options,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      if (response.status === 429) {
        throw new Error('Daily quota exceeded');
      }
      throw new Error(errorData?.detail || 'An error occurred');
    }

    return response.json();
  };

  return { makeRequest };
};
