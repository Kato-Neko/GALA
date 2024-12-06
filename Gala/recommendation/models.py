from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    weather = models.CharField(max_length=255)
    address = models.CharField(max_length=500, blank=True, null=True) 

    def __str__(self):
        return self.name
