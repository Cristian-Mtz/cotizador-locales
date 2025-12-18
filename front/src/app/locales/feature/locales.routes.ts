import { Routes } from '@angular/router';
import { provideEffects } from '@ngrx/effects';
import { provideState } from '@ngrx/store';

import { LocalesPageComponent } from './locales-page.component';
import { localesFeature } from '@locales/data-access/store/locales.reducer';
import { LocalesEffects } from '@locales/data-access/store/locales.effects';

export const LOCALES_ROUTES: Routes = [
  {
    path: '',
    component: LocalesPageComponent,
    providers: [provideState(localesFeature), provideEffects(LocalesEffects)],
  },
];
