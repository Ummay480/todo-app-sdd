/**
 * API Client Layer
 * Handles all requests to the backend with automatic JWT attachment
 * Reference: @specs/api/rest-endpoints.md
 */

import { authClient } from "./auth-client";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type HttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH';

interface RequestOptions extends Omit<RequestInit, 'body'> {
  params?: Record<string, string | number | boolean>;
  body?: any;
}

export async function apiRequest<T>(
  endpoint: string,
  method: HttpMethod = 'GET',
  options: RequestOptions = {}
): Promise<T> {
  const { params, body, headers, ...rest } = options;

  // Construct URL with query parameters
  // Add /api prefix for production URLs, but not for localhost (for backward compatibility)
  const baseUrl = API_BASE_URL.includes('localhost') || API_BASE_URL.includes('127.0.0.1')
    ? API_BASE_URL
    : `${API_BASE_URL}/api`;
  const url = new URL(`${baseUrl}${endpoint.startsWith('/') ? endpoint : `/${endpoint}`}`);
  if (params) {
    Object.entries(params).forEach(([key, value]) => {
      url.searchParams.append(key, String(value));
    });
  }

  // Get JWT from localStorage
  const token = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  const defaultHeaders: Record<string, string> = {
    'Content-Type': 'application/json',
  };

  if (token) {
    defaultHeaders['Authorization'] = `Bearer ${token}`;
  }

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
  getTasks: (params?: { status?: string; sort_by?: string; priority?: string; search?: string }) =>
    apiRequest<any[]>('/tasks', 'GET', { params }),

  getTask: (id: string) =>
    apiRequest<any>(`/tasks/${id}`, 'GET'),

  createTask: (data: { title: string; description?: string; priority?: string }) =>
    apiRequest<any>('/tasks', 'POST', { body: data }),

  updateTask: (id: string, data: any) =>
    apiRequest<any>(`/tasks/${id}`, 'PUT', { body: data }),

  deleteTask: (id: string) =>
    apiRequest<void>(`/tasks/${id}`, 'DELETE'),

  toggleComplete: (id: string, completed: boolean) =>
    apiRequest<any>(`/tasks/${id}/complete`, 'PATCH', { body: { completed } }),
};
