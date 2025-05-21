from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'nonexistent@mail.com'})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    new_user = {'name': 'New User', 'email': 'new@mail.com'}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert isinstance(response.json(), int)  # Проверяем, что возвращается ID

def test_create_user_with_invalid_email():
    '''Создание пользователя с существующей почтой'''
    duplicate_user = {'name': 'Duplicate', 'email': users[0]['email']}
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 409
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    '''Удаление пользователя'''
    # Сначала создаем пользователя для удаления
    test_email = 'temp@mail.com'
    client.post("/api/v1/user", json={'name': 'Temp', 'email': test_email})
    
    # Удаляем
    response = client.delete("/api/v1/user", params={'email': test_email})
    assert response.status_code == 204
    
    # Проверяем, что пользователь удален
    response = client.get("/api/v1/user", params={'email': test_email})
    assert response.status_code == 404