from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Label(models.Model):
    name = models.CharField(max_length=50)

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(null=True,blank=True,upload_to = 'images/' )

    def __str__(self):
        return self.title + "\n" + self.description