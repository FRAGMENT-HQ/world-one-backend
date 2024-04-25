from django.db import models

class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now_add=True,null=True,blank=True) 
    class Meta: 
        abstract = True

class TimeRecordMixin(TimeStampMixin):
    start_time = models.TimeField(auto_now_add=True,null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    class Meta: 
        abstract = True