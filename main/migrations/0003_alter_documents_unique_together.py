# Generated by Django 5.0.4 on 2024-05-26 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_documents'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='documents',
            unique_together={('documentname', 'chatbot')},
        ),
    ]
