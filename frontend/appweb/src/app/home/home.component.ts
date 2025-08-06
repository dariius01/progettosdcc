import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NotizieService } from '../services/notizie.service';
import { HttpClient } from '@angular/common/http';
import { MatIconModule } from '@angular/material/icon';

@Component({
  standalone: true,
  selector: 'app-home',
  imports: [CommonModule, FormsModule, MatIconModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent {
  query = '';
  risultati: any[] = [];
  loading = false;
  errore: string | null = null;
  notizieSelezionate: any[] = [];
  articoloGenerato: any = null;
  loadingGenerazione = false;
  erroreGenerazione: string | null = null;

  constructor(private notizieService: NotizieService) {}

  cerca(): void {
    const trimmed = this.query.trim();
    if (!trimmed) return;

    this.loading = true;
    this.errore = null;
    this.notizieSelezionate = [];

    this.notizieService.cercaNotizie(trimmed).subscribe({
      next: (res) => {
        this.risultati = res || [];
        this.loading = false;
      },
      error: () => {
        this.errore = 'Errore durante la ricerca';
        this.loading = false;
      },
    });
  }

  toggleSelezione(notizia: any, event: Event): void {
    event.stopPropagation();
    // Usa id univoco o combinazione chiave
    const id = this.getId(notizia);
    const exists = this.notizieSelezionate.some(n => this.getId(n) === id);
    if (exists) {
      this.notizieSelezionate = this.notizieSelezionate.filter(n => this.getId(n) !== id);
    } else {
      this.notizieSelezionate.push(notizia);
    }
  }

  isSelezionata(notizia: any): boolean {
    const id = this.getId(notizia);
    return this.notizieSelezionate.some(n => this.getId(n) === id);
  }

  private getId(notizia: any): string {
    // Se hai id vero, usalo
    if (notizia.id) return notizia.id.toString();
    // Altrimenti fallback su link o titolo uniti (assicurati sia unico!)
    return `${notizia.link || ''}||${notizia.titolo || ''}`;
  }
  generaArticolo(): void {
    if (this.notizieSelezionate.length === 0) {
      this.erroreGenerazione = 'Seleziona almeno un articolo prima di generare.';
      return;
    }

    this.loadingGenerazione = true;
    this.erroreGenerazione = null;
    this.articoloGenerato = null;

    // Manda gli articoli selezionati al servizio
    this.notizieService.generaNotizia(this.notizieSelezionate, [], '').subscribe({
      next: (res) => {
        this.articoloGenerato = res;
        this.loadingGenerazione = false;
      },
      error: (err) => {
        this.erroreGenerazione = 'Errore durante la generazione dell\'articolo.';
        this.loadingGenerazione = false;
        console.error(err);
      },
    });
  }
}
