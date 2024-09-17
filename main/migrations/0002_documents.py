# Generated by Django 5.0.4 on 2024-05-14 21:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentname', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('chatbot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.chatbots')),
            ],
        ),
    ]