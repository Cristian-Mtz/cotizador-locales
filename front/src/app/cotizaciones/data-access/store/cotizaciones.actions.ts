import { createActionGroup, emptyProps, props } from '@ngrx/store';
import { Cotizacion, CotizacionCreate } from '../models/cotizacion.model';

export const CotizacionesActions = createActionGroup({
  source: 'Cotizaciones',
  events: {
    Create: props<{ payload: CotizacionCreate }>(),
    'Create Success': props<{ item: Cotizacion }>(),
    'Create Failure': props<{ error: string }>(),
    'Clear Create Status': emptyProps(),

    'Load By Email': props<{ email: string }>(),
    'Load By Email Success': props<{ items: Cotizacion[] }>(),
    'Load By Email Failure': props<{ error: string }>(),
    'Clear List': emptyProps(),
  },
});
