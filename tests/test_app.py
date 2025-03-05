import pytest
import redis
from app.app import app

@pytest.fixture    
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def redis_client():
    client = redis.Redis(host='redis-final', port=6379, db=0)
    yield client
    client.close()

def test_home_page(client):
    """Prueba la página de inicio"""
    response = client.get('/')
    assert response.status_code == 200

def test_calculator_addition(client):
    """Prueba de operación de suma"""
    response = client.post('/', data={
        'num1': 5,
        'num2': 3,
        'operation': 'add'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'8.0' in response.data

def test_calculator_division_by_zero(client):
    """Prueba de división por cero"""
    response = client.post('/', data={
        'num1': 10,
        'num2': 0,
        'operation': 'divide'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Error: Divisi\xc3\xb3n por cero' in response.data

def test_redis_connection(redis_client):
    """Prueba de conexión a Redis"""
    try:
        redis_client.ping()
        assert True
    
    except Exception as e:
        pytest.fail(f"No se pudo conectar a Redis: {e}")
def test_operation_history(client, redis_client):
    """Prueba el historial de operaciones"""
    # Limpiar historial antes de la prueba
    redis_client.delete('history')

    # Realizar una operación
    client.post('/', data={
        'num1': 10,
        'num2': 5,
        'operation': 'add'
    }, follow_redirects=True)

    # Verificar que se guardó en el historial
    history = redis_client.lrange('history', 0, -1)
    assert len(history) > 0
    assert '10.0 add 5.0 = 15.0' in history