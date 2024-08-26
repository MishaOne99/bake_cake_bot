#with open('extra_scripts/db_fake_data_fill.py') as f:
#    exec(f.read())

import os
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import django
django.setup()

from datacenter.models import (
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

# Создание временных рамок (по умолчанию)
TimeFrames.objects.create()

# Создание клиентов
Client.objects.create(
    id_tg=100, full_name="Роман", phone_number="+79004217012"
)
Client.objects.create(id_tg=101, full_name="Егор", phone_number="+79004216012")
Client.objects.create(
    id_tg=102, full_name="Александр", phone_number="+79004215012"
)
Client.objects.create(
    id_tg=103, full_name="Николай", phone_number="+79004214012"
)
Client.objects.create(
    id_tg=104, full_name="Виктория", phone_number="+79004213012"
)
Client.objects.create(
    id_tg=105, full_name="Елизавета", phone_number="+79004212012"
)
Client.objects.create(
    id_tg=106, full_name="Кристина", phone_number="+79004211012"
)

# Создание уровней
Level.objects.create(title="1 уровень", price=400)
Level.objects.create(title="2 уровня", price=750)
Level.objects.create(title="3 уровня", price=1100)

# Создание форм
Form.objects.create(title="Квадрат", price=600)
Form.objects.create(title="Круг", price=400)
Form.objects.create(title="Прямоугольник", price=1000)

# Создание топпингов
Topping.objects.create(title="Без топпинга", price=0)
Topping.objects.create(title="Белый соус", price=200)
Topping.objects.create(title="Карамельный сироп", price=180)
Topping.objects.create(title="Кленовый сироп", price=200)
Topping.objects.create(title="Клубничный сироп", price=300)
Topping.objects.create(title="Черничный сироп", price=350)
Topping.objects.create(title="Молочный шоколад", price=200)

# Создание ягод
Berry.objects.create(title="Ежевика", price=400)
Berry.objects.create(title="Малина", price=300)
Berry.objects.create(title="Голубика", price=450)
Berry.objects.create(title="Клубника", price=500)

# Создание декора
Decor.objects.create(title="Фисташки", price=300)
Decor.objects.create(title="Безе", price=400)
Decor.objects.create(title="Фундук", price=350)
Decor.objects.create(title="Пекан", price=300)
Decor.objects.create(title="Маршмеллоу", price=200)
Decor.objects.create(title="Марципан", price=280)

# Создание тортов
image_mapping = {
     "napoleon.jpg": "Наполеон",
     "tiramisu.jpg": "Тирамису",
     "krasnii-barkhat.jpg": "Красный бархат",
     "medovik.jpg": "Медовик",
     "shokoladnii-muss.jpg": "Шоколадный мусс",
     "fruktovii-sad.jpg": "Фруктовый сад",
     "morkovnii-tort.jpg": "Морковный торт",
     "vanilnoye-yabloko.jpg": "Ванильное облако",
     "smetannik.jpg": "Сметанник",
     "praga.jpg": "Прага",
     "orekhoviy-ray.jpg": "Ореховый рай",
     "kappuchino.jpg": "Капучино",
     "krem-bryule.jpg": "Крем-брюле",
     "custom.jpg": None,  # Пропуск
}

# для тестов
#image_mapping = {
#    "https://narodny-konditer.ru/img/gall/big/516.jpg": "Наполеон",
###    "https://narodny-konditer.ru/img/gall/big/513.jpg": "Тирамису",
#    "https://narodny-konditer.ru/img/gall/big/1124.jpg": "Красный бархат",
#    "https://narodny-konditer.ru/img/gall/big/1018.jpg": "Медовик",
#    "https://narodny-konditer.ru/img/gall/big/1078.jpg": "Шоколадный мусс",
#    "https://narodny-konditer.ru/img/gall/big/1445.jpg": "Фруктовый сад",
##    "https://narodny-konditer.ru/img/gall/big/480.jpg": "Морковный торт",
#    "https://narodny-konditer.ru/img/gall/big/1075.jpg": "Ванильное облако",
#    "https://narodny-konditer.ru/img/gall/big/1072.jpg": "Сметанник",
##    "https://narodny-konditer.ru/img/gall/big/1448.jpg": "Прага",
#    "https://narodny-konditer.ru/img/gall/big/1063.jpg": "Ореховый рай",
#    "https://narodny-konditer.ru/img/gall/big/492.jpg": "Капучино",
#    "https://narodny-konditer.ru/img/gall/big/1102.jpg": "Крем-брюле",
#    "https://narodny-konditer.ru/img/gall/big/531.jpg": None,  # Пропуск
#}

cake_captions = [
    "С Днём Рождения!",
    "Люблю тебя!",
    "Сладкая жизнь",
    "Счастья и радости!",
    "Всегда вместе",
    "Лучший день!",
    "С юбилеем!",
    "Дорогой маме",
    "Вечная любовь",
    "На долгую память",
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

addresses = [
    "Москва, Тверская, 21, кв. 23",
    "Москва, Краснопресненская, 46, кв. 355",
    "Люберцы, Октябрьский проспект, 101, кв. 123",
    "Химки, Калинина, 4А, кв. 145",
    "Одинцово, Маршала Жукова, 46, кв. 299"
]
# Создание заказов
cakes = Cake.objects.all()
clients = list(Client.objects.all())

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
        amount=cake.price
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
        comment="Набрать за час до приезда. В дверь постучать 3 раза"
        if cake.title
        in [
            "Наполеон",
            "Тирамису",
            "Красный бархат",
            "Медовик",
        ]
        else "",
    )

AdvLink.objects.create(url="https://vk.cc/czLk7z")
AdvLink.objects.create(url="https://vk.cc/czLk8u")
AdvLink.objects.create(url="https://vk.cc/czJVIu")
AdvLink.objects.create(url="https://vk.cc/czLcvF")
