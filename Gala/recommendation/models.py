from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    longitude = models.FloatField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    weather = models.CharField(max_length=50)

    def __str__(self):
        return self.name