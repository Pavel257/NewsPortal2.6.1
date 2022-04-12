from django.contrib import admin
from .models import Appointment, Appoint


class ApoAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in Appointment._meta.get_fields()]
    list_display = ('client_name', 'message', 'date')


admin.site.register(Appointment, ApoAdmin)
admin.site.register(Appoint)






