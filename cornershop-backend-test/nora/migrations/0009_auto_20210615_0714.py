# Generated by Django 3.0.8 on 2021-06-15 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("nora", "0008_auto_20210615_0652"),
    ]

    operations = [
        migrations.RenameField(
            model_name="order",
            old_name="plates",
            new_name="plate",
        ),
    ]
