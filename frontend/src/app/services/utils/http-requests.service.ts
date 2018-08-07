import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

// Own services imports
import { ConstService } from './const.service';
import { AuthService } from '../auth/auth.service';


@Injectable({
  providedIn: 'root'
})
export class HttpRequestsService {

  // Constants
  apiUrl: any = this.constService.getApiUrls();
  constant: any = this.constService.getHttpRequestServiceConstants();


  constructor(
    // Inject HttpClient
    private http: HttpClient,
    // Inject constants
    private constService: ConstService,
    // Inject Auth service
    private auth: AuthService) { }

  // Get JWT Token
  getJWTToken(credentials) {
    return this.http.post(this.apiUrl.obtainJwtToken, credentials);
  }

  // Http request to change password
  changePassword(password) {
    // Create url: base + user id + end url
    const changePasswordUrl: string = this.apiUrl.userUrl + this.auth.getUserId() + this.constant.changePasswordUrl;
    // Return http response
    return this.http.post(changePasswordUrl, password);
  }

  /*
   * Post data into Access Audit table
   * @param loginOrLogout: if it was a login (true) or logout (false)
   * @param successAccess: if access was successful (true for success)
   * @param appId: app id
   * @param userId: user id
   * @param accessType: access type, true for granted, false for denied
  */
  postAccessAuditInfo(loginOrLogout: boolean, appId: number, userId: number|string, accessType: boolean): void {
    if (accessType) {
      this.http.post(
        this.apiUrl.grantedAccessAuditUrl,
        {
          login_or_logout: loginOrLogout,
          app: appId,
          user: userId,
        }
      ).subscribe(() => null);
    } else {
      this.http.post(
        this.apiUrl.deniedAccessAuditUrl,
        {
          app: appId,
          user: userId,
        }
      ).subscribe(() => null);
    }
  }

  /*
   * Post data into App Audit table
   * @param appModuleId: app id
   * @param userId: user id
  */
  postAppAuditInfo(appModuleId: number, userId: number) {
    this.http.post(
      this.apiUrl.appAuditUrl,
      {
        app_module: appModuleId,
        user: userId,
      }
    ).subscribe(() => null);
  }

}
