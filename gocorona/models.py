from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Code(models.Model):
    language = models.CharField(max_length = 100)
    language_id = models.IntegerField()
    stdin = models.TextField(null=True,blank=True, default="")
    stdout = models.TextField(null=True,blank=True, default = "")
    is_public = models.BooleanField(default = False)
    code = models.TextField()
    uptime = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True, default=None)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User,on_delete = models.CASCADE)
    token = models.CharField(max_length=100)