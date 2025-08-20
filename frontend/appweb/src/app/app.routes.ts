import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ArticoloGeneratoComponent } from './articolo-generato/articolo-generato.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { AggiuntaManualeComponent } from './aggiunta-manuale/aggiunta-manuale.component';
import { DettagliNotiziaComponent } from './dettagli-notizia/dettagli-notizia/dettagli-notizia.component';
import { ModificaNotiziaComponent } from './modifica-notizia/modifica-notizia/modifica-notizia.component';
  

export const routes: Routes = [
  { path: '', component: HomeComponent },

  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },

  { path: 'articolo-generato', component: ArticoloGeneratoComponent},
  { path: 'aggiunta-manuale', component: AggiuntaManualeComponent},
  { path: 'notizia/:id', component: DettagliNotiziaComponent},
  { path: 'notizia/:id/modifica', component: ModificaNotiziaComponent },


  // fallback
  { path: '**', redirectTo: '' },
];