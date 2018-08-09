# Cómo configurar el proyecto

1. Entrar en la carpeta ``bat-files`` y modificar la ruta del proyecto en los archivos ``angular.bat``, ``django.bat`` y ``jupyter.bat`` a la usada en su caso particular.

2. En la línea de comandos, ingresar en la ruta ``docker/requirements`` y ejecutar el comando ``pip install -r test.txt`` para instalar las dependencias para los ambientes de desarrollo

3. Modificar la clave de usuario de Jupyter:
    * Ejecutar el archivo ``jupyter.bat``
    * Ingresar con la clave genérica ``abc123++``, acceder al cuaderno ``ProjectSettings.ipynb`` y ejecutar la primera celda e ingresar su nueva contraseña. Anote el código SHA obtenido para un paso posterior
    * Ingresar a la ruta ``docker/jupyter_notebook_config.py``
    * Copiar el token SHA obtenido en pasos previos y asignarlo en la variable ``c.NotebookApp.password``
    * Guardar el archivo ``jupyter_notebook_config.py`` en la ruta ``C:\Users\<su_numero_carnet>\.jupyter``. De no existir la carpeta ``.jupyter``, crearla.

4. Configurar el archivo ``base.yml``:
    * Cambiar "app" por el nombre del proyecto (ej: fallas_criticas)
    * Configurar proxy en build/args/http_proxy y https_proxy

5. Configurar el archivo ``test.yml``:
    * Cambiar "app" e "identidad" por el nombre del proyecto (ej: fallas_criticas)

6. Configurar el archivo ``.env``:
    * Configurar la IP del servidor ``APP_HOSTNAME`` y las bases de datos y las variables para uso del proxy ``http_proxy``, ``https_proxy``

7. Entrar en el archivo ``frontend/src/index.html`` y cambiar el título al nombre de su proyecto.