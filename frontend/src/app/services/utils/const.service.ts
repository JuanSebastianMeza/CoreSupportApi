import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
@Injectable({
  providedIn: 'root'
})
export class ConstService {

  // Properties
  apiUrl = environment.apiUrl;
  ambiente = environment.production;
  dummyUserId = 6;

  constructor() { }

  // Get API urls
  getApiUrls() {
    return {
      obtainJwtToken: this.apiUrl + 'get-auth-token/',
      userUrl: this.apiUrl + 'api/users/',
      grantedAccessAuditUrl: this.apiUrl + 'api/granted-access-audit/',
      deniedAccessAuditUrl: this.apiUrl + 'api/denied-access-audit/',
      appAuditUrl: this.apiUrl + 'api/app-audit/',
    };
  }

  // Change password view constants
  getAppComponentViewConstants() {
    return {
      welcome: '¡Bienvenidos!',
      appTitle: 'Título de la aplicación',
      saUrl: 'http://solucionesagiles.tmve.local/',
      // SA footer
      saName: 'Soluciones Ágiles. ',
      saManager: 'Gerencia de Soporte de Servicios de Red',
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
    };
  }

  // Change password view constants
  getChangePasswordViewConstants() {
    return {
      title: 'Ingrese su nueva contraseña',
      status: 'status',
      controls: 'controls',
      validPassword: 'valid_password',
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
      passLast: 'No se puede repertir ninguna de las últimas 10 contraseñas usadas',
      passSubmit: 'Cambiar contraseña',
      // Error messages
      passOldError: 'Contraseña actual requerida',
      passNewError: 'Nueva contraseña requerida',
      passRepError1: 'Repetir nueva contraseña',
      passRepError2: 'No coincide con el valor anterior',
      minLength: 'Debe contener mínimo 8 caracteres',
      specialCharacter: 'Debe contener un carácter especial (@/./+/-/_)',
      number: 'Debe contener un número',
      letter: 'Debe contener una letra',
    };
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
    };
  }

  // Http requests service constants
  getHttpRequestServiceConstants() {
    return {
      changePasswordUrl: '/change-password/',
    };
  }

  // Utils service constants
  getUtilsServiceConstants() {
    return {
      // Routing
      loginUrl: 'login',
      // Advisor snackbar
      hideSnackBar: 'Aceptar',
      advisorMessage: 'Ha accedido a un sistema propiedad \
        de Telefónica Venezolana, C.A. Necesita tener autorización \
        antes de usarlo, estando usted estrictamente limitado al uso \
        indicado en dicha autorización. El acceso no autorizado a este \
        sistema o el uso indebido del mismo está prohibido y es contrario \
        a la Política Corporativa de Seguridad y a la legislación vigente. \
        El uso que realice de este sistema puede ser monitorizado.',
      firstTimeLoginMessage: 'Para poder acceder al contenido de esta \
        aplicación, en necesario que cambie su contraseña.',
      passwordExpirationMessage: 'Su contraseña está vencida. Por favor, \
        ingrese una nueva.',
      passwordExpirationBanner1: 'Su contraseña se vencerá en ',
      passwordExpirationBanner2: '. Pulse ',
      passwordExpirationBanner3: 'aquí',
      passwordExpirationBanner4: ' para renovarla.',
      // SnackBar Color
      snackbarColor: 'purple-bg',
      advisorSnackbarColor: 'dark-blue-bg',
      guardSnackbarColor: 'purple-bg',
      duration: 3000,
      // Password change limits
      blockAccess: 30,
      blockNotification: 25,
    };
  }

}
