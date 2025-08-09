import { bootstrapApplication } from '@angular/platform-browser';
import { provideHttpClient, HTTP_INTERCEPTORS } from '@angular/common/http';
import { provideRouter } from '@angular/router';
import { App } from './app/app'; 
import { AuthInterceptor } from './app/services/auth.interceptor';
import { routes } from './app/app.routes'; // importa le tue rotte

bootstrapApplication(App, {
  providers: [
    provideHttpClient(),
    provideRouter(routes),  // <-- aggiungi questo
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true,
    },
  ],
});