import { createFeature, createReducer, on } from '@ngrx/store';
import { CotizacionesActions } from './cotizaciones.actions';
import { Cotizacion } from '../models/cotizacion.model';

export type CreateStatus = 'idle' | 'saving' | 'saved' | 'error';
export type ListStatus = 'idle' | 'loading' | 'loaded' | 'error';

export interface CotizacionesState {
  createStatus: CreateStatus;
  createError: string | null;
  lastCreated: Cotizacion | null;

  listStatus: ListStatus;
  listError: string | null;
  items: Cotizacion[];
}

const initialState: CotizacionesState = {
  createStatus: 'idle',
  createError: null,
  lastCreated: null,

  listStatus: 'idle',
  listError: null,
  items: [],
};

export const cotizacionesFeature = createFeature({
  name: 'cotizaciones',
  reducer: createReducer(
    initialState,

    // Create actions
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

    // Load By Email actions
    on(CotizacionesActions.loadByEmail, (state) => ({
      ...state,
      listStatus: 'loading',
      listError: null,
    })),
    on(CotizacionesActions.loadByEmailSuccess, (state, { items }) => ({
      ...state,
      listStatus: 'loaded',
      items,
    })),
    on(CotizacionesActions.loadByEmailFailure, (state, { error }) => ({
      ...state,
      listStatus: 'error',
      listError: error,
    })),
    on(CotizacionesActions.clearList, (state) => ({
      ...state,
      listStatus: 'idle',
      listError: null,
      items: [],
    }))
  ),
});
