from django.shortcuts import render, reverse, redirect
from django.views import View
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from datetime import datetime
from django.core.mail import mail_admins, send_mail, mail_managers  # импортируем функцию для массовой отправки писем админам
from django.template.loader import render_to_string  # импортируем функцию, которая срендерит наш html в текст
from .models import Appointment



class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'make_appointment.html', {})

    def post(self, request, *args, **kwargs):
        appointment = Appointment(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['client_name'],
            message=request.POST['message'],
        )
        appointment.save()


        send_mail(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',
            # имя клиента и дата записи будут в теме для удобства
            message=appointment.message,  # сообщение с кратким описанием проблемы
            from_email='st3p.pavel@yandex.ru',  # здесь указываете почту, с которой будете отправлять (об этом попозже)
            recipient_list=['stepa.hax@gmail.com']  # здесь список получателей. Например, секретарь, сам врач и т. д.
        )
        # # отправляем письмо всем админам по аналогии с send_mail, только здесь получателя указывать не надо
        # mail_admins(
        #     subject=f'{appointment.client_name} {appointment.date.strftime("%d %m %Y")}',
        #     message=appointment.message,
        # )
        # # получаем наш html
        html_content = render_to_string(
            'appointment_created.html',
            {
                'appointment': appointment,
            }
        )

        # # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{appointment.client_name} {appointment.date.strftime("%Y-%M-%d")}',   # имя клиента и дата записи будут в теме для удобства
            body=appointment.message,  # это то же, что и message
            from_email='st3p.pavel@yandex.ru',
            to=['stepa.hax@gmail.com'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        # msg.send()  # отсылаем

        return redirect('appointments:make_appointment')



