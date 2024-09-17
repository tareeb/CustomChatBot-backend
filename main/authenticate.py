from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class UserProfileBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Get the user profile for the given username
            user = User.objects.get(username=username)

            # Authenticate the user using the password provided
            if user.check_password(password):
                return user

        except User.DoesNotExist:
            # If the user profile does not exist, return None
            return None
