import { Injectable } from '@angular/core';

// Router imports
import { Router,
         CanActivate,
         ActivatedRouteSnapshot } from '@angular/router';

// Auth imports
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class RoleGuardService implements CanActivate {

  constructor(
    // Inject auth service
    public auth: AuthService,
    // Inject router
    public router: Router) { }

  canActivate(route: ActivatedRouteSnapshot): boolean {
    // This will be passed from the route config
    // on the data property
    const expectedRole = route.data.expectedRole;
    // Get user permissions
    const permissions = this.auth.getUserPermissions();
    // Validate access
    if (!this.auth.checkValidAccess(permissions, expectedRole)) {
      this.router.navigate(['home']);
      return false;
    }
    // Return false instead
    return true;
  }

}
