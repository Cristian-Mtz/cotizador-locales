import {
  AfterViewInit,
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  OnChanges,
  SimpleChanges,
  ViewChild,
  input,
  output,
} from '@angular/core';

import { Local } from '../../data-access/models/local.model';

@Component({
  selector: 'locales-map-client',
  standalone: true,
  template: `
    <div #mapEl class="h-[60dvh] w-full rounded-2xl border border-zinc-800 overflow-hidden"></div>
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LocalesMapClientComponent implements AfterViewInit, OnChanges {
  items = input<Local[]>([]);
  cotizar = output<Local>();

  @ViewChild('mapEl', { static: true }) mapEl!: ElementRef<HTMLDivElement>;

  private L: any;
  private map: any;
  private markersLayer: any;
  private didFit = false;

  async ngAfterViewInit(): Promise<void> {
    try {
      const leafletMod: any = await import('leaflet');
      const L = leafletMod.default ?? leafletMod; // ✅ clave para prod (CJS/UMD)
      this.L = L;

      const iconRetinaUrl = new URL(
        'leaflet/dist/images/marker-icon-2x.png',
        import.meta.url
      ).toString();
      const iconUrl = new URL('leaflet/dist/images/marker-icon.png', import.meta.url).toString();
      const shadowUrl = new URL(
        'leaflet/dist/images/marker-shadow.png',
        import.meta.url
      ).toString();
      L.Icon.Default.mergeOptions({ iconRetinaUrl, iconUrl, shadowUrl });

      this.map = L.map(this.mapEl.nativeElement, { zoomControl: true }).setView(
        [19.4326, -99.1332],
        12
      );

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors',
        maxZoom: 19,
      }).addTo(this.map);

      this.markersLayer = L.layerGroup().addTo(this.map);

      // ✅ evita mapa “en blanco” si el contenedor cambia de tamaño al montar
      requestAnimationFrame(() => this.map.invalidateSize());

      // Render inicial
      this.renderMarkers(this.items());
    } catch (e) {
      console.error('[Leaflet] failed to init', e);
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (!this.map || !this.markersLayer) return;
    if (changes['items']) this.renderMarkers(this.items());
  }

  private renderMarkers(items: Local[]): void {
    if (!this.L || !this.map || !this.markersLayer) return;

    this.markersLayer.clearLayers();

    const L = this.L;
    const bounds = L.latLngBounds([]);

    for (const local of items ?? []) {
      const lat = Number(local?.ubicacion?.lat);
      const lng = Number(local?.ubicacion?.lng);
      if (!Number.isFinite(lat) || !Number.isFinite(lng)) continue;

      const marker = L.marker([lat, lng]).addTo(this.markersLayer);

      const popupHtml = `
        <div class="space-y-2">
          <div class="text-sm font-semibold">${local.codigo} · Pabellón ${local.pabellon}</div>
          <div class="text-xs text-zinc-300">${local.area_m2} m² · $${local.precio_mensual} / mes</div>
          <div class="text-[11px] text-zinc-400">Status: ${local.status}</div>
          <button
            class="cotizar-btn rounded-lg bg-zinc-800 px-2 py-1 text-xs text-white hover:bg-zinc-700"
            data-codigo="${local.codigo}"
          >
            Cotizar
          </button>
        </div>
      `;

      marker.bindPopup(popupHtml, { closeButton: true });

      marker.on('popupopen', (e: any) => {
        const el: HTMLElement | null = e?.popup?.getElement?.() ?? null;
        const btn = el?.querySelector<HTMLButtonElement>('.cotizar-btn');
        if (!btn) return;

        // Evita duplicar listeners
        btn.onclick = () => this.cotizar.emit(local);
      });

      bounds.extend([lat, lng]);
    }

    if (!this.didFit && bounds.isValid()) {
      this.map.fitBounds(bounds.pad(0.2));
      this.didFit = true;
    }
  }
}
