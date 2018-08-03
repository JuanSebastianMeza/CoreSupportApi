import { Injectable } from '@angular/core';

// Router imports
import { Router,
         CanActivate } from '@angular/router';

// Auth imports
import { AuthService } from './auth.service';
import { UtilsService } from '../utils/utils.service';
import { ConstService } from '../utils/const.service';

// Import globals
import { Globals } from '../../globals';


@Injectable({
  providedIn: 'root'
})
export class PasswordGuardService implements CanActivate {

  // Constants
  constant: any = this.constService.getUtilsServiceConstants();

  constructor(
    // Inject services
    public auth: AuthService,
    public utils: UtilsService,
    public constService: ConstService,
    // Inject router
    public router: Router,
    // Inject globals
    public globals: Globals) { }

  canActivate(): boolean {
    // Get if it is user first time for login
    const isFirstTime = this.auth.isUserFirstTime();
    // Get when was the last password change
    const lastPassChangeDiff = this.globals.remainingDaysToPasswordChange;
    // Validate access
    if (isFirstTime || (lastPassChangeDiff > this.constant.blockAccess )) {
      this.router.navigate(['password']);
      this.utils.openSnackBar(
        isFirstTime ? this.constant.firstTimeLoginMessage : this.constant.passwordExpirationMessage
      );
      return false;
    } else if (lastPassChangeDiff > this.constant.blockNotification ) {
      // Show notification panel
      this.globals.showPasswordNotification = true;
      this.globals.passChangeMessage = (1
        + this.constService.getUtilsServiceConstants().blockAccess - this.auth.getLastPassChangeDiff()).toString()
        + (((this.constService.getUtilsServiceConstants().blockAccess - this.auth.getLastPassChangeDiff()) === 0) ? ' día' : ' días');
      return true;
    } else {
      return true;
    }
  }

}
