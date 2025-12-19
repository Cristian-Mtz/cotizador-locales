import { Injectable, inject } from '@angular/core';
import { Actions, createEffect, ofType } from '@ngrx/effects';
import { catchError, map, of, switchMap } from 'rxjs';

import { CotizacionesActions } from './cotizaciones.actions';
import { CotizacionesApiService } from '../services/cotizaciones-api.service';
import { normalizeEmail } from '@locales/util/normalize';

@Injectable()
export class CotizacionesEffects {
  private readonly actions$ = inject(Actions);
  private readonly api = inject(CotizacionesApiService);

  create$ = createEffect(() =>
    this.actions$.pipe(
      ofType(CotizacionesActions.create),
      switchMap(({ payload }) =>
        this.api.create(payload).pipe(
          map((item) => CotizacionesActions.createSuccess({ item })),
          catchError((err) =>
            of(
              CotizacionesActions.createFailure({
                error: err?.error?.error?.message ?? err?.message ?? 'Error creando cotización',
              })
            )
          )
        )
      )
    )
  );

  loadByEmail$ = createEffect(() =>
    this.actions$.pipe(
      ofType(CotizacionesActions.loadByEmail),
      switchMap(({ email }) =>
        this.api.listByEmail(normalizeEmail(email)).pipe(
          map((items) => CotizacionesActions.loadByEmailSuccess({ items })),
          catchError((err) =>
            of(
              CotizacionesActions.loadByEmailFailure({
                error: err?.error?.error?.message ?? err?.message ?? 'Error cargando historial',
              })
            )
          )
        )
      )
    )
  );
}
