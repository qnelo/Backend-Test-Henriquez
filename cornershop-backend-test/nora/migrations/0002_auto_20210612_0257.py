# Generated by Django 3.0.8 on 2021-06-12 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nora", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="menu",
            options={"ordering": ["-date"]},
        ),
        migrations.AlterField(
            model_name="menu",
            name="date",
            field=models.DateField(unique=True),
        ),
    ]
