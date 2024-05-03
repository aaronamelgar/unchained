from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from taggit.models import CommonGenericTaggedItemBase, TaggedItemBase

__all__ = [
    "Tag"
]


class GenericCharFieldItemBase(CommonGenericTaggedItemBase):
    class Meta:
        abstract = True

    object_id = models.CharField(
        verbose_name=_("object ID"),
        db_index=True,
        max_length=64,  # Replace with your length
    )


class Tag(GenericCharFieldItemBase, TaggedItemBase):
    class Meta(TaggedItemBase.Meta):
        pass
