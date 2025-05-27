from django.contrib.auth.backends import ModelBackend
from .models import Nutzer

class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Nutzer.objects.get(email=email)
            if user.check_password(password):
                return user
        except Nutzer.DoesNotExist:
            return None
