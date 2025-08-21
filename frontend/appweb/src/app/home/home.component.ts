import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { NotizieService } from '../services/notizie.service';
import { MatIconModule } from '@angular/material/icon';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { Subscription } from 'rxjs';
import { ArticoliManualiService } from '../services/articoli-manuali.service';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, MatIconModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit, OnDestroy {
  query = '';
  risultati: any[] = [];
  loading = false;
  errore: string | null = null;
  notizieSelezionate: any[] = [];
  articoloGenerato: any = null;
  loadingGenerazione = false;
  erroreGenerazione: string | null = null;
  mostraCronologia = false;
  cronologiaNotizie: any[] = []; // ✅ nuove variabile
  isLoggedIn = false;
  erroreCronologia: string | null = null; 
  nessunRisultato: boolean = false;

  articoliManuali: any[] = [];
  mostraArticoliManuali = false;
  articoloManualeSelezionato: any | null = null;
  articoloPopup: any = null;
  loginAlert: string | null = null;




  private authSubscription!: Subscription;
  private articoliSubscription!: Subscription;

  constructor(
    private notizieService: NotizieService,
    private router: Router,
    private authService: AuthService,
    private articoliManualiService: ArticoliManualiService
  ) {}

  ngOnInit(): void {
    this.authSubscription = this.authService.isLoggedIn().subscribe(status => {
      this.isLoggedIn = status;
    });

    // Carica articoli manuali dal service
    this.articoliSubscription = this.articoliManualiService.articoli$.subscribe(articoli => {
      this.articoliManuali = articoli;
    });

    // Riprendi stato se esiste
    const state = history.state;
    if (state) {
      if (state.query) this.query = state.query;
      if (state.risultati) this.risultati = state.risultati;
      if (state.notizieSelezionate) this.notizieSelezionate = state.notizieSelezionate;
      if (state.articoloGenerato) this.articoloGenerato = state.articoloGenerato;
    }
  }

  ngOnDestroy(): void {
    this.authSubscription.unsubscribe();
    if (this.articoliSubscription) this.articoliSubscription.unsubscribe();
  }

  apriPopup(articolo: any) {
    this.articoloPopup = articolo;
  }

  chiudiPopup() {
    this.articoloPopup = null;
  }

  cerca(): void {
    const trimmed = this.query.trim();
    if (!trimmed) return;

    this.loading = true;
    this.errore = null;
    this.notizieSelezionate = [];
    this.nessunRisultato = false; // reset

    this.notizieService.cercaNotizie(trimmed).subscribe({
      next: (res) => {
        this.risultati = res || [];
        this.loading = false;
        this.nessunRisultato = this.risultati.length === 0;
      },
      error: () => {
        this.errore = 'Errore durante la ricerca';
        this.loading = false;
        this.nessunRisultato = false;
      },
    });
  }


  toggleSelezione(notizia: any, event: Event): void {
    event.stopPropagation();
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
    if (notizia.id) return notizia.id.toString();
    return `${notizia.link || ''}||${notizia.titolo || ''}`;
  }

  generaNotizia(): void {
    const articoliDaGenerare = [...this.notizieSelezionate, ...this.articoliManuali];
    if (articoliDaGenerare.length === 0) {
      this.erroreGenerazione = 'Seleziona almeno un articolo (web o manuale) prima di generare.';
      return;
    }

    this.loadingGenerazione = true;
    this.erroreGenerazione = null;

    // Passa this.query come tema
    this.notizieService.generaNotizia(this.notizieSelezionate, this.articoliManuali, this.query.trim()).subscribe({
      next: (res) => {
        this.loadingGenerazione = false;
        this.router.navigate(['/articolo-generato'], {
          state: {
            articolo: res,
            query: this.query,
            risultati: this.risultati,
            notizieSelezionate: this.notizieSelezionate,
            articoliManuali: this.articoliManuali
          }
        });
      },
      error: (err) => {
        this.erroreGenerazione = 'Errore durante la generazione dell\'articolo.';
        this.loadingGenerazione = false;
        console.error(err);
      },
    });
  }


  apriLink(notizia: any): void {
    if (notizia && notizia.url) {
      window.open(notizia.url, '_blank', 'noopener,noreferrer');
    }
  }


   toggleCronologia(): void {
    this.mostraCronologia = !this.mostraCronologia;

    if (this.mostraCronologia && this.cronologiaNotizie.length === 0) {
      this.notizieService.getAllNotizie().subscribe({
        next: (res) => {
          this.cronologiaNotizie = res;
          this.erroreCronologia = null; // ✅ reset
        },
        error: () => {
          this.erroreCronologia = 'Errore nel recupero della cronologia.'; // ✅ messaggio
        }
      });
    }
  }




  logout(): void {
    this.authService.logout();
    this.router.navigate(['/']);
  }

  vaiAdAggiuntaManuale(): void {
    this.router.navigate(['/aggiunta-manuale'], {
      state: {
        query: this.query,
        risultati: this.risultati,
        notizieSelezionate: this.notizieSelezionate
      }
    });
  }


  toggleMostraArticoliManuali(): void {
    this.mostraArticoliManuali = !this.mostraArticoliManuali;
    this.articoloManualeSelezionato = null;
  }

  selezionaArticoloManuale(articolo: any): void {
    if (this.articoloManualeSelezionato === articolo) {
      // Se è già selezionato, lo deseleziono
      this.articoloManualeSelezionato = null;
    } else {
      // Altrimenti lo seleziono
      this.articoloManualeSelezionato = articolo;
    }
  }


  rimuoviArticoloManuale(articolo: any, event: Event): void {
    event.stopPropagation();
    this.articoliManualiService.rimuoviArticolo(articolo);

    if (this.articoloManualeSelezionato === articolo) {
      this.articoloManualeSelezionato = null;
    }
  }
}
