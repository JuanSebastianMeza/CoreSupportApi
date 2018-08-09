# Arquitectura

1. **backEnd:** En la carpeta ``backend`` se encuentran las siguientes carpetas:
    * ``api``: proyecto Django que servirá de API
    * ``notebooks``: cuadernos de Jupyter

2. **bat-files:** contiene archivos ejecutables ``.bat`` para levantar el entorno de desarrollo local con mayor facilidad
    * ``all.bat``: ejecuta las tres aplicaciones ``angular.bat``, ``django.bat`` y ``jupyter.bat``
    * ``angular-jupyter.bat``: ejecuta ``angular.bat`` y ``jupyter.bat``
    * ``angular.bat``: ejecuta el comando ``ng serve`` para la aplicación Angular
    * ``django.bat``: ejecuta el comando ``python manage.py runserver`` para la aplicación Django
    * ``jupyter.bat``: ejecuta el comando ``python ../api/manage.py shell_plus --notebook`` para ejecutar Jupyter localmente, asociado a la app de Django

3. **dist:** es una carpeta creada únicamente para copiar el resultado de ejecutar el comando ``ng build --prod`` a la aplicación de Angular

4. **docker:** archivos de configuración de Docker para despliegue en ambientes de prueba, calidad y producción

5. **documentacion:** contiene la documentación sobre la aplicación: Especificaciones funcionales; Instalación y Configuración; Operación y Mantenimiento

6. **frontEnd:** En la ruta ``frontend/src/app`` se encuentran todos los componentes, servicios e interfaces de la aplicación Angular. Las funciones de cada carpeta son las siguientes:
    * ``interfaces``: interfaces del proyecto.
    * ``private-views``: componentes cuyas vistas requieren autenticación para ser visualizadas.
    * ``public-views``: componentes cuyas vistas no requieren autenticación para ser visualizadas.
    * ``services``: servicios del proyecto.
