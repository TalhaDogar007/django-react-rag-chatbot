const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';


export const searchQuery = async (query: string): Promise<string> => {
  const response = await fetch(`${API_URL}/search/?query=${encodeURIComponent(query)}`);
  if (!response.ok) {
    throw new Error('Search failed');
  }
  const data = await response.json();
  return data.response || 'No response.';
};