import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { Notizia, NotizieService } from '../services/notizie.service';
import { AuthService } from '../services/auth.service';
import { MatIcon } from '@angular/material/icon';
import { catchError, switchMap, of } from 'rxjs';

@Component({
  selector: 'app-articolo-generato',
  standalone: true,
  imports: [CommonModule, MatIcon],
  templateUrl: './articolo-generato.component.html',
  styleUrls: ['./articolo-generato.component.css'],
})
export class ArticoloGeneratoComponent {
  articolo: Notizia | null = null;
  messaggio: string | null = null;
  errore: string | null = null;
  isLoggedIn = false;
  mostraAccessoRichiesto = false;
  mostraConfermaUscita: boolean = false;

  constructor(
    private router: Router,
    private authService: AuthService,
    private notizieService: NotizieService
  ) {
    const stato = this.router.getCurrentNavigation()?.extras.state as {
      articolo?: Notizia;
      autoSave?: boolean;
    };
    this.articolo = stato?.articolo ? this.pulisciNotizia(stato.articolo) : null;

    this.authService.isLoggedIn().subscribe((logged) => {
      this.isLoggedIn = logged;
      if (logged && stato?.autoSave && this.articolo) {
        this.salvaArticolo();
      }
    });
  }

  //Rimuove caratteri extra
  private pulisciNotizia(n: Notizia): Notizia {
    return {
      ...n,
      titolo: n.titolo.replace(/\*\*/g, '').replace(/^Titolo:\s*'|'$/g, ''),
      sottotitolo:
        n.sottotitolo?.replace(/\*\*/g, '').replace(/^Sottotitolo:\s*'|'$/g, '') || '',
      testo: n.testo.replace(/\*\*/g, ''),
    };
  }

  tornaHome(): void {
    if (this.articolo && !this.messaggio) {
      this.mostraConfermaUscita = true;
    } else {
      this.router.navigate(['/']);
    }
  }

  // Per confermare di non voler salvare
  tornaHomeConfermata() {
    this.mostraConfermaUscita = false;
    this.router.navigate(['/']);
  }

  salvaArticolo(): void {
    if (!this.articolo || !this.articolo.titolo || !this.articolo.testo) {
      this.errore = 'Titolo e testo sono obbligatori';
      return;
    }

    if (!this.isLoggedIn) {
      // Mostra popup con scelte login/registrazione
      this.mostraAccessoRichiesto = true;
      return;
    }

    // Salva con testo pulito
    const notiziaPulita = this.pulisciNotizia(this.articolo);
    this.notizieService.salvaNotizia(notiziaPulita).subscribe({
      next: () => {
        this.messaggio = 'Articolo salvato con successo!';
        this.mostraAccessoRichiesto = false;
      },
      error: (err) => {
        console.error('[DEBUG] Errore salvataggio:', err);
        this.errore = err.error?.errore || 'Errore durante il salvataggio';
      }
    });
  }

  vaiAlLogin() {
    this.router.navigate(['/login'], {
      state: { articolo: this.articolo, autoSave: true },
    });
  }

  vaiARegistrazione() {
    this.router.navigate(['/register'], {
      state: { articolo: this.articolo, autoSave: true },
    });
  }

  chiudiMessaggio() {
    this.messaggio = null;
    this.router.navigate(['/']);
  }
}
