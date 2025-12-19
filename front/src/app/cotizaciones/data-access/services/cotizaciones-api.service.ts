import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '@core/data-access/api-base-url';
import { joinUrl } from '@core/data-access/http-client.util';
import { Cotizacion, CotizacionCreate } from '../models/cotizacion.model';

@Injectable({ providedIn: 'root' })
export class CotizacionesApiService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = inject(API_BASE_URL);

  create(payload: CotizacionCreate): Observable<Cotizacion> {
    return this.http.post<Cotizacion>(joinUrl(this.baseUrl, '/cotizaciones'), payload);
  }

  listByEmail(email: string): Observable<Cotizacion[]> {
    return this.http.get<Cotizacion[]>(joinUrl(this.baseUrl, `/cotizaciones/prospecto/${encodeURIComponent(email)}`));
  }
}
