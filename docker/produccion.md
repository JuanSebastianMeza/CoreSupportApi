# Contenedores Docker

El proyecto se levanta usando Docker en servidores Linux. La imagen se construye a partir del archivo Dockerfile. No modificar los archivos .yml para construirla desde allí porque creará una imagen para cada contenedor, lo que termina ocupando mucho espacio.

## Imagen

Para la construcción de la imagen, ejecutar este comando:
```
docker build coresupportapi/docker -f /home/satest/coresupportapi/docker/Dockerfile -t core_api
```

En caso de ejecutarse en el servidor RedHat, los cotenedores requieren tener permisos de escritura para que puedan ser usados dentro de los contenedores que usan volumenes:
```
chmod -R 777 coresupportapi/dist
```
## Librerías

Librerías para LDAP: libldap2-dev, libsasl2-dev, gcc