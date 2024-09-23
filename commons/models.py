import uuid

from django.db import models

from .enums import STATUS_TYPE, ACTIVE


class BaseModel(models.Model):
    """
    BaseModel class used for grouping common attributes that will be shared by all other models.
    """
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=False, auto_created=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    status = models.CharField(max_length=8, choices=STATUS_TYPE, default=ACTIVE)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
