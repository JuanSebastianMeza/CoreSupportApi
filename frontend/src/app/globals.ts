import { Injectable } from '@angular/core';

// Own services imports
import { AuthService } from './services/auth/auth.service';
import { ConstService } from './services/utils/const.service';


@Injectable()
export class Globals {

  // Variables
  isAuthenticated: boolean = this.auth.isAuthenticated();
  userName: string = this.isAuthenticated ? this.auth.getUserName() : null;
  lastLoginDate: Date = this.auth.getLastLoginDate();
  // Variables for password change module
  showPasswordNotification = false;
  remainingDaysToPasswordChange: number = this.auth.getLastPassChangeDiff();
  passChangeMessage: string = (1 + this.constants.getUtilsServiceConstants().blockAccess - this.remainingDaysToPasswordChange).toString()
    + (((this.constants.getUtilsServiceConstants().blockAccess - this.remainingDaysToPasswordChange) === 0) ? ' día' : ' días');

  constructor(
    // Inject auth service
    private auth: AuthService,
    private constants: ConstService) {}

}
