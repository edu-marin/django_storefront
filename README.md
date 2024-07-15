
# Configuración de la Base de Datos MySQL con Docker

Este documento proporciona instrucciones sobre cómo levantar una base de datos MySQL utilizando `docker-compose` y cómo conectarse a ella desde un cliente local.

## Requisitos

- Docker
- Docker Compose

## Pasos para Levantar la Base de Datos

1. **Clonar el repositorio o crear los archivos necesarios**:
    Asegúrate de tener un archivo `docker-compose.yml` con la siguiente configuración:

    ```yaml
    version: '3.8'

    services:
      mysql:
        image: mysql:9.0.0
        container_name: mysql_voga_container
        restart: always
        environment:
          MYSQL_ROOT_PASSWORD: root_password
          MYSQL_DATABASE: voga_db
          MYSQL_USER: django_user
          MYSQL_PASSWORD: django_password
        ports:
          - "3306:3306"
        volumes:
          - mysql_data:/var/lib/mysql

    volumes:
      mysql_data:
    ```

2. **Levantar el contenedor**:
    Navega hasta el directorio donde se encuentra tu archivo `docker-compose.yml` y ejecuta el siguiente comando para levantar el contenedor:

    ```sh
    docker-compose up -d
    ```

    Este comando descargará la imagen de MySQL (si no la tienes ya), creará y levantará un contenedor con la configuración especificada.

3. **Verificar que el contenedor está corriendo**:
    Puedes verificar que el contenedor de MySQL está corriendo con el siguiente comando:

    ```sh
    docker ps
    ```

    Deberías ver algo similar a esto en la salida:

    ```plaintext
    CONTAINER ID   IMAGE          COMMAND                  CREATED          STATUS          PORTS                               NAMES
    abc123def456   mysql:9.0.0    "docker-entrypoint.s…"   X seconds ago    Up X seconds    0.0.0.0:3306->3306/tcp, 33060/tcp   mysql_voga_container
    ```
4. **Verifica la configuración de MySQL**: Se puede acceder a la base de datos levantada en el contenedor con el comando
    ```sh
    docker exec -it mysql_voga_container mysql -u django_user -p
    ```
    Se pedirá ingresar el password del usuario. 
    
## Conexión desde un Cliente Local

Para conectarte a la base de datos MySQL desde un cliente local, utiliza las siguientes credenciales:

- **Host**: `127.0.0.1`
- **Puerto**: `3306`
- **Usuario**: `django_user`
- **Contraseña**: `django_password`
- **Base de Datos**: `voga_db`

### Ejemplo de Conexión

Puedes usar cualquier cliente de base de datos como MySQL Workbench, DBeaver, o incluso la línea de comandos de MySQL. Aquí hay un ejemplo de cómo conectarse usando la línea de comandos de MySQL:

```sh
mysql -h 127.0.0.1 -P 3306 -u django_user -p
```

Cuando se te solicite, introduce `django_password` como contraseña.

### Notas Adicionales

- Asegúrate de que no haya ningún firewall o regla de red que esté bloqueando el puerto 3306 en tu máquina host.
- Si necesitas cambiar la configuración de la base de datos, actualiza el archivo `docker-compose.yml` y reinicia el contenedor con los siguientes comandos:

    ```sh
    docker-compose down
    docker-compose up -d
    ```

¡Ahora deberías poder conectarte y utilizar tu base de datos MySQL!

