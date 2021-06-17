import logging
from datetime import date

from django.db.models.functions import Lower

from accounts.models import Client

from .models import Menu, Order
from .slack import generate_message, send_message

logger = logging.getLogger(__name__)


def get_menu_of_the_day():

    try:
        menu = Menu.objects.get(date=date.today())
    except Menu.DoesNotExist:
        logger.info("No menu of the day")
        return False

    return menu


def get_clients():

    try:
        client_annotate = Client.objects.annotate(lower_country=Lower("country_code"))
        clients = client_annotate.filter(lower_country__iexact="cl")
    except Client.DoesNotExist:
        logger.info("No Chilean clients")
        return False
    return clients


def send_reminder(order):

    user_id = order.client.slack_id
    message = generate_message(order)

    return send_message(slack_user_id=user_id, message=message)


def create_order(client, menu):
    order, created = Order.objects.get_or_create(
        client=client,
        menu=menu,
    )

    return send_reminder(order)


def create_orders():

    menu = get_menu_of_the_day()
    if menu:
        clients = get_clients()
        if clients:
            for client in clients:
                create_order(client, menu)
            return True

        return False

    return False
