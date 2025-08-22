import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

export interface ArticoloManuale {
  titolo: string;
  sottotitolo?: string;
  testo: string;
}

@Injectable({
  providedIn: 'root'
})
export class ArticoliManualiService {
  private articoli: ArticoloManuale[] = [];
  private articoliSubject = new BehaviorSubject<ArticoloManuale[]>([]);

  get articoli$() {
    return this.articoliSubject.asObservable();
  }

  aggiungiArticolo(articolo: ArticoloManuale) {
    this.articoli.push(articolo);
    this.articoliSubject.next([...this.articoli]);
  }

  getArticoli(): ArticoloManuale[] {
    return [...this.articoli];
  }

  rimuoviArticolo(articolo: ArticoloManuale) {
    this.articoli = this.articoli.filter(a => a !== articolo);
    this.articoliSubject.next([...this.articoli]);
  }
}