from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    es_profesor = models.BooleanField(default=False)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.username
