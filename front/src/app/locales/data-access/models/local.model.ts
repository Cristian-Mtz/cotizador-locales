export interface Ubicacion {
  lat: number;
  lng: number;
}

export interface Caracteristicas {
  instalacion_electrica: string;
  carga_maxima_kg: number;
  altura_m: number;
}

export type LocalStatus = 'disponible' | 'ocupado' | 'mantenimiento' | string;

export interface Local {
  codigo: string;
  pabellon: string;
  area_m2: number;
  precio_mensual: number;
  status: LocalStatus;
  ubicacion: Ubicacion;
  caracteristicas: Caracteristicas;
}

export interface PagedResponse<T> {
  items: T[];
  page: number;
  page_size: number;
  total: number;
  total_pages: number;
}
