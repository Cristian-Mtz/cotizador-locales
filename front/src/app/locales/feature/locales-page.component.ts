
import { ChangeDetectionStrategy, Component, PLATFORM_ID, inject } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { toSignal } from '@angular/core/rxjs-interop';

import { LocalesFacade } from '../data-access/locales.facade';

@Component({
  standalone: true,
  templateUrl: './locales-page.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LocalesPageComponent {
  private readonly platformId = inject(PLATFORM_ID);
  readonly facade = inject(LocalesFacade);

  readonly items = toSignal(this.facade.items$, { initialValue: [] });
  readonly status = toSignal(this.facade.status$, { initialValue: 'idle' as const });
  readonly error = toSignal(this.facade.error$, { initialValue: null });

  readonly page = toSignal(this.facade.page$, { initialValue: 1 });
  readonly totalPages = toSignal(this.facade.totalPages$, { initialValue: 1 });
  readonly total = toSignal(this.facade.total$, { initialValue: 0 });

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) this.facade.load();
  }

  reload(): void {
    this.facade.load();
  }

  next(): void {
    if (this.page() < this.totalPages()) this.facade.load(this.page() + 1);
  }
}
