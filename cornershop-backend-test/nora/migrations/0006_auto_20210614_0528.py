# Generated by Django 3.0.8 on 2021-06-14 05:28

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("nora", "0005_auto_20210614_0524"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="uuid",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
