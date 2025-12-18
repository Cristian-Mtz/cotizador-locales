import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  standalone: true,
  template: `
    <section class="space-y-2">
      <h1 class="text-xl font-semibold">Cotizaciones</h1>
      <p class="text-sm text-zinc-300">Crear/listar cotizaciones.</p>
    </section>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CotizacionesPageComponent {}
