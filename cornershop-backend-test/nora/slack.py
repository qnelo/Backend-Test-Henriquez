from django.conf import settings

import requests


def send_message(slack_user_id, message):
    """Generate a post request to the slack API to send a message to a user

    Args:
        slack_user_id (str): slack user id
        message (string): message to a client with the menu reminder

    Returns:
        str: slack API response
    """

    url = "https://slack.com/api/chat.postMessage?channel={}&text={}".format(
        slack_user_id, message
    )

    payload = ""
    headers = {"Authorization": "Bearer {}".format(settings.SLACK_OAUTH_TOKEN)}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def generate_message(order):
    """Generate the message to a user

    Args:
        order (Model): the client order Model

    Returns:
        str: The message that the client will view in slack
    """

    plates = order.menu.plates.all()
    menu_list = ""
    for plate in plates:
        menu_list = menu_list + "• " + plate.name + "\n"

    order_url = "{}/menu/{}/".format(settings.SERVER_URL, order.uuid)

    message = """Hi {}, the menu for today {} is:\n{}
    \nYou can place your order before 11am
    \nTo review it and request a plate you can access the following link: {}""".format(
        order.client.name, order.menu.date, menu_list, order_url
    )

    return message
