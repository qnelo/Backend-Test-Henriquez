import pytest

from accounts.models import Client

pytestmark = pytest.mark.django_db


@pytest.mark.django_db()
class TestPlate:
    def test_basic(self):
        client = Client(name="waldo", country_code="CL", slack_id="SDF-1")
        client.save()

        assert client.name == "waldo"
        assert client.country_code == "CL"
        assert client.slack_id == "SDF-1"

    @pytest.mark.django_db()
    def test_country(self):

        with pytest.raises(Exception) as e:

            client = Client(country_code="Shile")
            client.save()

        assert "value too long for type character" in str(e.value)
