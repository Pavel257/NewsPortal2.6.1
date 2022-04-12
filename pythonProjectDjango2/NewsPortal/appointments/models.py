from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow, verbose_name='Дата обращения'
    )
    client_name = models.CharField(
        max_length=200, verbose_name='Имя клиента'
    )
    message = models.TextField(verbose_name='Сообщение клиента')

    def __str__(self):
        return f'{self.client_name}: {self.message}'

    class Meta:
        verbose_name = "Записаться на приём"
        verbose_name_plural = "Записаться на приём"


class Appoint(models.Model):
    idpk = models.IntegerField()
    idpkid = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.idpk}'