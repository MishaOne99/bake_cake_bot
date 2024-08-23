from django.contrib import admin

from .models import (
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

admin.site.register(Address)
admin.site.register(AdvLink)
admin.site.register(Berry)
admin.site.register(Cake)
admin.site.register(Client)
admin.site.register(Decor)
admin.site.register(Form)
admin.site.register(Invoice)
admin.site.register(Level)
admin.site.register(Order)
admin.site.register(TimeFrames)
admin.site.register(Topping)
