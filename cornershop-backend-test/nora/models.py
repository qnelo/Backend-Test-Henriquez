import uuid

from django.db import models
from django.db.models.deletion import SET_NULL

from accounts.models import Client


class Plate(models.Model):
    """
    A class to represent a plates or meals.

    ...

    Attributes
    ----------
    name : str
        Name of the plate
    description : str
        Dish description
    """

    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class Menu(models.Model):
    """
    A class to represent a plates or Menus.

    ...

    Attributes
    ----------
    date : date
        Name of the plate
    plates : Model
        Plate Model
    """

    date = models.DateField(auto_now_add=False, unique=True)
    plates = models.ManyToManyField(Plate)

    class Meta:
        ordering = ["-date"]


class Order(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    customization = models.TextField(blank=True, null=True)
    place_order = models.BooleanField(default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    plate = models.ForeignKey(Plate, blank=True, null=True, on_delete=SET_NULL)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)

    class Meta:
        unique_together = ["client", "menu"]
