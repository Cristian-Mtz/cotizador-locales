export interface CotizacionCreate {
  prospecto_email: string;
  local_codigo: string;
  duracion_meses: number;
  notas?: string;
}

export interface Cotizacion {
  id: string;
  prospecto_email: string;
  local_codigo: string;
  duracion_meses: number;
  notas?: string;
  subtotal: number;
  iva: number;
  total: number;
  created_at: string; // ISO
}
