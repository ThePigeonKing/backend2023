# Generated by Django 4.2.7 on 2023-12-06 23:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_alter_post_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="text",
            field=models.TextField(verbose_name="Текст"),
        ),
    ]
