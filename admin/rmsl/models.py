from django.db import models
from django.db.models import UniqueConstraint
# Create your models here.


class Resource(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(max_length=255)
    token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Event(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    link = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    is_posted = models.BooleanField(default=False)

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=['resource', 'name', 'published_at', 'link'],
                name='unique_event'
            )
        ]
