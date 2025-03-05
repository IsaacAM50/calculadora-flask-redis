import logging
import redis
from flask import Flask, request, render_template

# Configuración de la aplicación Flask
app = Flask(__name__)

# Configuración de Redis
cache = redis.Redis(host='redis-final', port=6379)

# Configuración del logger en formato JSON
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Handler para los logs
log_handler = logging.StreamHandler()
log_handler.setLevel(logging.INFO)

# Formato del log en JSON
formatter = logging.Formatter(
    '{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
log_handler.setFormatter(formatter)
logger.addHandler(log_handler)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    result = ''  
    if request.method == 'POST':
        try:
            # Obtener los datos del formulario
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']

            # Realizar la operación correspondiente
            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 != 0:
                    result = num1 / num2
                else:
                    result = 'Error: División por cero'
            else:
                result = 'Operación no válida'

            # Log de la operación realizada
            logger.info(f'Operación: {num1} {operation} {num2} = {result}')

            # Guardar el historial de operaciones en Redis
            cache.rpush('history', f'{num1} {operation} {num2} = {result}')
        except ValueError:
            result = 'Error: Ingrese números válidos'
            logger.error('Error: Ingreso de datos no válidos')

    # Recuperar el historial desde Redis
    history = cache.lrange('history', 0, -1)

    return render_template('index.html', result=result, history=history)

if __name__ == '__main__':
    app.run(debug=True)