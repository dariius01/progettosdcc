import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MatIconModule } from '@angular/material/icon'; 

@Component({
  standalone: true,
  selector: 'app-root',
  imports: [
    RouterOutlet,
    MatIconModule  // aggiungi qui
  ],
  template: `<router-outlet></router-outlet>`,
})
export class App {}
