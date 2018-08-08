import { Injectable } from '@angular/core';

// Router imports
import { Router,
         CanActivate } from '@angular/router';

// Own imports
import { AuthService } from './auth.service';


@Injectable({
  providedIn: 'root'
})
export class LoginGuardService {

  constructor(
  // Inject AuthService
    public auth: AuthService,
  // Inject router
    public router: Router) { }

  // Override CanActivate method
  canActivate(): boolean {
    // If it is autenticated, go to home, else go to login
    if (this.auth.isAuthenticated()) {
      this.router.navigate(['home']);
    }
    return true;
  }

}
