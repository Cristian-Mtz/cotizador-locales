import { createActionGroup, props } from '@ngrx/store';
import { Local } from '../models/local.model';

export const LocalesActions = createActionGroup({
  source: 'Locales',
  events: {
    'Load': props<{ page?: number; pageSize?: number }>(),
    'Load Success': props<{ items: Local[]; total: number; totalPages: number; page: number; pageSize: number }>(),
    'Load Failure': props<{ error: string }>(),

    'Set Filters': props<{
      codigo?: string;
      pabellon?: string;
      areaMin?: number;
      areaMax?: number;
      precioMin?: number;
      precioMax?: number;
    }>(),
  },
});
