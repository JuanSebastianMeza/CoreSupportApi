import { Injectable } from '@angular/core';
import { HttpRequest,
         HttpHandler,
         HttpEvent,
         HttpInterceptor } from '@angular/common/http';
import { Observable } from 'rxjs';

// Inject own services
import { AuthService } from './auth.service';


@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(
    // Inject auth service
    private auth: AuthService) {}

  // Override intercept method
  intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {    
    // Get token
    const token = this.auth.getTokenFromLocalStorage();
    // If there is a token, clone request, else continue the flow
    if (token) {
      // We cannot modify the original request so we need to clone it
      const cloned = request.clone({
        // This is a configuration argument
        // With this, we take old header and add authorization to it
        headers: request.headers.set("Authorization", "JWT " + token)
      });
      // Return the cloned request to the browser
      return next.handle(cloned);
    } else {
      // Make HttpHandler handle the request and pass it to the browser
      return next.handle(request);
    }
  }

}