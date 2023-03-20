
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=25, blank=True, unique=True, null=True)

    picture = models.ImageField(upload_to='Profil_Images', blank=True)



    gender = models.CharField(max_length=25, blank=True, null=True)
    profession = models.CharField(max_length=25, blank=True, null=True)

    otp = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.owner.email

    class Meta:
        verbose_name_plural = 'Profile'