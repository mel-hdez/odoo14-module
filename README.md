Contenedor de Odoo y Posgres para desarrolladores

Como esta estructurado este repositorio:

1- Directorio addons donde guardaras tus módulos personalizados, incluso si usas enterprise debes colocarlo dentro de este directorio.

2- Directorio /conf que contiene odoo.conf
   Basicamente lo unico que deberías modificar es la ruta donde están tus modulo propios, por defecto ya apunta a extra-addons, falta agregar si tienes otros dentro de sub-directorios o incluso si usas enterprise debes indicarlo acá.

3- docker-compose.yml
   Contiene la configuración de los container, puertos, y usuarios y claves, por lo regular acá solo deberías modificar tu version de Odoo, como ejemplo esta la version 14.0

4-  Ante todo actualizar el sistema operativo dentro de contenedor para que te pueda dejar instalar paquetes.

# Entrar al contenedor
docker exec -u 0 -it mi_contenedor_mel bash

# Ya dentro del contenedor actualizar
apt update
apt install git

# exit para salir del contenedor

# Para instalar paquetes python dentro del contenedor Odoo no es necesario entrar en el, desde afuera ejecutar
# para actualizar a la ultima version de pip
docker exec -u odoo mi_contenedor_mel pip3 install --upgrade pip

5- Como se usa (debes estar dentro de la ruta donde esta tu .yml) y ejecutar desde consola:

- docker-compose up

- Para entrar al contenedor donde esta el sistema operativo (El nombre del contenedor esta en el docker-compose.xml)
  $ docker exec -u 0 -it mi_contenedor_mel bash

- Si quieres copiar desde tu PC hacia dentro del contenedor:
  docker cp filestore/. mi_contenedor_mel:/var/lib/odoo/filestore/backup

- Tener en tu odoo docker una copia exacta de tu Odoo de producción (debes tener el dump.sql y el directorio filestore en tu PC).
  $ docker exec -u 0 -it mi_contenedor_mel bash
  $ mkdir -p /var/lib/odoo/filestore/backup
  $ chown odoo:odoo -R /var/lib/odoo/filestore

  $ docker cp filestore/. mi_contenedor_mel:/var/lib/odoo/filestore/backup
  $ docker cp dump.sql postgres10:/root

  $ docker exec -it postgres10 psql -U odoo -a template1 -c 'CREATE DATABASE backup;'
  $ docker exec -it postgres10 psql -U odoo -a template1 -c 'GRANT ALL PRIVILEGES ON DATABASE backup TO odoo;'
  $ docker exec -it postgres10 psql -U odoo -a backup -f /root/dump.sql





