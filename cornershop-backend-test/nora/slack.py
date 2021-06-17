from django.conf import settings

import requests


def send_message(slack_user_id, message):

    url = "https://slack.com/api/chat.postMessage?channel={}&text={}".format(
        slack_user_id, message
    )

    payload = ""
    headers = {"Authorization": "Bearer {}".format(settings.SLACK_OAUTH_TOKEN)}

    response = requests.request("POST", url, headers=headers, data=payload)

    return response.text


def generate_message(order):

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
