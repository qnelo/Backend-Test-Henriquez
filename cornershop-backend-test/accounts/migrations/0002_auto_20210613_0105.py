# Generated by Django 3.0.8 on 2021-06-13 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="client",
            name="country_code",
            field=models.CharField(max_length=2),
        ),
    ]
