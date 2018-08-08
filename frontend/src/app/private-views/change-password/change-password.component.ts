import { Component, OnInit, Inject } from '@angular/core';
import { Router } from '@angular/router';
import { FormBuilder,
         FormGroup,
         Validators,
         FormControl,
         ValidatorFn } from '@angular/forms';

// Own services imports
import { HttpRequestsService } from '../../services/utils/http-requests.service';
import { UtilsService } from '../../services/utils/utils.service';
import { ConstService } from '../../services/utils/const.service';
import { AuthService } from '../../services/auth/auth.service';

// Import global class
import { Globals } from '../../globals';

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
    // Inject services
    private http: HttpRequestsService,
    private utils: UtilsService,
    private constants: ConstService,
    private auth: AuthService,
    // Inject router
    public router: Router,
    // Inject FormBuilder
    private fb: FormBuilder,
    // Inject global class
    private globals: Globals,
  ) { }

  ngOnInit() {
    // Build Form
    this.buildForm();
    // Get constants
    this.constant = this.constants.getChangePasswordViewConstants();
    // Post login view was rendered
    this.http.postAppAuditInfo(
      this.globals.appPasswordId,
      this.auth.getUserId()
    );
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
        if (data[this.constant.validPassword]) {
          this.utils.openSnackBar(this.constant.passError, null);
        } else {
          this.utils.openSnackBar(this.constant.passLast, null);
        }
        // Reset form fields
        this.changePasswordForm.get(this.constant.passOld).setValue(null);
        this.changePasswordForm.get(this.constant.passNew).setValue(null);
        this.changePasswordForm.get(this.constant.passRep).setValue(null);
      }
    });
  }

  // This method builds the form
  buildForm(): void {
    // Build group
    this.changePasswordForm = this.fb.group({
      // checks password validation
      oldPassword: [null, Validators.compose([Validators.required])],
      newPassword: [null, Validators.compose([
        Validators.required,
        Validators.minLength(8),
        this.specialCharacterValidator(),
        this.digitValidator(),
        this.letterValidator(),
      ])],
      repeatNewPassword: [null, Validators.compose([
        Validators.required,
        this.repeatNewPasswordValidator()
      ])],
    });
  }

  // This validator function checks if the new password is repeated correctly
  repeatNewPasswordValidator(): ValidatorFn {
    return (control: FormControl): {[key: string]: any} => {
      // If controls is null, return null
      if (!control.root['controls']) {
        return null;
      }
      // Check if passwords match
      return (control.root['controls'].newPassword.value !== control.value) ? {'repeatNewPassword': {value: control.value}} : null;
    };
  }

  // This validator function checks if expression has at least one special character
  specialCharacterValidator(): ValidatorFn {
    return (control: FormControl): {[key: string]: any} => {
      const regex = /[\@\.\+\-\_]/;
      const special = regex.test(control.value);
      return !special ? {'specialCharacter': {value: control.value}} : null;
    };
  }

  // This validator function checks if expression has at least one digit
  digitValidator(): ValidatorFn {
    return (control: FormControl): {[key: string]: any} => {
      const regex = /\d/;
      const special = regex.test(control.value);
      return !special ? {'digit': {value: control.value}} : null;
    };
  }

  // This validator function checks if expression has at least one letter
  letterValidator(): ValidatorFn {
    return (control: FormControl): {[key: string]: any} => {
      const regex = /[a-zA-Z]/;
      const special = regex.test(control.value);
      return !special ? {'letter': {value: control.value}} : null;
    };
  }

}
