#with open('extra_scripts/db_fake_data_fill.py') as f:
#    exec(f.read())

import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

from datacenter.models import (
    Address,
    AdvLink,
    Berry,
    Cake,
    Client,
    Decor,
    Form,
    Invoice,
    Level,
    Order,
    TimeFrames,
    Topping,
)


# �������� ��������� ����� (�� ���������)
TimeFrames.objects.create()

# �������� ��������
Client.objects.create(
    id_tg=100, full_name="�����", phone_number="+79004217012"
)
Client.objects.create(id_tg=101, full_name="����", phone_number="+79004216012")
Client.objects.create(
    id_tg=102, full_name="���������", phone_number="+79004215012"
)
Client.objects.create(
    id_tg=103, full_name="�������", phone_number="+79004214012"
)
Client.objects.create(
    id_tg=104, full_name="��������", phone_number="+79004213012"
)
Client.objects.create(
    id_tg=105, full_name="���������", phone_number="+79004212012"
)
Client.objects.create(
    id_tg=106, full_name="��������", phone_number="+79004211012"
)

# �������� �������
Level.objects.create(title="1 �������", price=400)
Level.objects.create(title="2 ������", price=750)
Level.objects.create(title="3 ������", price=1100)

# �������� ����
Form.objects.create(title="�������", price=600)
Form.objects.create(title="����", price=400)
Form.objects.create(title="�������������", price=1000)

# �������� ���������
Topping.objects.create(title="��� ��������", price=0)
Topping.objects.create(title="����� ����", price=200)
Topping.objects.create(title="����������� �����", price=180)
Topping.objects.create(title="�������� �����", price=200)
Topping.objects.create(title="���������� �����", price=300)
Topping.objects.create(title="��������� �����", price=350)
Topping.objects.create(title="�������� �������", price=200)

# �������� ����
Berry.objects.create(title="�������", price=400)
Berry.objects.create(title="������", price=300)
Berry.objects.create(title="��������", price=450)
Berry.objects.create(title="��������", price=500)

# �������� ������
Decor.objects.create(title="��������", price=300)
Decor.objects.create(title="����", price=400)
Decor.objects.create(title="������", price=350)
Decor.objects.create(title="�����", price=300)
Decor.objects.create(title="����������", price=200)
Decor.objects.create(title="��������", price=280)

# �������� ������
cakes_titles = [
    "��������",
    "��������",
    "������� ������",
    "�������",
    "���������� ����",
    "��������� ���",
    "��������� ����",
    "��������� ������",
    "���������",
    "�����",
    "",
    "�������� ���",
    "��������",
    "����-�����",
    "",
]


image_mapping = {
    "napoleon.jpg": "��������",
    "tiramisu.jpg": "��������",
    "krasnii-barkhat.jpg": "������� ������",
    "medovik.jpg": "�������",
    "shokoladnii-muss.jpg": "���������� ����",
    "fruktovii-sad.jpg": "��������� ���",
    "morkovnii-tort.jpg": "��������� ����",
    "vanilnoye-yabloko.jpg": "��������� ������",
    "smetannik.jpg": "���������",
    "praga.jpg": "�����",
    "orekhoviy-ray.jpg": "�������� ���",
    "kappuchino.jpg": "��������",
    "krem-bryule.jpg": "����-�����",
    "custom.jpg": None,  # �������
}

cake_captions = [
    "� ��� ��������!",
    "����� ����!",
    "������� �����",
    "������� � �������!",
    "������ ������",
    "������ ����!",
    "� �������!",
    "������� ����",
    "������ ������",
    "�� ������ ������",
]

levels = list(Level.objects.all())
forms = list(Form.objects.all())
toppings = list(Topping.objects.all())
berries = list(Berry.objects.all())
decors = list(Decor.objects.all())

for image, title in image_mapping.items():
    level = random.choice(levels)
    form = random.choice(forms)
    topping = random.choice(toppings)
    berry = random.choice(berries)
    decor = random.choice(decors)
    caption = random.choice(cake_captions) if not title else ""
    Cake.objects.create(
        title=title,
        image=image,
        price=level.price
        + form.price
        + topping.price
        + berry.price
        + decor.price,
        level=level,
        form=form,
        topping=topping,
        berry=berry,
        decor=decor,
        caption=caption,
    )

Address.objects.create(city="������", street="��������, 21", flat=23)
Address.objects.create(city="������", street="�����������������, 46", flat=355)
Address.objects.create(
    city="�������", street="����������� ��������, 101", flat=123
)
Address.objects.create(city="�����", street="��������, 4�", flat=145)
Address.objects.create(city="��������", street="������� ������, 46", flat=299)

# �������� �������
cakes = Cake.objects.all()
clients = list(Client.objects.all())
addresses = list(Address.objects.all())

for cake in cakes:
    client = random.choice(clients)
    address = random.choice(addresses)
    receipt_id = random.randint(100, 999)
    receipt = f"https://receipt.com/id={receipt_id}"
    day = random.randint(1, 24)
    date = f"2024-08-{day:02d}"
    hour = random.randint(9, 17)
    minute = random.randint(1, 59)
    time = f"{hour:02d}:{minute:02d}"
    delivery_date = f"2024-08-{day+1:02d}"
    delivery_time = f"{hour:02d}:00"

    Invoice.objects.create(
        client=client,
        status="paid",
        receipt=receipt,
    )
    invoice = Invoice.objects.last()

    Order.objects.create(
        status="accepted",
        date=date,
        time=time,
        client=client,
        cake=cake,
        delivery_date=delivery_date,
        delivery_time=delivery_time,
        delivery_address=address,
        invoice=invoice,
        comment="������� �� ��� �� �������. � ����� ��������� 3 ����"
        if cake.title
        in [
            "��������",
            "��������",
            "������� ������",
            "�������",
        ]
        else "",
    )
    