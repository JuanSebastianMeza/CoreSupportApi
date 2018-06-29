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
    let token = localStorage.getItem('token');
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
    let token = this.getTokenFromLocalStorage();
    // Decode token
    return this.decodeToken(token);
  }

  // Get user permissions
  public getUserPermissions(): string[] {
    // Get payload
    let payload = this.getPayload();
    // Save permissions
    let permissions: string[];
    if (payload) {
      permissions = payload.user.permissions;
      // Add staff permission
      payload.user.is_staff ? permissions.push('is_staff') : null;
      // Add superuser permission
      payload.user.is_superuser ? permissions.push('is_superuser') : null;
      // Return permissions
    } else {
      permissions = [];
    }
    return permissions;
  }

  // Get staff permissions
  public getStaffPermission(): boolean {
    // Get payload
    let payload = this.getPayload();
    // Return permissions
    return payload.user.is_staff;
  }

  // Get staff permissions
  public getSuperUserPermission(): boolean {
    // Get payload
    let payload = this.getPayload();
    // Return permissions
    return payload.user.is_superuser;
  }

  // Gets user's full name
  public getUserName(): string {
    // Get payload
    let payload = this.getPayload();
    // Return permissions
    return payload.user.full_name;
  }

  // Returns user's id
  public getUserId(): string {
    // Get payload
    let payload = this.getPayload();
    // Return permissions
    return payload.user_id;
  }

  // Check if user can access command
  public checkValidAccess(permissions, permissionToValidate): boolean {
    // Loop over each permission
    for (var perm of permissions){
      // If there is matching, 
      if (perm == permissionToValidate){
        return true;
      }
    }
    return false;
  };
  
}
