from django.contrib.auth.models import User
from django.db import models


class CitySubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return str(self.city_name)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city_subscription = models.ForeignKey(
        CitySubscription, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.city_subscription.city_name}"
