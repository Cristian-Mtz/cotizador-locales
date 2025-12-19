import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { map } from 'rxjs';

import { CotizacionesFacade } from '../data-access/cotizaciones.facade';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <section class="space-y-4">
      <div>
        <h1 class="text-xl font-semibold">Cotizaciones</h1>
        <p class="text-sm text-zinc-300">Crea una cotización por local + email.</p>
      </div>

      <form
        class="rounded-2xl border border-zinc-800 bg-zinc-900 p-4 space-y-3"
        [formGroup]="form"
        (ngSubmit)="submit()"
      >
        <div class="grid gap-3 sm:grid-cols-2">
          <label class="space-y-1">
            <div class="text-xs text-zinc-400">Email del prospecto</div>
            <input
              class="w-full rounded-xl bg-zinc-950 border border-zinc-800 px-3 py-2 text-sm"
              formControlName="prospecto_email"
              placeholder="demo@mail.com"
            />
          </label>

          <label class="space-y-1">
            <div class="text-xs text-zinc-400">Local</div>
            <input
              class="w-full rounded-xl bg-zinc-950 border border-zinc-800 px-3 py-2 text-sm"
              formControlName="local_codigo"
              placeholder="L-A-001"
            />
          </label>
        </div>

        <label class="space-y-1">
          <div class="text-xs text-zinc-400">Duración (meses)</div>
          <input
            type="number"
            class="w-full rounded-xl bg-zinc-950 border border-zinc-800 px-3 py-2 text-sm"
            formControlName="duracion_meses"
            min="1"
          />
        </label>

        <label class="space-y-1">
          <div class="text-xs text-zinc-400">Notas</div>
          <textarea
            class="w-full rounded-xl bg-zinc-950 border border-zinc-800 px-3 py-2 text-sm"
            rows="3"
            formControlName="notas"
          ></textarea>
        </label>

        <div class="flex gap-2">
          <button
            class="rounded-xl bg-zinc-800 px-3 py-2 text-sm hover:bg-zinc-700 disabled:opacity-50"
            [disabled]="form.invalid || createStatus() === 'saving'"
            type="submit"
          >
            @if (createStatus() === 'saving') { Guardando... } @else { Crear cotización }
          </button>

          <button
            type="button"
            class="rounded-xl bg-zinc-900 px-3 py-2 text-sm border border-zinc-800 hover:bg-zinc-800"
            (click)="reset()"
          >
            Limpiar
          </button>

          <button
            type="button"
            class="rounded-xl bg-zinc-900 px-3 py-2 text-sm border border-zinc-800 hover:bg-zinc-800"
            (click)="loadHistory()"
            [disabled]="form.controls.prospecto_email.invalid || listStatus() === 'loading'"
          >
            @if (listStatus() === 'loading') { Buscando... } @else { Ver historial }
          </button>
        </div>

        @if (createStatus() === 'error') {
        <div class="text-sm text-red-300">Error: {{ createError() }}</div>
        } @if (createStatus() === 'saved' && lastCreated()) {
        <div class="rounded-xl border border-emerald-900 bg-emerald-950/30 p-3 text-sm">
          <div class="font-semibold text-emerald-200">Cotización creada</div>
          <div class="text-emerald-200/80">
            Total: ${'$'}{{ lastCreated()!.total }} · Subtotal: ${'$'}{{
              lastCreated()!.subtotal
            }}
            · IVA: ${'$'}{{ lastCreated()!.iva }}
          </div>
        </div>
        }
      </form>

      @if (listStatus() === 'error') {
      <div class="text-sm text-red-300">Error historial: {{ listError() }}</div>
      } @if (sortedItems().length > 0) {
      <div class="rounded-2xl border border-zinc-800 bg-zinc-900 p-4">
        <div class="flex items-center justify-between">
          <div class="font-semibold">Historial</div>
          <div class="text-xs text-zinc-400">{{ sortedItems().length }} cotizaciones</div>
        </div>

        <div class="mt-3 space-y-2">
          @for (c of sortedItems(); track c.id) {
          <div class="rounded-xl border border-zinc-800 bg-zinc-950 p-3">
            <div class="flex items-center justify-between">
              <div class="text-sm font-semibold">
                {{ c.local_codigo }} · {{ c.duracion_meses }} meses
              </div>
              <div class="text-sm text-emerald-200 font-semibold">${'$'}{{ c.total }}</div>
            </div>
            <div class="mt-1 text-xs text-zinc-400">
              {{ c.prospecto_email }} · {{ c.created_at }}
            </div>
          </div>
          }
        </div>
      </div>
      }
    </section>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CotizacionesPageComponent {
  private readonly fb = inject(FormBuilder);
  private readonly route = inject(ActivatedRoute);
  private readonly facade = inject(CotizacionesFacade);

  readonly createStatus = toSignal(this.facade.createStatus$, { initialValue: 'idle' as const });
  readonly createError = toSignal(this.facade.createError$, { initialValue: null });
  readonly lastCreated = toSignal(this.facade.lastCreated$, { initialValue: null });

  readonly localFromQuery = toSignal(
    this.route.queryParamMap.pipe(map((q) => q.get('local') ?? '')),
    { initialValue: '' }
  );

  readonly listStatus = toSignal(this.facade.listStatus$, { initialValue: 'idle' as const });
  readonly listError = toSignal(this.facade.listError$, { initialValue: null });
  readonly items = toSignal(this.facade.items$, { initialValue: [] });

  readonly sortedItems = computed(() =>
    [...this.items()].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
    )
  );

  form = this.fb.group({
    prospecto_email: this.fb.nonNullable.control('', [Validators.required, Validators.email]),
    local_codigo: this.fb.nonNullable.control('', [Validators.required]),
    duracion_meses: this.fb.nonNullable.control(6, [Validators.required, Validators.min(1)]),
    notas: this.fb.nonNullable.control(''),
  });

  ngOnInit(): void {
    const local = this.localFromQuery();
    if (local) this.form.controls.local_codigo.setValue(local);
  }

  loadHistory(): void {
    this.facade.loadByEmail(this.form.controls.prospecto_email.value ?? '');
  }

  submit(): void {
    this.facade.create(this.form.getRawValue());
  }

  reset(): void {
    this.facade.clearCreateStatus();
    this.form.reset({
      prospecto_email: '',
      local_codigo: this.localFromQuery() || '',
      duracion_meses: 6,
      notas: '',
    });
  }
}
