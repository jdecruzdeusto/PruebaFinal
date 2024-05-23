#!/bin/bash

# Abre la primera terminal y ejecuta el comando de Docker para Grafana
gnome-terminal -- bash -c "sudo docker run -d -p 3000:3000 grafana/grafana; exec bash"

# Abre la segunda terminal y ejecuta el comando para iniciar el servidor con Uvicorn
gnome-terminal -- bash -c "uvicorn api:app --reload; exec bash"
