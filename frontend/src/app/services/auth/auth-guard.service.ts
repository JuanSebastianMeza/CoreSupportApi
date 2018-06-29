import { Injectable } from '@angular/core';

// Import router dependencies
import { Router, 
         CanActivate } from '@angular/router';

// Imports own services
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class AuthGuardService implements CanActivate {

  constructor(
	// Inject AuthService
  	public auth: AuthService, 
	// Inject router
  	public router: Router) { }

  // Override CanActivate method
  canActivate(): boolean {
  	// If not authenticated redirect to 'login' return false
    if (!this.auth.isAuthenticated()) {
      this.router.navigate(['login']);
      return false;
    }
    return true;
  }
  
}
