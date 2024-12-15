from django.db import models
from django.contrib.auth.models import User


class Docs(models.Model):
    id = models.BigAutoField(primary_key=True)
    fastapi_document_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="ID документа от FastAPI",
    )
    file_path = models.CharField(max_length=255, unique=True, verbose_name="Путь к файлу")
    size = models.PositiveIntegerField(verbose_name="Размер файла (Кб)")

    class Meta:
        verbose_name = "Документ пользователя"
        verbose_name_plural = "Документы пользователей"




