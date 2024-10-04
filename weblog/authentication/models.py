from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
# Modèle utilisateur personnalisé héritant d'AbstractUser

    email = models.EmailField(unique=True)
