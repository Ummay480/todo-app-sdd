/**
 * API Client Layer
 * Handles all requests to the backend with automatic JWT attachment
 * Reference: @specs/api/rest-endpoints.md
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api";

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

interface RequestOptions extends RequestInit {
  params?: Record<string, string | number | boolean>;
}

export async function apiRequest<T>(
  endpoint: string,
  method: HttpMethod = 'GET',
  options: RequestOptions = {}
): Promise<T> {
  const { params, body, headers, ...rest } = options;

  // Construct URL with query parameters
  const url = new URL(`${API_BASE_URL}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`);
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      url.searchParams.append(key, String(value));
    });
  }

  // Get token from better-auth (Better Auth handles session persistence in cookies/localstorage)
  // The backend expects JWT from better-auth JWT plugin
  const defaultHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  // better-auth-react handles the token automatically in the client,
  // but if we need manual attachment for non-browser environments or specific headers:
  // if (typeof window !== 'undefined') {
  //   const token = localStorage.getItem('better-auth.session-token');
  //   if (token) defaultHeaders['Authorization'] = `Bearer ${token}`;
  // }

  const response = await fetch(url.toString(), {
    method,
    headers: {
      ...defaultHeaders,
      ...headers,
    } as HeadersInit,
    body: body ? JSON.stringify(body) : undefined,
    ...rest,
  });

  if (!response.ok) {
    let errorData;
    try {
      errorData = await response.json();
    } catch {
      errorData = { message: response.statusText };
    }

    const errorMessage = errorData.detail || errorData.message || 'An unexpected error occurred';
    throw new Error(errorMessage);
  }

  // Handle 204 No Content
  if (response.status === 204) {
    return {} as T;
  }

  return response.json();
}

/**
 * Task-specific API calls
 * Reference: @specs/features/task-crud.md
 */

export const tasksApi = {
  getTasks: (params?: { status?: string; sort_by?: string }) =>
    apiRequest<any[]>('/tasks', 'GET', { params }),

  getTask: (id: string) =>
    apiRequest<any>(`/tasks/${id}`, 'GET'),

  createTask: (data: { title: string; description?: string; due_date?: string }) =>
    apiRequest<any>('/tasks', 'POST', { body: data }),

  updateTask: (id: string, data: any) =>
    apiRequest<any>(`/tasks/${id}`, 'PUT', { body: data }),

  deleteTask: (id: string) =>
    apiRequest<void>(`/tasks/${id}`, 'DELETE'),

  toggleComplete: (id: string, completed: boolean) =>
    apiRequest<any>(`/tasks/${id}`, 'PATCH', { body: { completed } }),
};
