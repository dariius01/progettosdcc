import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http'; 
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface Notizia {
  id?: number;
  titolo: string;
  sottotitolo?: string;
  testo: string;
  data_creazione?: string; 
  data_modifica?: string;
}

@Injectable({
  providedIn: 'root',
})
export class NotizieService {
  private apiUrl = environment.apiUrl;; 

  constructor(private http: HttpClient) {}

  // (POST /api/salva-notizia)
  salvaNotizia(notizia: Notizia): Observable<Notizia> {
    return this.http.post<Notizia>(`${this.apiUrl}/salva-notizia`, notizia, { withCredentials: true });
  }

  // (GET /api/ricerca-notizie?q=...)
  cercaNotizie(query: string): Observable<any[]> {
    const params = new HttpParams().set('q', query);
    return this.http.get<any[]>(`${this.apiUrl}/ricerca-notizie`, { params });
  }

  // (GET /api/notizie)
  getAllNotizie(): Observable<Notizia[]> {
    return this.http.get<Notizia[]>(`${this.apiUrl}/notizie`, { withCredentials: true });
  }

  // (GET /api/notizie/:id)
  getNotizia(id: number) {
    return this.http.get<Notizia>(`${this.apiUrl}/notizie/${id}`, { withCredentials: true });
  }

  // (PUT /api/notizie/:id)
  modificaNotizia(id: number, notizia: Partial<Notizia>): Observable<any> {
    return this.http.put(`${this.apiUrl}/notizie/${id}`, notizia, { withCredentials: true });
  }

  // (DELETE /api/notizie/:id)
  eliminaNotizia(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/notizie/${id}`, { withCredentials: true });
  }

  // (POST /api/genera-notizia)
  generaNotizia(
    articoliWeb: any[],
    articoliManuali: any[],
    tema: string
  ): Observable<any> {
    const body = { articoli_web: articoliWeb, articoli_manuali: articoliManuali, tema };
    return this.http.post<any>(`${this.apiUrl}/genera-notizia`, body);
  }
}