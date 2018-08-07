import { Injectable, Inject } from '@angular/core';
import { Router } from '@angular/router';

// Import global class
import { Globals } from '../../globals';

// Angular Material imports
import { MatSnackBar } from '@angular/material';

// Own services imports
import { ConstService } from './const.service';
import { AuthService } from '../../services/auth/auth.service';
import { HttpRequestsService } from '../../services/utils/http-requests.service';


@Injectable({
  providedIn: 'root'
})
export class UtilsService {

  // Constants
  constant: any = this.constService.getUtilsServiceConstants();

  constructor(
    // Inject localStorage factory
    @Inject('LocalStorage') public localStorage: any,
    // Inject router
    public router: Router,
    // Inject global variables
    private globals: Globals,
    // Inject SnackBar
    private snackBar: MatSnackBar,
    // Inject services
    private http: HttpRequestsService,
    private auth: AuthService,
    private constService: ConstService) { }

  // SnackBar action
  openSnackBar(message: string, action: string = null) {
    this.snackBar.open(message, action, {
      duration: this.constant.duration,
      panelClass: [this.constant.snackbarColor],
    });
  }

  // SnackBar action
  openAdvisorSnackBar() {
    this.snackBar.open(
      this.constant.advisorMessage,
      this.constant.hideSnackBar,
      { panelClass: [this.constant.advisorSnackbarColor] }
    );
  }

  // Log out method
  logOut(message: string): void {
      // Initiate access audit constant
      const accessAudit = {
        logoutAccess: false,
        accessGranted: true,
      };
      // Notify successful logout
      this.http.postAccessAuditInfo(
        accessAudit.logoutAccess,
        this.globals.appId,
        this.auth.getUserId(),
        accessAudit.accessGranted
      );
      // Clear Storage
      this.localStorage.clear();
      // Go to login view
      this.router.navigate([this.constant.loginUrl]);
      // Reset globals
      this.globals.isAuthenticated = false;
      this.globals.showPasswordNotification = false;
      this.globals.userName = null;
      this.globals.lastLoginDate = null;
      this.globals.remainingDaysToPasswordChange = null;
      // Reset user name
      this.globals.userName = null;
      // Show success password change
      this.openSnackBar(message, null);
  }

}
