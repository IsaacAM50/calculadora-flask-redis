import os
import logging
import redis
from flask import Flask, request, render_template, jsonify

# Configuración de la aplicación Flask
app = Flask(__name__)

# Configuración de Redis
redis_host = os.getenv('REDIS_HOST', 'redis-final')
redis_port = int(os.getenv('REDIS_PORT', 6379))
cache = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

# Configuración del logger
logging.basicConfig(
    level=logging.INFO,
    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
)
logger = logging.getLogger(__name__)

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
                    logger.error('División por cero intendada')
            else:
                result = 'Operación no válida'
                logger.warning(f'Operación no válida: {operation}')
            
            # Log de la operación realizada
            operation_log = f'{num1} {operation} {num2} = {result}'
            logger.info(operation_log)
            
            # Guardar el historial de operaciones en Redis
            cache.rpush('history', operation_log)
            
            # Limitar el historial a los últimos 10 registros
            if cache.llen('history') > 10:
                cache.lpop('history')
        
        except ValueError:
            result = 'Error: Ingrese números válidos'
            logger.error('Error: Ingreso de datos no válidos')
    
    # Recuperar el historial desde Redis
    history = cache.lrange('history', 0, -1)
    
    return render_template('index.html', result=result, history=history)

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check para monitoreo"""
    try:
        cache.ping()
        return jsonify({"status": "healthy", "redis": "connected"}), 200
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)