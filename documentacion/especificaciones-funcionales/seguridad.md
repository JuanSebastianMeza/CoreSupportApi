# Seguridad

* Arquitectura diseñada para cuatro (4) ambientes: desarrollo, prueba, calidad y producción.
* Despliegue de aplicaciones (frontend, backend, bases de datos) en contenedores separados.
* Histórico de contreseñas se guarda de forma cifrada
* Eliminación de datos temporales al finalizar la sesión
* Obligación en el cumplimiento de la política de contraseñas (validaciones):
  * Sobre la estructura de las contraseñas:
    * Las contraseñas tendrán un mínimo de 8 caracteres.
    * Deben ser complejas: al menos un carácter especial, una letra y un número.
  * Sobre el proceso de control de seguridad de cambio de contraseña:
    * Forzar al usuario a cambiar la contraseña inicial en el primer acceso o uso de la misma
    * Forzar al usuario a cambiar la contraseña una vez reiniciada por el área encargada de tal actividad.
    * Las contraseñas no se visualizarán en pantalla durante la introducción de las mismas.
    * Se pedirá la contraseña antigua antes de continuar con el mecanismo de cambio de contraseña.
    * Se pedirá confirmación de la nueva contraseña antes de proceder al cambio (para evitar posibles errores de escritura).
    * No se permitirá la reutilización de al menos las 10 últimas contraseñas que el usuario haya utilizado.
    * El sistema validará la correcta longitud y sintaxis de la nueva contraseña antes de proceder al cambio.
    * La contraseña tendrá una vigencia de 30 días, al término de los cuales el sistema forzará al usuario a cambiar la misma, previo 5 días de sugerirle cambiar voluntariamente la contraseña antes de cumplirse el día 30.
* Registros de eventos para auditoría:
  * Para accesos concedidos:
    * Fecha y hora
    * Ingreso o cierre de sesión
    * Aplicación que genera el registro
    * Usuario que genera el evento
  * Para accesos denegados:
    * Fecha y hora
    * Aplicación que genera el registro
    * Nombre de Usuario que intentó el acceso
  * Para información general de uso del aplicativo:
    * Fecha y hora
    * Módulo de la aplicación al que se accede
    * Usuario que genera el evento
* Uso del método POST como método para enviar datos al servidor
* Políticas de control de acceso:
  * El número de intentos fallidos para bloquear las cuentas es de 3 (tres).
  * Mostrar histórico de autenticación:
    * La fecha y hora del anterior acceso satisfactorio
    * El número de autenticaciones fallidas realizadas
* Desplegar banner inmediatamente después del proceso de autenticación satisfactorio con el siguiente mensaje:

``Ha accedido a un sistema propiedad de Telefónica Venezolana, C.A. Necesita tener autorización antes de usarlo, estando usted estrictamente limitado al uso indicado en dicha autorización. El acceso no autorizado a este sistema o el uso indebido del mismo está prohibido y es contrario a la Política Corporativa de Seguridad y a la legislación vigente. El uso que realice de este sistema puede ser monitorizado.``

* Uso del algoritmo RSA (encriptación) en procesos de transmisión de token de validación de usuarios.