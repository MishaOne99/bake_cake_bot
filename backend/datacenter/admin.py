from django.contrib import admin

from .vc_api import get_link_click_count, get_shortened_link

from .models import (
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
    actions = ['get_count_clicks', 'get_shorten_url']
    
    @admin.action(description='Узнать количество переходов')
    def get_count_clicks(self, requests, queryset):
        for obj in queryset:
            obj.visits_number = get_link_click_count(obj.short_url)
            obj.save()

    @admin.action(description='Сократить ссылки')
    def get_shorten_url(self, requests, queryset):
        for obj in queryset:
            obj.short_url = get_shortened_link(obj.url)
            obj.save()

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
