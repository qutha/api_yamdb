from api_yamdb.settings import ADMIN_EMAIL
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    admin_email = ADMIN_EMAIL
    user_email = [user.email]
    subject = 'Код подтверждения регистрации'
    message = f'{confirmation_code} - код регистрации'
    return send_mail(subject, message, admin_email, user_email)
