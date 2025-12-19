import { Injectable, inject } from '@angular/core';
import { Store } from '@ngrx/store';

import { CotizacionCreate } from './models/cotizacion.model';
import { CotizacionesActions } from './store/cotizaciones.actions';
import {
  selectCreateError,
  selectCreateStatus,
  selectLastCreated,
} from './store/cotizaciones.selectors';

@Injectable({ providedIn: 'root' })
export class CotizacionesFacade {
  private readonly store = inject(Store);

  readonly createStatus$ = this.store.select(selectCreateStatus);
  readonly createError$ = this.store.select(selectCreateError);
  readonly lastCreated$ = this.store.select(selectLastCreated);

  create(payload: CotizacionCreate): void {
    this.store.dispatch(CotizacionesActions.create({ payload }));
  }

  clearCreateStatus(): void {
    this.store.dispatch(CotizacionesActions.clearCreateStatus());
  }
}
