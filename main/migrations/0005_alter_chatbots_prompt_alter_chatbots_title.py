# Generated by Django 5.0.4 on 2024-09-15 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_chatbots_ispublic_chatbots_model_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbots',
            name='prompt',
            field=models.TextField(default='', null=True),
        ),
        migrations.AlterField(
            model_name='chatbots',
            name='title',
            field=models.TextField(default='', null=True),
        ),
    ]
