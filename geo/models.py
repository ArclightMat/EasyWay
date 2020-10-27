from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    pass


class Rank(models.Model):
    classification = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.classification


class AccessibleLocal(models.Model):
    name = models.CharField(max_length=100)
    comments = models.CharField(max_length=255, default="", blank=True)
    location = models.PointField()
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
