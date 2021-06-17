from django.db import models


class Client(models.Model):
    """
    This is a class to represent a clients.


    Attributes:
        name (str): Name of the person.
        country_code (str): ISO 3166 country code `Alpha-2 code`.
        slack_id (str): Slack user id in the workspace, example `U024AAE5351`.
    """

    name = models.CharField(max_length=50)
    country_code = models.CharField(max_length=2)
    slack_id = models.CharField(max_length=20)

    class Meta:
        ordering = ["name"]
