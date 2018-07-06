import { Injectable } from '@angular/core';

// Own services imports
import { AuthService } from './services/auth/auth.service';


@Injectable()
export class Globals {

  // Variables
  isAuthenticated: boolean = this.auth.isAuthenticated();
  userName: string = this.isAuthenticated ? this.auth.getUserName() : null;
  lastLoginDate: Date = this.auth.getLastLoginDate();

  constructor(
	// Inject auth service
  	private auth: AuthService) {}

}