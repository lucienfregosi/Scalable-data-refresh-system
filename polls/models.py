from django.db import models


class ServerRequest(models.Model):
    longitude = models.FloatField(default=0)
    latitude = models.FloatField(default=0)
    Accuracy = models.FloatField(default=0)
