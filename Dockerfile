# Utiliza una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de la aplicación al contenedor
COPY . /app

# Actualiza los paquetes e instala dependencias necesarias
RUN apt-get update && apt-get install -y \
    gcc \
    libc-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
# Configura variables de entorno necesarias
ENV FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000

# Expone el puerto que usará Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["flask", "run"]

