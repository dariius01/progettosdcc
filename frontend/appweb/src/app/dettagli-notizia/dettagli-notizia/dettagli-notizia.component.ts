import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { NotizieService, Notizia } from '../../services/notizie.service';
import { CommonModule, DatePipe } from '@angular/common';
import { Router } from '@angular/router';
import { MatIcon } from '@angular/material/icon';
import jsPDF from 'jspdf';

@Component({
  selector: 'app-dettagli-notizia',
  templateUrl: './dettagli-notizia.component.html',
  styleUrls: ['./dettagli-notizia.component.css'],
  standalone: true,
  imports: [CommonModule, MatIcon],  
})
export class DettagliNotiziaComponent implements OnInit {
  notizia?: Notizia;
  errore: string | null = null;
  loading = true;
  queryCorrente = '';
  risultatiCorrenti: any[] = [];
  notizieSelezionateCorrenti: any[] = [];
  mostraConfermaEliminazione = false;
  mostraSuccessoEliminazione = false;

  constructor(
    private route: ActivatedRoute,
    private notizieService: NotizieService,
    private router: Router
  ) {}

  ngOnInit(): void {
    // Recupera lo stato passato dalla pagina precedente (se presente)
    const navState = history.state || {};
    this.queryCorrente = navState.query ?? '';
    this.risultatiCorrenti = navState.risultati ?? [];
    this.notizieSelezionateCorrenti = navState.notizieSelezionate ?? [];

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

  vaiAllaHome(): void {
    this.router.navigate(['/']);
  }

  vaiAModifica(): void {
    if (!this.notizia?.id) return;
    this.router.navigate(['/notizia', this.notizia.id, 'modifica']);
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
    this.mostraConfermaEliminazione = true;
  }

  confermaEliminazione(): void {
    if (!this.notizia?.id) return;

    this.notizieService.eliminaNotizia(this.notizia.id).subscribe({
      next: () => {
        this.mostraConfermaEliminazione = false;
        this.mostraSuccessoEliminazione = true; 
      },
      error: (err) => {
        console.error('Errore durante l\'eliminazione', err);
        this.errore = 'Errore durante l\'eliminazione della notizia.';
        this.mostraConfermaEliminazione = false;
      }
    });
  }

  annullaEliminazione(): void {
    this.mostraConfermaEliminazione = false;
  }

  tornaHome(): void {
   this.router.navigate(['/'], {
      state: {
        query: this.queryCorrente,
        risultati: this.risultatiCorrenti,
        notizieSelezionate: this.notizieSelezionateCorrenti,
      },
    });
  }

  // Gestione PDF
  scaricaPDF(): void {
    if (!this.notizia) return;

    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 20;
    let y = 40;

    doc.setFont('helvetica', 'bold');
    doc.setFontSize(24);
    doc.setTextColor(34, 15, 103); 
    const titleLines = doc.splitTextToSize(this.notizia.titolo || '', pageWidth - 2 * margin);
    doc.text(titleLines, pageWidth / 2, y, { align: 'center' });
    y += titleLines.length * 10 + 5;

    doc.setDrawColor(34, 15, 103);
    doc.setLineWidth(0.5);
    doc.line(margin, y, pageWidth - margin, y);
    y += 10;

    if (this.notizia.sottotitolo) {
      doc.setFont('helvetica', 'italic');
      doc.setFontSize(14);
      doc.setTextColor(80, 80, 80);
      const subLines = doc.splitTextToSize(this.notizia.sottotitolo, pageWidth - 2 * margin);
      doc.text(subLines, margin, y);
      y += subLines.length * 8 + 10;
    }

    doc.setFont('helvetica', 'normal');
    doc.setFontSize(12);
    doc.setTextColor(0, 0, 0);
    const testo = this.notizia.testo || '';
    const lines = doc.splitTextToSize(testo, pageWidth - 2 * margin);

    for (const line of lines) {
      if (y > pageHeight - 30) {
        doc.addPage();
        y = 30;
      }
      doc.text(line, margin, y, { align: 'justify', maxWidth: pageWidth - 2 * margin });
      y += 7; 
    }

    doc.setFontSize(10);
    doc.setFont('helvetica', 'italic');
    doc.setTextColor(100, 100, 100);
    const dataStr = this.notizia.data_creazione ? new Date(this.notizia.data_creazione).toLocaleString() : '';
    doc.text(`Pubblicato il: ${dataStr}`, pageWidth - margin, pageHeight - 15, { align: 'right' });

    doc.save(`${this.notizia.titolo || 'articolo'}.pdf`);
  }
}