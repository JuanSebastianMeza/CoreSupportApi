import { Component, OnInit, Inject } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

// Own services imports
import { AuthService } from '../../services/auth/auth.service';
import { HttpRequestsService } from '../../services/utils/http-requests.service';
import { ConstService } from '../../services/utils/const.service';
import { UtilsService } from '../../services/utils/utils.service';

// Import global class
import { Globals } from '../../globals';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  // Constants
  loginForm: FormGroup;
  token: string;
  constant: any;
  accessAudit: any;
  userCheck: boolean =true;
  loginCharging: boolean;
  constructor(
    // Inject localStorage factory
    @Inject('LocalStorage') public localStorage: any,
    // Inject router
    public router: Router,
    // Inject global class
    private globals: Globals,
    // Inject FormBuilder
    private fb: FormBuilder,
    // Inject services
    private http: HttpRequestsService,
    private auth: AuthService,
    private constants: ConstService,
    private utils: UtilsService) { }

  ngOnInit() {
    this.loginCharging = false;
    // Build Form
    this.buildForm();
    // Get login constants
    this.constant = this.constants.getLoginViewConstants();
    // Post login view was rendered
    if (this.constants.ambiente){
      this.http.postAppAuditInfo(
        this.globals.appLoginId,
        this.globals.isAuthenticated ? this.auth.getUserId() : this.constants.dummyUserId
      );
    }
    // Initiate access audit constant
    this.accessAudit = {
      loginAccess: true,
      accessGranted: true,
      accessDenied: false,
    };
  }

  // Method for log in
  logIn(): void {
    // Get token from server
    this.loginCharging = true;
    this.http.getJWTToken({
      username: this.loginForm.get(this.constant.username).value,
      password: this.loginForm.get(this.constant.password).value,
    }).subscribe(
      data => {
        this.loginCharging = false;
        // Save token into credentials
        // this.token = data[this.constant.token];
        this.token = JSON.stringify(data);               // En Data se encuentra "access" que es el token
        // Save token in localStorage
        this.localStorage.setItem(this.constant.token, this.token);
        // Change globals state
        if (this.auth.getLastPassChangeDiff() > this.constants.getUtilsServiceConstants().blockNotification) {
          this.globals.showPasswordNotification = true;
        }
        // Set globals
        this.globals.remainingDaysToPasswordChange = this.auth.getLastPassChangeDiff();
        this.globals.isAuthenticated = true;
        this.globals.userName = this.auth.getUserName();
        // Notify successful access
        this.http.postAccessAuditInfo(
          this.accessAudit.loginAccess,
          this.globals.appId,
          this.auth.getUserId(),
          this.accessAudit.accessGranted
        );
        // Show advisor snackbar
        this.utils.openAdvisorSnackBar();
        // Get to the cms main view
        this.router.navigate([this.constant.home]);
      },
      error => {
        this.loginCharging = false;
        // Open snackbar
        console.log(error.error)
        let mensaje = 'Error desconocido al autenticar, contactar equipo de Herramientas Operativas(herramientasop.ve@telefonica.com)'
        if (error.error.failed_attempts_msg){
          mensaje = error.error.failed_attempts_msg;
        }
        this.utils.openSnackBar(mensaje, null);
        // Delete password value
        this.loginForm.get(this.constant.password).setValue(null);
        // Notify access denied
        this.http.postAccessAuditInfo(
          this.accessAudit.loginAccess,
          this.globals.appId,
          this.loginForm.get(this.constant.username).value,
          this.accessAudit.accessDenied
        );
      },
    );
  }

  // This method builds the form
  buildForm(): void {
    // Build group
    this.loginForm = this.fb.group({
      // username must have the form "E12345"
      username: ['', Validators.compose([
        Validators.required,
        Validators.pattern(/^[cCdDeEpP]{1}[0-9]{5}$/)
      ])],
      password: ['', Validators.compose([Validators.required])],
    });
  }
}
