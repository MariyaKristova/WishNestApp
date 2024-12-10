from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def normalize_email(self, email):
        email = email.lower().strip()
        return super().normalize_email(email)

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Please provide an email address')

        email = self.normalize_email(email)
        try:
            self.model.objects.get(email__iexact=email)
            raise ValueError('A user with this email already exists')
        except self.model.DoesNotExist:
            pass

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
