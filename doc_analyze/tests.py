import tempfile
import os
from unittest.mock import patch
import pytest
from django.urls import reverse #возвращает URL по имени маршрута.
from django.core.files.uploadedfile import SimpleUploadedFile #эмулирует загружаемый файл в тестах.
from doc_analyze.models import Docs

@pytest.mark.django_db
def test_upload_document(client, django_user_model):
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        temp_file.write(b"Test content")
        temp_file.seek(0)
        uploaded_file = SimpleUploadedFile(
            name=os.path.basename(temp_file.name),
            content=temp_file.read(),
            content_type="text/plain"
        )

    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"document": 1}  # Возвращаем фиктивный ID документа

        response = client.post(reverse('upload'), {'file': uploaded_file})

        assert response.status_code == 302  # Проверка перенаправления
        assert Docs.objects.count() == 1

        doc = Docs.objects.first()
        assert doc.file_path is not None
        assert doc.fastapi_document_id == '1'


@pytest.mark.django_db
def test_delete_document(client, django_user_model):
    # Создание тестового пользователя
    django_user_model.objects.create_user(username='testuser', password='password123')
    client.login(username='testuser', password='password123')

    # Создание документа
    with tempfile.NamedTemporaryFile(suffix=".png") as temp_file:
        temp_file.write(b"Delete me")
        temp_file.seek(0)
        doc = Docs.objects.create(
            fastapi_document_id="12345",
            file_path=temp_file.name,
            size=1
        )

    response = client.post(reverse('delete_doc'), {'doc_id': doc.fastapi_document_id})

    assert response.status_code == 302  # Перенаправление на home
    assert not Docs.objects.filter(fastapi_document_id="12345").exists()
