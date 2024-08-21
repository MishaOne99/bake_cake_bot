
from datacenter.models import TimeFrames, Client, Level, Form, Topping, Decor, Cake, Berry, Order, Appointment
import random

# # # ! запуск через PowerShell команда - >>> exec(open("db_fake_data_fill.py", encoding="utf-8").read())

# Создание временных рамок (по умолчанию)
TimeFrames.objects.create()

# Создание клиентов
Client.objects.create(id_tg=100, full_name='Ричард', phone_number='+79004217012')
Client.objects.create(id_tg=101, full_name='Егор', phone_number='+79004216012')
Client.objects.create(id_tg=102, full_name='Александр', phone_number='+79004215012')
Client.objects.create(id_tg=103, full_name='Николай', phone_number='+79004214012')
Client.objects.create(id_tg=104, full_name='Виктория', phone_number='+79004213012')
Client.objects.create(id_tg=105, full_name='Елизавета', phone_number='+79004212012')
Client.objects.create(id_tg=106, full_name='Христина', phone_number='+79004211012')

client1 = Client.objects.get(id_tg=100)
client2 = Client.objects.get(id_tg=101)
client3 = Client.objects.get(id_tg=102)
client4 = Client.objects.get(id_tg=103)
client5 = Client.objects.get(id_tg=104)
client6 = Client.objects.get(id_tg=105)
client7 = Client.objects.get(id_tg=106)

# Создание уровней
Level.objects.create(title="1 уровень", price=400)
Level.objects.create(title="2 уровеня", price=750)
Level.objects.create(title="3 уровеня", price=1100)

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


cakes_titles = [
    'Наполеон',
    'Тирамису',
    'Красный бархат',
    'Медовик',
    'Шоколадный мусс',
    'Фруктовый сад',
    'Морковный торт',
    'Ванильное облако',
    'Сметанник',
    'Прага',
    'Шарлотка',
    'Ореховый рай',
    'Капучино',
    'Крем-брюле',
    'Павлова'
]

cake_inscriptions = [
    'С Днём Рождения!',
    'Люблю тебя!',
    'Сладкая жизнь',
    'Счастья и радости!',
    'Всегда вместе',
    'Лучший день!',
    'С юбилеем!',
    'Дорогой маме',
    'Вечная любовь',
    'На долгую память'
]

levels = list(Level.objects.all())
forms = list(Form.objects.all())
toppings = list(Topping.objects.all())
berries = list(Berry.objects.all())
decors = list(Decor.objects.all())

for title in cakes_titles:
    level = random.choice(levels)
    form = random.choice(forms)
    topping = random.choice(toppings)
    berry = random.choice(berries)
    decor = random.choice(decors)
    Cake.objects.create(
        title=title,
        price=level.get('price')+form.get('price')+topping.price+berry.price+decor.price,
        level=level,
        form=form,
        topping=topping,
        berry=berry,
        decor=decor
    )
