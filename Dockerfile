# Usa una imagen base de Python
FROM python:3.8-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Copia el archivo de requisitos primero, para aprovechar la caché de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de los archivos de tu aplicación
COPY . .

# Expone el puerto 8000 para acceder a tu aplicación FastAPI
EXPOSE 8000

# Comando para ejecutar tu aplicación usando Uvicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
