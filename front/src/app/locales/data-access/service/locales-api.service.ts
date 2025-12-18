import { inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Local, PagedResponse } from '../models/local.model';
import { HttpClient } from '@angular/common/http';
import { API_BASE_URL } from '@core/data-access/api-base-url';
import { joinUrl } from '@core/data-access/http-client.util';

@Injectable({ providedIn: 'root' })
export class LocalesApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = inject(API_BASE_URL);

  list(params?: Record<string, string | number | boolean | undefined>): Observable<PagedResponse<Local>> {
    return this.http.get<PagedResponse<Local>>(joinUrl(this.baseUrl, '/locales'), {
      params: (params ?? {}) as any,
    });
  }
}
