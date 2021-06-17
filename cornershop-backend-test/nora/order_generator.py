import logging
from datetime import date

from django.db.models.functions import Lower

from accounts.models import Client

from .models import Menu, Order
from .slack import generate_message, send_message

logger = logging.getLogger(__name__)


def get_menu_of_the_day():
    """Obtain the menu of the current date

    Returns:
        Model: Menu of the day
    """

    try:
        menu = Menu.objects.get(date=date.today())
    except Menu.DoesNotExist:
        logger.info("No menu of the day")
        return False

    return menu


def get_clients():
    """Obtains all the clients in Chile

    Returns:
        Model: Clients
    """

    try:
        client_annotate = Client.objects.annotate(lower_country=Lower("country_code"))
        clients = client_annotate.filter(lower_country__iexact="cl")
    except Client.DoesNotExist:
        logger.info("No clients in Chile")
        return False
    return clients


def send_reminder(order):
    """This function prepare the message and call the sender

    Args:
        order (Model): order Model

    Returns:
        function: ejecution of the reminder sender
    """

    user_id = order.client.slack_id
    message = generate_message(order)

    return send_message(slack_user_id=user_id, message=message)


def create_order(client, menu):
    """Get or create a new order for a client

    Args:
        client (Model): client Model
        menu (Model): menu Model

    Returns:
        function: ejecution of a reminder function
    """
    order, created = Order.objects.get_or_create(
        client=client,
        menu=menu,
    )

    return send_reminder(order)


def create_orders():
    """Create clients orders once time per day

    Returns:
        bool: without description
    """
    menu = get_menu_of_the_day()
    if menu:
        clients = get_clients()
        if clients:
            for client in clients:
                create_order(client, menu)
            return True

        return False

    return False
