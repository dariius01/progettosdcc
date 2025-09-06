import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { Notizia } from '../../services/notizie.service';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule, MatIcon],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  email = '';
  password = '';
  error = '';
  articoloDaSalvare: Notizia | null = null;
  autoSave = false;
  mostraPassword = true;

  constructor(private router: Router, private authService: AuthService) {
    // Verifica se presente flag autosave (si è cercato di salvare l'articolo denza essere loggati)
    const stato = this.router.getCurrentNavigation()?.extras.state as {
      articolo?: Notizia;
      autoSave?: boolean;
    };
    this.articoloDaSalvare = stato?.articolo ?? null;
    this.autoSave = stato?.autoSave ?? false;
  }

  onLogin() {
    this.error = '';
    this.authService.login(this.email, this.password).subscribe({
      next: () => {
        if (this.articoloDaSalvare) {
          this.router.navigate(['/articolo-generato'], {
            state: {
              articolo: this.articoloDaSalvare,
              autoSave: this.autoSave,
            },
            replaceUrl: true,
          });
        } else {
          this.router.navigate(['/'], { replaceUrl: true });
        }
      },
      error: () => (this.error = 'Credenziali errate'),
    });
  }

  vaiARegister() {
    this.router.navigate(['/register']);
  }

  tornaHome() {
    this.router.navigate(['/']);
  }
}
