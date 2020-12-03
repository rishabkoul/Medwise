from django.db import models
from django.conf import settings
from query.models import Query

# Create your models here.


class Comment(models.Model):
    written_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(max_length=2500, null=False, blank=False)
    commented_on = models.ForeignKey(Query, on_delete=models.CASCADE)
    date_published = models.DateTimeField(
        auto_now_add=True, verbose_name="date published")

    def __str__(self):
        return self.commented_on.slug
