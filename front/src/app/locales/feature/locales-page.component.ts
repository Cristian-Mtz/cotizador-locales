import { ChangeDetectionStrategy, Component } from '@angular/core';

@Component({
  standalone: true,
  template: `
    <section class="space-y-2">
      <h1 class="text-xl font-semibold">Locales</h1>
      <p class="text-sm text-zinc-300">Hello world.</p>
    </section>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LocalesPageComponent {}
