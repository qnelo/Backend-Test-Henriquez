from django.forms import (
    CheckboxSelectMultiple,
    DateField,
    ModelChoiceField,
    ModelForm,
    ModelMultipleChoiceField,
    RadioSelect,
    SelectDateWidget,
)

from .models import Menu, Order, Plate


class PlateForm(ModelForm):
    class Meta:
        model = Plate
        fields = (
            "name",
            "description",
        )


class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = (
            "date",
            "plates",
        )

    date = DateField(widget=SelectDateWidget)
    plates = ModelMultipleChoiceField(
        queryset=Plate.objects.all(), widget=CheckboxSelectMultiple
    )


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = (
            "plate",
            "customization",
            "place_order",
        )

    plate = ModelChoiceField(queryset=Plate.objects.all(), widget=RadioSelect())
