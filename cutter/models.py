from django.db import models


class Link(models.Model):
    short = models.CharField(max_length=5, unique=True)
    orig = models.CharField(max_length=512)
    extra = models.BooleanField(default=False)

    def __str__(self):
        return self.short


class Stats(models.Model):
    ip = models.CharField(max_length=15)
    short = models.ForeignKey(Link, on_delete=models.CASCADE, to_field='short')
    date = models.DateTimeField('Get request time')
    long = models.IntegerField()
    lat = models.IntegerField()
    agent = models.CharField(max_length=128)

    def __str__(self):
        return self.ip
