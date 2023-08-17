from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BookInfo(models.Model):
    id=models.AutoField(primary_key=True);
    title=models.CharField(max_length=1000,default="")
    authors=models.CharField(max_length=200, default="")
    pageCount=models.IntegerField(default=0);
    averageRating=models.FloatField(default=0);
    user=models.ForeignKey(User, on_delete=models.CASCADE)