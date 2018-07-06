import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class ConstService {

  // Properties
  // apiUrl: string = 'http://dev1.tmve.local/';
  apiUrl: string = 'http://localhost:8000/';
  
  constructor() { }
  
  // Get API urls
  getApiUrls() {
    return {
      obtainJwtToken: this.apiUrl + 'get-auth-token/',
      userUrl: this.apiUrl + 'api/users/',
    }
  }

  // Change password view constants
  getAppComponentViewConstants() {
    return {
      welcome: '¡Bienvenidos!',
      appTitle: 'Título de la aplicación',
      saUrl: 'http://solucionesagiles.tmve.local/',
      // SA footer
      saName: 'Soluciones Ágiles. ',
      saManager: 'Gerencia de Soporte de Servicios a la Red',
      saMail: ' soluciones.agiles.ve@telefonica.com',
      web: ' Web: ',
      saBaseUrl: 'solucionesagiles.tmve.local',
      lastLogin: 'Último ingreso a la página',
      // SideBar
      home: 'home',
      homeTitle: 'Inicio',
      tutorial: 'Tutorial',
      menu: 'Menú',
      // Button options
      changePassword: 'Cambiar contraseña',
      logOut: 'Cerrar sesión',
      // Routing
      password: 'password',
      // Success msg
      successMsg: 'Sesión cerrada exitosamente',
    }
  }

  // Change password view constants
  getChangePasswordViewConstants() {
    return {
      title: 'Ingrese su nueva contraseña',
      status: 'status',
      controls: 'controls',
      // Input place holders
      phPassOld: 'Contraseña actual',
      phPassNew: 'Nueva contraseña',
      phPassRep: 'Repetir nueva contraseña',
      // Input keys
      passOld: 'oldPassword',
      passNew: 'newPassword',
      passRep: 'repeatNewPassword',
      // Submit messages
      passSuccess: 'La contraseña fue cambiada exitosamente. Ingrese nuevamente',
      passError: 'La contraseña actual es incorrecta',
      passSubmit: 'Cambiar contraseña',
      // Error messages
      passOldError: 'Contraseña actual requerida',
      passNewError: 'Nueva contraseña requerida',
      passRepError1: 'Repetir nueva contraseña',
      passRepError2: 'No coincide con el valor anterior',
    }
  }

  // Login view constants
  getLoginViewConstants() {
    return {
      title: 'Credenciales',
      login: 'Ingrese',
      // Input placeholders
      phUsername: 'Nombre de usuario',
      phPassword: 'Contraseña',
      // Input keys
      username: 'username',
      password: 'password',
      token: 'token',
      home: 'home',
      // Error messages
      loginError: 'El usuario y la contraseña no son válidos',
      userError1: 'Nombre de usuario requerido',
      userError2: 'Nombre de usuario no válido',
      userError3: 'Ej: E12345 o P12345',
      passError: 'Contraseña requerida',
      // SnackBar Color
      snackbarColor: 'purple-bg',
      duration: 3000,
    }
  }

  // Http requests service constants
  getHttpRequestServiceConstants() {
    return {
      changePasswordUrl: '/change-password/',
    }
  }

  // Utils service constants
  getUtilsServiceConstants() {
    return {
      // Routing
      loginUrl: 'login',
      // SnackBar Color
      snackbarColor: 'purple-bg',
      duration: 3000,
    }
  }
  
}
