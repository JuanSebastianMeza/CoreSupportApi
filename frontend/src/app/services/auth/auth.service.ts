import { Injectable } from '@angular/core';

// JWT imports
import { JwtHelperService } from '@auth0/angular-jwt';

// Import own services
import { ConstService } from '../utils/const.service';

// Create jwt helper service
const jwtHelper = new JwtHelperService();

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  // Constants
  // allPermissions: any = this.constService.getAllPermissions();

  constructor(private constService: ConstService) { }

  // Gets token from local storage
  public getTokenFromLocalStorage(): string {
    // Get credentials
    const token = localStorage.getItem('token');
    // Return null if there is no token
    return token ? token : null;
  }

  // Check if token is not expired
  public isAuthenticated(): boolean {
    // Get token
    const token = this.getTokenFromLocalStorage();
    // Check and return if token is expired
    return !jwtHelper.isTokenExpired(token);
  }

  // Decode token
  public decodeToken(token): any {
    return jwtHelper.decodeToken(token);
  }

  // Get payload
  public getPayload() {
    // Get token
    const token = this.getTokenFromLocalStorage();
    // Decode token
    return this.decodeToken(token);
  }

  // Get user permissions
  public getUserPermissions(): string[] {
    // Get payload
    const payload = this.getPayload();
    // Save permissions
    let permissions: string[];
    if (payload) {
      permissions = payload.user.permissions;
      // Add staff permission
      if (payload.user.is_staff) {
        permissions.push('is_staff');
      }
      // Add superuser permission
      if (payload.user.is_superuser) {
        permissions.push('is_superuser');
      }
      // Return permissions
    } else {
      permissions = [];
    }
    return permissions;
  }

  // Get staff permissions
  public getStaffPermission(): boolean {
    // Get payload
    const payload = this.getPayload();
    // Return permissions
    return payload.user.is_staff;
  }

  // Get last login date
  public getLastLoginDate(): Date {
    // Get payload
    const payload = this.getPayload();
    // Return last login date
    return payload ? new Date(payload.user.last_login) : null;
  }

  // Get staff permissions
  public getSuperUserPermission(): boolean {
    // Get payload
    const payload = this.getPayload();
    // Return permissions
    return payload.user.is_superuser;
  }

  // Gets user's full name
  public getUserName(): string {
    // Get payload
    const payload = this.getPayload();
    // Return permissions
    return payload.user.full_name;
  }

  // Returns user's id
  public getUserId(): string {
    // Get payload
    const payload = this.getPayload();
    // Return permissions
    return payload.user_id;
  }

  // Check if user can access command
  public checkValidAccess(permissions, permissionToValidate): boolean {
    // Loop over each permission
    for (const perm of permissions) {
      // If there is matching,
      if (perm === permissionToValidate) {
        return true;
      }
    }
    return false;
  }

  // Returns if it is user first time for login
  public isUserFirstTime(): boolean {
    // Get payload
    const payload = this.getPayload();
    // Return permissions
    return payload.user.profile.is_first_time;
  }

  // Returns if it is user first time for login
  public getLastPassChangeDiff(): number {
    // Get payload
    const payload = this.getPayload();
    console.log(payload.user.profile.last_password_change);
    // Return permissions
    return payload.user.profile.last_password_change;
  }

}
