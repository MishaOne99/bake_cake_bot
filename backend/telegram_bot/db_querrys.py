import random

from datacenter.models import (
    Berry,
    Cake,
    Client,
    Decor,
    Form,
    Level,
    Order,
    TimeFrames,
    Topping,
    Invoice
)

import datetime as dt


def check_and_add_phone_number(id, phone_num):
    if not Client.objects.filter(id_tg=id, phone_number=phone_num).exists():
        client = Client.objects.get(id_tg=id)
        client.phone_number = phone_num
        client.save()


def get_time_frame():
    return TimeFrames.objects.first()

def get_orders_by_client(client_id):
    return Order.objects.filter(client__id_tg=client_id, status="accepted")

def create_order(client, cake, delivery_date, delivery_time, delivery_address, invoice, comment):
    order = Order.objects.create(
        client=client,
        cake=cake,
        delivery_date=dt.datetime.strptime(delivery_date, "%Y-%m-%d").date(),
        delivery_time=dt.datetime.strptime(delivery_time, "%H").time(),
        delivery_address=delivery_address,
        invoice=invoice,
        comment=comment
    )
    return order


def check_client(id):
    return Client.objects.filter(id_tg__exact=id).exists()


def get_client(id):
    return Client.objects.get(id_tg__exact=id)

def create_invoice(client, cake_price, delivery_date, delivery_time):
    time_frame = get_time_frame()
    date = dt.datetime.strptime(delivery_date, "%Y-%m-%d").date()
    time = dt.datetime.strptime(delivery_time, "%H").time()
    delivery_datetime = dt.datetime.combine(date, time)
    hours_on_delivery = (delivery_datetime - dt.datetime.now()).total_seconds() / 3600
    if hours_on_delivery <= time_frame.maximum_expedited_lead_time:
        cake_price*=1.2
    invoice = Invoice.objects.create(
        client=client,
        amount=cake_price
    )
    return invoice

def create_cake(level, form, topping, berry=None, decor=None, caption=None):
    cake = Cake.objects.create(
        price=level.price+form.price+topping.price+((berry and berry.price) or 0)+((decor and decor.price) or 0),
        level=level,
        form=form,
        topping=topping,
        berry=berry,
        decor=decor,
        caption=caption        
    )
    return cake

def create_client(id, first_name, last_name, username=None, phone_number=None):
    Client.objects.create(
            id_tg=id,
            full_name=f"{first_name} {last_name} aka {username}",
            phone_number=phone_number
        )
    return id


def get_cake(id):
    return Cake.objects.get(id=id)


def get_presets_cakes():
    return Cake.objects.filter(title__isnull=False)


def get_random_preset_cake():
    return random.choice(get_presets_cakes())


def get_levels():
    return Level.objects.all()


def get_level(id):
    return Level.objects.get(id=id)


def get_forms():
    return Form.objects.all()


def get_form(id):
    return Form.objects.get(id=id)


def get_toppings():
    return Topping.objects.all()


def get_topping(id):
    return Topping.objects.get(id=id)


def get_berries():
    return Berry.objects.all()


def get_berry(id):
    if not id:
        return None
    return Berry.objects.get(id=id)


def get_decors():
    return Decor.objects.all()


def get_decor(id):
    if not id:
        return None
    return Decor.objects.get(id=id)
