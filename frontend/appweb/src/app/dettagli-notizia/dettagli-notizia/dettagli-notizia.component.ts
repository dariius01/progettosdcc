import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NotizieService, Notizia } from '../../services/notizie.service';
import { CommonModule, DatePipe } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-dettagli-notizia',
  templateUrl: './dettagli-notizia.component.html',
  styleUrls: ['./dettagli-notizia.component.css'],
  standalone: true,
  imports: [CommonModule],  // qui importa CommonModule per *ngIf e pipe date
})
export class DettagliNotiziaComponent implements OnInit {
  notizia?: Notizia;
  errore: string | null = null;
  loading = true;

  constructor(
    private route: ActivatedRoute,
    private notizieService: NotizieService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Prendo l'id dalla route (es. /notizia/:id)
    const idParam = this.route.snapshot.paramMap.get('id');
    if (idParam) {
      const id = +idParam;
      this.caricaNotizia(id);
    } else {
      this.errore = 'ID notizia non valido.';
      this.loading = false;
    }
  }

  caricaNotizia(id: number) {
    this.loading = true;
    this.notizieService.getNotizia(id).subscribe({
      next: (data) => {
        this.notizia = data;
        this.errore = null;
        this.loading = false;
      },
      error: (err) => {
        console.error('Errore nel caricamento della notizia', err);
        this.errore = 'Errore nel caricamento della notizia. Potrebbe non esistere o non hai accesso.';
        this.loading = false;
      }
    });
  }

  onEliminaNotizia(): void {
  if (!this.notizia?.id) return;

  if (confirm('Sei sicuro di voler eliminare questa notizia?')) {
    this.notizieService.eliminaNotizia(this.notizia.id).subscribe({
      next: () => {
        alert('Notizia eliminata con successo.');
        this.router.navigate(['/home']); // torna alla lista
      },
      error: (err) => {
        console.error('Errore durante l\'eliminazione', err);
        alert('Errore durante l\'eliminazione della notizia.');
      }
    });
  }
  }


}
