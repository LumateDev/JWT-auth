from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Нужно указать действительный адресс почты"))

    def create_user(self, first_name, last_name, email, password, **extra_fields):

        if not first_name:
            raise ValueError(_("Имя не может отсутствовать"))

        if not last_name:
            ValueError(_("Фамилия не может отсутсвовать"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Email не может отсутствовать"))

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=email,
            **extra_fields
        )

        user.set_password(password)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, email, password, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("У superuser должно быть значение is_superuser = True "))

        if extra_fields.get("is_staff")is not True:
            raise ValueError(_("У staff должно быть значение is_staff = True "))

        if not password:
            raise ValueError(_("У superuser должен быть пароль"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Email не может отсутствовать"))

        user = self.create_user(first_name, last_name, email, password, **extra_fields)
        user.save()
        return user
