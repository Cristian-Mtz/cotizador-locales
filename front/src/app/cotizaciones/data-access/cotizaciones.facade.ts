import { Injectable, inject } from '@angular/core';
import { Store } from '@ngrx/store';

import { CotizacionCreate } from './models/cotizacion.model';
import { CotizacionesActions } from './store/cotizaciones.actions';
import {
  selectCreateError,
  selectCreateStatus,
  selectLastCreated,
  selectItems,
  selectListError,
  selectListStatus,
} from './store/cotizaciones.selectors';

@Injectable({ providedIn: 'root' })
export class CotizacionesFacade {
  private readonly store = inject(Store);

  readonly createStatus$ = this.store.select(selectCreateStatus);
  readonly createError$ = this.store.select(selectCreateError);
  readonly lastCreated$ = this.store.select(selectLastCreated);

  readonly listStatus$ = this.store.select(selectListStatus);
  readonly listError$ = this.store.select(selectListError);
  readonly items$ = this.store.select(selectItems);

  create(payload: CotizacionCreate): void {
    this.store.dispatch(CotizacionesActions.create({ payload }));
  }

  clearCreateStatus(): void {
    this.store.dispatch(CotizacionesActions.clearCreateStatus());
  }

  loadByEmail(email: string): void {
    this.store.dispatch(CotizacionesActions.loadByEmail({ email }));
  }

  clearList(): void {
    this.store.dispatch(CotizacionesActions.clearList());
  }
}
