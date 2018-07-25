# Plantilla Web Soluciones Ágiles

### **TABLA DE CONTENIDOS**
1. Funcionalidades incluidas
2. Estado del código
3. Cómo instalar las dependencias necesarias
4. Cómo configurar el proyecto
5. Cómo probar las configuraciones
6. Cómo usar

### 1. Funcionalidades incluidas
* Paleta de colores de SA
* Sistema de autenticación: 
    * Solicitud de credenciales
    * Inicio y cierre de sesión
* Servicio de verificación de permisología del usuario
* Cambio de contraseña del usuario
* Barra lateral desplegable de opciones
* Validaciones mínimas requeridas por Seguridad Telemática (ver documentación correspondiente)

### 2. Estado del código
* Version: 1.0
* Cubre requerimientos mínimos de autenticación
* En implementación de validaciones mínimas de Seguridad Telemática

### 3. Cómo instalar las dependencias necesarias
1. Ubicarse en la carpeta donde se guardará el código.
2. Usando la herramienta de control de versiones de su preferencia, descargar el código de bitbucket ``git clone https://bitbucket.org/solucionesagiles/plantilla-web.git``
3. Entrar en la carpeta frontend y correr el comando ``yarn install`` para instalar las dependencias de Angular 6+

### 4. Cómo configurar el proyecto
1. Entrar en la carpeta ``bat-files`` y modificar la ruta del proyecto en los archivos ``angular.bat``, ``django.bat`` y ``jupyter.bat`` a la usada en su caso particular.
2. Modificar la clave de usuario de Jupyter:
    * Ejecutar el archivo ``jupyter.bat``
    * Ingresar con la clave genérica ``abc123++``, acceder al cuaderno ``ProjectSettings.ipynb`` y ejecutar la primera celda e ingresar su nueva contraseña. Anote el código SHA obtenido para un paso posterior
    * Ingresar a la ruta ``docker/jupyter_notebook_config.py`` 
    * Copiar el token SHA obtenido en pasos previos y asignarlo en la variable ``c.NotebookApp.password``
    * Guardar el archivo ``jupyter_notebook_config.py`` en la ruta ``C:\Users\<su_numero_carnet>\.jupyter``. De no existir la carpeta ``.jupyter``, crearla.
3. Configurar el archivo ```base.yml``:
    * Cambiar "app" por el nombre del proyecto (ej: fallas_criticas)
    * Configurar proxy en build/args/http_proxy y https_proxy
4. Configurar el archivo ```test.yml``:
    * Cambiar "app" e "identidad" por el nombre del proyecto (ej: fallas_criticas)
    * Configurar los puertos. NOTA: en app_backend el segundo puerto establecido en ``ports`` debe coincidir con el colocado en ```command``
5. Configurar el archivo ```.env``:
    * Configurar las direcciones de ``APP_HOSTNAME``, ``http_proxy``, ``https_proxy`` y las bases de datos.
6. Entrar en el archivo ```frontend/src/index.html`` y cambiar el título al nombre de su proyecto.

### 5. Cómo probar las configuraciones


### 6. Cómo usar

