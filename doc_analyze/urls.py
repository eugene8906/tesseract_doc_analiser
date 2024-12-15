from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_document, name='upload'),
    path('analyze/<int:doc_id>/', views.analyze_document, name='analyze_document'),
    path('analyze/<int:fastapi_id>/result/', views.analyze_result, name='analyze_result'),
    path('delete_doc_form/', views.delete_doc_form, name='delete_doc_form'),
    path('delete_doc/', views.delete_doc, name='delete_doc'),
]