from django.db import models
from django.contrib.auth.models import User

class EmailDevice(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    email = models.EmailField()

    def verify_otp(self, otp):
        return self.otp == otp
