from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Code(models.Model):
    language = models.CharField(max_length = 100)
    input = models.TextField()
    output = models.TextField(default = "")
    is_public = models.BooleanField(default = False)
    code = models.TextField()
    uptime = models.DecimalField(max_digits=3, decimal_places=2,default = 0.0)
    #owner = models.ForeignKey('User',on_delete = models.CASCADE)   to be linked with user
