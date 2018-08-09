# Cómo validar las configuraciones

1. Ejecutar el archivo ``bat-files/all.bat``

2. Verificar que se despliegue en el navegador lo siguiente:
    * Aplicación de Angular en ``localhost:4200``
    * Aplicación Django en ``localhost:8000``
    * Cuaderno Jupyter en ``localhost:8888``

3. Para montaje en el servidor, configurar en el archivo ``sftp-config.json`` (Sublime) o ``sftp.json`` (Visual Studio Code) los campos mostrados en la tabla a final de esta lista de pasos.

4. Crear en el servidor la carpeta correspondiente a la ruta especificada en el punto anterior. **NOTA:** no usar privilegios root

5. Verificar en el servidor los puertos disponibles (usar los puertos entre 8050 y 8080)usando el comando ``docker ps``.

6. En el servicio ``app_backend`` del archivo ``docker/test.yml`` cambiar los puertos respectivos por los seleccionados. **NOTA:** el segundo puerto establecido en ``ports`` debe coincidir con el colocado en ``command``

7. Subir el código al servidor

8. Ejecutar el comando ``docker-compose -f <nombre de la carpeta>/docker/test.yml up`` para levantar los contenedores de Docker con las aplicaciones.

9. Desde el navegador de su preferencia, colocar en la url ``<ip del servidor>:<puerto>`` para verificar que la aplicación está operativa

10. Registrar la nueva aplicación en el [Sistema Centralizado de información](http://sci.tmve.local/aplicaciones/).

11. En el achivo ``frontend/src/app/globals.ts``, colocar la información correspondiente a la aplicación en las variables ``appId``, ``appLoginId``, ``appHomeId`` y ``appPassword`` según muestra el registro del punto previo. **NOTA**: Es importante registrar en el SCI cada nuevo componente que se programe para que pueda ser tomado por el proceso de auditoría.

12. En el método ngOnInit de cada componente agregar las líneas de código mostradas abajo haciendo las sustituciones correspondientes.

## Para componentes públicos

```javascript
// Post login view was rendered
this.http.postAppAuditInfo(
  this.globals.<id_componente>, // Ej: this.globals.appLoginId,
  this.globals.isAuthenticated ? this.auth.getUserId() : this.constants.dummyUserId
);
```

## Para componentes privados

```javascript
// Post login view was rendered
this.http.postAppAuditInfo(
  this.globals.<id_componente>, // Ej: this.globals.appPasswordId
  this.auth.getUserId()
);
```

## Tabla configuración SFTP

Campo | Sublime | VS Code
----- | ----- | -----
Host | host | host
Usuario | user | username
Contraseña | password | password
Ruta destino | remote_path | remotePath