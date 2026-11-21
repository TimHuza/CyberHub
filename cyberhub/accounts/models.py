from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """CyberHub's user.

    Empty on purpose: it behaves exactly like Django's built-in User today.
    Having our own class from the start means we can add fields later
    (e.g. a display name) with a normal migration instead of a painful swap.
    """
