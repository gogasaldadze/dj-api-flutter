from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid


# Create your models here.
class AbstractModel(models.Model):
    uuid = models.UUIDField(
        _("UUID"), default=uuid.uuid4(), unique=True, editable=False, db_index=True
    )
    created_at = models.DateTimeField(_("Created_At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated_At"), auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
