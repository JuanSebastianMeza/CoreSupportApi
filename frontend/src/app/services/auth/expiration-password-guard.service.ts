import { Injectable } from '@angular/core';

// Router imports
import { Router,
         CanActivate } from '@angular/router';

// Auth imports
import { AuthService } from './auth.service';
import { UtilsService } from '../utils/utils.service';
import { ConstService } from '../utils/const.service';


@Injectable({
  providedIn: 'root'
})
export class ExpirationPasswordGuardService implements CanActivate {

  // Constants
  constant: any = this.constService.getUtilsServiceConstants();

  constructor(
    // Inject services
    public auth: AuthService,
    public utils: UtilsService,
    public constService: ConstService,
    // Inject router
    public router: Router) { }

  canActivate(): boolean {
    // Get when was the last password change
    const lastPassChangeDiff = this.auth.getLastPassChangeDiff();
    // Validate access
    if (lastPassChangeDiff > 30) {
      this.router.navigate(['password']);
      this.utils.openSnackBar(this.constant.passwordExpirationMessage);
      return false;
    } else if (lastPassChangeDiff > 25) {
      // TODO: Save variable in globals to show a banner
      // TODO: limits to const.service
      return true;
    } else {
      return true;
    }
  }

}
