from django.db import models
from django.contrib.auth.models import User

class Location(models.Model):
    name = models.CharField(max_length=100)  # City name
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    country = models.CharField(null=True, blank=True, max_length=50)

    def __str__(self):
        return f"{self.name}, {self.country}"

class WeatherData(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date_time = models.DateTimeField()  # date + time for precise data
    temperature = models.FloatField()
    feels_like = models.FloatField() 
    pressure = models.IntegerField()  # hPa
    humidity = models.IntegerField()  # %
    description = models.CharField(max_length=100) 
    icon = models.CharField(max_length=10)  # weather condition icon code

    def __str__(self):
        return f"Weather for {self.location.name} on {self.date_time.strftime('%Y-%m-%d %H:%M:%S')}"

class Forecast(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    date = models.DateField()
    min_temperature = models.FloatField()
    max_temperature = models.FloatField()
    description = models.CharField(max_length=100)
    icon = models.CharField(max_length=10)  # Weather condition icon code

    def __str__(self):
        return f"Forecast for {self.location.name} on {self.date}"

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'location')  # Prevent duplicate subscriptions

    def __str__(self):
        return f"{self.user.username} - {self.location.name}"

class Observation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='observations')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='observations')
    name = models.CharField(max_length=255)
    temperature = models.FloatField()
    feels_like = models.FloatField()  
    min_temperature = models.FloatField()  
    max_temperature = models.FloatField() 
    pressure = models.IntegerField()  
    humidity = models.IntegerField()
    date_of_review = models.DateTimeField()
    state = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='observation_icons/', blank=True, null=True)
    commentary = models.TextField()

    def __str__(self):
        return f"{self.name} by {self.user.username} on {self.date_of_review.strftime('%Y-%m-%d')}"

