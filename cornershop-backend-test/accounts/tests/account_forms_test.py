import pytest

from accounts.forms import ClientForm

pytestmark = pytest.mark.django_db


class TestOrderMenu:
    def test_basic(self):

        client_form_data = {
            "name": "Willy Sabor",
            "country_code": "CL",
            "slack_id": "DEQUIENESLA",
        }
        client_form = ClientForm(data=client_form_data)

        assert client_form.is_valid() is True

    def test_partial_form(self):

        client_form_data = {"name": "Willy Sabor"}
        client_form = ClientForm(data=client_form_data)

        assert client_form.is_valid() is False
        assert client_form.errors["country_code"][0] == "This field is required."
        assert client_form.errors["slack_id"][0] == "This field is required."

    def test_incomplete_form(self):

        client_form_data = {
            "name": "Willy Sabor",
            "country_code": "CLX",
            "slack_id": "DEQUIENESLA",
        }
        client_form = ClientForm(data=client_form_data)

        assert client_form.is_valid() is False
        assert (
            "Ensure this value has at most 2 characters"
            in client_form.errors["country_code"][0]
        )
