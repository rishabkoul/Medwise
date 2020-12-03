from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import pre_save
from datetime import datetime
from query.models import Query

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    phone = models.BigIntegerField(null=True, blank=True, unique=True)
    qualification = models.CharField(max_length=50, null=True, blank=True)
    year_of_ex = models.IntegerField(null=True, blank=True)
    comment_on = models.ManyToManyField(Query, related_name="commented_on")
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published")
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.user.email


def pre_save_userprofile_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.user.username+str(instance.user.pk))


pre_save.connect(pre_save_userprofile_receiver, sender=UserProfile)
