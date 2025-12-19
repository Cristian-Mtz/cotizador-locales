import { Routes } from '@angular/router';
import { provideEffects } from '@ngrx/effects';
import { provideState } from '@ngrx/store';

import { CotizacionesPageComponent } from './cotizaciones-page.component';
import { cotizacionesFeature } from '../data-access/store/cotizaciones.reducer';
import { CotizacionesEffects } from '../data-access/store/cotizaciones.effects';

export const COTIZACIONES_ROUTES: Routes = [
  {
    path: '',
    component: CotizacionesPageComponent,
    providers: [provideState(cotizacionesFeature), provideEffects(CotizacionesEffects)],
  },
];
