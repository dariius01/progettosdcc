import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ArticoloGeneratoComponent } from './articolo-generato/articolo-generato.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { AggiuntaManualeComponent } from './aggiunta-manuale/aggiunta-manuale.component';
  

export const routes: Routes = [
  { path: '', component: HomeComponent },

  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },

  // Rotta protetta con AuthGuard
  { path: 'articolo-generato', component: ArticoloGeneratoComponent},
  { path: 'aggiunta-manuale', component: AggiuntaManualeComponent},

  // fallback
  { path: '**', redirectTo: '' },
];