from django.core.mail import send_mail


def send_confirmation_email(user, code):
    full_link = f'http://localhost:8000/api/v1/accounts/activate/{code}/'
    full_link_server = f'http://35.188.106.94:8000/api/v1/accounts/activate/{code}/'
    send_mail(
        'Здравствуйте, активируйте ваш аккаунт!',
        f'Чтобы активировать ваш аккаунт нужно перейти по ссылке: \n{full_link}\n{full_link_server}',
        'kazakovdanier24@gmail.com',
        [user],
        fail_silently=False
    )


def send_notification(user_email, order_id, price):
    send_mail(
        'Уведомление о создании заказа.',
        f'''Вы создали заказ №{order_id}, ожидайте звонка!\nПолная стоимость вашего заказа - {price}.
        Спасибо, что выбрали нас!''',
        'from@example.com',
        [user_email],
        fail_silently=False
    )