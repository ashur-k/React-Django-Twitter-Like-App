import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Tweet(models.Model):
    # id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # many users can many tweets
    content = models.TextField(blank=True, null=True)
    images = models.FileField(upload_to='images/', blank=True, null=True)

    class Meta:
        ordering = ['-id']

    def serialize(self):
        return{
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 200)
        }
