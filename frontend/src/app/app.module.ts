import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

// Import ngModel
import { FormsModule, ReactiveFormsModule } from '@angular/forms';

// JWT imports
import { JwtModule } from '@auth0/angular-jwt';

// Routing module
import { AppRoutingModule } from './/app-routing.module';

// Component imports
import { AppComponent } from './app.component';
import { LoginComponent } from './public-views/login/login.component';
import { HomeComponent } from './private-views/home/home.component';
import { ChangePasswordComponent } from './private-views/change-password/change-password.component';

// Material imports
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatMenuModule } from '@angular/material/menu';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatSnackBarModule } from '@angular/material/snack-bar';

// Import fortawesome
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';

// Import global class
import { Globals } from './globals';

// Import own classes
import { AuthInterceptor } from './services/auth/auth.interceptor';


@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    HomeComponent,
    ChangePasswordComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    // Add routing
    AppRoutingModule,
    // Material imports
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatMenuModule,
    MatSidenavModule,
    MatSnackBarModule,
    // Import fontawesome
    FontAwesomeModule,
    // Jwt module config
    JwtModule.forRoot({
      config: {
        // Token getter function
        tokenGetter: getAuthToken,
        allowedDomains: ['localhost:8000'],
        authScheme: 'Bearer ',
      }
    }),
  ],
  exports: [
    // Material exports
    MatButtonModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatMenuModule,
    MatSidenavModule,
    MatSnackBarModule,
  ],
  providers: [
    // Provides global variables
    Globals,
    // Provide local storage as factory
    { provide: 'LocalStorage', useFactory: getLocalStorage },
    {
      // To what injection token do we want to associate our class
      provide: HTTP_INTERCEPTORS,
      // Class to use for interceptors
      useClass: AuthInterceptor,
      // This says that there can be multiple HTTP interceptors
      multi: true
    },
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }

// Return localStorage
export function getLocalStorage() {
    console.log('getLocalStorage called');
    return (typeof window !== 'undefined') ? window.localStorage : null;
}

// Get token
export function getAuthToken() {
    const token = localStorage.getItem('token');
    console.log('getAuthToken called, token:', token);

    if (!token) {
      return null;
    }
    const real_token = JSON.parse(token);
    console.log('getAuthToken called, real_token:', real_token);
    return real_token.access ? real_token.access : null;  // Enviado solo el token almacedado en el Objeto del LocalStorage
}
