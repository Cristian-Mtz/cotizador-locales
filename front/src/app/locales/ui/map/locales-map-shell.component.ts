import { ChangeDetectionStrategy, Component, PLATFORM_ID, computed, inject, input, output } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';

import { Local } from '../../data-access/models/local.model';
import { LocalesMapClientComponent } from './locales-map-client.component';

@Component({
  selector: 'locales-map-shell',
  standalone: true,
  imports: [LocalesMapClientComponent],
  template: `
    @if (isBrowser()) {
      <locales-map-client [items]="items()" (cotizar)="cotizar.emit($event)" />
    } @else {
      <!-- SSR placeholder (evita hydration mismatch y window/document) -->
      <div class="h-[60dvh] w-full rounded-2xl border border-zinc-800 bg-zinc-900/40 grid place-items-center">
        <div class="text-sm text-zinc-400">Mapa disponible al cargar en el navegador…</div>
      </div>
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LocalesMapShellComponent {
  items = input<Local[]>([]);
  cotizar = output<Local>();

  private readonly platformId = inject(PLATFORM_ID);
  readonly isBrowser = computed(() => isPlatformBrowser(this.platformId));
}
