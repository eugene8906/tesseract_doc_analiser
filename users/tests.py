import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_register_user(client):
    response = client.post(reverse('register'), {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123',
        'password_confirm': 'password123'
    })
    assert response.status_code == 302  # Перенаправление на login
    assert response.url == reverse('login')

@pytest.mark.django_db
def test_login_user(client, django_user_model):
    # Создание тестового пользователя
    user = django_user_model.objects.create_user(username='testuser', password='password123')
    response = client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'password123'
    })
    assert response.status_code == 302  # Перенаправление на home
    assert response.url == reverse('home')
