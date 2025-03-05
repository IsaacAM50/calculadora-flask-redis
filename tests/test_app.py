import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

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