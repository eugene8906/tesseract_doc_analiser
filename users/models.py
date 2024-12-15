from django.contrib.auth.models import AbstractUser
from django.db import models
from doc_analyze.models import Docs


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name="Имя пользователя")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    password = models.CharField(max_length=128, verbose_name="Пароль")

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class UsersToDocs(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_docs", verbose_name="Пользователь")
    doc = models.ForeignKey(Docs, on_delete=models.CASCADE, related_name="doc_users", verbose_name="Документ")
    added_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        verbose_name = "Документ пользователя"
        verbose_name_plural = "Документы пользователей"

    def __str__(self):
        return f"{self.user.username} -> {self.doc.file_path}"


