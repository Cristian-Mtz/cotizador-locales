import { Injectable, inject } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { Store } from '@ngrx/store';
import { catchError, map, of, switchMap, withLatestFrom } from 'rxjs';

import { LocalesActions } from './locales.actions';
import { selectLocalesFilters, selectLocalesPage, selectLocalesPageSize } from './locales.selectors';
import { LocalesApiService } from '../service/locales-api.service';

@Injectable()
export class LocalesEffects {
  private readonly actions$ = inject(Actions);
  private readonly api = inject(LocalesApiService);
  private readonly store = inject(Store);

  load$ = createEffect(() =>
    this.actions$.pipe(
      ofType(LocalesActions.load),
      withLatestFrom(
        this.store.select(selectLocalesFilters),
        this.store.select(selectLocalesPage),
        this.store.select(selectLocalesPageSize),
      ),
      switchMap(([action, filters, page, pageSize]) => {
        const finalPage = action.page ?? page;
        const finalPageSize = action.pageSize ?? pageSize;

        const params: Record<string, any> = {
          page: finalPage,
          page_size: finalPageSize,
          ...(filters.codigo ? { codigo: filters.codigo } : {}),
          ...(filters.pabellon ? { pabellon: filters.pabellon } : {}),
          ...(filters.areaMin != null ? { area_min: filters.areaMin } : {}),
          ...(filters.areaMax != null ? { area_max: filters.areaMax } : {}),
          ...(filters.precioMin != null ? { precio_min: filters.precioMin } : {}),
          ...(filters.precioMax != null ? { precio_max: filters.precioMax } : {}),
        };

        return this.api.list(params).pipe(
          map((res) =>
            LocalesActions.loadSuccess({
              items: res.items,
              total: res.total,
              totalPages: res.total_pages,
              page: res.page,
              pageSize: res.page_size,
            }),
          ),
          catchError((err) =>
            of(
              LocalesActions.loadFailure({
                error: err?.message ?? 'Error cargando locales',
              }),
            ),
          ),
        );
      }),
    ),
  );
}
