# Generated by Django 5.0.1 on 2024-02-03 21:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0006_remove_weatheralert_location_delete_userprofile_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="observation",
            name="feels_like",
            field=models.FloatField(default=20.5),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="observation",
            name="humidity",
            field=models.IntegerField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="observation",
            name="max_temperature",
            field=models.FloatField(default=85),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="observation",
            name="min_temperature",
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="observation",
            name="pressure",
            field=models.IntegerField(default=5),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="observation",
            name="icon",
            field=models.ImageField(
                blank=True, null=True, upload_to="observation_icons/"
            ),
        ),
    ]
