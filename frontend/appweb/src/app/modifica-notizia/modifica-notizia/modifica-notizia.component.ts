import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { NotizieService, Notizia } from '../../services/notizie.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // <-- FormsModule qui!

@Component({
  selector: 'app-modifica-notizia',
  standalone: true,
  imports: [CommonModule, FormsModule], // <-- aggiunto FormsModule
  templateUrl: './modifica-notizia.component.html',
  styleUrls: ['./modifica-notizia.component.css']
})
export class ModificaNotiziaComponent implements OnInit {
  notizia: Notizia | null = null;
  errore: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private notizieService: NotizieService
  ) {}

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');
    if (idParam) {
      const id = +idParam;
      this.notizieService.getNotizia(id).subscribe({
        next: (data) => this.notizia = data,
        error: () => this.errore = 'Errore nel caricamento della notizia.'
      });
    }
  }

  salvaModifiche(): void {
    if (!this.notizia?.id) return;
    this.notizieService.modificaNotizia(this.notizia.id, this.notizia).subscribe({
      next: () => this.router.navigate(['/notizia', this.notizia!.id]),
      error: () => this.errore = 'Errore durante il salvataggio delle modifiche.'
    });
  }

  annulla(): void {
    if (this.notizia?.id) {
      this.router.navigate(['/notizia', this.notizia.id]);
    } else {
      this.router.navigate(['/home']);
    }
  }
}
