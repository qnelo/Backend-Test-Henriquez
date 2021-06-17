import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.http import urlencode

from accounts.models import Client
from nora.models import Menu, Order, Plate

pytestmark = pytest.mark.django_db


@pytest.mark.django_db()
class TestIndexView:

    pytestmark = pytest.mark.django_db

    def test_index_view_get_with_login(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        Menu.objects.create(date="2021-01-01")
        Menu.objects.create(date="2021-01-02")

        url = reverse("index")
        client.login(username="nora", password="nora123")

        res = client.get(url)

        content = res.content.decode(res.charset)

        assert res.status_code == 200
        assert "2021-01-01" in content
        assert "2021-01-02" in content

    def test_index_view_get_without_login(self, client):

        url = reverse("index")
        res = client.get(url)

        assert res.status_code == 302


@pytest.mark.django_db()
class TestDailyMenuView:

    pytestmark = pytest.mark.django_db

    def test_daily_menu_view_get_with_login(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        plate = Plate.objects.create(name="charquican")
        menu = Menu.objects.create(date="2021-01-01")
        menu.plates.add(plate)
        client_object = Client.objects.create(name="Willy Sabor")

        Order.objects.create(menu=menu, place_order=True, client=client_object)

        url = reverse("daily_menu", args=["2021-01-01"])
        client.login(username="nora", password="nora123")

        res = client.get(url)

        content = res.content.decode(res.charset)

        assert res.status_code == 200
        assert "charquican" in content
        assert "Willy Sabor" in content

    def test_daily_menu_view_get_with_login_404(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")
        url = reverse("daily_menu", args=["1900-01-01"])
        client.login(username="nora", password="nora123")

        res = client.get(url)

        res.content.decode(res.charset)

        assert res.status_code == 404

    def test_daily_menu_view_post_with_login(self, client):
        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        plate = Plate.objects.create(name="charquican")
        menu = Menu.objects.create(date="2021-01-01")
        menu.plates.add(plate)
        client_object = Client.objects.create(name="Willy Sabor")

        Order.objects.create(menu=menu, place_order=True, client=client_object)

        url = reverse("daily_menu", args=["2021-01-01"])
        client.login(username="nora", password="nora123")

        data = urlencode({"data": "2020-02-02"})
        content_type = "application/x-www-form-urlencoded"

        res = client.post(url, data, content_type)

        content = res.content.decode(res.charset)

        assert res.status_code == 200
        assert "charquican" in content
        assert "2021-01-01" not in content
        assert "Willy Sabor" not in content


@pytest.mark.django_db()
class TestDeleteMenuView:

    pytestmark = pytest.mark.django_db

    def test_delete_menu_view_get_with_login(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        plate = Plate.objects.create(name="charquican")
        menu = Menu.objects.create(date="2021-01-01")
        menu.plates.add(plate)
        client_object = Client.objects.create(name="Willy Sabor")

        Order.objects.create(menu=menu, place_order=True, client=client_object)

        url = reverse("delete_menu", args=[menu.pk])
        client.login(username="nora", password="nora123")

        res = client.post(url)
        redirect = client.get(res.url)

        content = redirect.content.decode(redirect.charset)

        assert redirect.status_code == 200
        assert "charquican" in content
        assert "Willy Sabor" not in content


@pytest.mark.django_db()
class TestPlateView:

    pytestmark = pytest.mark.django_db

    def test_plate_view_get_with_login(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        Plate.objects.create(name="charquican")
        Plate.objects.create(name="porotos")

        url = reverse("plate")
        client.login(username="nora", password="nora123")

        res = client.get(url)

        content = res.content.decode(res.charset)

        assert res.status_code == 200
        assert "charquican" in content
        assert "porotos" in content

    def test_plate_view_post_with_login(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        Plate.objects.create(name="charquican")
        data = urlencode({"name": "porotos", "description": "con mazamorra"})
        content_type = "application/x-www-form-urlencoded"

        url = reverse("plate")
        client.login(username="nora", password="nora123")

        res = client.post(url, data, content_type)
        redirect = client.get(res.url)

        content = redirect.content.decode(redirect.charset)

        assert redirect.status_code == 200
        assert "charquican" in content
        assert "porotos" in content

    def test_plate_view_error_post_with_login(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        Plate.objects.create(name="charquican")
        data = urlencode({})
        content_type = "application/x-www-form-urlencoded"

        url = reverse("plate")
        client.login(username="nora", password="nora123")

        res = client.post(url, data, content_type)

        assert res.status_code == 422


@pytest.mark.django_db()
class TestDeletePlateView:

    pytestmark = pytest.mark.django_db

    def test_delete_plate_view_post_with_login(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        plate = Plate.objects.create(name="charquican")
        Plate.objects.create(name="porotos")

        url = reverse("delete_plate", args=[plate.pk])
        client.login(username="nora", password="nora123")

        res = client.post(url)
        redirect = client.get(res.url)

        content = redirect.content.decode(redirect.charset)

        assert redirect.status_code == 200
        assert "charquican" not in content
        assert "porotos" in content


@pytest.mark.django_db()
class TestEditPlateView:

    pytestmark = pytest.mark.django_db

    def test_edit_plate_view_get_with_login(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        plate = Plate.objects.create(name="charquican", description="con huevo frito")

        url = reverse("edit_plate", args=[plate.pk])
        client.login(username="nora", password="nora123")

        res = client.get(url)

        content = res.content.decode(res.charset)

        assert res.status_code == 200
        assert "charquican" in content
        assert "con huevo frito" in content

    def test_edit_plate_view_post_with_login(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        plate = Plate.objects.create(name="charquican", description="con huevo frito")

        url = reverse("edit_plate", args=[plate.pk])
        client.login(username="nora", password="nora123")

        data = urlencode(
            {"name": "charquican vegano", "description": "sin huevo frito"}
        )
        content_type = "application/x-www-form-urlencoded"

        res = client.post(url, data, content_type)
        redirect = client.get(res.url)

        content = redirect.content.decode(redirect.charset)

        assert redirect.status_code == 200
        assert "charquican vegano" in content
        assert "sin huevo frito" in content

    def test_edit_plate_view_post_pk_error_with_login(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        url = reverse("edit_plate", args=[12341234])
        client.login(username="nora", password="nora123")

        data = urlencode(
            {"name": "charquican vegano", "description": "sin huevo frito"}
        )
        content_type = "application/x-www-form-urlencoded"

        res = client.post(url, data, content_type)

        assert res.status_code == 404

    def test_edit_plate_view_post_error_with_login(self, client):

        User.objects.create_user("nora", "nora@cornershop.com", "nora123")

        plate = Plate.objects.create(name="charquican", description="con huevo frito")

        url = reverse("edit_plate", args=[plate.pk])
        client.login(username="nora", password="nora123")

        data = urlencode({"name": "charquican vegano"})
        content_type = "application/x-www-form-urlencoded"

        res = client.post(url, data, content_type)

        assert res.status_code == 422
