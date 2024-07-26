#!/bin/sh

# Esperar hasta que Docker esté listo
until docker info > /dev/null 2>&1; do
  echo "Esperando a que Docker se inicie..."
  sleep 1
done

# Levantar los servicios con docker-compose
docker-compose up -d

# Esperar hasta que MySQL esté listo
until docker exec mysql_voga_container mysqladmin ping -h "localhost" --silent; do
  echo "Esperando a que MySQL se inicie..."
  sleep 1
done