import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise ValidationError(_('Некорректный email адрес.'))

def validate_username(username):
    if len(username) < 3:
        raise ValidationError(_('Имя пользователя должно содержать не менее 3 символов.'))
    if not username.isalnum():
        raise ValidationError(_('Имя пользователя может содержать только буквы и цифры.'))

def validate_password(password):
    if len(password) < 8:
        raise ValidationError(_('Пароль должен содержать не менее 8 символов.'))
    if not re.search(r'[A-Z]', password):
        raise ValidationError(_('Пароль должен содержать хотя бы одну заглавную букву.'))
    if not re.search(r'[a-z]', password):
        raise ValidationError(_('Пароль должен содержать хотя бы одну строчную букву.'))
    if not re.search(r'\d', password):
        raise ValidationError(_('Пароль должен содержать хотя бы одну цифру.'))
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(_('Пароль должен содержать хотя бы один специальный символ.'))