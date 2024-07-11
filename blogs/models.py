from django.db import models
from django.utils import timezone

from ckeditor.fields import RichTextField


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    name = models.CharField(max_length=30)
    mini_content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    web_image = models.ImageField()
    mobile_image = models.ImageField()
    view_count = models.PositiveIntegerField(default=0)
    # seo content
    meta_title = models.CharField(max_length=200,default="")
    meta_description = models.TextField(default="")
    meta_keywords = models.TextField(default="")







    def __str__(self):
        return self.title
