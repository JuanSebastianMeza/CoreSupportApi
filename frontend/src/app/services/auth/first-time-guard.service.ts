import { Injectable } from '@angular/core';

// Router imports
import { Router,
         CanActivate } from '@angular/router';

// Auth imports
import { AuthService } from './auth.service';


@Injectable({
  providedIn: 'root'
})
export class FirstTimeGuardService implements CanActivate {

  constructor(
    // Inject auth service
    public auth: AuthService,
    // Inject router
    public router: Router) { }

  canActivate(): boolean {
    // Get if it is user first time for login
    const isFirstTime = this.auth.isUserFirstTime();
    console.log(isFirstTime);
    // Validate access
    if (isFirstTime) {
      this.router.navigate(['password']);
      return false;
    } else {
      return true;
    }
  }

}
