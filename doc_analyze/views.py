import os

import requests
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from users.models import UsersToDocs
from .models import Docs


def index(request):
    return HttpResponse("Страница тестирования Tesseract")


def home(request):
    documents = Docs.objects.all()
    return render(request, 'home.html', {'documents': documents, 'MEDIA_URL': settings.MEDIA_URL})


@login_required
@csrf_exempt
def upload_document(request):
    if request.method == "POST":
        try:
            file = request.FILES.get("file")

            if not file:
                return JsonResponse({"error": "Файл не предоставлен"}, status=400)

            # Сохраняем файл локально
            local_path = default_storage.save(f"documents/{file.name}", ContentFile(file.read()))

            # Отправляем файл в FastAPI
            fastapi_url = "http://file_analyzer_app:8000/upload_doc"
            with open(default_storage.path(local_path), "rb") as f:
                response = requests.post(
                    fastapi_url,
                    files={"file": (file.name, f)},
                    timeout=10
                )

            if response.status_code != 200:
                return JsonResponse({"error": f"Ошибка FastAPI: {response.text}"}, status=500)

            fastapi_response = response.json()
            fastapi_document_id = fastapi_response.get("document")

            if not fastapi_document_id:
                return JsonResponse({"error": "FastAPI не вернул ID документа"}, status=500)

            # Сохраняем данные в таблицу Docs
            doc = Docs.objects.create(
                fastapi_document_id=fastapi_document_id,
                file_path=local_path,
                size=file.size // 1024  # Размер в КБ
            )

            # Создаём связь в UsersToDocs
            UsersToDocs.objects.create(user=request.user, doc=doc)

            # Перенаправляем на страницу profile.html
            return redirect("profile")  # Здесь "profile" — это имя маршрута (name) из urls.py

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "upload.html")


@login_required
def analyze_document(request, doc_id):
    try:
        fastapi_document_id = str(doc_id)
        document = Docs.objects.get(fastapi_document_id=fastapi_document_id)
        fastapi_document_id_int = int(fastapi_document_id)
        fastapi_url = f"http://file_analyzer_app:8000/doc_analyse/{fastapi_document_id_int}"

        response = requests.post(fastapi_url)

        if response.status_code == 200:
            # Перенаправление на другой endpoint
            return redirect(f"/analyze/{fastapi_document_id_int}/result/")
        else:
            return JsonResponse({"error": f"Ошибка при запросе в FastAPI: {response.text}"},
                                status=response.status_code)
    except Docs.DoesNotExist:
        return JsonResponse({"error": f"Документ с ID {doc_id} не найден в базе данных"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Ошибка сервера: {str(e)}"}, status=500)



@login_required
def analyze_result(request, fastapi_id):
    try:
        # Формируем URL для получения текста из FastAPI
        fastapi_url = f"http://file_analyzer_app:8000/get_text/{int(fastapi_id)}"

        # Отправляем GET-запрос на FastAPI для получения текста
        response = requests.get(fastapi_url)

        if response.status_code == 200:
            # Если запрос успешен, отображаем результат анализа
            result_text = response.json().get("text", "Текст не найден.")
            return render(request, 'analyze.html', {'result_text': result_text, 'document_id': fastapi_id})
        else:
            return render(request, 'analyze.html', {
                'error': f"Ошибка при запросе в FastAPI: {response.text}",
                'document_id': fastapi_id
            })
    except Exception as e:
        return render(request, 'analyze.html', {
            'error': f"Ошибка сервера: {str(e)}",
            'document_id': fastapi_id
        })


def delete_doc_form(request):
    return render(request, 'delete_doc_form.html')

def delete_doc(request):
    if request.method == 'POST':
        doc_id = request.POST.get('doc_id')
        try:
            # Удаление через FastAPI
            try:
                response = requests.delete(f'http://file_analyzer_app:8000/doc_delete/{doc_id}')
                if response.status_code == 200:
                    messages.success(request, 'Документ успешно удалён через FastAPI.')
                else:
                    messages.warning(request, 'Документ не найден в FastAPI, но удалим из Django.')
            except requests.RequestException as e:
                messages.error(request, f'Ошибка при удалении через FastAPI: {e}')

            # Удаление документа из Django
            doc = Docs.objects.filter(fastapi_document_id=doc_id).first()
            if doc:
                file_path = os.path.join(settings.MEDIA_ROOT, doc.file_path)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    messages.success(request, 'Файл удалён из файловой системы.')
                doc.delete()
                messages.success(request, 'Документ успешно удалён из Django.')
            else:
                messages.warning(request, 'Документ с указанным ID не найден в базе Django.')

        except Exception as e:
            messages.error(request, f'Ошибка: {e}')

        return redirect('home')