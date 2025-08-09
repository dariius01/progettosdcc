import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http'; // aggiungi HttpHeaders
import { Observable } from 'rxjs';
import { AuthService } from './auth.service';  // importa AuthService per prendere il token

export interface Notizia {
  id?: number;
  titolo: string;
  sottotitolo?: string;
  testo: string;
  created_at?: string;  
}


@Injectable({
  providedIn: 'root',
})
export class NotizieService {
  private apiUrl = 'http://localhost:5000/api'; 

  constructor(private http: HttpClient, private authService: AuthService) {}

  // Metodo per creare headers con token se presente
  private getAuthHeaders(): HttpHeaders {
    const token = this.authService.getToken();
    let headers = new HttpHeaders();
    if (token) {
      headers = headers.set('Authorization', `Bearer ${token}`);
    }
    return headers;
  }

  // Salva nuova notizia (POST /api/salva-notizia)
  salvaNotizia(notizia: Notizia): Observable<Notizia> {
    const headers = this.getAuthHeaders();
    return this.http.post<Notizia>(`${this.apiUrl}/salva-notizia`, notizia, { headers });
  }


  // Cerca notizie web (GET /api/ricerca-notizie?q=...)
  cercaNotizie(query: string): Observable<any[]> {
    const params = new HttpParams().set('q', query);
    return this.http.get<any[]>(`${this.apiUrl}/ricerca-notizie`, { params });
  }

  // Recupera tutte le notizie (GET /api/notizie)
  getAllNotizie(): Observable<Notizia[]> {
    const headers = this.getAuthHeaders();
    return this.http.get<Notizia[]>(`${this.apiUrl}/notizie`, { headers });
  }


  // Recupera notizia per ID (GET /api/notizie/:id)
  getNotizia(id: number) {
    const headers = this.getAuthHeaders();
    return this.http.get<Notizia>(`${this.apiUrl}/notizie/${id}`, { headers });
  }


  // Recupera ultime 4 notizie (GET /api/cronologia-notizie)
  getCronologiaNotizie(): Observable<Notizia[]> {
    const headers = this.getAuthHeaders();
    return this.http.get<Notizia[]>(`${this.apiUrl}/cronologia-notizie`, { headers });
  }

  // Modifica notizia esistente (PUT /api/notizie/:id)
  //modificaNotizia(id: number, notizia: Partial<Notizia>): Observable<any> {
    //return this.http.put(`${this.apiUrl}/notizie/${id}`, notizia);
  //}

  // Elimina notizia (DELETE /api/notizie/:id)
  eliminaNotizia(id: number): Observable<any> {
    const headers = this.getAuthHeaders();
    return this.http.delete(`${this.apiUrl}/notizie/${id}`, { headers });
  }


  // Genera notizia da articoli (POST /api/genera-notizia)
  generaNotizia(
    articoliWeb: any[],
    articoliManuali: any[],
    tema: string
  ): Observable<any> {
    const body = { articoli_web: articoliWeb, articoli_manuali: articoliManuali, tema };
    return this.http.post<any>(`${this.apiUrl}/genera-notizia`, body);
  }
}
