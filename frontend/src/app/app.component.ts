import { Component } from '@angular/core';
import { Router } from '@angular/router';

// Add font-awesome to project
import { faBars,
		 faCaretDown,
		 faSignOutAlt,
		 faLock, } from '@fortawesome/free-solid-svg-icons';

// Import global class
import { Globals } from './globals';

// Import own services
import { UtilsService } from './services/utils/utils.service';
import { ConstService } from './services/utils/const.service';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {

	// Font awesome icons
	faCaretDown = faCaretDown;
	faBars = faBars;
	faSignOutAlt = faSignOutAlt;
	faLock = faLock;

	// Constants
	constant: any = this.constants.getAppComponentViewConstants();

	constructor(
    	// Inject router
  		public router: Router,
		// Inject utils
		private utils: UtilsService,
		// Inject globals
		private globals: Globals,
		// Inject constants
    	private constants: ConstService) {}


	// Log out method
	changePassword(): void {
        // Go to password view
        this.router.navigate([this.constant.password]);
	}

	// Log out method
	logOut(): void {
	    // Log out
		this.utils.logOut(this.constant.successMsg);
	}

}
