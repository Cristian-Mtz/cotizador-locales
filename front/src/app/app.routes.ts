import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'locales' },
  {
    path: 'locales',
    loadChildren: () =>
      import('./locales/feature/locales.routes').then((m) => m.LOCALES_ROUTES),
  },
  {
    path: 'cotizaciones',
    loadChildren: () =>
      import('./cotizaciones/feature/cotizaciones.routes').then((m) => m.COTIZACIONES_ROUTES),
  },
  { path: '**', redirectTo: 'locales' },
];
