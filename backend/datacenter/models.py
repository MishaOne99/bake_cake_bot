from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import datetime as dt


class Client(models.Model):

    id_tg = models.IntegerField(
        "id в телеграмм", blank=True, null=True, unique=True
    )
    full_name = models.CharField("ФИО", max_length=200)
    phone_number = PhoneNumberField(null=True, region="RU")

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = 'Клиент',
        verbose_name_plural = 'Клиенты'


class Level(models.Model):

    title = models.CharField("Название уровня", max_length=200)
    price = models.FloatField('Цена')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Размер/уровень для торта',
        verbose_name_plural = 'Размеры/уровни для торта'


class Form(models.Model):
    title = models.CharField("Название формы", max_length=200)
    price = models.FloatField('Цена')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Форма для торта',
        verbose_name_plural = 'Формы для торта'


class Topping(models.Model):
    title = models.CharField("Название топпинга", max_length=200)
    price = models.FloatField('Цена')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Топпинг для торта',
        verbose_name_plural = 'Топпинги для торта'


class Berry(models.Model):
    title = models.CharField("Название ягоды", max_length=200)
    price = models.FloatField('Цена')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Ягода для торта',
        verbose_name_plural = 'Ягоды для торта'


class Decor(models.Model):
    title = models.CharField("Название декора", max_length=200)
    price = models.FloatField('Цена')

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = 'Декор для торта',
        verbose_name_plural = 'Декоры для торта'


class Cake(models.Model):
    title = models.CharField(
        "Название торта", max_length=200, null=True, blank=True
    )
    price = models.FloatField("Цена торта")
    level = models.ForeignKey(
        Level, on_delete=models.PROTECT,
        verbose_name="Количество уровней торта"
    )
    form = models.ForeignKey(
        Form, on_delete=models.PROTECT, verbose_name="Форма"
    )
    topping = models.ForeignKey(
        Topping, on_delete=models.PROTECT, verbose_name="Топпинг"
    )
    berry = models.ForeignKey(
        Berry, on_delete=models.PROTECT, verbose_name="Ягода",
        null=True, blank=True
    )
    decor = models.ForeignKey(
        Decor, on_delete=models.PROTECT, verbose_name="Декор",
        null=True, blank=True
    )
    inscription = models.CharField(
        "Надпись на торте", max_length=200, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.title or 'Кастом'

    class Meta:
        verbose_name = 'Торт',
        verbose_name_plural = 'Торты'


class Order(models.Model):
    STATUS = [
        ("waiting", "Ожидает оплаты"),
        ("paid", "Оплачено"),
        ("cancel", "Отменено"),
    ]
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Клиент"
    )
    status = models.CharField("Статус заказа", max_length=14, choices=STATUS)
    receipt = models.URLField("Чек", blank=True)
    created_at = models.DateTimeField("Счёт выставлен", auto_now_add=True)
    updated_at = models.DateTimeField("Последнее обновление", auto_now=True)

    def __str__(self) -> str:
        return f"{self.updated_at} {self.client.full_name} {self.status}"

    class Meta:
        verbose_name = 'Счет на оплату',
        verbose_name_plural = 'Счета на оплату'


class Appointment(models.Model):
    STATUSES = [
        ("accepted", "Принято"),
        ("ended", "Завершено"),
        ("discard", "Отменено"),
    ]
    status = models.CharField("Статус заказа", max_length=9, choices=STATUSES)
    date = models.DateField("Дата доставки")
    time = models.TimeField("Время доставки")
    extra_delivery_speed = models.BooleanField(
        "Доп. плата за скорость доставки", default=False
    )
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    cake = models.ForeignKey(Cake, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f"{self.status} {self.date} {self.cake.title} {self.client.full_name}"

    class Meta:
        verbose_name = 'Заказ',
        verbose_name_plural = 'Заказы'


class TimeFrames(models.Model):
    workday_start = models.TimeField(
        "Время начала рабочего дня", default=dt.time(hour=9)
    )
    workday_end = models.TimeField(
        "Время окончания рабочего дня", default=dt.time(hour=18)
    )
    minimum_lead_time = models.IntegerField(
        "Минимальное время доставки (в часах)", default=12
    )
    maximum_expedited_lead_time = models.IntegerField(
        "Максимальное время ускоренной доставки (в часах)", default=24
    )

    class Meta:
        verbose_name = 'Временные рамки',
        verbose_name_plural = 'Временные рамки'
