from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
from datetime import datetime
from django.core.exceptions import ValidationError
from account.models import Account


def file_size(value):  # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')

# Create your models here.


def upload_loaction(instance, filename, **kwargs):
    file_path = 'queries/{patient_id}/{heading}+{datetiming}+{filename}'.format(
        patient_id=str(instance.patient.id), heading=str(instance.heading), filename=filename, datetiming=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    )
    return file_path


class Query(models.Model):
    heading = models.TextField(max_length=100, null=False, blank=False)
    body = models.TextField(max_length=2500, null=False, blank=False)
    image = models.FileField(
        upload_to=upload_loaction, null=True, blank=True, validators=[file_size])
    image2 = models.FileField(
        upload_to=upload_loaction, null=True, blank=True, validators=[file_size])
    image3 = models.FileField(
        upload_to=upload_loaction, null=True, blank=True, validators=[file_size])
    image4 = models.FileField(
        upload_to=upload_loaction, null=True, blank=True, validators=[file_size])
    image5 = models.FileField(
        upload_to=upload_loaction, null=True, blank=True, validators=[file_size])
    image6 = models.FileField(
        upload_to=upload_loaction, null=True, blank=True, validators=[file_size])
    image7 = models.FileField(
        upload_to=upload_loaction, null=True, blank=True, validators=[file_size])
    image8 = models.FileField(
        upload_to=upload_loaction, null=True, blank=True, validators=[file_size])
    image9 = models.FileField(
        upload_to=upload_loaction, null=True, blank=True, validators=[file_size])
    image10 = models.FileField(
        upload_to=upload_loaction, null=True, blank=True, validators=[file_size])
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published")
    date_updated = models.DateTimeField(
        auto_now=True, verbose_name="date updated")
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    commented_by = models.ManyToManyField(Account, related_name="commented_by")
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.heading


@receiver(post_delete, sender=Query)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


def pre_save_query_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        info = (instance.heading[30]) if len(
            instance.heading) > 30 else instance.heading
        instance.slug = slugify(instance.patient.username+"-"+info +
                                "-"+datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


pre_save.connect(pre_save_query_receiver, sender=Query)
