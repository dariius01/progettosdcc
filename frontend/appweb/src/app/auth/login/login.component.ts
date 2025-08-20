import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { Notizia } from '../../services/notizie.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css'],
})
export class LoginComponent {
  email = '';
  password = '';
  error = '';
  articoloDaSalvare: Notizia | null = null;
  autoSave = false; // <- aggiunto

  constructor(private router: Router, private authService: AuthService) {
    const stato = this.router.getCurrentNavigation()?.extras.state as { articolo?: Notizia, autoSave?: boolean };
    this.articoloDaSalvare = stato?.articolo ?? null;
    this.autoSave = stato?.autoSave ?? false; // <- aggiunto
  }

  onLogin() {
    this.error = '';
    this.authService.login(this.email, this.password).subscribe({
      next: () => {
        if (this.articoloDaSalvare) {
          this.router.navigate(['/articolo-generato'], { 
            state: { 
              articolo: this.articoloDaSalvare, 
              autoSave: this.autoSave
            },
            replaceUrl: true  // <-- qui
          });
        } else {
          this.router.navigate(['/'], { replaceUrl: true });  // <-- qui
        }
      },
      error: () => this.error = 'Credenziali errate'
    });
  }
}
