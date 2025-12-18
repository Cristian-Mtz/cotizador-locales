import { createFeature, createReducer, on } from '@ngrx/store';
import { Local } from '../models/local.model';
import { LocalesActions } from './locales.actions';

export type LocalesStatus = 'idle' | 'loading' | 'loaded' | 'error';

export interface LocalesFilters {
  codigo?: string;
  pabellon?: string;
  areaMin?: number;
  areaMax?: number;
  precioMin?: number;
  precioMax?: number;
}

export interface LocalesState {
  items: Local[];
  status: LocalesStatus;
  error: string | null;

  page: number;
  pageSize: number;
  total: number;
  totalPages: number;

  filters: LocalesFilters;
}

const initialState: LocalesState = {
  items: [],
  status: 'idle',
  error: null,
  page: 1,
  pageSize: 10,
  total: 0,
  totalPages: 0,
  filters: {},
};

export const localesFeature = createFeature({
  name: 'locales',
  reducer: createReducer(
    initialState,

    on(LocalesActions.setFilters, (state, filters) => ({
      ...state,
      filters: { ...state.filters, ...filters },
      page: 1,
    })),

    on(LocalesActions.load, (state, { page, pageSize }) => ({
      ...state,
      status: 'loading',
      error: null,
      page: page ?? state.page,
      pageSize: pageSize ?? state.pageSize,
    })),

    on(LocalesActions.loadSuccess, (state, { items, total, totalPages, page, pageSize }) => ({
      ...state,
      status: 'loaded',
      items,
      total,
      totalPages,
      page,
      pageSize,
    })),

    on(LocalesActions.loadFailure, (state, { error }) => ({ ...state, status: 'error', error })),
  ),
});
