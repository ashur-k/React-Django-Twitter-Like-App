from django.db import models


class Tweet(models.Model):
    # id = models.AutoField(primary_key=True)
    content = models.TextField(blank=True, null=True)
    images = models.FileField(upload_to='images/', blank=True, null=True)
