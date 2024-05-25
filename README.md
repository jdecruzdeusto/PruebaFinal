# Prueba Final

Este proyecto es el resultado de una colaboración entre Juan de Cruz e Imanol Anda. El objetivo principal de este repositorio es demostrar la integración y funcionamiento de las herramientas y tecnologías específicas que hemos estudiado.

## Colaboradores

- Juan de Cruz - Estudiante en Deusto
- Imanol Anda - Estudiante en Deusto

## Instalación

Proporcione instrucciones sobre cómo clonar y configurar el proyecto localmente. Esto puede incluir pasos para instalar dependencias, configurar entornos virtuales, etc.

```bash
git clone https://github.com/jdecruzdeusto/PruebaFinal.git
cd PruebaFinal
# Instalar dependencias
pip install -r requirements.txt
```

## Como ejecutar

Para ejecutar contenedores utilizando Docker Compose de manera correcta y efectiva, aquí tengo una guía paso a paso:

### 1. Ejecutar Docker Compose

Abrir una terminal en el directorio donde se encuentra el archivo `docker-compose.yml`. Ejecutar el siguiente comando para iniciar todos los servicios definidos en el archivo de manera desatendida (en modo "detached"):

```bash
sudo docker-compose up -d
```

### 2. Verificar el Estado de los Contenedores

Para asegurarse de que todos los contenedores están funcionando correctamente, utilizar el siguiente comando:

```bash
sudo docker-compose ps
```

### 3. Acceder a los Servicios

Una vez que los contenedores están en funcionamiento, podemos acceder a ellos mediante las direcciones IP y puertos configurados en el archivo `docker-compose.yml`. 

- FastApi: http://localhost:8000/docs
- Grafana: http://localhost:3000
- Influxdb: http://localhost:8088

### 4. Detener y Remover los Contenedores

Si es necesario detener los servicios, ejecutar:

```bash
sudo docker-compose down
```

## Configuración

### Grafana

#### Integración de InfluxDB como datasource

- **Cambiar el Lenguaje de Consulta a Flux:** Al configurar el datasource en Grafana, asegúrate de seleccionar Flux como el lenguaje de consulta.

- **Configurar el URL:** En el campo de URL, introduce la dirección IP donde se está ejecutando Grafana, seguido del puerto utilizado por InfluxDB.

```plaintext
http://influxdb:8088
```

- **Configuración de Autenticación Básica (Basic Auth):** Activa la opción de 'Basic Auth' para utilizar autenticación básica. Ingresa las credenciales predeterminadas de administrador para Grafana:

  - Usuario: admin
  - Contraseña: admin

- **Rellenar las Credenciales de InfluxDB:** Deberás proporcionar detalles específicos de tu instancia de InfluxDB:

  - Organización: deusto-org
  - Token: deusto2024-secret-token
  - Bucket: deusto-bucket

  Ir al menú de los dashboard e importar el dashboard de la carpeta del proyecto final.

### Influxdb

Después de ranear el `docker-compose up`, introducir el usuario y contraseña:

- Usuario: Deusto
- Contraseña: Deusto2024

Después de acceder a influx, ir a buckets y entrar en el bucket `deusto-bucket` donde se podrán comprobar todos los datos.

### FastApi

Para hacer el post primero introducir el usuario y contraseña que es el siguiente:

- Usuario: Admin
- Contraseña: Secret

## models.py

### AirQualityData

Esta clase es un modelo Pydantic que define la estructura para almacenar datos de calidad del aire. Los campos incluyen valores e indicadores de calidad del aire para CO, ozono, NO2 y PM2.5. Cuenta con validadores para asegurarse de que los valores sean no negativos.

### CityAirQuality

Otro modelo Pydantic que representa la calidad del aire en una ciudad específica en una fecha y hora determinadas. Incluye un objeto AirQualityData y atributos adicionales para el país y la ciudad.

## api.py

### Configuración de InfluxDB

Conexión con InfluxDB para almacenar y manejar los puntos de datos relacionados con la calidad del aire.

### Autenticación y Tokens

Uso de JWT (JSON Web Tokens) para manejar la autenticación y seguridad de la API. Implementa funciones para crear y validar tokens.

### Endpoints

- `/token`: Genera

 un token de acceso para autenticación.
- `/load_csv_data/`: Carga y procesa datos desde un archivo CSV, y luego los escribe en InfluxDB utilizando un ThreadPoolExecutor para realizar la escritura en paralelo.
- `/received_air_quality_data/`: Retorna los datos de calidad del aire que han sido recibidos y almacenados.

## entrypoint.sh

Este script shell configura y ejecuta comandos iniciales para InfluxDB, asegurando que todas las variables de entorno necesarias estén establecidas y maneja la configuración inicial del bucket de InfluxDB.

## Otros Archivos

- `docker-compose.yml` y `Dockerfile` se utilizan para definir y construir el entorno de Docker para el proyecto, especificando cómo se deben construir y ejecutar los servicios.
