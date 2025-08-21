import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';
import { Notizia } from '../../services/notizie.service';
import { MatIcon } from '@angular/material/icon';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatIcon],
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  errorMessage: string | null = null;
  articoloDaSalvare: Notizia | null = null;
  autoSave = false;
  submitted = false;  // <--- variabile per controllo submit

  constructor(
    private fb: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    const stato = this.router.getCurrentNavigation()?.extras.state as { articolo?: Notizia, autoSave?: boolean };
    this.articoloDaSalvare = stato?.articolo ?? null;
    this.autoSave = stato?.autoSave ?? false;
  }

  ngOnInit(): void {
    this.registerForm = this.fb.group({
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
    });
  }

  onSubmit(): void {
    this.submitted = true;  // <--- segna che è stato premuto submit

    if (this.registerForm.invalid) return;

    const { email, password } = this.registerForm.value;

    this.authService.register(email, password).subscribe({
      next: () => {
        this.authService.login(email, password).subscribe({
          next: () => {
            if (this.articoloDaSalvare) {
              this.router.navigate(['/articolo-generato'], {
                state: {
                  articolo: this.articoloDaSalvare,
                  autoSave: this.autoSave
                },
                replaceUrl: true
              });
            } else {
              this.router.navigate(['/'], { replaceUrl: true });
            }
          },
          error: () => {
            this.errorMessage = 'Registrazione riuscita ma login automatico fallito';
          }
        });
      },
      error: (err) => {
        if (!err.status) {
          this.errorMessage = 'Errore di connessione o server non disponibile';
          return;
        }

        switch (err.status) {
          case 400:
            this.errorMessage = err.error?.errore || 'Dati non validi';
            break;
          case 409:
            this.errorMessage = 'Utente già esistente';
            break;
          default:
            this.errorMessage = err.error?.errore || 'Errore nella registrazione';
            break;
        }
      }
    });
  }
  goToLogin(){
    this.router.navigate(['/login']);
  }
}
