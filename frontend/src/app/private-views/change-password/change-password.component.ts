import { Component, OnInit, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { FormBuilder, 
         FormGroup, 
         Validators, 
         FormControl, 
         ValidatorFn } from '@angular/forms';

// Own services imports
import { AuthService } from '../../services/auth/auth.service';
import { HttpRequestsService } from '../../services/utils/http-requests.service';
import { UtilsService } from '../../services/utils/utils.service';
import { ConstService } from '../../services/utils/const.service';

// Own interfaces imports
import { Password } from '../../interfaces/auth.interfaces';


@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.css']
})
export class ChangePasswordComponent implements OnInit {

  // Constants
  password: Password;
  changePasswordForm: FormGroup;
  constant: any;

  constructor(
    // Inject localStorage factory
    @Inject('LocalStorage') public localStorage: any,
  	// Inject HttpClient
  	private http: HttpRequestsService,
  	// Import auth service
    private auth: AuthService,
	  // Inject router
  	public router: Router,
    // Inject FormBuilder
    private fb: FormBuilder,
    // Inject Utils
    private utils: UtilsService,
    // Inject constants
    private constants: ConstService) { }

  ngOnInit() {
    // Build Form
    this.buildForm();
    // Get constants
    this.constant = this.constants.getChangePasswordViewConstants();
  }

  // Change password on submit
  changePassword(): void {
    // Change password
    this.http.changePassword({
      oldPassword: this.changePasswordForm.get(this.constant.passOld).value, 
      newPassword: this.changePasswordForm.get(this.constant.passNew).value, 
      repeatNewPassword: this.changePasswordForm.get(this.constant.passRep).value, 
    }).subscribe(data => {
      // Evaluate if status is True
      if (data[this.constant.status]) {
        // Clear Storage
        this.utils.logOut(this.constant.passSuccess);
      } else {
        // Show password error
        this.utils.openSnackBar(this.constant.passError, null);
        // Reset form fields
        this.changePasswordForm.get(this.constant.passOld).setValue(null);
        this.changePasswordForm.get(this.constant.passNew).setValue(null);
        this.changePasswordForm.get(this.constant.passRep).setValue(null);
      }
    })
  }

  // This method builds the form
  buildForm(): void {
    // Build group
    this.changePasswordForm = this.fb.group({
      // checks password validation
      oldPassword: [null, Validators.compose([Validators.required])],
      newPassword: [null, Validators.compose([Validators.required])],
      repeatNewPassword: [null, Validators.compose([Validators.required, this.repeatNewPasswordValidator()])],
    });
  };

  // This validator function checks if the new password is repeated correctly
  repeatNewPasswordValidator(): ValidatorFn {
    return (control: FormControl): {[key: string]: any} => {
      // If controls is null, return null
      if (!control.root['controls']){
        return null;
      }
      // Check if passwords match
      return (control.root['controls'].newPassword.value !== control.value) ? {'repeatNewPassword': {value: control.value}} : null;
    };
  }

}
