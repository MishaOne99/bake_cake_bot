from django.contrib import admin

from .vc_api import get_short_link_and_click_count

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


@admin.register(AdvLink)
class AdvLinkAdmin(admin.ModelAdmin):
    list_display = ('url', 'short_url', 'visits_number')
    ordering = ['visits_number']
    actions = ['count_clicks']
    
    @admin.action(description='Узнать количество переходов')
    def count_clicks(self, requests, queryset):
        url = queryset.values_list('url', flat=True)
        short_url, click_count = get_short_link_and_click_count(url[0])
        queryset.update(short_url=short_url, visits_number=click_count)


admin.site.register(Address)
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
