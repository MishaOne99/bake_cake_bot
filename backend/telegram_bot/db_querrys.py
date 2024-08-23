import datetime as dt

from datacenter.models import (
    TimeFrames, Client, Level, Form,
    Topping, Decor, Cake, Berry,
    Order
)

import random


def get_time_frame():
    return TimeFrames.objects.first()


def create_order(client):
    return Order.objects.create(client=client, status="waiting")


def check_and_add_phone_number(id, phone_num):
    if not Client.objects.filter(id_tg=id, phone_number=phone_num).exists():
        client = Client.objects.get(id_tg=id)
        client.phone_number = phone_num
        client.save()


def check_client(id):
    return Client.objects.filter(id_tg__exact=id).exists()


def get_client(id):
    return Client.objects.get(id_tg__exact=id)


def create_client(id, first_name, last_name, username=None, phone_number=None):
    Client.objects.create(
            id_tg=id,
            full_name=f"{first_name} {last_name} aka {username}",
            phone_number=phone_number
        )
    return id


def get_presets_cakes():
    return Cake.objects.filter(title__isnull=False)


def get_random_preset_cake():
    return random.choice(get_presets_cakes())


def get_levels():
    return Level.objects.all()


def get_forms():
    return Form.objects.all()


def get_toppings():
    return Topping.objects.all()


def get_berries():
    return Berry.objects.all()


def get_decors():
    return Decor.objects.all()
