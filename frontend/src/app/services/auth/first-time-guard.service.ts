import { Injectable } from '@angular/core';

// Router imports
import { Router,
         CanActivate } from '@angular/router';

// Auth imports
import { AuthService } from './auth.service';
import { UtilsService } from '../utils/utils.service';


@Injectable({
  providedIn: 'root'
})
export class FirstTimeGuardService implements CanActivate {

  constructor(
    // Inject services
    public auth: AuthService,
    public utils: UtilsService,
    // Inject router
    public router: Router) { }

  canActivate(): boolean {
    // Get if it is user first time for login
    const isFirstTime = this.auth.isUserFirstTime();
    // Validate access
    if (isFirstTime) {
      this.router.navigate(['password']);
      this.utils.openFirstTimeLoginSnackBar();
      return false;
    } else {
      return true;
    }
  }

}
