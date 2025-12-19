import { ChangeDetectionStrategy, Component, PLATFORM_ID, inject, signal } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { toSignal } from '@angular/core/rxjs-interop';
import { Router } from '@angular/router';

import { LocalesFacade } from '../data-access/locales.facade';
import { Local } from '../data-access/models/local.model';
import { LocalesMapShellComponent } from '../ui/map/locales-map-shell.component';

@Component({
  standalone: true,
  imports: [LocalesMapShellComponent],
  templateUrl: './locales-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LocalesPageComponent {
  private readonly platformId = inject(PLATFORM_ID);
  private readonly router = inject(Router);

  readonly facade = inject(LocalesFacade);

  readonly items = toSignal(this.facade.items$, { initialValue: [] as Local[] });
  readonly status = toSignal(this.facade.status$, { initialValue: 'idle' as const });
  readonly error = toSignal(this.facade.error$, { initialValue: null });

  readonly page = toSignal(this.facade.page$, { initialValue: 1 });
  readonly totalPages = toSignal(this.facade.totalPages$, { initialValue: 1 });
  readonly total = toSignal(this.facade.total$, { initialValue: 0 });

  readonly selected = signal<Local | null>(null);

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) this.facade.load();
  }

  reload(): void {
    this.facade.load();
  }

  next(): void {
    if (this.page() < this.totalPages()) this.facade.load(this.page() + 1);
  }

  // Recibe evento desde el mapa (botón Cotizar del popup)
  onCotizar(local: Local): void {
    this.selected.set(local);
  }

  // Click en tarjeta (fallback/listado)
  selectLocal(local: Local): void {
    this.selected.set(local);
  }

  goToCotizar(): void {
    const local = this.selected();
    if (!local) return;

    this.router.navigate(['/cotizaciones'], {
      queryParams: { local: local.codigo },
    });
  }
}
