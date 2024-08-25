import datetime as dt

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Client(models.Model):
    id_tg = models.IntegerField(
        "id в телеграмм", blank=True, null=True, unique=True
    )
    full_name = models.CharField("ФИО", max_length=200)
    phone_number = PhoneNumberField("Номер телефона", null=True, region="RU")

    def __str__(self) -> str:
        return self.full_name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Level(models.Model):
    title = models.CharField("Название уровня", max_length=200)
    price = models.FloatField("Цена")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Размер/уровень для торта"
        verbose_name_plural = "Размеры/уровни для торта"


class Form(models.Model):
    title = models.CharField("Название формы", max_length=200)
    price = models.FloatField("Цена")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Форма для торта"
        verbose_name_plural = "Формы для торта"


class Topping(models.Model):
    title = models.CharField("Название топпинга", max_length=200)
    price = models.FloatField("Цена")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Топпинг для торта"
        verbose_name_plural = "Топпинги для торта"


class Berry(models.Model):
    title = models.CharField("Название ягоды", max_length=200)
    price = models.FloatField("Цена")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Ягода для торта"
        verbose_name_plural = "Ягоды для торта"


class Decor(models.Model):
    title = models.CharField("Название декора", max_length=200)
    price = models.FloatField("Цена")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "Декор для торта"
        verbose_name_plural = "Декоры для торта"


class Cake(models.Model):
    title = models.CharField(
        "Название торта", max_length=200, null=True, blank=True
    )
    price = models.FloatField("Цена торта")
    image = models.ImageField("Изображение торта", null=True, blank=True)
    level = models.ForeignKey(
        Level,
        on_delete=models.PROTECT,
        verbose_name="Количество уровней торта",
    )
    form = models.ForeignKey(
        Form, on_delete=models.PROTECT, verbose_name="Форма торта"
    )
    topping = models.ForeignKey(
        Topping, on_delete=models.PROTECT, verbose_name="Топпинг"
    )
    berry = models.ForeignKey(
        Berry,
        on_delete=models.PROTECT,
        verbose_name="Ягода",
        null=True,
        blank=True,
    )
    decor = models.ForeignKey(
        Decor,
        on_delete=models.PROTECT,
        verbose_name="Декор",
        null=True,
        blank=True,
    )
    caption = models.CharField(
        "Надпись на торте", max_length=200, null=True, blank=True
    )

    def __str__(self) -> str:
        return self.title or "Кастом"

    class Meta:
        verbose_name = "Торт"
        verbose_name_plural = "Торты"


class Invoice(models.Model):
    STATUS = [
        ("waiting", "Ожидает оплаты"),
        ("paid", "Оплачено"),
        ("canceled", "Отменено"),
    ]
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Клиент"
    )
    status = models.CharField("Статус счета", max_length=14, choices=STATUS, default="waiting")
    receipt = models.URLField("Чек", blank=True, null=True)
    created_at = models.DateTimeField("Счёт выставлен", auto_now_add=True)
    updated_at = models.DateTimeField("Последнее обновление", auto_now=True)

    def __str__(self) -> str:
        return f"{self.updated_at} {self.client.full_name} {self.status}"

    class Meta:
        verbose_name = "Счет на оплату"
        verbose_name_plural = "Счета на оплату"



class Order(models.Model):
    STATUSES = [
        ("accepted", "Принят"),
        ("closed", "Закрыт"),
        ("canceled", "Отменен"),
    ]
    status = models.CharField("Статус заказа", max_length=9, choices=STATUSES)
    date = models.DateField("Дата заказа", auto_now_add=True)
    time = models.TimeField("Время заказа", auto_now_add=True)
    client = models.ForeignKey(
        Client, on_delete=models.PROTECT, verbose_name="Клиент"
    )
    cake = models.ForeignKey(
        Cake, on_delete=models.PROTECT, verbose_name="Торт"
    )
    delivery_date = models.DateField("Дата доставки")
    delivery_time = models.TimeField("Время доставки")
    delivery_address = models.TextField(
        verbose_name="Адрес доставки",
        max_length=200,
        null=True,
        blank=True
    )
    invoice = models.ForeignKey(
        Invoice, on_delete=models.PROTECT, verbose_name="Счет на оплату"
    )
    comment = models.CharField(
        "Комментарий для курьера",
        max_length=200,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.status} {self.date} {self.cake.title} {self.client.full_name}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


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

    def __str__(self) -> str:
        return f"{self.workday_start}-{self.workday_end}, {self.minimum_lead_time}, {self.maximum_expedited_lead_time}"

    class Meta:
        verbose_name = "Временные рамки"
        verbose_name_plural = "Временные рамки"


class AdvLink(models.Model):
    url = models.URLField("Ссылка")
    short_url = models.URLField('Сокращенная ссылка', blank=True)
    visits_number = models.IntegerField(
        "Количество визитов",
        default=0
    )

    class Meta:
        verbose_name = "Рекламную ссылку"
        verbose_name_plural = "Рекламные ссылки"
