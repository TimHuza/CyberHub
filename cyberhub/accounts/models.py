from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    """CyberHub's user: Django's built-in User plus appearance preferences."""

    class ColorMode(models.TextChoices):
        LIGHT = "light", "Light"
        DARK = "dark", "Dark"

    MIN_FONT_SIZE = 12
    MAX_FONT_SIZE = 24

    color_mode = models.CharField(max_length=5, choices=ColorMode.choices, default=ColorMode.DARK)
    font_size = models.PositiveSmallIntegerField(default=16, validators=[MinValueValidator(MIN_FONT_SIZE), MaxValueValidator(MAX_FONT_SIZE)])
