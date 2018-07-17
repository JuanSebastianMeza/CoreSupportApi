import { Component } from '@angular/core';
import { Router } from '@angular/router';

// Add font-awesome to project
import { faBars,
         faCaretDown,
         faEnvelope,
         faGlobe,
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
    faGlobe = faGlobe;
    faEnvelope = faEnvelope;

    // Constants
    constant: any = this.constants.getAppComponentViewConstants();
    lastLoginDate: Date = new Date(this.globals.lastLoginDate);
    // lastLoginDate = true ? console.log(this.globals.lastLoginDate) : console.log(this.globals.lastLoginDate);

    constructor(
        // Inject router
        public router: Router,
        // Inject utils
        public utils: UtilsService,
        // Inject globals
        public globals: Globals,
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
