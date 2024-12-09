from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    image = models.ImageField(upload_to='location_images/', blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    weather = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['latitude', 'longitude']),
            models.Index(fields=['name']),
        ]
        verbose_name = "Location"
        verbose_name_plural = "Locations"

    def __str__(self):
        return f"{self.name} ({self.latitude}, {self.longitude})"
