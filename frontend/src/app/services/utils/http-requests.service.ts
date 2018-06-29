import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

// Own services imports
import { ConstService } from './const.service';
import { AuthService } from '../auth/auth.service';

// Own interfaces imports
import { Password } from '../../interfaces/auth.interfaces';


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
    let changePasswordUrl: string = this.apiUrl.userUrl + this.auth.getUserId() + this.constant.changePasswordUrl;
    // Return http response
    return this.http.post(changePasswordUrl, password);
  }

}
