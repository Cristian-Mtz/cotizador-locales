import { createFeature, createReducer, on } from '@ngrx/store';
import { CotizacionesActions } from './cotizaciones.actions';
import { Cotizacion } from '../models/cotizacion.model';

export type CreateStatus = 'idle' | 'saving' | 'saved' | 'error';

export interface CotizacionesState {
  createStatus: CreateStatus;
  createError: string | null;
  lastCreated: Cotizacion | null;
}

const initialState: CotizacionesState = {
  createStatus: 'idle',
  createError: null,
  lastCreated: null,
};

export const cotizacionesFeature = createFeature({
  name: 'cotizaciones',
  reducer: createReducer(
    initialState,

    on(CotizacionesActions.create, (state) => ({
      ...state,
      createStatus: 'saving',
      createError: null,
      lastCreated: null,
    })),

    on(CotizacionesActions.createSuccess, (state, { item }) => ({
      ...state,
      createStatus: 'saved',
      lastCreated: item,
    })),

    on(CotizacionesActions.createFailure, (state, { error }) => ({
      ...state,
      createStatus: 'error',
      createError: error,
    })),

    on(CotizacionesActions.clearCreateStatus, (state) => ({
      ...state,
      createStatus: 'idle',
      createError: null,
      lastCreated: null,
    })),
  ),
});
