from django.db import models
from django.contrib.auth.models import User

class CitySubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.city_name)
