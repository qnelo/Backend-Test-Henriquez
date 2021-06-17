from django.db import models


class Client(models.Model):
    """Clients Model

    Args:
        models (Model): Basic information about clients
    """

    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2)
    slack_id = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]
