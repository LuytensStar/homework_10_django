from django.contrib.auth.models import User
from django.db import models

class Author(models.Model):
    fullname = models.CharField(max_length=200, null=False)
    born_date = models.CharField(max_length=50,blank=True)
    born_location = models.CharField(max_length=50, blank=True)
    description = models.CharField(max_length=10000, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','fullname'],name='author of username')

        ]

    def __str__(self):
        return f"{self.fullname}"

class Quote(models.Model):
    author = models.OneToOneField(Author, on_delete=models.CASCADE)
    quote = models.CharField(max_length=1000, null=False)
    tags = models.TextField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='quotes')

    def __str__(self):
        return f"{self.quote}"





