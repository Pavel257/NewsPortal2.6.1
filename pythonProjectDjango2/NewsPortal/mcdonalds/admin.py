from django.contrib import admin

from mcdonalds.models import *



class OrderAdmin(admin.ModelAdmin):
    list_display = ('time_in', 'time_out', 'cost', 'take_away', 'complete')
    list_filter = ('time_in', 'time_out', 'cost', 'take_away', 'complete')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    # list_display = [field.name for field in Product._meta.get_fields()]
    list_filter = ('price',)
    list_display_links = ('name',)
    # paginator = 3
    list_editable = ('price', )
    ordering = ('name', '-price', )


admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)