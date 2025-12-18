import { Injectable, inject } from '@angular/core';
import { Store } from '@ngrx/store';
import {
  selectLocalesError,
  selectLocalesItems,
  selectLocalesPage,
  selectLocalesPageSize,
  selectLocalesStatus,
  selectLocalesTotal,
  selectLocalesTotalPages,
} from './store/locales.selectors';
import { LocalesActions } from './store/locales.actions';

@Injectable({ providedIn: 'root' })
export class LocalesFacade {
  private readonly store = inject(Store);

  readonly items$ = this.store.select(selectLocalesItems);
  readonly status$ = this.store.select(selectLocalesStatus);
  readonly error$ = this.store.select(selectLocalesError);

  readonly total$ = this.store.select(selectLocalesTotal);
  readonly totalPages$ = this.store.select(selectLocalesTotalPages);
  readonly page$ = this.store.select(selectLocalesPage);
  readonly pageSize$ = this.store.select(selectLocalesPageSize);

  load(page?: number, pageSize?: number): void {
    this.store.dispatch(LocalesActions.load({ page, pageSize }));
  }

  setFilters(filters: {
    codigo?: string;
    pabellon?: string;
    areaMin?: number;
    areaMax?: number;
    precioMin?: number;
    precioMax?: number;
  }): void {
    this.store.dispatch(LocalesActions.setFilters(filters));
    this.load(1);
  }
}
