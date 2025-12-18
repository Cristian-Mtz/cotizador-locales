import { HttpClient } from '@angular/common/http';
import { inject } from '@angular/core';
import { API_BASE_URL } from './api-base-url';

export function apiUrl(path: string): string {
  const base = inject(API_BASE_URL);
  const cleanBase = base.endsWith('/') ? base.slice(0, -1) : base;
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${cleanBase}${cleanPath}`;
}

export function injectHttp(): HttpClient {
  return inject(HttpClient);
}
