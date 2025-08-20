import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';  // per *ngIf
import { FormsModule } from '@angular/forms';
import { ArticoliManualiService } from '../services/articoli-manuali.service';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'app-aggiunta-manuale',
  imports: [CommonModule, FormsModule, MatIcon],
  templateUrl: './aggiunta-manuale.component.html',
  styleUrls: ['./aggiunta-manuale.component.css'],
  standalone: true,
})
export class AggiuntaManualeComponent {
  titolo = '';
  sottotitolo = '';
  testo = '';
  errore: string | null = null;

  queryCorrente = '';
  risultatiCorrenti: any[] = [];
  notizieSelezionateCorrenti: any[] = [];

  constructor(
    private router: Router,
    private articoliManualiService: ArticoliManualiService
  ) {
    // Recupera stato passato da home (se presente)
    const state = history.state;
    if (state) {
      this.queryCorrente = state.query ?? '';
      this.risultatiCorrenti = state.risultati ?? [];
      this.notizieSelezionateCorrenti = state.notizieSelezionate ?? [];
    }
  }

  aggiungiNotizia(): void {
    this.errore = null;

    if (!this.titolo.trim() || !this.testo.trim()) {
      this.errore = 'Titolo e testo sono obbligatori.';
      return;
    }

    const nuovoArticolo = {
      titolo: this.titolo.trim(),
      sottotitolo: this.sottotitolo.trim(),
      testo: this.testo.trim(),
    };

    this.articoliManualiService.aggiungiArticolo(nuovoArticolo);

    // Torna alla home mantenendo stato ricerca e selezione
    this.router.navigate(['/'], {
      state: {
        query: this.queryCorrente,
        risultati: this.risultatiCorrenti,
        notizieSelezionate: this.notizieSelezionateCorrenti,
      },
    });
  }

  tornaHome(): void {
  // Torna alla home mantenendo stato ricerca e selezione
    this.router.navigate(['/'], {
      state: {
        query: this.queryCorrente,
        risultati: this.risultatiCorrenti,
        notizieSelezionate: this.notizieSelezionateCorrenti,
      },
    });
  }

}
