from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверяем, что имя пользователя != me."""

    if value.lower() == 'me':
        raise ValidationError(
            ("Имя зарезервировано."),
            params={'value': value},
        )
