# Generated by Django 5.1.3 on 2024-12-04 15:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doc_analyze', '0002_alter_docs_options_docs_fastapi_document_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Price',
        ),
    ]
