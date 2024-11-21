from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    distance = models.CharField(max_length=50)
    weather = models.CharField(max_length=50)

    def __str__(self):
        return self.name