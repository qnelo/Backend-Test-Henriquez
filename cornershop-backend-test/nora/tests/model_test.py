import uuid

import pytest

from accounts.models import Client
from nora.models import Menu, Order, Plate

pytestmark = pytest.mark.django_db


@pytest.mark.django_db()
class TestPlate:
    def test_basic(self):
        charquican = Plate(name="charquican", description="con huevo frito")
        charquican.save()

        assert charquican.__str__() == "charquican"
        assert charquican.description == "con huevo frito"


class TestMenu:
    @pytest.mark.django_db()
    def test_basic(self):

        plate1 = Plate(name="a")
        plate1.save()
        plate2 = Plate(name="b", description="b")
        plate2.save()

        menu = Menu(date="2021-01-01")
        menu.save()
        menu.plates.add(plate1, plate2)
        assert menu.date == "2021-01-01"
        assert menu.plates.get(name="b").description == "b"

    @pytest.mark.django_db()
    def test_date(self):

        with pytest.raises(Exception) as e:

            menu = Menu(date="asdf")
            menu.save()

        assert (
            str(e.value)
            == "['“asdf” value has an invalid date format. It must be in YYYY-MM-DD format.']"
        )


@pytest.mark.django_db()
class TestOrder:
    def test_basic(self):

        order = Order()
        assert uuid.UUID(str(order.uuid)).version == 4

    def test_unique(self):

        client = Client(name="client")
        client.save()
        menu1 = Menu(date="2021-02-01")
        menu2 = Menu(date="2021-02-02")
        menu1.save()
        menu2.save()

        order1 = Order()
        order1.menu = menu1
        order1.client = client
        order1.save()

        assert order1.client.name == "client"
        assert order1.menu.date == "2021-02-01"

        with pytest.raises(Exception) as e:
            order2 = Order()
            order2.menu = menu1
            order2.client = client
            order2.save()

        assert "duplicate key value violates unique constraint" in str(e.value)
