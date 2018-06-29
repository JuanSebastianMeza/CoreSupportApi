import { Injectable, Inject } from '@angular/core';
import { Router } from '@angular/router';

// Import global class
import { Globals } from '../../globals';

// Angular Material imports
import { MatSnackBar } from '@angular/material';

// Own services imports
import { ConstService } from './const.service';


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
    // Inject constants
    private constService: ConstService) { }

  // SnackBar action
  openSnackBar(message: string, action: string) {
    this.snackBar.open(message, action, {
      duration: this.constant.duration,
      panelClass: [this.constant.snackbarColor],
    });
  }

  // Log out method
  logOut(message: string): void {
      // Clear Storage
	    this.localStorage.clear();
      // Go to login view
      this.router.navigate([this.constant.loginUrl]);
      // Reset auth false
      this.globals.isAuthenticated = false;
      // Reset user name
      this.globals.userName = null;
      // Show success password change
      this.openSnackBar(message, null);
  }

}
