from celery import shared_task
import time
from django.core.mail import EmailMultiAlternatives, send_mail





@shared_task
def send_mail_for_sub_once(sub_username, sub_useremail, html_content):
    print('Таска_на_раз - старт')
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {sub_username}. Новая статья в вашем разделе!',
        from_email='st3p.pavel@yandex.ru',
        to=[sub_useremail]
    )

    msg.attach_alternative(html_content, 'text/html')


    print()
    print(html_content)
    print()

    # код ниже временно заблокирован, чтоб в процессе отладки не производилась реальная рассылка писем
    # msg.send()
    # print('Таска_на_раз - конец')


# таска для еженедельной рассылки писем
@shared_task
def send_mail_for_sub_every_week(sub_username, sub_useremail, html_content):
    print('Таска-неделя - старт')
    msg = EmailMultiAlternatives(
        subject=f'Здравствуй, {sub_username}, новые статьи за прошлую неделю в вашем разделе!',
        from_email='st3p.pavel@yandex.ru',
        to=[sub_useremail]
    )

    print('Таска-неделя - стоп')
    msg.attach_alternative(html_content, 'text/html')
    print()

    # для удобства в консоль выводим содержимое нашего письма, в тестовом режиме проверим, что и
    # кому отправляем
    print(html_content)

    # Чтобы запустить реальную рассылку нужно раскоментить нижнюю строчку
    # msg.send()


