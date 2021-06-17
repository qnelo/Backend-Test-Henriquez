import pytest

from nora.forms import MenuForm, OrderForm, PlateForm
from nora.models import Plate

pytestmark = pytest.mark.django_db


class TestFormPlate:
    def test_basic(self):
        plate_form_data = {"name": "charquican", "description": "con huevo frito"}
        plate_form = PlateForm(data=plate_form_data)

        assert plate_form.is_valid() is True

    def test_imcomplete_form(self):
        plate_form_data = {"name": "charquican"}
        plate_form = PlateForm(data=plate_form_data)

        assert plate_form.is_valid() is False
        assert plate_form.errors["description"][0] == "This field is required."


class TestFormMenu:
    def test_basic(self):

        plate = Plate(name="charquican", description=".")
        plate.save()

        menu_form_data = {"date": "2021-01-01", "plates": Plate.objects.all()}
        menu_form = MenuForm(data=menu_form_data)

        assert menu_form.is_valid() is True

    def test_invalid_date(self):

        plate = Plate(name="charquican", description=".")
        plate.save()

        menu_form_data = {"date": "año-01-01", "plates": Plate.objects.all()}
        menu_form = MenuForm(data=menu_form_data)

        assert menu_form.is_valid() is False
        assert menu_form.errors["date"][0] == "Enter a valid date."

    def test_incomplete_form(self):

        menu_form_data = {"date": "2021-01-01"}
        menu_form = MenuForm(data=menu_form_data)

        assert menu_form.is_valid() is False
        assert menu_form.errors["plates"][0] == "This field is required."


class TestOrderMenu:
    def test_basic(self):

        plate = Plate(name="charquican", description=".")
        plate.save()

        order_form_data = {
            "customization": "sin charqui",
            "plate": plate,
            "place_order": False,
        }
        order_form = OrderForm(data=order_form_data)

        assert order_form.is_valid() is True

    def test_valid_partial_form(self):

        plate = Plate(name="charquican", description=".")
        plate.save()

        order_form_data = {"customization": "sin charqui", "plate": plate}
        order_form = OrderForm(data=order_form_data)

        assert order_form.is_valid() is True

    def test_incomplete_form(self):

        order_form_data = {"customization": "sin charqui"}
        order_form = OrderForm(data=order_form_data)

        assert order_form.is_valid() is False
        assert order_form.errors["plate"][0] == "This field is required."
