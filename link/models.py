from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ShareLink(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, default=None, null=True)
    share_code = models.CharField(max_length=30)
    redirect_timer = models.IntegerField(default=5)
    redirect_to = models.URLField()
    valid_until = models.DateTimeField()
    allowed_redirects = models.IntegerField(default=-1)
    redirects = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    is_sharable = models.BooleanField(default=True)
