from django.db import models


class Link(models.Model):
    orig = models.CharField(max_length=512)
    short = models.CharField(max_length=5, unique=True)
    extra = models.BooleanField(default=False)

    def __str__(self):
        return {self.short}


class Stats(models.Model):
    ip = models.BigIntegerField()
    short = models.ForeignKey(Link, on_delete=models.CASCADE, to_field='short')
    date = models.DateTimeField('Get request time')
    long = models.IntegerField()
    lat = models.IntegerField()
    agent = models.CharField(max_length=128)

    def __str__(self):
        return str(self.ip)
