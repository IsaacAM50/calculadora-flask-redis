
Esta es una aplicación de calculadora simple desarrollada con Flask y Redis, diseñada para realizar operaciones básicas (suma, resta, multiplicación y división) y almacenar un historial de cálculos en Redis.

Instalación y Configuración

Requisitos previos

Docker

Docker Compose

Configuración de variables de entorno

Crea un archivo .env en la raíz del proyecto con el siguiente contenido:

APP_PORT=5000
REDIS_PORT=6379
NETWORK=gestor_tareas_net
REDIS=3.9

Instrucciones de instalación

Clona este repositorio:

git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>

Construye y levanta la aplicación con Docker Compose:

docker-compose up --build

Accede a la aplicación en tu navegador en http://localhost:5000.

Uso

Interfaz web

Introduce dos números en los campos correspondientes.

Selecciona una operación (suma, resta, multiplicación o división).

Haz clic en el botón "Calcular" para obtener el resultado.

Visualiza el historial de cálculos en la misma página.

Historial

El historial de operaciones se almacena en Redis y se muestra en la interfaz web.

Logs

Los logs de la aplicación se generan en formato JSON y se pueden consultar en la salida estándar del contenedor. Cada registro incluye:

Nivel del log (INFO, ERROR, etc.)

Mensaje descriptivo

Detalles de la operación realizada (si aplica)

Estructura del proyecto

.
├── app.py                  # Código principal de la aplicación
├── templates
│   └── index.html          # Plantilla HTML para la interfaz web
├── Dockerfile              # Configuración de Docker para la aplicación
├── docker-compose.yml      # Configuración de Docker Compose
├── requirements.txt        # Dependencias de Python
├── .env                    # Variables de entorno
└── README.md               # Documentación del proyecto

Configuración adicional

Variables de entorno

APP_PORT: Puerto en el que se ejecuta la aplicación Flask.

NETWORK: Red en la que se ejecutan los dos programas

REDIS_PORT: Puerto del servidor Redis.

REDIS: Versión de REDIS

Personalización del historial

El tamaño del historial almacenado puede ajustarse modificando la lógica en app.py para limitar la cantidad de entradas recuperadas de Redis.

Logs

Para habilitar y personalizar los logs JSON, se configura el registro en el archivo app.py utilizando la biblioteca logging. Asegúrate de revisar la configuración inicial de logs para adaptarla según tus necesidades.

Pruebas

Ejecuta la aplicación con docker-compose.

Abre la interfaz web en tu navegador.

Realiza varias operaciones y verifica el historial y los logs generados.

