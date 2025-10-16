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
    const token = localStorage.getItem('token');            // En token viene un objeto con data
    if (!token) {
      return null;
    }
    const real_token = JSON.parse(token);
    return real_token.access ? real_token.access : null;    // Envío el "token" de acceso
 
  }
 
  // Check if token is not expired
  public isAuthenticated(): boolean {
    // Get token
    const token = this.getTokenFromLocalStorage();
    console.log(token); // PRUEBA
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
 
  // Get payload from local storage (NUEVA)
  public getPayloadv2() {
    // Get Data
    const token = localStorage.getItem('token');            // En token viene un objeto con data
    if (!token) {
      return null;
    }
    const payloadData = JSON.parse(token);
    return payloadData ? payloadData : null;    // Envío el "token" de acceso
 
  }
 
  // Get user permissions
  public getUserPermissions(): string[] {
    // Get payload
    // const payload = this.getPayload();  // ORIGINAL
    const payload = this.getPayloadv2(); // NUEVO
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
    // console.log(permissions); // PRUEBA
    return permissions;
  }
 
  // Get staff permissions
  public getStaffPermission(): boolean {
    // Get payload
    // const payload = this.getPayload();  // ORIGINAL
    const payload = this.getPayloadv2(); // NUEVO
    // Return permissions
    return payload.user.is_staff;
  }
 
  // Get last login date
  public getLastLoginDate(): Date {
    // Get payload
    // const payload = this.getPayload();    // ORIGINAL
    const payload = this.getPayloadv2(); // NUEVO
    // Return last login date
    return payload ? new Date(payload.user.last_login) : new Date();
  }
 
  // Get staff permissions
  public getSuperUserPermission(): boolean {
    // Get payload
    // const payload = this.getPayload();  // ORIGINAL
    const payload = this.getPayloadv2(); // NUEVO
    // Return permissions
    return payload.user.is_superuser;
  }
 
  // Gets user's full name
  public getUserName(): string {
    // Get payload
    // const payload = this.getPayload();  // ORIGINAL
    const payload = this.getPayloadv2(); // NUEVO
    // Return permissions
    return payload.user.full_name;
  }
 
  // Returns user's id
  public getUserId(): number {
    // Get payload
    // const payload = this.getPayload();  // ORIGINAL
    const payload = this.getPayloadv2(); // NUEVO
    // Return permissions
    return Number(payload.user_id);
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
    // const payload = this.getPayload(); // ORIGINAL
    const payload = this.getPayloadv2(); // NUEVO
    // Return permissions
    return payload.user.profile.is_first_time;
  }
 
  // Returns how many days left to change user's password
  public getLastPassChangeDiff(): number {
    // Get payload
    // const payload = this.getPayload();  // ORIGINAL
    const payload = this.getPayloadv2(); // NUEVO
    // Return number of days if authenticated
    return payload ? payload.user.profile.last_password_change : null;
  }
 
}
