from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import datetime, date

from authentication.models import Profile


# Create your models here.


class attached_documents(models.Model):

    associated_doc = models.FileField(upload_to='Tasks_Documents', blank=True, verbose_name='Associated Document')
    proof_of_completion = models.FileField(upload_to='Tasks_Complete_Documents', blank=True, verbose_name='Complete Proof Document')
    def __int__(self):
        return self.id
    class Meta:
        verbose_name_plural = 'Associated Doc'

class Task(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(max_length=2000, null=True, blank=True)
    complete = models.BooleanField(default=False)
    nature_of_task = models.CharField(max_length=2000, null=True, blank=False)
    associated_documents = models.ManyToManyField(attached_documents, null=True, blank=True)

    creation_date = models.DateField(default=timezone.now)
    ending_date = models.DateField(editable=True,null=True, blank=False)

    def __str__(self):
        return self.title

    def is_end_date(self):
        if date.today() > self.ending_date:
            if not self.complete:
                return True
            else:
                pass
        else:
            pass


    class Meta:
        ordering = ['creation_date']
