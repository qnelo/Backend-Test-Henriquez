from django.forms import ModelForm

from .models import Client


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = (
            "name",
            "country_code",
            "slack_id",
        )
