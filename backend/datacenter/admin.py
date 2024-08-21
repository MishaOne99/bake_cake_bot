from django.contrib import admin

from .models import (
    TimeFrames, Client, Level, Form,
    Topping, Decor, Cake, Berry,
    Order, Appointment
)

admin.site.register(Client)
admin.site.register(Level)
admin.site.register(Form)
admin.site.register(Topping)
admin.site.register(Decor)
admin.site.register(Cake)
admin.site.register(Berry)
admin.site.register(Order)
admin.site.register(Appointment)
admin.site.register(TimeFrames)
